from aiogram import types
from loader import dp, db
from keyboards.inline.category import Keyboard
from data.config import file_id_1
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(state='products')
async def products_choice(callback: types.CallbackQuery, state: FSMContext):
    product_id = int(callback.data)
    count = 1
    keyboard = await Keyboard.inline_category_product_choose(product_id, count=count)
    products = await db.select_product(id=product_id)
    await callback.message.delete()
    for product in products:
        photo = product[2]
        name = product[1]
        await callback.message.answer_photo(photo=photo, caption=f"<b>{name}</b>, {product[3]} ming so\'m.",
                                            reply_markup=keyboard)
    await state.update_data(
        {'product_id': product_id, 'count': count}
    )
    await state.set_state('add_to_cart')


@dp.callback_query_handler(state='add_to_cart')
async def add_to_cart(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    product_id = int(data.get('product_id'))
    count = data.get('count')
    user_id = callback.from_user.id
    keyboard = None
    if callback.data == '+':
        count += 1
        keyboard = await Keyboard.inline_category_product_choose(product_id=product_id, count=count)
        await state.update_data({'count': count})
    elif callback.data == '-':
        count -= 1
        keyboard = await Keyboard.inline_category_product_choose(product_id=product_id, count=count)
        await state.update_data({'count': count})

    products = await db.select_product(id=product_id)
    for product in products:
        name = product[1]
        price = product[3]
        summa = count * price
        await state.update_data({'summa': summa, 'name': name})
        await callback.message.edit_caption(caption=f'<b>{name}</b>\nJami:<b>{summa}</b> ming so\'m',
                                            reply_markup=keyboard)
    if callback.data == 'add':
        keyboard = await Keyboard.inline_category()
        data = await state.get_data()
        price = data.get('summa')
        name = data.get('name')
        await state.update_data({'user_id': callback.from_user.id})
        try:
            await db.add_order(count=count, product_id=product_id, user_id=user_id, price=price, name=name)
            await callback.answer("The product has been added to the cart!", show_alert=True, cache_time=1)
            await callback.message.answer_photo(photo=file_id_1, caption='All Category', reply_markup=keyboard)
            await state.set_state('category')
        except Exception as e:
            pass

    if callback.data == 'back:product':
        await callback.message.delete()
        data = await state.get_data()
        category_id = data.get('category_id')
        keyboard = await Keyboard.inline_category_product(category_id=category_id)
        await callback.message.answer_photo(photo=file_id_1, caption='This Category,All Products',
                                            reply_markup=keyboard)
        await state.set_state('products')
