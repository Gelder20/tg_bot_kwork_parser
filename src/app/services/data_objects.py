from dataclasses import dataclass, asdict


@dataclass
class Order:
	id_: int
	name: str
	allow_higher_price: bool
	price_limit: int
	responces_count: int
	desc: str
