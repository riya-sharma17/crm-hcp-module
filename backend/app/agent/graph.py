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


# State - what the agent remembers during a conversation
class AgentState(TypedDict):
    messages: Annotated[List, operator.add]
    interaction_data: dict
    tool_results: dict


# Initialize the LLM
llm = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model="gemma2-9b-it",
    temperature=0.1,
)

# Bind tools to LLM
llm_with_tools = llm.bind_tools(tools)


def agent_node(state: AgentState) -> AgentState:
    """Main agent node - decides what to do next"""

    # Add system prompt to messages
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
    """Decide whether to use a tool or end"""
    last_message = state["messages"][-1]

    # If AI wants to use a tool
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    # Otherwise end
    return END


def process_tool_results(state: AgentState) -> AgentState:
    """Process results from tool calls"""
    last_message = state["messages"][-1]
    tool_results = state.get("tool_results", {})

    # Store tool results in state
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


# Build the graph
tool_node = ToolNode(tools)

graph_builder = StateGraph(AgentState)

# Add nodes
graph_builder.add_node("agent", agent_node)
graph_builder.add_node("tools", tool_node)
graph_builder.add_node("process_results", process_tool_results)

# Set entry point
graph_builder.set_entry_point("agent")

# Add edges
graph_builder.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)

graph_builder.add_edge("tools", "process_results")
graph_builder.add_edge("process_results", "agent")

# Compile the graph
agent_graph = graph_builder.compile()


async def run_agent(message: str, conversation_history: list = []) -> dict:
    """Run the agent with a user message"""

    # Build initial state
    initial_state = {
        "messages": conversation_history + [HumanMessage(content=message)],
        "interaction_data": {},
        "tool_results": {}
    }

    # Run the graph
    result = await agent_graph.ainvoke(initial_state)

    # Extract final response
    final_message = result["messages"][-1]
    response_text = final_message.content if hasattr(
        final_message, "content"
    ) else str(final_message)

    return {
        "response": response_text,
        "tool_results": result.get("tool_results", {}),
        "interaction_data": result.get("interaction_data", {})
    }