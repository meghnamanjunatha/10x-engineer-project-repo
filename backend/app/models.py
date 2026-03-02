"""Pydantic models for PromptLab"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import uuid4


def generate_id() -> str:
    return str(uuid4())


def get_current_time() -> datetime:
    return datetime.utcnow()


# ============== Prompt Models ==============

class PromptBase(BaseModel):
    """Base model for a Prompt.

    Attributes:
        title (str): The title of the prompt.
        content (str): The content of the prompt.
        description (Optional[str]): A brief description of the prompt.
        collection_id (Optional[str]): The ID of the collection this prompt belongs to.
    """
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None


class PromptCreate(PromptBase):
    """Data required to create a Prompt. Inherits from PromptBase."""
    pass


class PromptUpdate(PromptBase):
    """Data required to update a Prompt. Inherits from PromptBase."""
    pass


class Prompt(PromptBase):
    """Model representing a complete Prompt with metadata.

    Attributes:
        id (str): Unique identifier for the prompt.
        created_at (datetime): Timestamp when the prompt was created.
        updated_at (datetime): Timestamp when the prompt was last updated.
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Collection Models ==============

class CollectionBase(BaseModel):
    """Base model for a Collection.

    Attributes:
        name (str): The name of the collection.
        description (Optional[str]): A brief description of the collection.
    """
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CollectionCreate(CollectionBase):
    """Data required to create a Collection. Inherits from CollectionBase."""
    pass


class Collection(CollectionBase):
    """Model representing a complete Collection with metadata.

    Attributes:
        id (str): Unique identifier for the collection.
        created_at (datetime): Timestamp when the collection was created.
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Response Models ==============

class PromptList(BaseModel):
    """Model for a list of Prompts.

    Attributes:
        prompts (List[Prompt]): A list of Prompt objects.
        total (int): Total number of prompts in the list.
    """
    prompts: List[Prompt]
    total: int


class CollectionList(BaseModel):
    """Model for a list of Collections.

    Attributes:
        collections (List[Collection]): A list of Collection objects.
        total (int): Total number of collections in the list.
    """
    collections: List[Collection]
    total: int


class HealthResponse(BaseModel):
    """Model for service health response.

    Attributes:
        status (str): Status of the service.
        version (str): Version of the service.
    """
    status: str
    version: str

