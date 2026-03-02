# PromptLab

## Project Overview
PromptLab is an innovative platform designed for

## Project Overview
PromptLab is an innovative platform designed for## Project Overview
PromptLab is an innovative platform designed for AI prompt engineering, providing tools for AI engineers to efficiently store, organize, and manage their prompts. This platform can be thought of as a "Postman for Prompts," facilitating a professional workspace with advanced functionalities like variable storage, organization, tagging, version tracking, and testing.

## Setup

**Installation Guide with Step-by-Step Instructions:**
1. **Prerequisites:**
   - Install Python 3.10+ and Node.js 18+
   - Ensure Git is installed

2. **Installation Steps:**
   - Clone the repository:
     ```bash
     git clone <your-repo-url>
     cd promptlab
     ```
   - Set up the backend:
     ```bash
     cd backend
     pip install -r requirements.txt
     python main.py
     ```
   - Access the API at: `http://localhost:8000` and API docs at: `http://localhost:8000/docs`

**API Summary with List of Endpoints with Descriptions:**
- **GET /health** - Checks the health status of the API service
- **GET /prompts** - Lists all stored prompts (issues present)
- **GET /prompts/{id}** - Retrieves a single prompt by ID (bug present)
- **POST /prompts** - Creates a new prompt
- **PUT /prompts/{id}** - Updates an existing prompt by ID (issues present)
- **DELETE /prompts/{id}** - Deletes a prompt by ID
- **GET /collections** - Lists all collections
- **GET /collections/{id}** - Retrieves a specific collection by ID
- **POST /collections** - Creates a new collection
- **DELETE /collections/{id}** - Deletes a collection by ID (bug present)

## Usage

**Code Examples for Common Operations:**
- **Creating a Prompt:**
  ```python
  import requests

  response = requests.post('http://localhost:8000/prompts', json={
      'title': 'Example Prompt',
      'template': 'Define the role of {{actor}} in {{context}}.',
  })
  print(response.json())
  ```

- **Listing all Prompts:**
  ```python
  import requests

  response = requests.get('http://localhost:8000/prompts')
  print(response.json())
  ```