from contextlib import contextmanager
from typing import (
    TypeVar,
    Generic,
    Callable as _Callable,
    Any,
    Tuple,
    Dict as _Dict,
    Union,
)

from src.providers_injection.exceptions import ProviderException

Injection = Any
ProviderParent = Union["Provider", Any]
T = TypeVar("T")
P = TypeVar("P", bound="Provider")


class Attributes:
    _attributes: _Dict[str, Any] = {}

    def __call__(self, obj: Injection, attributes: _Dict[str, Injection] = {}, **kwargs: _Dict[str, Injection]):
        for key, value in {**attributes, **kwargs}.items():
            setattr(obj, key, value)
        return obj

    @property
    def attributes(self) -> _Dict[str, Any]:
        return self._attributes

    def add_attribute(self, key: str, value: Any):
        self._attributes[key] = value

    def set_attribute(self, **kwargs: _Dict[str, Injection]):
        self._attributes = kwargs

    def clean_attributes(self):
        self._attributes.clear()


class Provider(Generic[T]):
    _args: Tuple[Injection] = []
    _kwargs: _Dict[str, Injection] = {}
    _provides: Injection = None
    _override = None

    def __init__(self, provides: _Callable[..., T], *args: Tuple[Injection], **kwargs: _Dict[str, Injection]):
        self._provides = provides
        self._args = args
        self._kwargs = kwargs
        print("init")

    def __call__(self, *args: Injection, **kwargs: Injection) -> T:
        raise NotImplementedError()

    @property
    def args(self) -> Tuple[Injection]:
        if self._override:
            return self._override[1]
        return self._args

    def add_args(self, *args: Tuple[Injection]):
        self.args.extend(args)

    def set_args(self, *args: Tuple[Injection]):
        if self._override:
            self._override[1] = args
        else:
            self._args = args

    def clean_args(self):
        self.args.clear()

    @property
    def kwargs(self) -> _Dict[str, Injection]:
        if self._override:
            return self._override[2]
        return self._kwargs

    def add_kwargs(self, **kwargs: _Dict[str, Injection]):
        self.kwargs.update(kwargs)

    def set_kwargs(self, **kwargs: _Dict[str, Injection]):
        if self._override:
            self._override[2] = kwargs
        else:
            self._kwargs = kwargs

    def clean_kwargs(self):
        self.kwargs.clear()

    @property
    def provides(self) -> Injection:
        if self._override:
            return self._override[0]
        return self._provides

    @contextmanager
    def override_context(self, provides, *args, **kwargs):
        try:
            self.override(provides, *args, **kwargs)
            yield self
        finally:
            self._override = None

    def override(self, provides, *args, **kwargs):
        self._override = [provides, args, kwargs]

    def reset_override(self):
        self._override = None

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.provides})>"

    def __str__(self):
        return f"<{self.__class__.__name__}({self.provides})>"


class Factory(Provider[T], Attributes):
    def __call__(self, *args: Injection, **kwargs: Injection) -> T:
        obj = self.provides(*self.args, *args, **{**self.kwargs, **kwargs})
        for key, value in self.attributes.items():
            setattr(obj, key, value)
        return obj


class Singleton(Provider[T], Attributes):
    _instance = None

    def __call__(self, *args: Injection, **kwargs: Injection) -> T:
        if self._instance is None:
            self._instance = self.provides(*self.args, *args, **{**self.kwargs, **kwargs})
            for key, value in self.attributes.items():
                setattr(self, key, value)
        return self._instance

    def override(self, provides, *args, **kwargs):
        if self._instance is not None:
            raise ProviderException("Singleton instance already created")
        super().override(provides, *args, **kwargs)


class Callable(Provider[T]):
    def __call__(self, *args: Injection, **kwargs: Injection) -> T:
        return self.provides(*self.args, *args, **{**self.kwargs, **kwargs})


class Coroutine(Callable[T]):
    async def __call__(self, *args: Injection, **kwargs: Injection) -> T:
        return await self.provides(*self.args, *args, **{**self.kwargs, **kwargs})
