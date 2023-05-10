from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from utils.db_api.db_postgres import Database

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database()

# from aiogram.types import ContentType
#
#
# @dp.message_handler(content_types=ContentType.PHOTO)
# async def get_photo(message:types.Message):
#     ph_id = message.photo[-1].file_id
#     await message.answer(ph_id)
