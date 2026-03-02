"""FastAPI routes for PromptLab"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.models import (
    Prompt, PromptCreate, PromptUpdate,
    Collection, CollectionCreate,
    PromptList, CollectionList, HealthResponse,
    get_current_time
)
from app.storage import storage
from app.utils import sort_prompts_by_date, filter_prompts_by_collection, search_prompts
from app import __version__


app = FastAPI(
    title="PromptLab API",
    description="AI Prompt Engineering Platform",
    version=__version__
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Health Check ==============

@app.get("/health", response_model=HealthResponse)
def health_check():
    """
    Health check endpoint.

    This endpoint returns the health status and version of the application.

    Args:
        None

    Returns:
        HealthResponse: An object containing the health status and app version.
    """
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None
):
    """Retrieve a list of prompts with optional filtering and sorting.
    Fetches all prompts from storage and applies optional filters for collection 
    and search terms. Results are sorted by date in descending order (newest first).
    Args:
        collection_id (Optional[str]): Filter prompts by collection ID. If provided,
            only prompts belonging to this collection will be returned. Defaults to None.
        search (Optional[str]): Filter prompts by search term. Searches across the 
            prompt title and template fields (case-insensitive). Defaults to None.
    Returns:
        PromptList: A PromptList object containing:
            - prompts (List): List of filtered and sorted Prompt objects
            - total (int): Total count of prompts in the filtered results
    """
    prompts = list(storage.prompts.values())
    
    # Filter by collection if provided
    if collection_id:
        prompts = [p for p in prompts if getattr(p, "collection_id", None) == collection_id]
    
    # Filter by search term if provided
    if search:
        search_lower = search.lower()
        prompts = [
            p for p in prompts 
            if search_lower in getattr(p, "title", "").lower() 
            or search_lower in getattr(p, "template", "").lower()
        ]
    
    # Sort newest first
    prompts = sort_prompts_by_date(prompts, descending=True)
    
    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str):
    """Retrieves a prompt by its ID.
    
    Args:
        prompt_id (str): The unique identifier of the prompt to retrieve.
        
    Returns:
        dict: The prompt object containing the requested prompt details.
        
    Raises:
        HTTPException: If the prompt with the given ID is not found (status code 404).
    """
    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    """Creates a new prompt.
    
    Creates a new prompt with the provided data and stores it in storage.
    Validates that the specified collection exists if provided.
    
    Args:
        prompt_data (PromptCreate): The prompt data to create, containing:
            - title: The prompt title
            - content: The prompt content
            - description: The prompt description
            - collection_id: Optional ID of the collection to associate with the prompt
    
    Returns:
        Prompt: The created prompt object with all fields populated, including
            the assigned ID, created_at and updated_at timestamps.
    
    Raises:
        HTTPException: 400 if the specified collection_id is provided but does not exist.
    """
    # Validate collection exists if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    prompt = Prompt(**prompt_data.model_dump())
    return storage.create_prompt(prompt)


@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """Updates an existing prompt by ID.
    Updates the prompt with the provided data, including title, content, 
    description, and collection association. Validates that the specified 
    collection exists before updating.
    Args:
        prompt_id (str): The unique identifier of the prompt to update.
        prompt_data (PromptUpdate): The updated prompt data containing:
            - title: The new prompt title
            - content: The new prompt content
            - description: The new prompt description
            - collection_id: The ID of the collection to associate with the prompt
    Returns:
        Prompt: The updated prompt object with all fields populated, including
            the original created_at timestamp and updated_at timestamp.
    Raises:
        HTTPException: 404 if the prompt with the given prompt_id does not exist.
        HTTPException: 400 if the specified collection_id is provided but does not exist.
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Validate collection if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    # BUG #2: We're not updating the updated_at timestamp!
    # The updated prompt keeps the old timestamp
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        created_at=existing.created_at,
        updated_at=existing.updated_at  # BUG: Should be get_current_time()
    )
    
    return storage.update_prompt(prompt_id, updated_prompt)


@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def patch_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """Partially updates an existing prompt by ID.
    
    Updates only the provided fields of a prompt, leaving unset fields unchanged.
    Validates that the specified collection exists if provided. Automatically
    updates the updated_at timestamp.
    
    Args:
        prompt_id (str): The unique identifier of the prompt to update.
        prompt_data (PromptUpdate): The partial prompt data containing only fields
            to be updated:
            - title: The new prompt title (optional)
            - content: The new prompt content (optional)
            - description: The new prompt description (optional)
            - collection_id: The ID of the collection to associate with (optional)
    
    Returns:
        Prompt: The updated prompt object with all fields populated, including
            the original created_at timestamp and newly updated updated_at timestamp.
    
    Raises:
        HTTPException: 404 if the prompt with the given prompt_id does not exist.
        HTTPException: 400 if the specified collection_id is provided but does not exist.
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")

    # Only take provided fields
    update_data = prompt_data.model_dump(exclude_unset=True)
    if not update_data:
        return existing

    # Validate collection if provided
    if "collection_id" in update_data and update_data["collection_id"]:
        collection = storage.get_collection(update_data["collection_id"])
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    # Refresh updated_at
    update_data["updated_at"] = get_current_time()

    updated = storage.update_prompt(prompt_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Prompt not found")

    return updated


@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    """Deletes a prompt by ID.
    
    Removes the prompt with the specified ID from storage.
    
    Args:
        prompt_id (str): The unique identifier of the prompt to delete.
    
    Returns:
        None
    
    Raises:
        HTTPException: 404 if the prompt with the given prompt_id does not exist.
    """
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None


# ============== Collection Endpoints ==============

@app.get("/collections", response_model=CollectionList)
def list_collections():
    """
    List all collections.

    This endpoint retrieves all available collections from storage.

    Args:
        None

    Returns:
        CollectionList: A CollectionList object containing:
            - collections (list): List of all collections
            - total (int): Total count of collections
    """
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str):
    """Retrieve a collection by its ID.

    This endpoint fetches a specific collection from storage using the provided
    collection ID. If the collection does not exist, a 404 error is returned.

    Args:
        collection_id (str): The unique identifier of the collection to retrieve.

    Returns:
        Collection: The collection object matching the provided collection_id.

    Raises:
        HTTPException: If the collection is not found (status_code=404).
    """
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate):
    """Create a new collection.

    This endpoint creates a new collection with the provided data and stores it
    in the database.

    Args:
        collection_data (CollectionCreate): The collection data to create,
            including all required fields for a new collection.

    Returns:
        Collection: The created collection object with all fields populated,
            including the assigned ID and timestamps.

    Raises:
        ValidationError: If the collection_data fails validation.
    """
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str):
    """
    Delete a collection by its ID.
    This endpoint removes a collection from storage. Note: Prompts associated with
    the deleted collection may become orphaned and require separate handling.
    Args:
        collection_id (str): The unique identifier of the collection to delete.
    Returns:
        None: Returns HTTP 204 No Content on successful deletion.
    Raises:
        HTTPException: Returns HTTP 404 if the collection with the given ID is not found.
    Endpoints:
        DELETE /collections/{collection_id}
            Status Code: 204 No Content on success
            Status Code: 404 Not Found if collection_id does not exist
    """
    # BUG #4: We delete the collection but don't handle the prompts!
    # Prompts with this collection_id become orphaned with invalid reference
    # Should either: delete the prompts, set collection_id to None, or prevent deletion
    
    if not storage.delete_collection(collection_id):
        raise HTTPException(status_code=404, detail="Collection not found")
    
    # Missing: Handle prompts that belong to this collection!
    
    return None






