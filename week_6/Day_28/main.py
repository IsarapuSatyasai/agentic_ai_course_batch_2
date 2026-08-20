from pydantic import BaseModel, Field, field_validator, model_validator, computed_field, ConfigDict
from typing import Literal, Optional

class BasicMenuItem(BaseModel):
    item_id: int = Field(...)
    name: str = Field(...,min_length=3, max_length=50, description="Name of the dish.")
    price: float = Field(..., gt=0, description="Price must be greater than zero.")
    category: Literal["Starter", "Main Course", "Desserts", "Beverages"]
    is_available: bool = True
    description: Optional[str] = None

# item = BasicMenuItem(
#     item_id=101,
#     name="Garlic Bread",
#     price=150.0,
#     category="Starter",
#     spicy='So hot!'
# )
# print("Basic Item Created: ", item)

class ValidateMenuItem(BasicMenuItem):
    
    @field_validator("name")
    @classmethod
    def clean_name_format(cls, value: str):
        # Converts "pAnEeR tIkKa" -> "Paneer Tikka"
        return value.title()

    @model_validator(mode="after")
    def check_logical_pricing(self):
        # Business Rule: If an item is available, it must cost money.
        if self.is_available and self.price <= 0:
            raise ValueError("An available menu item must have a price > 0")
        return self
    @computed_field
    @property
    def price_with_tax(self) -> float:
        # Adds 5% tax and rounds to 2 decimal places
        return round(self.price * 1.05, 2)

# Testing
# messy_data = {
#     "item_id": 102,
#     "name": "mAsaLa dOSA",
#     "price": 120.0,
#     "category": "Main Course"
# }
# validated_item = ValidateMenuItem(**messy_data)
# print(f"Cleaned Name: ", {validated_item.name})
# print(f"Computed Tax Price: {validated_item.price_with_tax}")

# Model configuration
class ConfiguredMenuItem(ValidateMenuItem):
    
    #Apply model configuration
    model_config = ConfigDict(
        extra = "forbid", # Do not allow random extra fields.
        frozen=True,      # Lock the model so it can't be edited later
        strict=True      # Set to True if you want strict type checking without auto-conversion
    )
    
# # Testing config
# strict_item = ConfiguredMenuItem(
#     item_id='103',
#     name="Cold Coffee",
#     price=90.0,
#     category="Beverages",
# )

# try:
#     # Attempting to edit a frozen model will throw an error
#     strict_item.price = 100.0
# except Exception as e:
#     print("Error caught due to frozen=True: ", e)