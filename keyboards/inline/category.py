from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from loader import db, dp


class Keyboard:
    def __init__(self):
        pass

    @classmethod
    async def inline_category(cls):
        categories = await db.select_all_categories()
        markup = InlineKeyboardMarkup(row_width=2)
        count = 1
        for i in categories:
            text = f"{count} - {i[1]}"
            keyboard = markup.insert(InlineKeyboardButton(text=text, callback_data=i[1]))
            count += 1
        markup.add(InlineKeyboardButton(text='📦 Savatcha', callback_data='basket'))
        # markup.add(InlineKeyboardButton(text='Xaridlar tarixi', callback_data='history'))
        return markup

    @classmethod
    async def inline_category_product(cls, category_id):
        products = await db.select_product(category_id=category_id)
        markup = InlineKeyboardMarkup(row_width=2)
        count = 1
        if len(products) != 0:
            for i in products:
                text = f"{count} - {i[1]}"
                keyboard = markup.insert(InlineKeyboardButton(text=text, callback_data=i[0]))
                count += 1
            markup.add(InlineKeyboardButton(text='Back', callback_data='back:category'))
            return markup
        else:
            return 0

    @classmethod
    async def inline_category_product_choose(cls, product_id, count):

        inline_keys = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='Add to Cart', callback_data='add')
                ],
                [
                    InlineKeyboardButton(text='-', callback_data='-'),
                    InlineKeyboardButton(text=f"{count}", callback_data='0'),
                    InlineKeyboardButton(text='+', callback_data='+'),
                ],
                [
                    InlineKeyboardButton(text='Back', callback_data='back:product'),
                ]
            ]
        )
        return inline_keys


class Payment:
    def __init__(self):
        pass

    @classmethod
    async def choose_money(cls):
        markup = InlineKeyboardMarkup(row_width=2)
        markup.insert(InlineKeyboardButton(text='Online(click,payme)', callback_data='online'))
        markup.insert(InlineKeyboardButton(text='Offline(So\'m)', callback_data='offline'))
        return markup

    @classmethod
    async def successfully_order(cls):
        markup = InlineKeyboardMarkup(row_width=2)
        markup.insert(InlineKeyboardButton(text='Buyurtmani rasmiylashtirish', callback_data='buying'))
        markup.insert(InlineKeyboardButton(text='Savatni tozalash', callback_data='delete_order'))
        markup.add(InlineKeyboardButton(text='Back', callback_data='back:basket'))
        return markup

    @classmethod
    async def location(cls):
        button = ReplyKeyboardMarkup([
            [
                KeyboardButton(text='Send Location', request_location=True)
            ],

        ], resize_keyboard=True

        )
        return button

    @classmethod
    async def phone_number(cls):
        button = ReplyKeyboardMarkup([
            [
                KeyboardButton(text='Send Phone Number', request_contact=True)
            ],

        ], resize_keyboard=True

        )
        return button

    @classmethod
    async def history_back(cls):
        back_history = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='back', callback_data='back:history')
                ],
            ]
        )
        return back_history
