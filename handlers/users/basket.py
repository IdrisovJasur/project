from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp, db, bot
from keyboards.inline.category import Keyboard, Payment
from data.config import file_id_1, ADMINS
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(state='category', text='basket')
async def basket(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    orders = await db.select_order(user_id=user_id)
    if len(orders) == 0:
        await callback.answer('Savatchangiz bo\'sh!', show_alert=True)
    else:
        await callback.message.delete()
        text = ''
        s = 0
        for order in orders:
            count = order[1]
            name = order[5]
            price = order[4]
            s += price
            text += f'{count} ta <b>{name}</b> = {price}\n\n'
        keyboard = await Payment.successfully_order()
        await callback.message.answer(text=f'#{user_id}\n\n{text}Jami:{s}', reply_markup=keyboard)
        await state.set_state('basket')


@dp.callback_query_handler(state='basket', text='buying')
async def buying(call: types.CallbackQuery, state: FSMContext):
    keyboard = await Payment.choose_money()
    await call.message.edit_text(text='Select the payment type', reply_markup=keyboard)


@dp.callback_query_handler(state='basket', text='delete_order')
async def delete_order(call: types.CallbackQuery, state: FSMContext):
    keyboard = await Keyboard.inline_category()
    user_id = call.from_user.id
    await db.delete_order(user_id=user_id)
    await call.message.answer_photo(photo=file_id_1, caption=f"Choose all Category! ", reply_markup=keyboard)
    await state.set_state('category')
    await call.answer(text='Delete your orders!', show_alert=True)


@dp.callback_query_handler(state='basket', text='online')
async def online_payme(call: types.CallbackQuery, state: FSMContext):
    await call.answer(text='Currently, payme and click are not working!', show_alert=True)


@dp.callback_query_handler(state='basket', text='offline')
async def offline_payme(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    keyboard = await Payment.location()
    await call.message.answer(text='Turar joyingizni yuboring !', reply_markup=keyboard)


@dp.message_handler(state='basket', content_types=types.ContentType.LOCATION)
async def location_phone(message: types.Message, state: FSMContext):
    lat = message.location.latitude
    long = message.location.longitude
    keyboard = await Payment.phone_number()
    await state.update_data({'long': long, 'lat': lat})
    await message.answer('Telefon raqamingizni yuboring!', reply_markup=keyboard)


@dp.message_handler(state='basket', content_types=types.ContentType.CONTACT)
async def phone_numbers(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number
    await state.update_data({'phone': phone})
    data = await state.get_data()
    lat = data.get('lat')
    long = data.get('long')
    user_id = data.get('user_id')
    keyboard = await Keyboard.inline_category()
    text = ''
    s = 0
    orders = await db.select_order(user_id=user_id)
    for order in orders:
        count = order[1]
        name = order[5]
        price = order[4]
        s += price
        text += f'{count} ta <b>{name}</b> = {price}\nJami:{s}\n\n'

    await bot.send_location(chat_id=ADMINS[0], latitude=lat, longitude=long)
    await bot.send_message(chat_id=ADMINS[0], text=text + phone, reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Buyurtma qabul qilindi,Tez orada bog\'lanamiz!', reply_markup=types.ReplyKeyboardRemove())
    await message.answer_photo(photo=file_id_1, caption=f"Choose all Category! ", reply_markup=keyboard)
    await state.set_state('category')
    try:
        await db.add_history(user_id=user_id, price=str(s))
        await db.delete_order(user_id=user_id)
    except Exception as e:
        print(e)


@dp.callback_query_handler(state='category', text='history')
async def history_def(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = call.from_user.id
    history = await db.select_history(user_id=user_id)
    keyboard = await Payment.history_back()
    print(history)


