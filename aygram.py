import logging
import shutil
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import NetworkError

from dotenv import load_dotenv
from putube import upload_video

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('token'))
dp = Dispatcher(bot)

@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.reply("Здравствуйте. Чтобы начать скачивать видео с ютуб достаточно только ссылки")

@dp.message_handler()
async def echo(message: types.Message):
    global path_video
    try:
        if message['text'].split('.')[0] == 'https://youtu' or message['text'].split('.')[0] == 'https://youtube':
            path_video = upload_video(message['text'],
                                      message['from']['first_name'],
                                      message['from']['last_name'],
                                      message['from']['id'],
                                      str(message['date']))
            await message.answer("Идёт загрузка, пожалуйста ожидайте...")
            if path_video == 'Error':
                await message.answer("Что-то пошло не так")
            else:
                await message.reply_video(video=open(path_video, 'rb'), supports_streaming=True)
                await message.answer("Всё готово Хозяин")
                shutil.rmtree('\\'.join(path_video.split("\\")[:-1]), ignore_errors=True)
        else:
            await message.answer("К сожалению не удалось распознать ссылку\nЯ работаю только с ссылками Ютуба")
    except NetworkError:
        await message.answer("Что-то пошло не так (Возможно ваше видео слишком большое)")
        shutil.rmtree('\\'.join(path_video.split("\\")[:-1]), ignore_errors=True)


def main():
    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    main()
