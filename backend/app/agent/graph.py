from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage
from typing import TypedDict, Annotated, List, Optional
import operator
import json
from datetime import datetime

from app.core.config import settings
from app.agent.tools import tools
from app.agent.prompts import SYSTEM_PROMPT

import logging
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────
# State Definition
# ─────────────────────────────────────────
class AgentState(TypedDict):
    messages: Annotated[List, operator.add]
    interaction_data: dict
    tool_results: dict


# ─────────────────────────────────────────
# LLM Initialization
# ─────────────────────────────────────────
llm = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
    temperature=0.1,
)

extraction_llm = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
    temperature=0,
)

llm_with_tools = llm.bind_tools(tools)


# ─────────────────────────────────────────
# Graph Nodes
# ─────────────────────────────────────────
def agent_node(state: AgentState) -> AgentState:
    system_message = SystemMessage(
        content=SYSTEM_PROMPT.format(
            current_date=datetime.now().strftime("%Y-%m-%d")
        )
    )
    messages = [system_message] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {
        "messages": [response],
        "interaction_data": state.get("interaction_data", {}),
        "tool_results": state.get("tool_results", {})
    }


def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END


def process_tool_results(state: AgentState) -> AgentState:
    tool_results = state.get("tool_results", {})
    return {
        "messages": state["messages"],
        "interaction_data": state.get("interaction_data", {}),
        "tool_results": tool_results
    }


# ─────────────────────────────────────────
# Build Graph
# ─────────────────────────────────────────
tool_node = ToolNode(tools)
graph_builder = StateGraph(AgentState)
graph_builder.add_node("agent", agent_node)
graph_builder.add_node("tools", tool_node)
graph_builder.add_node("process_results", process_tool_results)
graph_builder.set_entry_point("agent")
graph_builder.add_conditional_edges(
    "agent",
    should_continue,
    {"tools": "tools", END: END}
)
graph_builder.add_edge("tools", "process_results")
graph_builder.add_edge("process_results", "agent")
agent_graph = graph_builder.compile()


# ─────────────────────────────────────────
# Extract Form Data — Direct LLM Call
# ─────────────────────────────────────────
def extract_interaction_data(message: str) -> dict:
    """
    Uses LLM directly to extract structured form data.
    This is separate from the agent graph.
    """
    prompt = f"""You are a data extraction assistant for a pharmaceutical CRM.
Extract interaction details from the message below.
Return ONLY a valid JSON object. No explanation. No markdown. No extra text.

Message: "{message}"

JSON structure to return:
{{
    "hcp_name": "full name of doctor/HCP mentioned, or null",
    "interaction_type": "one of: Meeting, Call, Email, Conference, Virtual",
    "topics_discussed": "topics or products discussed, or null",
    "sentiment": "one of: Positive, Neutral, Negative",
    "outcomes": "any outcomes or agreements mentioned, or null",
    "follow_up_actions": ["array of follow up items, or empty array"],
    "materials_shared": [],
    "samples_distributed": [],
    "attendees": []
}}"""

    try:
        response = extraction_llm.invoke([
            HumanMessage(content=prompt)
        ])

        raw = response.content.strip()
        logger.info(f"Raw extraction response: {raw}")

        # Clean markdown fences if present
        if "```" in raw:
            parts = raw.split("```")
            for part in parts:
                part = part.strip()
                if part.startswith("json"):
                    part = part[4:].strip()
                if part.startswith("{"):
                    raw = part
                    break

        # Find JSON object in response
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start != -1 and end > start:
            raw = raw[start:end]

        data = json.loads(raw)
        logger.info(f"Extracted data: {data}")

        # Ensure all list fields are lists
        for field in [
            "follow_up_actions",
            "materials_shared",
            "samples_distributed",
            "attendees"
        ]:
            if field not in data:
                data[field] = []
            elif isinstance(data[field], str):
                data[field] = [data[field]] if data[field] else []

        return data

    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        return {
            "hcp_name": None,
            "interaction_type": "Meeting",
            "topics_discussed": None,
            "sentiment": "Neutral",
            "outcomes": None,
            "follow_up_actions": [],
            "materials_shared": [],
            "samples_distributed": [],
            "attendees": []
        }


# ─────────────────────────────────────────
# Conversational Response
# ─────────────────────────────────────────
async def get_agent_response(
    message: str,
    extracted: dict
) -> str:
    """Get conversational response from agent"""
    try:
        context = f"""
The user described this interaction: "{message}"

I have extracted these details:
- HCP: {extracted.get('hcp_name', 'Not mentioned')}
- Type: {extracted.get('interaction_type', 'Meeting')}
- Topics: {extracted.get('topics_discussed', 'Not mentioned')}
- Sentiment: {extracted.get('sentiment', 'Neutral')}
- Outcomes: {extracted.get('outcomes', 'None')}
- Follow-ups: {extracted.get('follow_up_actions', [])}

Respond conversationally confirming what was extracted.
If HCP name is missing, ask for it.
Keep response under 3 sentences.
"""
        initial_state = {
            "messages": [HumanMessage(content=context)],
            "interaction_data": extracted,
            "tool_results": {}
        }
        result = await agent_graph.ainvoke(initial_state)
        final_message = result["messages"][-1]
        return final_message.content if hasattr(
            final_message, "content"
        ) else str(final_message)
    except Exception as e:
        logger.error(f"Agent response error: {e}")
        hcp = extracted.get('hcp_name', 'the HCP')
        topics = extracted.get('topics_discussed', 'the discussed topics')
        sentiment = extracted.get('sentiment', 'Neutral')
        return (
            f"I've extracted the interaction details with {hcp}. "
            f"Topics: {topics}. "
            f"Sentiment: {sentiment}. "
            f"The form has been filled automatically!"
        )


# ─────────────────────────────────────────
# Main Entry Point
# ─────────────────────────────────────────
async def run_agent(
    message: str,
    conversation_history: list = []
) -> dict:
    """
    Main function called by the API.
    1. Extract structured data from message
    2. Get conversational response
    3. Return both
    """
    logger.info(f"Processing message: {message[:50]}...")

    # Step 1 - Extract form data
    extracted_data = extract_interaction_data(message)
    logger.info(f"Extraction complete: {extracted_data}")

    # Step 2 - Get conversational response
    response_text = await get_agent_response(message, extracted_data)
    logger.info(f"Agent response: {response_text[:50]}...")

    return {
        "response": response_text,
        "tool_results": {},
        "interaction_data": extracted_data
    }