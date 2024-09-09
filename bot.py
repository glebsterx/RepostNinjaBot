import os
import sys
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F, exceptions
from aiogram.filters.command import CommandStart, Command

# Получаем токен из переменной окружения или агрументов скрипта
API_TOKEN = os.getenv('API_TOKEN')
if not API_TOKEN:
   raise ValueError("No API_TOKEN provided. Please set the API_TOKEN environment variable.")

# Получаем режим из переменной окружения - тихий режим включен по умолчанию
SILENT_MODE = os.getenv("SILENT_MODE", 'True').lower() in ('true', '1', 't')

# Получаем ответ на репост из переменной окружения
REPOST_ANSWER = os.getenv('REPOST_ANSWER', 'R E P O O O O O O O O O S T ! ! !')

# Переменная для активации и деактивации бота
BOT_ACTIVE = True  

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Инициализация бота и диспетчера
# Объект бота
bot = Bot(token=API_TOKEN)
# Диспетчер
dp = Dispatcher()

# Обработчики сообщений

# Хэндлер на команду /start
@dp.message(CommandStart(), F.chat.type == "private")
async def cmd_start(message: types.Message):
    await message.answer(f"Привет, {message.chat.username}! Я RepostNinja.\nДобавь меня в свой чат, дай права на удаление сообщений и я тихо избавлю пользователей от репостов новостей из каналов.")

# Хэндлер на команду /test
@dp.message(Command("test"))
async def cmd_test(message: types.Message):
    await message.reply("Заняться что ли нечем?")
    
# Хэндлер на команду /test в личке
@dp.message(Command("test"), F.chat.type == "private")
async def cmd_test_private(message: types.Message):
    await message.reply(f"{message}")

# Хэндлер на команду /silent
@dp.message(Command("silent"), F.chat.type == "private")
async def cmd_silent(message: types.Message):
    global SILENT_MODE
    SILENT_MODE = not SILENT_MODE
    await message.reply("Silent mode is " + ("ON" if SILENT_MODE else "OFF"))

# Хэндлер на команду /activate
@dp.message(Command("activate"), F.chat.type == "private")
async def cmd_activate(message: types.Message):
    global BOT_ACTIVE
    BOT_ACTIVE = True
    await message.reply("Bot is now ACTIVATED.")

# Хэндлер на команду /deactivate
@dp.message(Command("deactivate"), F.chat.type == "private")
async def cmd_deactivate(message: types.Message):
    global BOT_ACTIVE
    BOT_ACTIVE = False
    await message.reply("Bot is now DEACTIVATED.")

# Хэндлер на команду /status
@dp.message(Command("status"), F.chat.type == "private")
async def cmd_status(message: types.Message):
    status = "ACTIVE" if BOT_ACTIVE else "DEACTIVATED"
    silent_status = "ON" if SILENT_MODE else "OFF"
    await message.reply(f"Bot Status: {status}\nSilent Mode: {silent_status}")
    
# Хэндлер на пересланные сообщения из каналов
@dp.message(F.forward_from_chat[F.type == "channel"])
async def forwarded_from_channel(message: types.Message):
    if not BOT_ACTIVE:
        return # Если бот не активен, ничего не делаем
    # Проверка на репост # если пересланное # если от канала # если сообщение не от того, кто пересылает
    # if message.forward_origin and \
       # message.forward_origin.type in ['channel']: # and message.forward_origin.chat.id != message.from_user.id
    # отвечаем если не тихий режим, ниндзя же
    if not SILENT_MODE: # тихий режим включен по умолчанию
        bot_reply = await message.reply(f"@{message.from_user.username} {REPOST_ANSWER}")
        asyncio.create_task(delayed_delete(bot_reply, 30)) # удаляем ответ через 30 секунд
    # удаляем репост
    await message.delete()

# Хэндлер ошибки/DDoS
@dp.error()
async def exception_handler():
    wait(5)
    return True

# Удаление ответа по таймеру
async def delayed_delete(message: types.Message, sleep_time: int = 0):
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

