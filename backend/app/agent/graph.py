from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from typing import TypedDict, Annotated, List
from datetime import datetime
import operator
import json

from app.core.config import settings
from app.agent.tools import tools
from app.agent.prompts import SYSTEM_PROMPT


class AgentState(TypedDict):
    messages: Annotated[List, operator.add]
    interaction_data: dict
    tool_results: dict


llm = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
    temperature=0.1,
)

llm_with_tools = llm.bind_tools(tools)


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
    last_message = state["messages"][-1]
    tool_results = state.get("tool_results", {})
    if hasattr(last_message, "content"):
        try:
            content = json.loads(last_message.content)
            if "tool" in content:
                tool_results[content["tool"]] = content["data"]
        except Exception:
            pass
    return {
        "messages": state["messages"],
        "interaction_data": state.get("interaction_data", {}),
        "tool_results": tool_results
    }


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


async def run_agent(message: str, conversation_history: list = []) -> dict:
    """Run agent AND extract form data from message"""

    # First — use LLM to extract structured data from message
    extraction_prompt = f"""
Extract interaction details from this message and return ONLY a JSON object.
No explanation, no markdown, just the JSON.

Message: "{message}"

Return this exact JSON structure:
{{
    "hcp_name": "extracted name or null",
    "interaction_type": "Meeting/Call/Email/Conference/Virtual or Meeting",
    "topics_discussed": "extracted topics or null",
    "sentiment": "Positive/Neutral/Negative or Neutral",
    "outcomes": "extracted outcomes or null",
    "follow_up_actions": ["list", "of", "followups"],
    "materials_shared": [],
    "samples_distributed": [],
    "attendees": []
}}
IMPORTANT: follow_up_actions, materials_shared, samples_distributed 
and attendees MUST always be arrays/lists, never strings.
"""

    extraction_llm = ChatGroq(
        api_key=settings.GROQ_API_KEY,
       model="llama-3.3-70b-versatile",
        temperature=0,
    )

    extraction_response = extraction_llm.invoke([
        HumanMessage(content=extraction_prompt)
    ])

    extracted_data = {}
    try:
        raw = extraction_response.content.strip()
        # Clean markdown if present
        if "```" in raw:
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        extracted_data = json.loads(raw.strip())
    except Exception as e:
        print(f"Extraction error: {e}")
        extracted_data = {}

    # Then — run the agent for conversational response
    initial_state = {
        "messages": conversation_history + [HumanMessage(content=message)],
        "interaction_data": extracted_data,
        "tool_results": {}
    }

    result = await agent_graph.ainvoke(initial_state)

    final_message = result["messages"][-1]
    response_text = final_message.content if hasattr(
        final_message, "content"
    ) else str(final_message)

    return {
        "response": response_text,
        "tool_results": result.get("tool_results", {}),
        "interaction_data": extracted_data
    }