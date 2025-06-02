from pydantic import BaseModel


class SubscriptionPlanCreate(BaseModel):
    title: str
    description: str
    price: int
    total_classes_monthly: int