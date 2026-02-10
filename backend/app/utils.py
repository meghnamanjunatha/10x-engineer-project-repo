"""Utility functions for PromptLab"""

from typing import List, Any
from app.models import Prompt
from datetime import datetime


def sort_prompts_by_date(prompts: List[Any], descending: bool = True):
    """Sort a list of prompts (Pydantic models or dicts) by updated_at (fallback to created_at).
    Returns newest first when descending=True.
    """

    def _get_ts(p):
        # handle Pydantic BaseModel or plain dict
        if hasattr(p, "updated_at"):
            ts = getattr(p, "updated_at")
        elif isinstance(p, dict):
            ts = p.get("updated_at") or p.get("created_at")
        else:
            # try attribute access fallback
            ts = getattr(p, "created_at", None)

        if not ts:
            return datetime.min

        # ISO format expected; try parsing safely
        try:
            return datetime.fromisoformat(ts)
        except Exception:
            try:
                return datetime.fromtimestamp(float(ts))
            except Exception:
                return datetime.min

    return sorted(prompts, key=_get_ts, reverse=descending)


def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    return [p for p in prompts if p.collection_id == collection_id]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    query_lower = query.lower()
    return [
        p for p in prompts 
        if query_lower in p.title.lower() or 
           (p.description and query_lower in p.description.lower())
    ]


def validate_prompt_content(content: str) -> bool:
    """Check if prompt content is valid.
    
    A valid prompt should:
    - Not be empty
    - Not be just whitespace
    - Be at least 10 characters
    """
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10


def extract_variables(content: str) -> List[str]:
    """Extract template variables from prompt content.
    
    Variables are in the format {{variable_name}}
    """
    import re
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, content)
