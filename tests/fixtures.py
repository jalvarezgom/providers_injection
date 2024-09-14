import pytest

from src.providers_injection import providers
from src.providers_injection.containers import ProviderContainer
from src.providers_injection.providers import Callable


class FactoryTest:
    test_data = "class attribute"

    def __init__(self, test_data):
        self.test_data = test_data


class SingletonTest:
    test_data = "class attribute"

    def __init__(self, test_data):
        self.test_data = test_data


class FixtureContainer(ProviderContainer):
    factory_test: FactoryTest = providers.Factory(FactoryTest, test_data="fixture attribute")
    singleton_test: SingletonTest = providers.Singleton(SingletonTest, test_data="fixture attribute")
    callable_test = Callable(
        lambda arg1, arg2: f"{arg1}-{arg2}",
        arg1="df_arg1",
        arg2="df_arg2",
    )


@pytest.fixture()
def fixture_container():
    return FixtureContainer
