import os
import string
import uuid
from math import log

import aiofiles
from fastapi import UploadFile


class FileService:


    @staticmethod
    async def content_analysis(content: str):
        """Преобразуем текст в словарь с данными"""
        text = (content
                .replace('\r','')
                .replace('\n', ' '))
        translator = str.maketrans("", "", string.punctuation + '–')
        clean_text = text.translate(translator)
        content_list = clean_text.split(" ")
        lower_list = [x.lower() for x in content_list if x != '']
        words_counter = len(lower_list)
        keys = set(lower_list)
        word_dict = {key: [0, 0.0] for key in keys}
        for word in lower_list:
            word_dict[word][0] += 1
        for key in word_dict.keys():
            word_dict[key][1] = round(log(words_counter / word_dict[key][0]), 3)
        result = []
        for key, value in word_dict.items():
            result.append([key, *value])
        result.sort(key=lambda x: x[-1], reverse=True)
        return result

    @staticmethod
    async def save_file(file: UploadFile, filename: str):
        dir = f'../files/{filename}.txt'
        dir_name = os.path.dirname(dir)
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        async with aiofiles.open(dir, "wb") as f:
            text = await file.read()
            await f.write(text)
            return text.decode('utf-8')


    async def download(self, file: UploadFile, filename: str):
        """Проверяем тип файла и возвращаем первые 50 слов"""
        if file.headers['content-type'] != 'text/plain':
            return False
        text = await self.save_file(file, filename)
        res = await self.content_analysis(text)
        return res


    async def read_file(self, filename: str, page_num: int):
        dir = f'../files/{filename}.txt'
        if os.path.exists(dir):
            async with aiofiles.open(dir, "rb") as f:
                text = await f.read()
                text = text.decode('utf-8')
                content = await self.content_analysis(text)
                total_pages = (len(content) + 49) // 50
                if total_pages == 1:
                    return content
                start = (page_num - 1) * 50
                end = start + 50
                content = content[start:end]
                return {'content': content,'total_pages': total_pages}

        else:
            raise FileNotFoundError('File not found')
