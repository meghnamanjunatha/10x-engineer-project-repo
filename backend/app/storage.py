from app.models import Prompt, Collection

# There should be a clear explanation for each input and output.

class Storage:
    def __init__(self):
        """
        Initialize a new Storage instance.

        Initializes empty dictionaries for prompts and collections to hold data.
        """
        self.prompts = {}  # Maps prompt IDs to Prompt objects
        self.collections = {}  # Maps collection IDs to Collection objects
    
    # ============== Prompt Operations ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """
        Add a new prompt to storage.

        Args:
            prompt (Prompt): The prompt instance to be added.

        Returns:
            Prompt: The added prompt instance.
        """
        self.prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """
        Retrieve a prompt by its ID.

        Args:
            prompt_id (str): The ID of the prompt to be retrieved.

        Returns:
            Optional[Prompt]: The prompt instance if found, otherwise None.
        """
        return self.prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        """
        Retrieve all stored prompts.

        Returns:
            List[Prompt]: A list of all prompt instances.
        """
        return list(self.prompts.values())
    
    def update_prompt(self, prompt_id: str, update_data: dict) -> Optional[Prompt]:
        """
        Update an existing prompt.

        Args:
            prompt_id (str): The ID of the prompt to be updated.
            update_data (dict): A dictionary of attributes to update in the prompt.

        Returns:
            Optional[Prompt]: The updated prompt instance if found, otherwise None.
        """
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
        """
        Delete a prompt by its ID.

        Args:
            prompt_id (str): The ID of the prompt to be deleted.

        Returns:
            bool: True if the prompt was successfully deleted, otherwise False.
        """
        if prompt_id in self.prompts:
            del self.prompts[prompt_id]
            return True
        return False
    
    # ============== Collection Operations ==============
    
    def create_collection(self, collection: Collection) -> Collection:
        """
        Add a new collection to storage.

        Args:
            collection (Collection): The collection instance to be added.

        Returns:
            Collection: The added collection instance.
        """
        self.collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """
        Retrieve a collection by its ID.

        Args:
            collection_id (str): The ID of the collection to be retrieved.

        Returns:
            Optional[Collection]: The collection instance if found, otherwise None.
        """
        return self.collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        """
        Retrieve all stored collections.

        Returns:
            List[Collection]: A list of all collection instances.
        """
        return list(self.collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        """
        Delete a collection by its ID, and remove its association from prompts.

        Args:
            collection_id (str): The ID of the collection to be deleted.

        Returns:
            bool: True if the collection was successfully deleted, otherwise False.
        """
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
        """
        Retrieve all prompts associated with a specific collection.

        Args:
            collection_id (str): The ID of the collection.

        Returns:
            List[Prompt]: A list of prompts belonging to the collection.
        """
        return [p for p in self.prompts.values() if p.collection_id == collection_id]
    
    # ============== Utility ==============
    
    def clear(self):
        """
        Clear all stored prompts and collections.

        Resets the storage by removing all entries from prompts and collections.
        """
        self.prompts.clear()
        self.collections.clear()


# Global storage instance
storage = Storage()
