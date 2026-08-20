# Pydantic: Data Validation in AI

Pydantic is a data validation library for Python. It acts as a strict checkpoint, ensuring that the data entering your application (like an ML model or API) is correct, formatted properly, and safe to use.

### 1. Setup and Essential Imports

First, we import the tools we need from Pydantic and standard Python typing libraries.

```python
# !pip install pydantic

from pydantic import BaseModel, Field, field_validator, model_validator, computed_field, ConfigDict, EmailStr, HttpUrl
from typing import Optional, Literal
from datetime import date

```

### 2. Basic Models, Fields, and Constraints

To use Pydantic, we create a class that inherits from `BaseModel`.
Here, we apply:

* **Required Fields:** By default, fields are required (or forced using `...` in `Field`).
* **Optional Fields:** Using `Optional[]` allows the field to be `None` if not provided.
* **Default Values:** e.g., `is_available: bool = True`.
* **Constraints:** Using `Field()` to enforce rules like `min_length` for strings, or `gt=0` (greater than zero) for numbers.
* **Nested/Literal Data:** `Literal` restricts inputs to a specific set of predefined choices.

```python
class BasicMenuItem(BaseModel):
    # Standard required field
    item_id: int
    
    # Required with constraints
    name: str = Field(..., min_length=3, max_length=50, description="Name of the dish")
    price: float = Field(..., gt=0, description="Price must be greater than zero")
    
    # Literal restricts this field to exactly these 4 string choices
    category: Literal["Starter", "Main Course", "Dessert", "Beverage"]
    
    # Default value (if user skips it, it becomes True)
    is_available: bool = True
    
    # Optional field (can be skipped entirely)
    description: Optional[str] = None

# Let's test it with a valid input
item1 = BasicMenuItem(
    item_id=101, 
    name="Garlic Bread", 
    price=150.0, 
    category="Starter"
)
print("Basic Item Created:", item1)

```

### 3. Custom Validators

Sometimes data is technically the right type (e.g., a string), but it's formatted poorly or fails a logical business rule. We use custom validators for this:

1. **`@field_validator`**: Cleans or checks a single field (e.g., fixing messy capitalization).
2. **`@model_validator`**: Checks logical relationships between *multiple* fields.
3. **`@computed_field`**: Automatically creates and calculates a brand new field.

```python
class ValidatedMenuItem(BasicMenuItem):
    
    # 1. Field Validator: Fixes messy text inputs
    @field_validator("name")
    @classmethod
    def clean_name_format(cls, value: str):
        # Converts "pAnEeR tIkKa" -> "Paneer Tikka"
        return value.title()

    # 2. Model Validator: Cross-checks multiple fields
    @model_validator(mode="after")
    def check_logical_pricing(self):
        # Business Rule: If an item is available, it must cost money.
        if self.is_available and self.price <= 0:
            raise ValueError("An available menu item must have a price > 0")
        return self

    # 3. Computed Field: Creates a new field automatically
    @computed_field
    @property
    def price_with_tax(self) -> float:
        # Adds 5% tax and rounds to 2 decimal places
        return round(self.price * 1.05, 2)

# Testing the validators
messy_data = {
    "item_id": 102,
    "name": "mAsAlA dOsA",  # Messy casing
    "price": 120.0,
    "category": "Main Course"
}

validated_item = ValidatedMenuItem(**messy_data)
print(f"Cleaned Name: {validated_item.name}")
print(f"Computed Tax Price: {validated_item.price_with_tax}")

```

### 4. Model Configurations (`model_config`)

Configurations let you control how the *entire* form behaves.

* **`extra='forbid'`**: Crashes if the user tries to pass fields that don't exist in our model.
* **`frozen=True`**: Prevents anyone from modifying the data after the object is created (like a Tuple).
* **`strict=True`**: Prevents Pydantic from trying to guess/convert data types (e.g., stops converting the string `"10"` into the integer `10`).

```python
class ConfiguredMenuItem(ValidatedMenuItem):
    
    # Apply model configurations
    model_config = ConfigDict(
        extra="forbid",   # Do not allow random extra fields (e.g. spicy="Yes")
        frozen=True,      # Lock the model so it can't be edited later
        strict=False      # Set to True if you want strict type checking without auto-conversion
    )

# Testing Config
strict_item = ConfiguredMenuItem(
    item_id=103,
    name="Cold Coffee",
    price=90.0,
    category="Beverage"
)

try:
    # Attempting to edit a frozen model will throw an error
    strict_item.price = 100.0 
except Exception as e:
    print("Error caught due to frozen=True:", e)

```

---

### 5. Special Data Types

Pydantic has built-in smart data types for common scenarios, ensuring you don't have to write complex Regex patterns to validate things like Emails or URLs. It also integrates seamlessly with Python's `datetime` module.


```python
class RestaurantContactDetails(BaseModel):
    # Built-in Special Types
    contact_email: EmailStr          # Validates standard email formats
    website_link: HttpUrl            # Validates HTTP/HTTPS links
    establishment_date: date         # Validates date strings (YYYY-MM-DD)

# Testing Special Types
contact_info = RestaurantContactDetails(
    contact_email="hello@sheryiansrestaurant.com",
    website_link="https://www.sheryians.com",
    establishment_date="2020-05-15"
)

print("\nValid Restaurant Info:")
print(f"Email: {contact_info.contact_email}")
print(f"URL: {contact_info.website_link}")
print(f"Date: {contact_info.establishment_date}")

```