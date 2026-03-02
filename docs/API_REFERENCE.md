# API Reference

## Health Check Endpoint

- **Endpoint**: `GET /health`
- **Description**: Returns the health status and version of the application.
- **Response Example**:
  ```json
  {
    "status": "healthy",
    "version": "1.0.0"
  }
  ```

## Prompt Endpoints

1. **List Prompts**

   - **Endpoint**: `GET /prompts`
   - **Description**: Retrieve a list of prompts, optionally filtered by collection and search term, sorted by date.
   - **Request Example**:
     ```
     GET /prompts?collection_id=123&search=example
     ```
   - **Response Example**:
     ```json
     {
       "prompts": [
         {
           "id": "prompt1",
           "title": "Example Prompt",
           "content": "This is an example prompt.",
           "collection_id": "123"
         }
       ],
       "total": 1
     }
     ```

2. **Get Prompt by ID**

   - **Endpoint**: `GET /prompts/{prompt_id}`
   - **Description**: Retrieves a prompt by its ID.
   - **Request Example**:
     ```
     GET /prompts/prompt1
     ```
   - **Response Example**:
     ```json
     {
       "id": "prompt1",
       "title": "Example Prompt",
       "content": "This is an example prompt.",
       "collection_id": "123"
     }
     ```
   - **Error Codes**:
     - `404`: Prompt not found.

3. **Create Prompt**

   - **Endpoint**: `POST /prompts`
   - **Description**: Creates a new prompt.
   - **Request Example**:
     ```json
     {
       "title": "Example Prompt",
       "content": "This is an example prompt.",
       "collection_id": "123"
     }
     ```
   - **Response Example**:
     ```json
     {
       "id": "prompt1",
       "title": "Example Prompt",
       "content": "This is an example prompt.",
       "collection_id": "123"
     }
     ```
   - **Error Codes**:
     - `400`: Collection not found.

4. **Update Prompt**

   - **Endpoint**: `PUT /prompts/{prompt_id}`
   - **Description**: Updates an existing prompt by ID.
   - **Request Example**:
     ```json
     {
       "title": "Updated Title",
       "content": "Updated content",
       "collection_id": "123"
     }
     ```
   - **Response Example**:
     ```json
     {
       "id": "prompt1",
       "title": "Updated Title",
       "content": "Updated content",
       "collection_id": "123"
     }
     ```
   - **Error Codes**:
     - `404`: Prompt not found.
     - `400`: Collection not found.

5. **Patch Prompt**

   - **Endpoint**: `PATCH /prompts/{prompt_id}`
   - **Description**: Partially updates an existing prompt by ID.
   - **Request Example**:
     ```json
     {
       "title": "Partially Updated Title"
     }
     ```
   - **Response Example**:
     ```json
     {
       "id": "prompt1",
       "title": "Partially Updated Title"
     }
     ```
   - **Error Codes**:
     - `404`: Prompt not found.
     - `400`: Collection not found.

6. **Delete Prompt**

   - **Endpoint**: `DELETE /prompts/{prompt_id}`
   - **Description**: Deletes a prompt by ID.
   - **Request Example**:
     ```
     DELETE /prompts/prompt1
     ```
   - **Error Codes**:
     - `404`: Prompt not found.

## Collection Endpoints

1. **List Collections**

   - **Endpoint**: `GET /collections`
   - **Description**: Retrieves all available collections.
   - **Response Example**:
     ```json
     {
       "collections": [
         {
           "id": "123",
           "name": "Example Collection"
         }
       ],
       "total": 1
     }
     ```

2. **Get Collection by ID**

   - **Endpoint**: `GET /collections/{collection_id}`
   - **Description**: Retrieves a collection by its ID.
   - **Request Example**:
     ```
     GET /collections/123
     ```
   - **Response Example**:
     ```json
     {
       "id": "123",
       "name": "Example Collection"
     }
     ```
   - **Error Codes**:
     - `404`: Collection not found.

3. **Create Collection**

   - **Endpoint**: `POST /collections`
   - **Description**: Creates a new collection.
   - **Request Example**:
     ```json
     {
       "name": "New Collection"
     }
     ```
   - **Response Example**:
     ```json
     {
       "id": "124",
       "name": "New Collection"
     }
     ```

4. **Delete Collection**

   - **Endpoint**: `DELETE /collections/{collection_id}`
   - **Description**: Deletes a collection by ID.
   - **Request Example**:
     ```
     DELETE /collections/123
     ```
   - **Error Codes**:
     - `404`: Collection not found.

## Error Codes

- **404 Not Found**: Resource not found (e.g., Prompt or Collection does not exist).
- **400 Bad Request**: Invalid request data or a collection does not exist when creating/updating a prompt.
