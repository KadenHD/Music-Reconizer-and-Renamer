import asyncio
import os
import re
from shutil import copyfile
from shazamio import Shazam
from tqdm import tqdm

class ShazamRecognizer:
    def __init__(self):
        self.shazam = Shazam()

    async def _recognize_song(self, file_path, index):
        try:
            result = await self.shazam.recognize(file_path)
            subtitle = self._sanitize_filename(result['track']['subtitle'])
            title = self._sanitize_filename(result['track']['title'])
            new_file_name = f"{index} - {subtitle} - {title}.mp3"
            new_file_path = os.path.join("convert", new_file_name)
            self._copy_and_rename(file_path, new_file_path)
            return subtitle, title
        except Exception as e:
            print(f"An error occurred: {e}")
            return None, None

    def _sanitize_filename(self, filename):
        sanitized_filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        sanitized_filename = sanitized_filename.replace(' ', '_')
        return sanitized_filename

    def _copy_and_rename(self, source_file, destination_file):
        try:
            os.makedirs("convert", exist_ok=True)
            copyfile(source_file, destination_file)
            print(f"File copied and renamed to: {destination_file}")
        except Exception as e:
            print(f"An error occurred during file copying: {e}")

    async def recognize_songs_in_directory(self, directory_path):
        try:
            files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
            for index, file in enumerate(tqdm(files, desc="Processing songs"), start=1):
                file_path = os.path.join(directory_path, file)
                await self._recognize_song(file_path, index)
        except Exception as e:
            print(f"An error occurred while processing directory: {e}")

async def main():
    recognizer = ShazamRecognizer()
    await recognizer.recognize_songs_in_directory('assets')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
