"""Wire and storage models. All money is integer paise."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class OrderItem(BaseModel):
    sku: str
    name: str
    unit_price_paise: int = Field(ge=0)
    quantity: int = Field(ge=1)


class AppliedDiscount(BaseModel):
    code: str
    percent_off_bps: int
    cap_paise: int
    amount_paise: int
    partner_share_bps: int
    rayy_share_bps: int
    partner_amount_paise: int
    rayy_amount_paise: int


class Payment(BaseModel):
    payment_id: str
    amount_paise: int = Field(ge=0)


class Order(BaseModel):
    order_id: str
    partner_id: str
    items: list[OrderItem]
    subtotal_paise: int = Field(ge=0)
    total_paise: int = Field(ge=0)
    currency: str = "INR"
    status: str
    created_at: datetime
    discount: AppliedDiscount | None = None
    payment: Payment | None = None


class ApplyDiscountRequest(BaseModel):
    code: str


class PaymentWebhook(BaseModel):
    event: Literal["payment.succeeded"]
    payment_id: str = Field(min_length=1)
    order_id: str = Field(min_length=1)
    amount_paise: int = Field(ge=0, strict=True)


class DiscountCode(BaseModel):
    """A partner discount code.

    ``percent_off_bps`` is the percentage in basis points (1500 = 15%).
    ``cap_paise`` is the most the code can take off one order.
    ``partner_share_bps`` + ``rayy_share_bps`` = 10000 and describe who funds
    the discount (7000 / 3000 is a 70/30 split).
    """

    code: str
    percent_off_bps: int = Field(gt=0, le=10000)
    cap_paise: int = Field(gt=0)
    expires_at: datetime
    partner_share_bps: int = Field(ge=0, le=10000)
    rayy_share_bps: int = Field(ge=0, le=10000)
