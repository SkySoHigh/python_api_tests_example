"""The module contains base random generator for providing live like random data."""
from functools import lru_cache

from mimesis.locales import Locale
from mimesis.providers.address import Address
from mimesis.providers.base import BaseDataProvider
from mimesis.providers.date import Datetime
from mimesis.providers.internet import Internet
from mimesis.providers.numeric import Numeric
from mimesis.providers.person import Person
from mimesis.providers.text import Text


class _RandomGenerators(BaseDataProvider):
    """
    Generates random data with specified locale and seed (for repetitive generation of same data)

    Note: The library has a provider (Generic) that provides access to all basic providers,
    but it is too large and takes up a lot of memory, so we use a custom provider
    """

    def __init__(self, locale=Locale.EN, seed=None):
        super().__init__(locale=locale, seed=seed)
        self.__person = Person(locale=locale, seed=seed)
        self.__text = Text(locale=locale, seed=seed)
        self.__addr = Address(locale=locale, seed=seed)
        self.__dt = Datetime(locale=locale, seed=seed)

        self.__numbers = Numeric(seed=seed)  # Does not support locale
        self.__inter = Internet(seed=seed)  # Does not support locale

    @property
    def person(self) -> Person:
        return self.__person

    @property
    def text(self) -> Text:
        return self.__text

    @property
    def address(self) -> Address:
        return self.__addr

    @property
    def internet(self) -> Internet:
        return self.__inter

    @property
    def datetime(self) -> Datetime:
        return self.__dt

    @property
    def numbers(self) -> Numeric:
        return self.__numbers

    def override_locale(self, *args, **kwargs):
        raise NotImplementedError("Locale overriding does not supported")


@lru_cache()
def get_random_generator(seed=None):
    return _RandomGenerators(seed=seed)
