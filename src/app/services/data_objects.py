from dataclasses import dataclass


@dataclass
class Order:
    name: str
    allow_higher_price: bool
    price_limit: int
    number_of_responces: int
    description: str
