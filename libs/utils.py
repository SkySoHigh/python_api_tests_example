from typing import Callable, Any


class classproperty(object):
    """
    @property for @classmethod
    References http://stackoverflow.com/a/13624858
    """

    def __init__(self, fget: Callable) -> None:
        self.fget = fget

    def __get__(self, owner_self: Any, owner_cls: Any) -> Any:
        return self.fget(owner_cls)
