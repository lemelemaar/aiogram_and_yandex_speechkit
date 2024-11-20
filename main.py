import asyncio, logging, requests, os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from dotenv import load_dotenv


load_dotenv()


IAM_TOKEN = os.getenv("IAM_TOKEN")
FOLDER_ID = os.getenv("FOLDER_ID")
FILE_PATH = "test.ogg"

url = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize"
headers = {
    "Authorization": f"Bearer {IAM_TOKEN}",
}
params = {
    "lang": "ru-RU",
    "folderId": FOLDER_ID,
}


logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()


@dp.message(lambda message: message.voice is not None)
async def handle_voice_message(message: Message):
    file_id = message.voice.file_id
    file_path = f"{file_id}.ogg"

    await bot.download(file_id, destination=file_path)
    with open(file_path, 'rb') as audio_file:
        data = audio_file.read()
    response = requests.post(url, params=params, headers=headers, data=data)

    if response.status_code == 200:
        if response.json().get("result"):
            await message.answer(text=f'{response.json().get("result")}')
        else:
            await message.answer(text='Ошибка распознавания')
    else:
        await message.answer(text=f'{"Ошибка распознавания:", response.status_code, response.text}')

    os.remove(file_path)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
