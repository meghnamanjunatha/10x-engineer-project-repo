import pytest
from pydantic import ValidationError
from datetime import datetime
import json  # Import json for serialization
from app.models import PromptCreate, PromptUpdate, Prompt, CollectionCreate, Collection

# ============== Prompt Models Validation Tests ==============

def test_prompt_create_validation():
    # Valid case
    prompt_data = {
        "title": "Valid Title",
        "content": "Valid content that meets the length requirements."
    }
    prompt = PromptCreate(**prompt_data)
    assert prompt.title == "Valid Title"

    # Title too short
    with pytest.raises(ValidationError):
        PromptCreate(title="", content="Valid content")

    # Content too short
    with pytest.raises(ValidationError):
        PromptCreate(title="Valid Title", content="")

    # Title too long
    with pytest.raises(ValidationError):
        PromptCreate(title="T" * 201, content="Valid content")

    # Description too long
    prompt_data["description"] = "D" * 501
    with pytest.raises(ValidationError):
        PromptCreate(**prompt_data)


def test_prompt_update_validation():
    # Valid case
    prompt_update_data = {
        "title": "Another Title",
        "content": "Content within valid limits."
    }
    prompt_update = PromptUpdate(**prompt_update_data)
    assert prompt_update.content == "Content within valid limits."


def test_prompt_model_defaults():
    prompt = Prompt(title="Default Title", content="Content")
    assert prompt.id is not None
    assert prompt.created_at is not None
    assert prompt.updated_at is not None

# ============== Default Value Tests ==============

def test_prompt_defaults():
    # Create a prompt with minimum fields
    prompt = Prompt(title="Test Title", content="Test content")

    # Ensure defaults are assigned
    assert prompt.id is not None
    assert isinstance(prompt.id, str) and len(prompt.id) > 0
    assert prompt.created_at is not None
    assert isinstance(prompt.created_at, datetime)
    assert prompt.updated_at is not None
    assert isinstance(prompt.updated_at, datetime)

    # Print out for visual confirmation (optional)
    print(prompt.json())

# ============== Collection Models Validation Tests ==============

def test_collection_create_validation():
    # Valid case
    collection_data = {
        "name": "Collection Name",
        "description": "A detailed description."
    }
    collection = CollectionCreate(**collection_data)
    assert collection.name == "Collection Name"

    # Name too short
    with pytest.raises(ValidationError):
        CollectionCreate(name="", description="Description")

    # Name too long
    with pytest.raises(ValidationError):
        CollectionCreate(name="N" * 101, description="Description")


def test_collection_model_defaults():
    collection = Collection(name="Collection Name")
    assert collection.id is not None
    assert collection.created_at is not None

# ============== Default Value Tests for Collection ==============

def test_collection_defaults():
    # Create a collection with minimum fields
    collection = Collection(name="Collection Name")

    # Ensure defaults are assigned
    assert collection.id is not None
    assert isinstance(collection.id, str) and len(collection.id) > 0
    assert collection.created_at is not None
    assert isinstance(collection.created_at, datetime)

    # Print out for visual confirmation (optional)
    print(collection.json())

# ============== Serialization Tests ==============

def test_prompt_serialization():
    # Create a Prompt
    prompt = Prompt(title="Test Title", content="Test content")

    # Serialize to JSON
    prompt_json = prompt.json()

    # Load back to dict for de-serialization verification
    prompt_dict = json.loads(prompt_json)

    # Ensure fields are correctly serialized
    assert prompt_dict["title"] == "Test Title"
    assert prompt_dict["content"] == "Test content"
    assert "id" in prompt_dict
    assert "created_at" in prompt_dict
    assert "updated_at" in prompt_dict


def test_collection_serialization():
    # Create a Collection
    collection = Collection(name="Collection Name")

    # Serialize to JSON
    collection_json = collection.json()

    # Load back to dict for de-serialization verification
    collection_dict = json.loads(collection_json)

    # Ensure fields are correctly serialized
    assert collection_dict["name"] == "Collection Name"
    assert "id" in collection_dict
    assert "created_at" in collection_dict

