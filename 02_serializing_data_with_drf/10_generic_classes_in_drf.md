# **Implementing Generic Views in DRF** 🚀

Hello! In this guide, we will implement all the **Generic Views** from Django REST Framework (DRF) as shown in the left sidebar of the provided screenshot. These views are pre-built tools that simplify CRUD (Create, Read, Update, Delete) operations. We’ll create separate classes for each view, set up their URLs, and provide detailed explanations in simple English with use cases. Let’s dive in! 🌟

---

## 📘 Step 1: Understanding Generic Views

Before we start coding, let’s understand the key components from the screenshot:

### GenericAPIView (Base Class)
- This is the foundation for all generic views. It allows us to configure `queryset` (data source) and `serializer_class` (data handler).

### Mixins (Helper Classes)
Mixins are small helper classes that add specific functionalities to `GenericAPIView`:
- **ListModelMixin**: Handles listing all objects (GET request).
- **CreateModelMixin**: Handles creating new objects (POST request).
- **RetrieveModelMixin**: Handles retrieving a single object (GET with ID).
- **UpdateModelMixin**: Handles updating objects (PUT/PATCH request).
- **DestroyModelMixin**: Handles deleting objects (DELETE request).

### Concrete View Classes (Ready-to-Use Classes)
These are pre-built classes that combine `GenericAPIView` with mixins:
- **CreateAPIView**: For creating new objects (POST).
- **ListAPIView**: For listing all objects (GET).
- **RetrieveAPIView**: For retrieving a single object (GET with ID).
- **DestroyAPIView**: For deleting an object (DELETE).
- **UpdateAPIView**: For updating an object (PUT/PATCH).
- **ListCreateAPIView**: For listing and creating objects (GET + POST).
- **RetrieveUpdateAPIView**: For retrieving and updating an object (GET + PUT/PATCH).

We’ll implement all these views for a blogging application using the `Blog` model and `BlogSerializer`. Let’s get started! 🎉

---

## 🛠️ Step 2: Implementing Generic Views

We’ll create a separate class for each view, explain it in detail, and provide URLs and use cases.

### 2.1 CreateAPIView (Create a New Blog) ➕

This view is used to create a new blog (POST request only).

#### Code

```python
# blog/views.py
from rest_framework.generics import CreateAPIView
from . import models
from . import serializers

class BlogCreateView(CreateAPIView):
    serializer_class = serializers.BlogSerializer
    queryset = models.Blog.objects.all()
```

#### URLs

```python
# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/blogs/create/', views.BlogCreateView.as_view(), name='blog-create'),
]
```

#### Detailed Explanation 🔍

- **What is This View?**: `CreateAPIView` is designed specifically to create new objects (e.g., a blog) using a POST request.
- **`serializer_class`**: This specifies that we’ll use `BlogSerializer` to validate and serialize the data sent by the client.
- **`queryset`**: This tells the view to work with the `Blog` model. It’s required because the serializer needs to know which model to interact with.
- **How It Works**:
  - When a client sends a POST request to `/api/blogs/create/`, this view automatically handles it.
  - It takes the JSON data from `request.data`, passes it to the serializer, validates it, and saves it to the database if valid.
  - If successful, it returns the new object with a `201 Created` status.
- **Use Case 🌟**: Imagine a user wants to add a new blog post. They send this JSON:
  ```json
  {
    "title": "My New Blog",
    "content": "This is my first blog!",
    "author": 1,
    "blog_cover_image": 1,
    "tags": [1, 2]
  }
  ```
  The view saves it and returns the new blog data.

---

### 2.2 ListAPIView (List All Blogs) 📋

This view is used to display a list of all blogs (GET request only).

#### Code

```python
class BlogListView(ListAPIView):
    serializer_class = serializers.BlogSerializer
    queryset = models.Blog.objects.all()
```

#### URLs

```python
urlpatterns.append(
    path('api/blogs/list/', views.BlogListView.as_view(), name='blog-list')
)
```

#### Detailed Explanation 🔍

- **What is This View?**: `ListAPIView` is designed to fetch and display a list of all objects (e.g., all blogs) using a GET request.
- **`serializer_class`**: Uses `BlogSerializer` to convert the list of blogs into JSON.
- **`queryset`**: Specifies that it should retrieve all `Blog` objects from the database.
- **How It Works**:
  - When a client sends a GET request to `/api/blogs/list/`, this view fetches all blogs and converts them into JSON using the serializer.
  - It then sends the JSON data back to the client.
- **Use Case 🌟**: If you want to show all blogs on a website, this view will return:
  ```json
  [
    {
      "id": 1,
      "title": "My First Blog",
      "content": "This is my first blog!",
      "author": 1,
      "blog_cover_image": 1,
      "tags": [1, 2]
    }
  ]
  ```

---

### 2.3 RetrieveAPIView (Retrieve a Single Blog) 📄

This view is used to display a single blog by its ID (GET request).

#### Code

```python
class BlogRetrieveView(RetrieveAPIView):
    serializer_class = serializers.BlogSerializer
    queryset = models.Blog.objects.all()
```

#### URLs

```python
urlpatterns.append(
    path('api/blogs/<int:pk>/retrieve/', views.BlogRetrieveView.as_view(), name='blog-retrieve')
)
```

#### Detailed Explanation 🔍

- **What is This View?**: `RetrieveAPIView` fetches and displays a single object (e.g., a blog) based on its ID using a GET request.
- **`queryset`**: Defines the data source as all `Blog` objects.
- **How It Works**:
  - When a client visits `/api/blogs/1/retrieve/`, the `pk` (primary key, e.g., 1) is used to find the specific blog.
  - The view uses `self.get_object()` (a built-in method) to retrieve the blog and converts it to JSON with the serializer.
  - If the blog exists, it returns the data; if not, it returns a `404 Not Found` error.
- **Use Case 🌟**: A user wants to see a specific blog:
  ```json
  {
    "id": 1,
    "title": "My First Blog",
    "content": "This is my first blog!",
    "author": 1,
    "blog_cover_image": 1,
    "tags": [1, 2]
  }
  ```

---

### 2.4 DestroyAPIView (Delete a Blog) 🗑️

This view is used to delete a single blog by its ID (DELETE request).

#### Code

```python
class BlogDestroyView(DestroyAPIView):
    serializer_class = serializers.BlogSerializer
    queryset = models.Blog.objects.all()
```

#### URLs

```python
urlpatterns.append(
    path('api/blogs/<int:pk>/delete/', views.BlogDestroyView.as_view(), name='blog-delete')
)
```

#### Detailed Explanation 🔍

- **What is This View?**: `DestroyAPIView` is designed to delete a specific object (e.g., a blog) using a DELETE request.
- **How It Works**:
  - When a client sends a DELETE request to `/api/blogs/1/delete/`, the view finds the blog with ID 1 and removes it from the database.
  - It returns a `204 No Content` status if successful.
- **Use Case 🌟**: A user wants to delete a blog. After sending a DELETE request, the blog is gone, and the server confirms with a 204 status.

---

### 2.5 UpdateAPIView (Update a Blog) 🔄

This view is used to update a blog (supports PUT and PATCH requests).

#### Code

```python
class BlogUpdateView(UpdateAPIView):
    serializer_class = serializers.BlogSerializer
    queryset = models.Blog.objects.all()
```

#### URLs

```python
urlpatterns.append(
    path('api/blogs/<int:pk>/update/', views.BlogUpdateView.as_view(), name='blog-update')
)
```

#### Detailed Explanation 🔍

- **What is This View?**: `UpdateAPIView` updates an existing object (e.g., a blog) using PUT (full update) or PATCH (partial update) requests.
- **How It Works**:
  - **PUT**: If a client sends a PUT request to `/api/blogs/1/update/` with all fields:
    ```json
    {
      "title": "Updated Blog",
      "content": "This is updated content!",
      "author": 1,
      "blog_cover_image": 1,
      "tags": [1, 2]
    }
    ```
    It replaces the entire blog with the new data.
  - **PATCH**: If a client sends a PATCH request with some fields:
    ```json
    {
      "title": "Partially Updated Blog"
    }
    ```
    It updates only the `title` field.
- **Use Case 🌟**: A user wants to modify a blog, either fully or partially, depending on the request type.

---

### 2.6 ListCreateAPIView (List and Create Blogs) 📋➕

This view handles both listing all blogs and creating a new blog (GET + POST).

#### Code

```python
class BlogListCreateView(ListCreateAPIView):
    serializer_class = serializers.BlogSerializer
    queryset = models.Blog.objects.all()
```

#### URLs

```python
urlpatterns.append(
    path('api/blogs/list-create/', views.BlogListCreateView.as_view(), name='blog-list-create')
)
```

#### Detailed Explanation 🔍

- **What is This View?**: `ListCreateAPIView` combines listing all objects (GET) and creating a new object (POST) in one view.
- **How It Works**:
  - **GET**: `/api/blogs/list-create/` returns a list of all blogs.
  - **POST**: A new blog is created when a POST request is sent.
- **Use Case 🌟**: If you want a single endpoint to show all blogs and allow creating new ones, this is perfect. For example, a GET request lists blogs, and a POST request adds a new one.

---

### 2.7 RetrieveUpdateAPIView (Retrieve and Update a Blog) 📄🔄

This view handles retrieving a blog and updating it (GET + PUT/PATCH).

#### Code

```python
class BlogRetrieveUpdateView(RetrieveUpdateAPIView):
    serializer_class = serializers.BlogSerializer
    queryset = models.Blog.objects.all()
```

#### URLs

```python
urlpatterns.append(
    path('api/blogs/<int:pk>/retrieve-update/', views.BlogRetrieveUpdateView.as_view(), name='blog-retrieve-update')
)
```

#### Detailed Explanation 🔍

- **What is This View?**: `RetrieveUpdateAPIView` allows retrieving a single blog (GET) and updating it (PUT/PATCH) at the same endpoint.
- **How It Works**:
  - **GET**: `/api/blogs/1/retrieve-update/` shows the blog with ID 1.
  - **PUT/PATCH**: Updates the blog based on the request data.
- **Use Case 🌟**: A user can view a blog and update it from the same URL, making it convenient for editing.

---

## 🌐 Step 3: Project URLs

We need to include these URLs in the project’s main `urls.py`:

```python
# projects/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]
```

- **Explanation**: `path('', include('blog.urls'))` integrates all the URLs from `blog/urls.py` into the project.

---

## 🧪 Step 4: Testing with Use Cases

Let’s test each view with examples using a tool like Postman.

### 1. CreateAPIView (Create a Blog)
- **URL**: `http://127.0.0.1:8000/api/blogs/create/`
- **Method**: POST
- **JSON Data**:
  ```json
  {
    "title": "New Blog",
    "content": "This is a new blog!",
    "author": 1,
    "blog_cover_image": 1,
    "tags": [1, 2]
  }
  ```
- **Expected Response**: 201 Created with the new blog data.

### 2. ListAPIView (List All Blogs)
- **URL**: `http://127.0.0.1:8000/api/blogs/list/`
- **Method**: GET
- **Expected Response**:
  ```json
  [
    {
      "id": 1,
      "title": "My First Blog",
      "content": "This is my first blog!",
      "author": 1,
      "blog_cover_image": 1,
      "tags": [1, 2]
    }
  ]
  ```

### 3. RetrieveAPIView (Retrieve a Blog)
- **URL**: `http://127.0.0.1:8000/api/blogs/1/retrieve/`
- **Method**: GET
- **Expected Response**: Data for the blog with ID 1.

### 4. DestroyAPIView (Delete a Blog)
- **URL**: `http://127.0.0.1:8000/api/blogs/1/delete/`
- **Method**: DELETE
- **Expected Response**: 204 No Content (success).

### 5. UpdateAPIView (Update a Blog)
- **URL**: `http://127.0.0.1:8000/api/blogs/1/update/`
- **Method**: PUT
- **JSON Data**:
  ```json
  {
    "title": "Updated Blog",
    "content": "This is updated content!",
    "author": 1,
    "blog_cover_image": 1,
    "tags": [1, 2]
  }
  ```
- **Expected Response**: 200 OK with updated data.

### 6. ListCreateAPIView (List and Create)
- **URL**: `http://127.0.0.1:8000/api/blogs/list-create/`
- **Method**: GET or POST
- **GET Response**: List of all blogs.
- **POST JSON Data**:
  ```json
  {
    "title": "Another Blog",
    "content": "This is another blog!",
    "author": 1,
    "blog_cover_image": 1,
    "tags": [1, 2]
  }
  ```
- **POST Response**: 201 Created with new data.

### 7. RetrieveUpdateAPIView (Retrieve and Update)
- **URL**: `http://127.0.0.1:8000/api/blogs/1/retrieve-update/`
- **Method**: GET or PUT/PATCH
- **GET Response**: Blog with ID 1.
- **PUT JSON Data**:
  ```json
  {
    "title": "Updated Again",
    "content": "This is updated again!",
    "author": 1,
    "blog_cover_image": 1,
    "tags": [1, 2]
  }
  ```
- **PUT Response**: 200 OK with updated data.

---

# **Customizing `get_queryset()`** 🚀

## 📘 Step 1: Understanding `get_queryset()` and QuerySet

Before diving into the implementation, let’s understand the key concepts:

- **GenericAPIView**: This is a base class in DRF that provides the foundation for generic views, allowing configuration of `queryset` and `serializer_class`.
- **queryset**: A static attribute that defines the data source, typically set as `Blog.objects.all()` to retrieve all objects from the `Blog` model.
- **get_queryset()**: A customizable method that dynamically returns a queryset. It’s preferred over the `queryset` attribute because it offers flexibility to filter or modify data based on request conditions.
- **Customization**: Using `get_queryset()`, we can apply filters (e.g., `id__gt=10` for IDs greater than 10) to tailor the data sent to the serializer.

The documentation suggests using `get_queryset()` over the `queryset` attribute for better control, especially when overriding view methods. Let’s implement this with an example.

---

## 🛠️ Step 2: Implementing the Code

We’ll create a `ListCreateAPIView` to handle listing blogs with IDs greater than 10 (GET request) and creating new blogs (POST request). Here’s the implementation.

### Code

```python
# blog/views.py
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from . import models
from . import serializers

class BlogGetUpdateView(ListCreateAPIView):
    serializer_class = serializers.BlogSerializer

    def get_queryset(self):
        # Customizing the queryset to filter blogs with ID greater than 10
        blogs_queryset = models.Blog.objects.filter(id__gt=10)
        return blogs_queryset

    def post(self, request):
        # Handling the creation of a new blog
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### URLs

```python
# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/blogs/custom/', views.BlogGetUpdateView.as_view(), name='blog-custom'),
]
```

### Project URLs

```python
# projects/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]
```

---

## 📝 Step 3: Detailed Explanation 🔍

Let’s break down the code and concepts step by step:

### Class Structure
- **`class BlogGetUpdateView(ListCreateAPIView)`**: This class inherits from `ListCreateAPIView`, which supports both listing objects (GET) and creating new objects (POST).
- **`serializer_class = serializers.BlogSerializer`**: This specifies that `BlogSerializer` will be used to validate, serialize, and deserialize the blog data.

### `get_queryset()` Method
- **What is It?**: This method allows us to customize the queryset dynamically. It runs whenever the view needs to fetch data from the database.
- **Code Breakdown**:
  - `blogs_queryset = models.Blog.objects.filter(id__gt=10)`:
    - `models.Blog.objects` accesses all `Blog` objects in the database.
    - `.filter(id__gt=10)` applies a filter to select only blogs where the `id` is greater than 10. The `__gt` stands for "greater than."
  - `return blogs_queryset`: Returns the customized queryset to be used by the serializer and view.
- **Why is It Better?**: If we used `queryset = models.Blog.objects.all()`, it would always return all blogs. With `get_queryset()`, we can change the filter based on the request or logic, making it more flexible.

### `post` Method
- **What is It?**: This method handles the creation of a new blog when a POST request is received.
- **Code Breakdown**:
  - `serializer = self.get_serializer(data=request.data)`: Passes the JSON data from the client (stored in `request.data`) to the serializer for validation.
  - `if serializer.is_valid()`: Checks if the data meets the model’s rules (e.g., unique title, required fields).
  - `serializer.save()`: Saves the validated data to the database if it’s valid.
  - `return Response(serializer.data, status=status.HTTP_201_CREATED)`: Returns the newly created blog data with a `201 Created` status.
  - `return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)`: Returns validation errors with a `400 Bad Request` status if the data is invalid.

### URLs
- **`path('api/blogs/custom/', views.BlogGetUpdateView.as_view(), name='blog-custom')`**: Maps the URL `/api/blogs/custom/` to the `BlogGetUpdateView` class. The `name` attribute allows us to refer to this URL in templates or code.
- **Project URLs**: `path('', include('blog.urls'))` integrates the `blog/urls.py` into the project’s root URL configuration.

---

## 🌐 Step 4: How It Works 🛠️

- **GET Request**: When a client sends a GET request to `/api/blogs/custom/`, the view executes `get_queryset()` and returns only the blogs with IDs greater than 10. For example, if the database has blogs with IDs 11, 12, and 13, only those will be included in the response.
- **POST Request**: When a client sends a POST request to `/api/blogs/custom/`, the view creates a new blog regardless of its ID and returns the saved data. The new blog’s ID will be assigned automatically by the database.

---

## 🧪 Step 5: Testing and Use Cases

### 1. GET Request (List Blogs with ID > 10)
- **URL**: `http://127.0.0.1:8000/api/blogs/custom/`
- **Method**: GET
- **Expected Response**:
  ```json
  [
    {
      "id": 11,
      "title": "Blog 11",
      "content": "This is blog 11",
      "author": 1,
      "blog_cover_image": 1,
      "tags": [1, 2]
    },
    {
      "id": 12,
      "title": "Blog 12",
      "content": "This is blog 12",
      "author": 1,
      "blog_cover_image": 1,
      "tags": [1, 2]
    }
  ]
  ```
  (This will only work if the database contains blogs with IDs greater than 10.)

### 2. POST Request (Create a New Blog)
- **URL**: `http://127.0.0.1:8000/api/blogs/custom/`
- **Method**: POST
- **JSON Data**:
  ```json
  {
    "title": "New Blog 13",
    "content": "This is a new blog with ID 13",
    "author": 1,
    "blog_cover_image": 1,
    "tags": [1, 2]
  }
  ```
- **Expected Response**: 201 Created with the new blog data (e.g., ID 13, assigned by the database).

---


# **Implementing Filtering with `SearchFilter` and `OrderingFilter`** 🔍


## 📘 Step 1: Understanding `SearchFilter` and `OrderingFilter`

Before we start coding, let’s understand the key concepts:

- **`SearchFilter`**: This backend enables basic search functionality across specified fields. Users can search for keywords, and the filter returns matching objects.
- **`OrderingFilter`**: This backend allows sorting of data based on one or more fields in ascending or descending order.
- **`filter_backends`**: A list attribute that specifies which filter backends to use (e.g., `[filters.SearchFilter, filters.OrderingFilter]`).
- **`ordering_fields`**: A list of fields that can be used for sorting.
- **`search_fields`**: A list of fields where the search operation will be applied.

### Comparison with `get_queryset()`
- The `get_queryset()` method provides low-level control, allowing manual filtering (e.g., `Blog.objects.filter(id__gt=10)`).
- In contrast, `SearchFilter` and `OrderingFilter` are higher-level tools designed for generic use cases like searching and ordering, reducing the need for custom code.

The DRF documentation recommends using these filters for standard operations, with the option to create custom filter backends if needed.

---

## 🛠️ Step 2: Implementing the Code

We’ll create two views:
1. A `ListAPIView` using `OrderingFilter` to sort blogs by title.
2. A `ListAPIView` using `SearchFilter` to search blogs by title or content.

### 2.1 Implementing `OrderingFilter`

This view will display a list of blogs sorted by the `title` field.

#### Code

```python
# blog/views.py
from rest_framework.generics import ListAPIView
from rest_framework import filters
from . import models
from . import serializers

class BlogGetUpdateFilterView(ListAPIView):
    serializer_class = serializers.BlogSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['title']  # Fields available for sorting
    ordering = 'title'  # Default sorting field

    def get_queryset(self):
        # Base queryset (optional, as filter will handle ordering)
        return models.Blog.objects.all()
```

#### URLs

```python
# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/blogs/ordered/', views.BlogGetUpdateFilterView.as_view(), name='blog-ordered'),
]
```

#### Project URLs

```python
# projects/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]
```

---

### 2.2 Implementing `SearchFilter`

This view will allow searching blogs based on the `title` or `content` fields.

#### Code

```python
class BlogSearchView(ListAPIView):
    serializer_class = serializers.BlogSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']  # Fields to search in

    def get_queryset(self):
        return models.Blog.objects.all()
```

#### URLs

```python
urlpatterns.append(
    path('api/blogs/search/', views.BlogSearchView.as_view(), name='blog-search')
)
```

---

## 📝 Step 3: Detailed Explanation 🔍

Let’s break down each component in detail:

### 3.1 `OrderingFilter` Implementation

#### Class Structure
- **`class BlogGetUpdateFilterView(ListAPIView)`**: This is a `ListAPIView` that handles listing objects.
- **`serializer_class = serializers.BlogSerializer`**: Specifies `BlogSerializer` to serialize the blog data into JSON.
- **`filter_backends = [filters.OrderingFilter]`**: Indicates that the `OrderingFilter` backend will be used.
- **`ordering_fields = ['title']`**: Defines `title` as the field users can sort by. Additional fields can be added to the list if needed.
- **`ordering = 'title'`**: Sets the default sorting order to `title` in ascending order. Users can override this with query parameters.
- **`get_queryset()`**: Returns all `Blog` objects as the base queryset, which the `OrderingFilter` will sort.

#### How It Works
- When a GET request is made to `/api/blogs/ordered/`, the view fetches all blogs and sorts them by `title` by default.
- Users can customize the sorting using the `ordering` query parameter:
  - `/api/blogs/ordered/?ordering=title` for ascending order.
  - `/api/blogs/ordered/?ordering=-title` for descending order (the `-` prefix indicates descending).
- The filter automatically applies the sorting based on the provided parameter.

#### Use Case 🌟
- **Example**: Suppose the database contains:
  - ID 1: Title = "Zebra Blog"
  - ID 2: Title = "Apple Blog"
  - ID 3: Title = "Mango Blog"
- **Default Response** (GET `/api/blogs/ordered/`):
  ```json
  [
    { "id": 2, "title": "Apple Blog", ... },
    { "id": 3, "title": "Mango Blog", ... },
    { "id": 1, "title": "Zebra Blog", ... }
  ]
  ```
- **Descending Response** (GET `/api/blogs/ordered/?ordering=-title`):
  ```json
  [
    { "id": 1, "title": "Zebra Blog", ... },
    { "id": 3, "title": "Mango Blog", ... },
    { "id": 2, "title": "Apple Blog", ... }
  ]
  ```

---

### 3.2 `SearchFilter` Implementation

#### Class Structure
- **`class BlogSearchView(ListAPIView)`**: Another `ListAPIView` for listing objects.
- **`filter_backends = [filters.SearchFilter]`**: Specifies the use of the `SearchFilter` backend.
- **`search_fields = ['title', 'content']`**: Defines `title` and `content` as the fields where search will be performed.
- **`get_queryset()`**: Returns all `Blog` objects as the base queryset, which the `SearchFilter` will filter.

#### How It Works
- When a GET request is made to `/api/blogs/search/`, users can add a `search` query parameter (e.g., `/api/blogs/search/?search=apple`).
- The `SearchFilter` searches for the keyword "apple" in the `title` and `content` fields.
- The search is case-insensitive, so "Apple" or "apple" will match.
- Only matching blogs are returned in the response.

#### Use Case 🌟
- **Example**: Suppose the database contains:
  - ID 1: Title = "Apple Blog", Content = "This is about apples"
  - ID 2: Title = "Mango Blog", Content = "This is about mangoes"
- **Search Response** (GET `/api/blogs/search/?search=apple`):
  ```json
  [
    { "id": 1, "title": "Apple Blog", "content": "This is about apples", ... }
  ]
  ```
- **Another Search Response** (GET `/api/blogs/search/?search=mango`):
  ```json
  [
    { "id": 2, "title": "Mango Blog", "content": "This is about mangoes", ... }
  ]
  ```

---

## 🧪 Step 4: Testing and Use Cases

### 1. `OrderingFilter` Testing
- **URL**: `http://127.0.0.1:8000/api/blogs/ordered/`
- **Method**: GET
- **Expected Response**: Blogs sorted by `title` in ascending order.
- **URL with Descending Order**: `http://127.0.0.1:8000/api/blogs/ordered/?ordering=-title`
- **Expected Response**: Blogs sorted by `title` in descending order.

### 2. `SearchFilter` Testing
- **URL**: `http://127.0.0.1:8000/api/blogs/search/?search=apple`
- **Method**: GET
- **Expected Response**: Blogs where `title` or `content` contains "apple".

---

