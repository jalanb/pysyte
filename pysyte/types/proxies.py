"""Classes to proxy other objects"""

from typing import Any


class Proxy(object):
    """Offers attributes from self, or another object"""

    def __init__(self, value: Any, name: str = "", **kwargs: dict) -> None:
        super().__init__()
        self.__dict__["_proxy"] = value
        if name:
            self.__dict__[name] = value

    def __getattr__(self, name: str) -> Any:
        try:
            return getattr(self._proxy, name)
        except AttributeError:
            raise AttributeError(
                f"'{self.__class__.__name__}' has no attribute '{name}'"
            )

    def __setattr__(self, name: str, value: Any) -> None:
        proxy = self.__dict__["_proxy"]
        try:
            getattr(proxy, name)
            setattr(proxy, name, value)
        except AttributeError:
            self.__dict__[name] = value

