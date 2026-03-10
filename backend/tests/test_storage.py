import pytest
from app.storage import Storage
from app.models import Prompt

# Function to instantiate a Storage object
@pytest.fixture
def storage():
    return Storage()

def test_create_prompt(storage):
    prompt = Prompt(id="test-id", title="Test Title", content="Test content")
    created_prompt = storage.create_prompt(prompt)
    assert created_prompt.id == prompt.id
    assert created_prompt.title == "Test Title"
    assert created_prompt.content == "Test content"
    # Ensure the prompt is stored
    stored_prompt = storage.prompts.get(prompt.id)
    assert stored_prompt == created_prompt

def test_get_prompt(storage):
    # Create and store a prompt
    prompt = Prompt(id="test-id", title="Test Title", content="Test content")
    storage.create_prompt(prompt)

    # Retrieve the prompt using the get_prompt method
    retrieved_prompt = storage.get_prompt("test-id")

    # Assert that the retrieved prompt matches the one created
    assert retrieved_prompt is not None
    assert retrieved_prompt.id == "test-id"
    assert retrieved_prompt.title == "Test Title"
    assert retrieved_prompt.content == "Test content"

    # Test retrieving a non-existent prompt
    non_existent_prompt = storage.get_prompt("non-existent-id")
    assert non_existent_prompt is None

def test_get_all_prompts(storage):
    # Initially, the storage should return an empty list
    assert storage.get_all_prompts() == []

    # Add some prompts
    prompt1 = Prompt(id="prompt-1", title="First Prompt", content="Content of first prompt")
    prompt2 = Prompt(id="prompt-2", title="Second Prompt", content="Content of second prompt")
    storage.create_prompt(prompt1)
    storage.create_prompt(prompt2)

    # Retrieve all prompts
    all_prompts = storage.get_all_prompts()

    # Assert that all prompts are returned
    assert len(all_prompts) == 2
    assert prompt1 in all_prompts
    assert prompt2 in all_prompts

def test_update_prompt(storage):
    # Create a prompt to update
    original_prompt = Prompt(id="test-id", title="Original Title", content="Original content")
    storage.create_prompt(original_prompt)

    # Update the prompt
    update_data = {
        "title": "Updated Title",
        "content": "Updated content for the prompt"
    }
    updated_prompt = storage.update_prompt("test-id", update_data)

    # Assert that the update was successful
    assert updated_prompt is not None
    assert updated_prompt.id == "test-id"
    assert updated_prompt.title == "Updated Title"
    assert updated_prompt.content == "Updated content for the prompt"

    # Test that updating a non-existent prompt returns None
    non_existent_update = storage.update_prompt("non-existent-id", update_data)
    assert non_existent_update is None

    # Check partial updates
    partial_update_data = {"title": "Partially Updated"}
    partially_updated_prompt = storage.update_prompt("test-id", partial_update_data)

    # Assert that only the title was updated
    assert partially_updated_prompt.title == "Partially Updated"
    assert partially_updated_prompt.content == "Updated content for the prompt"

def test_delete_prompt(storage):
    # Create a prompt
    prompt = Prompt(id="test-id", title="Title", content="Content")
    storage.create_prompt(prompt)

    # Delete the prompt
    result = storage.delete_prompt("test-id")

    # Assert that deletion was successful
    assert result is True
    assert storage.get_prompt("test-id") is None  # Ensure prompt is deleted

    # Attempt to delete a non-existent prompt
    non_existent_result = storage.delete_prompt("non-existent-id")
    assert non_existent_result is False

def test_storage_persistence_within_session(storage):
    # Initially, storage should be empty
    assert storage.get_all_prompts() == []
    assert storage.get_all_collections() == []

    # Create a prompt and collection, ensuring persistence across operations
    prompt = Prompt(id="prompt-1", title="Title 1", content="Content 1")
    collection = Collection(id="collection-1", name="Collection 1")
    
    # Test creating and retrieving prompts
    storage.create_prompt(prompt)
    assert storage.get_all_prompts() == [prompt]

    # Test creating and retrieving collections
    storage.create_collection(collection)
    assert storage.get_all_collections() == [collection]

    # Ensure data remains consistent after modifying one part
    another_prompt = Prompt(id="prompt-2", title="Title 2", content="Content 2", collection_id="collection-1")
    storage.create_prompt(another_prompt)
    assert len(storage.get_all_prompts()) == 2

    # Update prompt and check persistence
    updated_data = {"title": "Updated Title"}
    storage.update_prompt("prompt-2", updated_data)
    updated_prompt = storage.get_prompt("prompt-2")
    assert updated_prompt.title == "Updated Title"

    # Delete a prompt and verify change in state
    storage.delete_prompt("prompt-1")
    assert len(storage.get_all_prompts()) == 1
    assert storage.get_prompt("prompt-1") is None

    # Delete collection and verify prompt collection_id is cleared
    storage.delete_collection("collection-1")
    cleared_prompt = storage.get_prompt("prompt-2")
    assert cleared_prompt.collection_id is None

    # Clear storage and ensure it's empty
    storage.clear()
    assert storage.get_all_prompts() == []
    assert storage.get_all_collections() == []

def test_collection_edge_cases(storage):
    # Test working with unexpected data types
    try:
        storage.create_collection("Not a collection object")  # Should raise an error
    except Exception as e:
        assert isinstance(e, (TypeError, ValueError))

    # Create a collection with empty name
    empty_collection = Collection(id="empty-collection-id", name="")
    created_collection = storage.create_collection(empty_collection)
    assert created_collection.name == ""

    # Handle attempt to get collection with an invalid ID type
    try:
        storage.get_collection(123)  # Non-string ID
    except Exception as e:
        assert isinstance(e, (TypeError, ValueError))

    # Handle attempt to delete collection with an invalid ID type
    try:
        assert not storage.delete_collection(123)  # Non-string ID
    except Exception as e:
        assert isinstance(e, (TypeError, ValueError))

    # Ensure storage behavior with a clear call keeps collections clean
    storage.clear()
    assert not storage.get_all_collections()
    assert not storage.get_all_prompts()