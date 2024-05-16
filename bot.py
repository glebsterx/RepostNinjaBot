import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, exceptions
from aiogram.filters.command import Command

# Получаем токен из переменной окружения
API_TOKEN = os.getenv('API_TOKEN')
if not API_TOKEN:
   raise ValueError("No API_TOKEN provided. Please set the API_TOKEN environment variable.")

# Получаем режим из переменной окружения
# тихий режим включен по умолчанию
SILENT_MODE = os.getenv("SILENT_MODE", 'True').lower() in ('true', '1', 't')

# Получаем ответ на репост из переменной окружения
REPOST_ANSWER = os.getenv('REPOST_ANSWER', 'R E P O O O O O O O O O S T ! ! !')

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Инициализация бота и диспетчера
# Объект бота
bot = Bot(token=API_TOKEN)
# Диспетчер
dp = Dispatcher()

# Обработчики сообщений

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я Репост Низдзя.\nДобавь меня в свой чат, дай права на удаление сообщений и я тихо избавлю пользователей от репостов новостей из каналов.")

# Хэндлер на команду /test
# @dp.message(Command("test"))
# async def cmd_test(message: types.Message):
    # await message.reply("Заняться что ли нечем?")

@dp.message()
async def repostcleaner(message: types.Message):
    # Проверка на репост # если пересланное # если от канала # если сообщение не от того, кто пересылает
    if message.forward_origin and \
       message.forward_origin.type in ['channel']: # and message.forward_origin.chat.id != message.from_user.id
        # отвечаем если не тихий режим, ниндзя же
        if not SILENT_MODE: # тихий режим включен по умолчанию
            bot_reply = await message.reply(f"@{message.from_user.username} {REPOST_ANSWER}")
            asyncio.create_task(delete_msg(bot_reply, 30)) # удаляем ответ через 30 секунд
        # удаляем репост
        await message.delete()

@dp.error()
async def exception_handler():
    wait(5)
    return True

# удаление ответа по таймеру
async def delete_msg(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    await message.delete()
    
# Запуск процесса поллинга новых апдейтов
async def main():
    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())
