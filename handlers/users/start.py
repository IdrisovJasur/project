from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp, db, bot
from keyboards.inline.category import Keyboard
from data.config import file_id_1
from aiogram.dispatcher import FSMContext


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    try:
        await db.add_user(
            name=message.from_user.full_name,
            username=message.from_user.username,
            telegram_id=message.from_user.id
        )
    except Exception as e:
        pass
    keyboard = await Keyboard.inline_category()
    await message.answer_photo(photo=file_id_1, caption=f"{message.from_user.full_name},Choose all product! ",
                               reply_markup=keyboard)
    await state.set_state('category')


@dp.callback_query_handler(state='category')
async def choose_category(callback: types.CallbackQuery, state: FSMContext):
    category_name = callback.data
    db_category = await db.select_category(name=category_name)
    category_id = 0
    for i in db_category:
        category_id += i[0]
    keyboard = await Keyboard.inline_category_product(category_id=category_id)
    if keyboard == 0:
        await callback.answer('This Category empty!', show_alert=True, cache_time=1)
    else:
        await state.update_data({'category_id': category_id})
        await callback.message.edit_caption(caption='This Category,All Products', reply_markup=keyboard)
        await state.set_state('products')


@dp.callback_query_handler(state='products', text='back:category')
async def category_back(callback: types.CallbackQuery, state: FSMContext):
    keyboard = await Keyboard.inline_category()
    await callback.message.edit_caption(caption=f"Choose all Category! ", reply_markup=keyboard)
    await state.set_state('category')


@dp.callback_query_handler(state='products', text='back:product')
async def category_back(callback: types.CallbackQuery, state: FSMContext):
    keyboard = await Keyboard.inline_category()
    await callback.message.delete()
    await callback.message.answer_photo(photo=file_id_1, caption=f"Choose all Category! ", reply_markup=keyboard)
    await state.set_state('category')


@dp.callback_query_handler(state='basket', text='back:basket')
async def category_back(callback: types.CallbackQuery, state: FSMContext):
    keyboard = await Keyboard.inline_category()
    await callback.message.delete()
    await callback.message.answer_photo(photo=file_id_1, caption=f"Choose all Category! ", reply_markup=keyboard)
    await state.set_state('category')


@dp.callback_query_handler(state='category', text='back:history')
async def category_back(callback: types.CallbackQuery, state: FSMContext):
    keyboard = await Keyboard.inline_category()
    await callback.message.edit_caption(caption=f"Choose all Category! ", reply_markup=keyboard)
    await state.set_state('category')
