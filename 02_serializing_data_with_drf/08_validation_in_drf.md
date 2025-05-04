# **Django DRF Serializer Validation Guid**e 📑

This guide provides a detailed explanation of implementing and testing Django REST Framework (DRF) serializer validations using a Python shell. It covers the provided Django models and serializer examples, demonstrating their practical use with code snippets, use cases, and step-by-step instructions. The examples are tested in a Django project with the `blog` and `author` apps, ensuring clarity for developers. 🛠️

## Table of Contents 📑

1. Serializer Examples and Shell Implementation
   - BlogCustom7Serializer: Custom Field-Level Validation
   - BlogCustom8Serializer: Reusable Field-Level Validator
   - BlogCustom9Serializer: Object-Level Validation
   - BlogCustom10Serializer: Custom Object-Level Validator
   - BlogCustom11Serializer: Validation Order
   - BlogCustom12Serializer: Disabling Default Validators
2. Best Practices

---

## Serializer Examples and Shell Implementation 💻

Each serializer example is implemented in the Python shell, with detailed explanations, code snippets, and use cases. The shell commands assume the project is set up, and models are populated with sample data.

### Initial Shell Setup

Before testing serializers, create sample data in the shell:

```python
from blog.models import Blog, CoverImage, Tags
from author.models import Author
from rest_framework import serializers

# Create an author
author = Author.objects.create(name="John Doe", email="john@example.com", bio="A passionate writer")

# Create a cover image
cover = CoverImage.objects.create(image_link="https://example.com/image.jpg")

# Create a tag
tag = Tags.objects.create(name="Tech")

# Create a blog
blog = Blog.objects.create(title="My First Blog", content="This is content", author=author, blog_cover_image=cover)
blog.tags.add(tag)
```

### BlogCustom7Serializer: Custom Field-Level Validation 🔍

**Code**:

```python
class BlogCustom7Serializer(serializers.ModelSerializer):
    def validate_title(self, value):
        print('validate_title method')
        if '_' in value:
            raise serializers.ValidationError('illegal char')
        return value
    
    class Meta:
        model = models.Blog
        fields = '__all__'
```

**Explanation**:

- Validates the `title` field to ensure it does not contain underscores (`_`).
- The `validate_title` method is automatically called when `is_valid()` is invoked.
- Raises a `ValidationError` if the condition is not met.

**Use Case**:

- Ensures blog titles adhere to formatting rules, avoiding unprofessional characters like underscores.
- Example: A blog platform requiring clean, professional titles.

**Shell Implementation**:

1. **Import Serializer**:

   ```python
   from blog.serializers import BlogCustom7Serializer
   ```

2. **Test Valid Data**:

   ```python
   data = {
       "title": "New Blog",
       "content": "This is a new blog post",
       "author": author.id,
       "blog_cover_image": cover.id,
       "tags": [tag.id]
   }
   serializer = BlogCustom7Serializer(data=data)
   serializer.is_valid()  # Returns: True
   print(serializer.validated_data)
   ```

   **Output**:

   - Prints: `validate_title method`
   - Validation passes as the title has no underscores.

3. **Test Invalid Data**:

   ```python
   data = {
       "title": "New_Blog",
       "content": "This is a new blog post",
       "author": author.id,
       "blog_cover_image": cover.id,
       "tags": [tag.id]
   }
   serializer = BlogCustom7Serializer(data=data)
   serializer.is_valid()  # Returns: False
   print(serializer.errors)  # {'title': ['illegal char']}
   ```

   **Output**:

   - Prints: `validate_title method`
   - Validation fails due to the underscore in the title.

### BlogCustom8Serializer: Reusable Field-Level Validator 🔄

**Code**:

```python
def demo_func_validator(attr):
    print('func val')
    if '_' in attr:
        raise serializers.ValidationError('invalid char')
    return attr

class BlogCustom8Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Blog
        fields = '__all__'
        extra_kwargs = {
            'title': {'validators': [demo_func_validator]},
            'content': {'validators': [demo_func_validator]}
        }
```

**Explanation**:

- Uses a reusable validator function `demo_func_validator` to check for underscores in `title` and `content`.
- Applied via `extra_kwargs` for better readability and reusability.

**Use Case**:

- Ideal for applying the same validation logic across multiple fields or serializers.
- Example: Ensuring both title and content are free of underscores for consistency.

**Shell Implementation**:

1. **Import Serializer**:

   ```python
   from blog.serializers import BlogCustom8Serializer
   ```

2. **Test Valid Data**:

   ```python
   data = {
       "title": "Clean Title",
       "content": "Clean content here",
       "author": author.id,
       "blog_cover_image": cover.id,
       "tags": [tag.id]
   }
   serializer = BlogCustom8Serializer(data=data)
   serializer.is_valid()  # Returns: True
   print(serializer.validated_data)
   ```

   **Output**:

   - Prints: `func val` (twice, for title and content)
   - Validation passes.

3. **Test Invalid Data**:

   ```python
   data = {
       "title": "Clean_Title",
       "content": "Clean_content",
       "author": author.id,
       "blog_cover_image": cover.id,
       "tags": [tag.id]
   }
   serializer = BlogCustom8Serializer(data=data)
   serializer.is_valid()  # Returns: False
   print(serializer.errors)  # {'title': ['invalid char'], 'content': ['invalid char']}
   ```

   **Output**:

   - Prints: `func val` (twice)
   - Validation fails for both fields.

### BlogCustom9Serializer: Object-Level Validation 🌐

**Code**:

```python
class BlogCustom9Serializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs['title'] == attrs['content']:
            raise serializers.ValidationError('Title and content cannot have same value')
        return attrs
    
    class Meta:
        model = models.Blog
        fields = '__all__'
```

**Explanation**:

- Performs object-level validation to ensure `title` and `content` are not identical.
- The `validate` method runs after all field-level validations pass.

**Use Case**:

- Prevents identical title and content to avoid meaningless blog posts.
- Example: Ensuring a blog post has distinct title and content for better user experience.

**Shell Implementation**:

1. **Import Serializer**:

   ```python
   from blog.serializers import BlogCustom9Serializer
   ```

2. **Test Valid Data**:

   ```python
   data = {
       "title": "Unique Title",
       "content": "Different content",
       "author": author.id,
       "blog_cover_image": cover.id,
       "tags": [tag.id]
   }
   serializer = BlogCustom9Serializer(data=data)
   serializer.is_valid()  # Returns: True
   print(serializer.validated_data)
   ```

   **Output**:

   - Validation passes as title and content differ.

3. **Test Invalid Data**:

   ```python
   data = {
       "title": "Same Text",
       "content": "Same Text",
       "author": author.id,
       "blog_cover_image": cover.id,
       "tags": [tag.id]
   }
   serializer = BlogCustom9Serializer(data=data)
   serializer.is_valid()  # Returns: False
   print(serializer.errors)  # {'non_field_errors': ['Title and content cannot have same value']}
   ```

   **Output**:

   - Validation fails due to identical title and content.

### BlogCustom10Serializer: Custom Object-Level Validator 🔧

**Code**:

```python
def custom_obj_validator(attrs):
    print('custom object validator')
    if attrs['title'] == attrs['content']:
        raise serializers.ValidationError('Title and content cannot have the same')
    return attrs

class BlogCustom10Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Blog
        fields = '__all__'
        validators = [custom_obj_validator]
```

**Explanation**:

- Uses a reusable object-level validator to check that `title` and `content` are not the same.
- Defined in the `Meta` class using the `validators` attribute.

**Use Case**:

- Reusable across multiple serializers for consistent object-level validation.
- Example: Applying the same title-content check in different blog-related serializers.

**Shell Implementation**:

1. **Import Serializer**:

   ```python
   from blog.serializers import BlogCustom10Serializer
   ```

2. **Test Valid Data**:

   ```python
   data = {
       "title": "Unique Title",
       "content": "Different content",
       "author": author.id,
       "blog_cover_image": cover.id,
       "tags": [tag.id]
   }
   serializer = BlogCustom10Serializer(data=data)
   serializer.is_valid()  # Returns: True
   print(serializer.validated_data)
   ```

   **Output**:

   - Prints: `custom object validator`
   - Validation passes.

3. **Test Invalid Data**:

   ```python
   data = {
       "title": "Same Text",
       "content": "Same Text",
       "author": author.id,
       "blog_cover_image": cover.id,
       "tags": [tag.id]
   }
   serializer = BlogCustom10Serializer(data=data)
   serializer.is_valid()  # Returns: False
   print(serializer.errors)  # {'non_field_errors': ['Title and content cannot have the same']}
   ```

   **Output**:

   - Prints: `custom object validator`
   - Validation fails.

### BlogCustom11Serializer: Validation Order 📈

**Code**:

```python
def func_validator(attr):
    print('func val')
    if '*' in attr:
        raise serializers.ValidationError('Illegal char')
    return attr

class BlogCustom11Serializer(serializers.ModelSerializer):
    def validate_title(self, value):
        print('validate_title method')
        if '_' in value:
            raise serializers.ValidationError('Illegal char')
        return value
    
    def validate(self, attrs):
        print('main validate method')
        return attrs
    
    class Meta:
        model = models.Blog
        fields = '__all__'
        extra_kwargs = {
            'title': {'validators': [func_validator]}
        }
```

**Explanation**:

- Demonstrates the order of validator execution:
  1. `func_validator` (checks for `*` in title) via `extra_kwargs`.
  2. `validate_title` (checks for `_` in title).
  3. `validate` (object-level, runs if field validations pass).
- Shows the predictable sequence of validation.

**Use Case**:

- Useful when applying multiple validators to a field and needing to understand their execution order.
- Example: Ensuring title is free of both `*` and `_` with prioritized checks.

**Shell Implementation**:

1. **Import Serializer**:

   ```python
   from blog.serializers import BlogCustom11Serializer
   ```

2. **Test Valid Data**:

   ```python
   data = {
       "title": "Clean Title",
       "content": "Content here",
       "author": author.id,
       "blog_cover_image": cover.id,
       "tags": [tag.id]
   }
   serializer = BlogCustom11Serializer(data=data)
   serializer.is_valid()  # Returns: True
   print(serializer.validated_data)
   ```

   **Output**:

   - Prints: `func val`, `validate_title method`, `main validate method`
   - Validation passes.

3. **Test Invalid Data (with** `*`**)**:

   ```python
   data = {
       "title": "Bad*Title",
       "content": "Content here",
       "author": author.id,
       "blog_cover_image": cover.id,
       "tags": [tag.id]
   }
   serializer = BlogCustom11Serializer(data=data)
   serializer.is_valid()  # Returns: False
   print(serializer.errors)  # {'title': ['Illegal char']}
   ```

   **Output**:

   - Prints: `func val`
   - Validation fails due to `*`.

4. **Test Invalid Data (with** `_`**)**:

   ```python
   data = {
       "title": "Bad_Title",
       "content": "Content here",
       "author": author.id,
       "blog_cover_image": cover.id,
       "tags": [tag.id]
   }
   serializer = BlogCustom11Serializer(data=data)
   serializer.is_valid()  # Returns: False
   print(serializer.errors)  # {'title': ['Illegal char']}
   ```

   **Output**:

   - Prints: `func val`, `validate_title method`
   - Validation fails due to `_`.

### BlogCustom12Serializer: Disabling Default Validators 🚫

**Code**:

```python
class BlogCustom12Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Blog
        fields = '__all__'
        validators = []
```

**Explanation**:

- Disables DRF's default validators (e.g., unique constraints on `title`).
- Custom validators (if defined) still apply.
- Database constraints remain enforced during save operations.

**Use Case**:

- Useful for testing or scenarios where default validation rules need to be bypassed.
- Example: Allowing duplicate titles during testing, though database constraints may still apply.

**Shell Implementation**:

1. **Import Serializer**:

   ```python
   from blog.serializers import BlogCustom12Serializer
   ```

2. **Test with Duplicate Title**:

   ```python
   data = {
       "title": "My First Blog",  # Already exists
       "content": "New content",
       "author": author.id,
       "blog_cover_image": cover.id,
       "tags": [tag.id]
   }
   serializer = BlogCustom12Serializer(data=data)
   serializer.is_valid()  # Returns: True
   print(serializer.validated_data)
   ```

   **Output**:

   - Validation passes as unique constraint is ignored.

3. **Test Save**:

   ```python
   try:
       serializer.save()
   except Exception as e:
       print(str(e))  # Database unique constraint error
   ```

   **Output**:

   - Database error due to unique constraint on `title`.

---

## Best Practices ✅

- **Clear Error Messages**: Write descriptive error messages for better user feedback. 📢
- **Reusable Validators**: Use functions for field and object-level validations to reduce code duplication. 🔄
- **Understand Validation Order**: Know that `extra_kwargs` validators run first, followed by `validate_<field>`, then `validate`. 📈
- **Test Thoroughly**: Use the Python shell to test edge cases and ensure robust validation. 🧪
- **Database Constraints**: Disabling default validators doesn't bypass database rules; handle exceptions during save. ⚠️

---