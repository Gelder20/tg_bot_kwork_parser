from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot as _Bot
from jinja2 import Environment

from app.services.data_objects import Order, asdict




__env = Environment(enable_async=True)
_template = __env.from_string(
"""{{ name }}{% if allow_higher_price %}
Желаемая цена: до {{ to_int(price_limit) }}
Допустимый бюджет: до {{ to_int(price_limit) * 3 }}{% else %}
Цена: до {{ to_int(price_limit) }}{% endif %}
Откликов на данный момент: {{ kwork_count }}

{{ desc }}
"""
)
_url_template = 'https://kwork.ru/projects/{id}/view'


class Bot(_Bot):
	async def send_order(self, chat_id: int | str, order: Order):
		await self.send_message(
			chat_id,
			await _template.render_async(**asdict(order)),
			reply_markup=InlineKeyboardMarkup(
				inline_keyboard=[[
					InlineKeyboardButton(
						text='Перейти',
						url=_url_template.format(id=order.id_),
					),
				]],
			),
			disable_web_page_preview=True,
		)