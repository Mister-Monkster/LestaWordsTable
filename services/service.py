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
        return word_dict


    async def download(self, file: UploadFile):
        """Проверяем тип файла и возвращаем первые 50 слов"""
        if file.headers['content-type'] != 'text/plain':
            return False
        content = await file.read()
        text = content.decode("utf-8")
        if text == '':
            return False
        res = await self.content_analysis(text)
        result = []
        for key, value in res.items():
            result.append([key, *value])
        result.sort(key=lambda x: x[-1], reverse=True)
        return result[0: 50]
