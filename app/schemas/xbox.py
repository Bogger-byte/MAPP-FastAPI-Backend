__all__ = ["XboxDatabase", "Xbox"]

from tortoise.contrib.pydantic import pydantic_model_creator

from app.models import Xbox

XboxDatabase = pydantic_model_creator(
    Xbox, name="MCAccountDB"
)


Xbox = pydantic_model_creator(
    Xbox, name="MCAccount", exclude=("created_at", "modified_at")
)
