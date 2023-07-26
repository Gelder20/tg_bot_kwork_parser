from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot as _Bot

from services.kwork_parser_service import OrderView




class Bot(_Bot):
	async def send_order(self, chat_id: int | str, order_view: OrderView):
		await self.send_message(
			chat_id,
			order_view.message,
			reply_markup=InlineKeyboardMarkup(
				inline_keyboard=[[
					InlineKeyboardButton(
						text='Перейти',
						url=order_view.url,
					),
				]],
			),
			disable_web_page_preview=True,
		)