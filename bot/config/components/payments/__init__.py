from pydantic import Field, BaseModel


class PaymentsConfig(BaseModel):
    test: bool = Field(default=False)
    live_token: str = Field(default='<TOKEN>')
    test_token: str = Field(default='<TOKEN>')
    currency: str = Field(default='UZS')
    min_amount: int = Field(default=1298089)
    max_amount: int = Field(default=12980894361)

__all__ = ['PaymentsConfig']