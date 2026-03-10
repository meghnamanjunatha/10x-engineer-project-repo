import pytest
from app.utils import sort_prompts_by_date, filter_prompts_by_collection
from app.models import Prompt
from datetime import datetime


def test_sort_prompts_by_date():
    # Create test prompts with dates
    prompt1 = Prompt(id="1", title="Prompt 1", content="Content 1", updated_at="2023-10-01T15:00:00")
    prompt2 = Prompt(id="2", title="Prompt 2", content="Content 2", updated_at="2023-10-02T15:00:00")
    prompt3 = Prompt(id="3", title="Prompt 3", content="Content 3", updated_at="2023-09-30T15:00:00")
    
    prompts = [prompt1, prompt2, prompt3]

    # Test sorting in descending order (newest first)
    sorted_prompts = sort_prompts_by_date(prompts, descending=True)
    assert sorted_prompts[0] == prompt2  # Newest
    assert sorted_prompts[1] == prompt1
    assert sorted_prompts[2] == prompt3  # Oldest

    # Test sorting in ascending order (oldest first)
    sorted_prompts = sort_prompts_by_date(prompts, descending=False)
    assert sorted_prompts[0] == prompt3  # Oldest
    assert sorted_prompts[1] == prompt1
    assert sorted_prompts[2] == prompt2  # Newest

    # Test with incomplete prompt (missing updated_at and created_at)
    incomplete_prompt = Prompt(id="4", title="Incomplete", content="No Dates")
    prompts.append(incomplete_prompt)
    sorted_prompts = sort_prompts_by_date(prompts, descending=True)

    # Ensure incomplete prompt is placed appropriately
    assert sorted_prompts[-1] == incomplete_prompt  # Should be the last with datetime.min


def test_filter_prompts_by_collection():
    # Create test prompts with collection IDs
    prompt1 = Prompt(id="1", title="Prompt 1", content="Content 1", collection_id="collection-1")
    prompt2 = Prompt(id="2", title="Prompt 2", content="Content 2", collection_id="collection-2")
    prompt3 = Prompt(id="3", title="Prompt 3", content="Content 3", collection_id="collection-1")

    prompts = [prompt1, prompt2, prompt3]

    # Test filtering by collection ID collection-1
    filtered_prompts = filter_prompts_by_collection(prompts, "collection-1")
    assert len(filtered_prompts) == 2
    assert prompt1 in filtered_prompts
    assert prompt3 in filtered_prompts
    assert prompt2 not in filtered_prompts

    # Test filtering by collection ID collection-2
    filtered_prompts = filter_prompts_by_collection(prompts, "collection-2")
    assert len(filtered_prompts) == 1
    assert prompt2 in filtered_prompts

    # Test filtering by a non-existent collection ID
    filtered_prompts = filter_prompts_by_collection(prompts, "non-existent")
    assert len(filtered_prompts) == 0


def test_search_prompts():
    # Create test prompts with titles and descriptions
    prompt1 = Prompt(id="1", title="Learn Python", content="Content 1", description="An introduction to Python.")
    prompt2 = Prompt(id="2", title="Advanced Python", content="Content 2", description="Advanced topics in Python.")
    prompt3 = Prompt(id="3", title="Python Tips", content="Content 3", description="Tips for Python programming.")
    
    prompts = [prompt1, prompt2, prompt3]

    # Test searching with keyword present in titles
    search_results = search_prompts(prompts, "Python")
    assert len(search_results) == 3
    assert prompt1 in search_results
    assert prompt2 in search_results
    assert prompt3 in search_results

    # Test searching with keyword in the description
    search_results = search_prompts(prompts, "introduction")
    assert len(search_results) == 1
    assert prompt1 in search_results
    
    # Test searching with no matches
    search_results = search_prompts(prompts, "JavaScript")
    assert len(search_results) == 0

    # Test case insensitivity
    search_results = search_prompts(prompts, "python")  # Lowercase
    assert len(search_results) == 3
    assert prompt1 in search_results
    assert prompt2 in search_results
    assert prompt3 in search_results



def test_validate_prompt_content():
    # Test valid content
    valid_content = "This is valid content."
    assert validate_prompt_content(valid_content) is True

    # Test content that is too short
    short_content = "Too short"
    assert validate_prompt_content(short_content) is False

    # Test empty content
    empty_content = ""
    assert validate_prompt_content(empty_content) is False

    # Test content that is only whitespace
    whitespace_content = "     "
    assert validate_prompt_content(whitespace_content) is False

    # Test content that exactly meets the minimum length
    minimum_length_content = "1234567890"
    assert validate_prompt_content(minimum_length_content) is True


def test_extract_variables():
    # Test with single variable
    content_with_single_variable = "This is a template with a {{variable}}."
    extracted_variables = extract_variables(content_with_single_variable)
    assert extracted_variables == ["variable"]

    # Test with multiple variables
    content_with_multiple the task._variables = "This {{template}} has {{several}} {{variables}}."
    extracted_variables = extract_variables(content_with_multiple_variables)
    assert extracted_variables == ["template", "several", "variables"]

    # Test with no variables
    content_with_no_variables = "Just some plain text."
    extracted_variables = extract_variables(content_with_no_variables)
    assert extracted_variables == []

    # Test with nested braces
    content_with_nested_braces = "{{outer{{inner}}outer}}"

def test_sort_prompts_by_date_edge_cases():
    # Test with no prompts
    prompts = []
    sorted_prompts = sort_prompts_by_date(prompts, descending=True)
    assert sorted_prompts == []

    # Test with prompts missing date fields
    prompt_without_dates = Prompt(id="1", title="No Dates", content="Content")
    prompts = [prompt_without_dates]
    sorted_prompts = sort_prompts_by_date(prompts, descending=True)
    assert sorted_prompts == [prompt_without_dates]


def test_filter_prompts_by_collection_edge_cases():
    # Test with empty list of prompts
    prompts = []
    filtered_prompts = filter_prompts_by_collection(prompts, "any-id")
    assert filtered_prompts == []

    # Test with invalid collection_id data type
    prompts = [
        Prompt(id="1", title="Prompt 1", content="Content 1", collection_id="collection-1")
    ]
    try:
        filter_prompts_by_collection(prompts, None)
    except Exception as e:
        assert isinstance(e, TypeError)


def test_search_prompts_edge_cases():
    # Test with empty list of prompts
    prompts = []
    search_results = search_prompts(prompts, "query")
    assert search_results == []

    # Test with empty search query
    prompts = [Prompt(id="1", title="Python", content="Content")]
    search_results = search_prompts(prompts, "")
    assert search_results == prompts

    # Test with case insensitivity
    search_results = search_prompts(prompts, "python")
    assert search_results == prompts


def test_validate_prompt_content_edge_cases():
    # Valid content with special characters
    valid_content = "!@#$%^&*()_+=[]{}|;':\",.<>/?`~"
    assert validate_prompt_content(valid_content) is True

    # Content exactly at minimum length but with spaces
    content_with_spaces = "    1234567890    "
    assert validate_prompt_content(content_with_spaces) is True


def test_extract_variables_edge_cases():
    # Test with malformed variables
    content = "This is a {{malformed variable{{example}}."
    extracted_variables = extract_variables(content)
    assert extracted_variables == ["example"]

    # Test with no variable content
    content_no_variables = "This has no variables."
    extracted_variables = extract_variables(content_no_variables)
    assert extracted_variables == []

    # Test with nested variable-like structure but not a real variable
    content_with_nesting = "Nested like {{in}complete}} variable"
    extracted_variables = extract_variables(content_with_nesting)
    assert extracted_variables == ["in"]

    # Test with empty string
    empty_content = ""
    extracted_variables = extract_variables(empty_content)
    assert extracted_variables == []