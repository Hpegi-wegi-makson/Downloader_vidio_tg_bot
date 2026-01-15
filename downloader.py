import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import yt_dlp

TOKEN = "8245034590:AAE_mjmlPYN--Qdtnr-UBfXlNt2aTT4X0RU"

bot = Bot(token=TOKEN)
dp = Dispatcher()

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_video(url: str) -> str:
    ydl_opts = {
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "format": "best",
        "merge_output_format": "mp4",
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        if not filename.endswith(".mp4"):
            filename = filename.rsplit(".", 1)[0] + ".mp4"
        return filename


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Отправь ссылку на видео (YouTube / TikTok / VK и др.) — я скачаю его 📥"
    )


@dp.message()
async def handle_link(message: types.Message):
    url = message.text.strip()

    await message.answer("⏳ Скачиваю видео, подожди...")

    try:
        video_path = await asyncio.to_thread(download_video, url)

        await message.answer_video(
            video=types.FSInputFile(video_path),
            caption="✅ Готово"
        )

        os.remove(video_path)

    except Exception as e:
        await message.answer(f"❌ Ошибка:\n{e}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
