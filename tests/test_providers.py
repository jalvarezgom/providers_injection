from tests.fixtures import fixture_container
from src.providers_injection.containers import ProviderContainer
from tests.fixtures import FactoryTest, SingletonTest


def test_provider_factory(fixture_container):
    factory_test = fixture_container.factory_test()
    assert isinstance(factory_test, FactoryTest)
    assert factory_test.test_data == "fixture attribute"


def test_provider_singleton(fixture_container):
    singleton_test: SingletonTest = fixture_container.singleton_test(test_data="fixture attribute modified")
    assert isinstance(singleton_test, SingletonTest)
    assert singleton_test.test_data == "fixture attribute modified"
    singleton_test = fixture_container.singleton_test()
    assert isinstance(singleton_test, SingletonTest)
    assert singleton_test.test_data == "fixture attribute modified"


def test_provider_callable(fixture_container):
    callable_test: str = fixture_container.callable_test()
    assert callable_test == "df_arg1-df_arg2"
    callable_test: str = fixture_container.callable_test(arg1="arg1", arg2="arg2")
    assert callable_test == "arg1-arg2"


def test_create_container(fixture_container):
    container = fixture_container()
    assert isinstance(container, ProviderContainer)


fixture_container
