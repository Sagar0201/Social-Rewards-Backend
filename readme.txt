
1️⃣ 📄 User Login
-------------------
Endpoint:  POST /api/auth/login/
Description:  Logs in the user and returns the authentication token.
Parameters:
  - Request Body (JSON):
    {
        "username": "john_doe",
        "password": "password123"
    }
Response:
  - 200 OK: Returns a token for authenticated access.
    {
        "token": "abc123xyz456"
    }
Error Example:
  - 400 Bad Request: Occurs when the request body is missing parameters or is invalid.
    {
        "detail": "Invalid username or password."
    }

2️⃣ 📄 User Signup
--------------------
Endpoint:  POST /api/auth/signup/
Description:  Registers a new user and returns the user details.
Parameters:
  - Request Body (JSON):
    {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "username": "john_doe",
        "password": "password123",
        "phone": "9876543210"
    }
Response:
  - 201 Created: Returns the created user details.
    {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "phone": "9876543210"
    }
Error Example:
  - 400 Bad Request: Occurs when the request is missing required parameters.
    {
        "detail": "This field is required."
    }

3️⃣ 📄 Get User Profile
--------------------------
Endpoint:  GET /api/auth/profile/
Description:  Returns profile details of the authenticated user.
Permissions:  Authenticated user only.
Headers:
  - Authorization: Token <user_token>
Response:
  - 200 OK: Returns the profile details of the authenticated user.
    {
        "id": 1,
        "username": "john_doe",
	"is_staff": "true"
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "9876543210",
        "points": 100
    }
Error Example:
  - 401 Unauthorized: Occurs when authentication credentials are missing or invalid.
    {
        "detail": "Authentication credentials were not provided."
    }

4️⃣ 📄 App Category List and Create
------------------------------------
Endpoint:  GET /api/admin/categories/  [GET] | POST /api/admin/categories/  [POST]
Description:  
  - GET: Lists all app categories.
  - POST: Creates a new app category (Admin only).
Parameters:
  - Request Body (JSON) for POST:
    {
        "name": "Social Media"
    }
Response:
  - 200 OK for GET: Returns a list of app categories.
    [
        {
            "id": 1,
            "name": "Social Media"
        },
        {
            "id": 2,
            "name": "Productivity"
        }
    ]
  - 201 Created for POST: Returns the created app category.
    {
        "id": 3,
        "name": "Gaming"
    }

5️⃣ 📄 App Category Detail (Update/Delete)
--------------------------------------------
Endpoint:  PUT /api/admin/categories/<int:pk>/  [PUT] | DELETE /api/admin/categories/<int:pk>/  [DELETE]
Description:  
  - PUT: Updates an app category (Admin only).
  - DELETE: Deletes an app category (Admin only).
Parameters:
  - Request Body (JSON) for PUT:
    {
        "name": "Updated Category"
    }
  - URL Parameter:
    - pk: The ID of the category.
Response:
  - 200 OK for PUT: Returns the updated app category.
    {
        "id": 1,
        "name": "Updated Category"
    }
  - 204 No Content for DELETE: No content is returned upon successful deletion.

6️⃣ 📄 App Sub Category List and Create
-----------------------------------------
Endpoint:  GET /api/admin/subcategories/  [GET] | POST /api/admin/subcategories/  [POST]
Description:  
  - GET: Lists all app subcategories.
  - POST: Creates a new app subcategory (Admin only).
Parameters:
  - Request Body (JSON) for POST:
    {
        "name": "Messaging",
        "category_id": 1
    }
Response:
  - 200 OK for GET: Returns a list of app subcategories.
    [
        {
            "id": 1,
            "name": "Messaging",
            "category": {
                "id": 1,
                "name": "Social Media"
            }
        },
        {
            "id": 2,
            "name": "Video Calls",
            "category": {
                "id": 1,
                "name": "Social Media"
            }
        }
    ]
  - 201 Created for POST: Returns the created app subcategory.
    {
        "id": 3,
        "name": "Music Streaming",
        "category": {
            "id": 1,
            "name": "Social Media"
        }
    }

7️⃣ 📄 App List and Create
----------------------------
Endpoint:  GET /api/apps/  [GET] | POST /api/apps/  [POST]
Description:  
  - GET: Lists all apps (authenticated users).
  - POST: Creates a new app (Admin only).
Parameters:
  - Request Body (JSON) for POST:
    {
        "name": "Instagram",
        "description": "Social media app",
        "points": 100,
        "sub_category": 1
    }
Response:
  - 200 OK for GET: Returns a list of apps.
    [
        {
            "id": 1,
            "name": "Instagram",
            "description": "Social media app",
            "points": 100,
            "sub_category": {
                "id": 1,
                "name": "Messaging"
            }
        }
    ]
  - 201 Created for POST: Returns the created app.
    {
        "id": 2,
        "name": "Facebook",
        "description": "Social networking site",
        "points": 200,
        "sub_category": {
            "id": 1,
            "name": "Messaging"
        }
    }

8️⃣ 📄 App Task List and Create
-------------------------------
Endpoint:  GET /api/tasks/  [GET] | POST /api/tasks/  [POST]
Description:  
  - GET: Lists all tasks for users (authenticated users).
  - POST: Creates a new task (Users only).
Parameters:
  - Request Body (JSON) for POST:
    {
        "app_id": 1,
        "screenshot": "image_url"
    }
Response:
  - 200 OK for GET: Returns a list of tasks for the authenticated user.
    [
        {
            "id": 1,
            "app_name": "Instagram",
            "status": "Pending",
            "created_at": "2025-04-12T12:34:56Z"
        }
    ]
  - 201 Created for POST: Returns the created task.
    {
        "id": 1,
        "app_name": "Instagram",
        "status": "Pending",
        "created_at": "2025-04-12T12:34:56Z"
    }

9️⃣ 📄 Update Task Status
-------------------------
Endpoint:  PATCH /api/tasks/<int:pk>/update-status/
Description:  Admin can update the status of a task (Approve/Reject).
Parameters:
  - URL Parameter:
    - pk: The ID of the task.
  - Request Body (JSON):
    {
        "status": "Approved"
    }
Response:
  - 200 OK: Returns the updated task status.
    {
        "id": 1,
        "app_name": "Instagram",
        "status": "Approved",
        "created_at": "2025-04-12T12:34:56Z"
    }
