"""In-memory storage for PromptLab

This module provides simple in-memory storage for prompts and collections.
In a production environment, this would be replaced with a database.
"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection
from datetime import datetime


class Storage:
    def __init__(self):
        self.prompts = {}  # Add this line
        self.collections = {}
    
    # ============== Prompt Operations ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        self.prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        return self.prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        return list(self.prompts.values())
    
    def update_prompt(self, prompt_id: str, update_data: dict) -> Optional[Prompt]:
        prompt = self.prompts.get(prompt_id)
        if not prompt:
            return None

        # Convert Pydantic model to dict if needed
        if hasattr(prompt, "model_dump"):
            prompt_dict = prompt.model_dump()
        else:
            prompt_dict = prompt.__dict__ if not isinstance(prompt, dict) else prompt

        # Apply updates
        prompt_dict.update(update_data)

        # Reconstruct Prompt object
        updated_prompt = Prompt(**prompt_dict)
        self.prompts[prompt_id] = updated_prompt
        return updated_prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        if prompt_id in self.prompts:
            del self.prompts[prompt_id]
            return True
        return False
    
    # ============== Collection Operations ==============
    
    def create_collection(self, collection: Collection) -> Collection:
        self.collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        return self.collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        return list(self.collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        if collection_id not in self.collections:
            return False

        del self.collections[collection_id]

        # Clear collection_id from prompts that reference this collection
        for prompt_id, prompt in self.prompts.items():
            if hasattr(prompt, "collection_id") and prompt.collection_id == collection_id:
                prompt.collection_id = None
                prompt.updated_at = datetime.utcnow().isoformat()
                self.prompts[prompt_id] = prompt

        return True
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        return [p for p in self.prompts.values() if p.collection_id == collection_id]
    
    # ============== Utility ==============
    
    def clear(self):
        self.prompts.clear()
        self.collections.clear()


# Global storage instance
storage = Storage()
