from langchain_core.tools import tool
from typing import Optional, List, Union


@tool
def log_interaction(
    hcp_name: str,
    interaction_type: str,
    interaction_date: str,
    topics_discussed: str,
    sentiment: str,
    outcomes: Optional[str] = None,
    attendees: Optional[List[str]] = None,
    materials_shared: Optional[List[str]] = None,
    samples_distributed: Optional[List[str]] = None,
    follow_up_actions: Optional[List[str]] = None,
) -> dict:
    """
    Log a new HCP interaction in the CRM system.
    Use this when the user wants to record a new interaction with an HCP.
    attendees must be a list of strings, not a single string.
    materials_shared must be a list of strings.
    samples_distributed must be a list of strings.
    follow_up_actions must be a list of strings.
    """
    # Ensure all list fields are actually lists
    def ensure_list(val):
        if val is None:
            return []
        if isinstance(val, str):
            return [val] if val else []
        return val

    return {
        "tool": "log_interaction",
        "data": {
            "hcp_name": hcp_name,
            "interaction_type": interaction_type,
            "interaction_date": interaction_date,
            "topics_discussed": topics_discussed,
            "sentiment": sentiment,
            "outcomes": outcomes,
            "attendees": ensure_list(attendees),
            "materials_shared": ensure_list(materials_shared),
            "samples_distributed": ensure_list(samples_distributed),
            "follow_up_actions": ensure_list(follow_up_actions),
            "logged_via": "chat"
        }
    }


@tool
def edit_interaction(
    interaction_id: int,
    field_to_update: str,
    new_value: str
) -> dict:
    """
    Edit an existing interaction in the CRM system.
    Use this when the user wants to modify a previously logged interaction.
    Requires the interaction ID and the specific field to update.
    """
    return {
        "tool": "edit_interaction",
        "data": {
            "interaction_id": interaction_id,
            "field_to_update": field_to_update,
            "new_value": new_value
        }
    }


@tool
def search_hcp(
    name: Optional[str] = None,
    specialty: Optional[str] = None,
    city: Optional[str] = None
) -> dict:
    """
    Search for Healthcare Professionals in the CRM system.
    Use this when the user wants to find an HCP by name, specialty or city.
    """
    return {
        "tool": "search_hcp",
        "data": {
            "name": name,
            "specialty": specialty,
            "city": city
        }
    }


@tool
def suggest_followups(
    interaction_summary: str,
    hcp_name: str,
    sentiment: str
) -> dict:
    """
    Suggest follow-up actions based on an interaction.
    Use this to generate AI-powered next steps after an HCP interaction.
    """
    return {
        "tool": "suggest_followups",
        "data": {
            "interaction_summary": interaction_summary,
            "hcp_name": hcp_name,
            "sentiment": sentiment
        }
    }


@tool
def get_interaction_history(
    hcp_name: str,
    limit: Optional[int] = 5
) -> dict:
    """
    Get the past interaction history with a specific HCP.
    Use this when the user wants to review previous interactions.
    """
    return {
        "tool": "get_interaction_history",
        "data": {
            "hcp_name": hcp_name,
            "limit": limit
        }
    }


tools = [
    log_interaction,
    edit_interaction,
    search_hcp,
    suggest_followups,
    get_interaction_history
]