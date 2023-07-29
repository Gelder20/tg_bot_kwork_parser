from dataclasses import (
	asdict as _asdict,
	dataclass,
)




asdict = _asdict


@dataclass
class Order:
	id_: int
	name: str
	allow_higher_price: bool
	price_limit: int
	responces_count: int
	desc: str
