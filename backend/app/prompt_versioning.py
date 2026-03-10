class PromptVersioningSystem:
    def __init__(self):
        self.prompts = {}  # {prompt_id: {version: content}}
        self.current_versions = {}  # Keeps track of the latest version per prompt_id

    def get_prompt_version(self, prompt_id, version):
        if prompt_id in self.prompts and version in self.prompts[prompt_id]:
            return self.prompts[prompt_id][version]
        return {"error": "Version not found"}

    def update_prompt(self, prompt_id, new_content):
        if prompt_id not in self.prompts:
            self.prompts[prompt_id] = {}
            self.current_versions[prompt_id] = 0
        
        new_version = self.current_versions[prompt_id] + 1
        self.prompts[prompt_id][new_version] = new_content
        self.current_versions[prompt_id] = new_version
        return {"version": new_version}

    def list_prompt_versions(self, prompt_id):
        if prompt_id in self.prompts and self.prompts[prompt_id]:
            return list(self.prompts[prompt_id].keys())
        return {"error": "No versions found"}

    def rollback_to_version(self, prompt_id, version):
        if prompt_id in self.prompts and version in self.prompts[prompt_id]:
            self.current_versions[prompt_id] = version
            return {"success": True}
        return {"error": "Version not found"}

