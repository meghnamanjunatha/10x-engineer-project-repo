# Import the PromptVersioningSystem class
from app.prompt_versioning import PromptVersioningSystem

# Initialize the prompt_versioning_system
prompt_versioning_system = PromptVersioningSystem()

# Test: Attempting to retrieve a specific version of a prompt fails if version does not exist
def test_retrieve_nonexistent_prompt_version():
    prompt_id = 1
    version = 999  # Assume this version does not exist
    result = prompt_versioning_system.get_prompt_version(prompt_id, version)
    
    assert result is None or result.error == "Version not found"

# Test: Updating a prompt fails to directly overwrite without versioning
def test_prevent_direct_prompt_update_without_versioning():
    prompt_id = 1
    new_content = "Updated prompt content"
    result = prompt_versioning_system.update_prompt(prompt_id, new_content)
    
    assert result.error == "Direct update without versioning not allowed"

# Test: Listing all versions of a prompt returns empty if no versions exist
def test_list_prompt_versions_empty():
    prompt_id = 1
    result = prompt_versioning_system.list_prompt_versions(prompt_id)
    
    assert result == [] or result.error == "No versions found"

# Test: Rolling back to a non-existent version of a prompt fails
def test_rollback_to_nonexistent_prompt_version():
    prompt_id = 1
    version = 999  # Assume this version does not exist
    result = prompt_versioning_system.rollback_to_version(prompt_id, version)
    
    assert result.error == "Version not found"
