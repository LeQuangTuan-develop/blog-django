from django.http import JsonResponse
from pydantic import BaseModel
import json
import os
from pathlib import Path
import random


class QuoteData(BaseModel):
    text: str
    author: str


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Quote(metaclass=SingletonMeta):
    """this class is a SINGLETON class (no duplication)
    the senior worker generate: file path info, date time info, get target spreadsheet
    """
    BASE_DIR = Path(__file__).resolve().parent
    TARGET_FILE = os.path.join(BASE_DIR, 'quotes.json')

    def __init__(self):
        f = open(self.TARGET_FILE)
        self._data: list[QuoteData] = json.load(f)
        self._max: int = len(self._data)
        f.close()

    def get_random_quote(self) -> QuoteData:
        return self._data[random.randint(0, self._max-1)]


def get_quote(request):
    """get quote from json file"""
    quote: Quote = Quote()
    data = quote.get_random_quote()
    return JsonResponse(data, content_type="application/json")


if __name__ == '__main__':
    print(get_quote(None))
