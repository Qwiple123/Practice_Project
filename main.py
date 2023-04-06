import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import Bot, Dispatcher, types, executor
import keyboards
from config import TOKEN


storage = MemoryStorage()
bot = Bot(token = TOKEN)
dp = Dispatcher(bot=bot, storage=storage)

class Quest(StatesGroup):
    first = State()
    second = State()
    third = State()
    fourth = State()


@dp.message_handler(commands='start')
async def start(msg: types.Message):
    print(f'{msg.from_user.full_name} : start')
    await msg.answer('''Здравствуйте\nЭто бот посвященный книге "Хроники разбитого мира"\nПройдите небольшой квест и получите подарок ''', reply_markup=keyboards.main_keyboard()) 


@dp.callback_query_handler(text="start")
async def first_ask(query: types.CallbackQuery):
    print(f'{query.from_user.full_name} : gallery')
    user_id = query.message.chat.id
    await query.message.delete()
    media = types.MediaGroup()
    media.attach_photo(types.InputFile('gallery/1.JPG'))
    await bot.send_media_group(user_id, media=media)
    await bot.send_message(user_id, '''Фриджиты это маленькие существа которые привязанны к человеку и олицетворяют его внутренний талант\nВопрос сколько фриджитов находится на этой картинке''')
    await Quest.first.set()

@dp.message_handler(state=Quest.first)
async def first_answer(msg: types.Message, state: FSMContext):
    answer = msg.text
    print(answer)
    
    if answer != '3':
        await state.finish()
        await msg.answer('Неверно, попробуй еще раз')
        await Quest.first.set()

    elif answer == '3':
        await state.finish()
        await msg.answer('Верно, следующее задание')
        user_id = msg.from_user.id
        media = types.MediaGroup()
        media.attach_photo(types.InputFile('gallery/2.PNG'))
        await bot.send_media_group(user_id, media=media)
        await bot.send_message(user_id, '''Сейчас вы видите статую человеку с фриджитом\nНапишите сколько отличий вы нашли на этих картинках''')
        await Quest.second.set()


@dp.message_handler(state=Quest.second)
async def second_answer(msg: types.Message, state: FSMContext):
    answer = msg.text
    print(answer)
    
    if answer != '5':
        await state.finish()
        await msg.answer('Неверно, попробуй еще раз')
        await Quest.second.set()

    elif answer == '5':
        await state.finish()
        await msg.answer('Верно, следующее задание')
        user_id = msg.from_user.id
        media = types.MediaGroup()
        media.attach_photo(types.InputFile('gallery/3.PNG'))
        await bot.send_media_group(user_id, media=media)
        await bot.send_message(user_id, '''На картинке изображен главный герой который держит в руках шкатулку с фриджитами\nНапишите сколько отличий вы нашли на картинках''')
        await Quest.third.set()

@dp.message_handler(state=Quest.third)
async def third_answer(msg: types.Message, state: FSMContext):
    answer = msg.text
    print(answer)
    
    if answer != '4':
        await state.finish()
        await msg.answer('Неверно, попробуй еще раз')
        await Quest.third.set()

    elif answer == '4':
        await state.finish()
        await msg.answer('Верно, следующее задание')
        user_id = msg.from_user.id
        media = types.MediaGroup()
        media.attach_photo(types.InputFile('gallery/4.JPG'))
        await bot.send_media_group(user_id, media=media)
        await bot.send_message(user_id, '''На картинке изображен парк фриджитов\nНапишите сколько аттракционов вы нашли''')
        await Quest.fourth.set()

@dp.message_handler(state=Quest.fourth)
async def fourth_answer(msg: types.Message, state: FSMContext):
    answer = msg.text
    print(answer)
    
    if answer != '8':
        await state.finish()
        await msg.answer('Неверно, попробуй еще раз')
        await Quest.fourth.set()

    elif answer == '8':
        await state.finish()
        await msg.answer('Отлично! вы справились со всеми заданиями и получаете в награду 3 главы многоголосой озвучки \n')
        



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)