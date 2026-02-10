"""Utility functions for PromptLab"""

from typing import List, Any
from app.models import Prompt
from datetime import datetime


def sort_prompts_by_date(prompts: List[Any], descending: bool = True):
    """Sort prompts by updated_at (newest first when descending=True)."""
    def _get_ts(p):
        ts = getattr(p, "updated_at", None) or getattr(p, "created_at", None)
        if isinstance(ts, str):
            try:
                return datetime.fromisoformat(ts)
            except:
                return datetime.min
        return ts or datetime.min

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
