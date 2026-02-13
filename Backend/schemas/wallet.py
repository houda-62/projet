from pydantic import BaseModel
from decimal import Decimal

class WalletResponse(BaseModel):
    balance: Decimal

    # Pydantic v2: enable reading attributes from ORM objects
    model_config = {"from_attributes": True}

class WalletUpdate(BaseModel):
    amount: Decimal  # positif pour ajouter, négatif pour dépenser
