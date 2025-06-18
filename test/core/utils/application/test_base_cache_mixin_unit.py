import pytest
from unittest.mock import create_autospec
from typing import Any
from pydantic import BaseModel

from core.utils.application.base_cache_mixin import BaseCachingMixin
from core.utils.exceptions import InvalidDependencyException
from core.utils.infrastructure.adapters.redis import RedisSessionAdapter
from core.utils.domain.interfaces.hosts.redis import RedisSessionHost
from config import SESSIONS_EXPIRY

class DummyDTO(BaseModel):
    field_1: int = 0
    field_2: str = 'string'

class DummyService(BaseCachingMixin):
    @BaseCachingMixin.cache_result(key_template='some_arg', dtos=[DummyDTO])
    def service_method(self, some_args: dict) -> DummyDTO:
        return DummyDTO(**some_args)

class DummyAdapter(RedisSessionHost):
    def __init__(self, session_key: str | None = None): ...
    @property
    def session_key(self) -> str: ...
    def hand_over_session_key(self, session_key: str) -> None: ...
    def get(self, key: str, default: Any = None, deserialize: bool = True, *args, **kwargs) -> Any: ...
    def set(self, key: str, data: Any, expire: int = SESSIONS_EXPIRY, serialize: bool = True): ...
    def delete(self, key): ...
    def pop(self, key: str, default: Any = None, deserialize: bool = True, *args, **kwargs) -> Any: ...
    def _get_session_key(self) -> str: ...
    def cache_key(self, key: str, prefix: str = "cache") -> str: ...

def test_cache_result_calls_func_and_sets_cache():
    dto = DummyDTO(**{"field_1": 4, "field_2": "paramX"})
    mock_adapter = create_autospec(RedisSessionAdapter)
    mock_adapter.cache_key.return_value = "prefix:DummyService.compute.paramX"
    mock_adapter.get.return_value = None

    DummyService.set_session_adapter(mock_adapter)
    service = DummyService(mock_adapter)

    result = service.service_method(dto.model_dump(mode="python"))

    assert result == dto
    mock_adapter.get.assert_called_once_with("prefix:DummyService.compute.paramX", dtos=[DummyDTO])
    mock_adapter.set.assert_called_once_with("prefix:DummyService.compute.paramX", dto)

def test_cache_result_returns_cached_value():
    dto = DummyDTO(**{"field_1": 4, "field_2": "paramX"})
    mock_adapter = create_autospec(RedisSessionAdapter)
    mock_adapter.cache_key.return_value = "prefix:DummyService.compute.paramY"
    mock_adapter.get.return_value = dto

    DummyService.set_session_adapter(mock_adapter)
    service = DummyService(mock_adapter)

    result = service.service_method(dto.model_dump(mode="python"))

    assert result == dto
    mock_adapter.set.assert_not_called()

def test_session_adapter_injection_class():
    mixin = BaseCachingMixin(DummyAdapter)
    assert isinstance(mixin.session_adapter, DummyAdapter)

def test_session_adapter_injection_instance():
    mixin = BaseCachingMixin(DummyAdapter())
    assert isinstance(mixin.session_adapter, DummyAdapter)

def test_session_adapter_injection_non_adapter():
    with pytest.raises(InvalidDependencyException):
        BaseCachingMixin(session_adapter=type) #some other class

def test_basic_key_generation():
    mock_adapter = create_autospec(RedisSessionAdapter)
    
    class TestService(BaseCachingMixin):
        @BaseCachingMixin.cache_result(key_template='static_key')
        def simple_method(self):
            ...

    service = TestService(mock_adapter)
    service.simple_method()
    
    mock_adapter.cache_key.assert_called_once_with(
        "TestService.simple_method.static_key",
        "TestService.simple_method"           
    )

def test_dynamic_key_from_args():
    mock_adapter = create_autospec(RedisSessionAdapter)
    
    class TestService(BaseCachingMixin):
        @BaseCachingMixin.cache_result(key_template='{arg1}_{arg2}')
        def method_with_args(self, arg1, arg2):
            ...

    service = TestService(mock_adapter)
    service.method_with_args("foo", "bar")
    
    mock_adapter.cache_key.assert_called_once_with(
        "TestService.method_with_args.foo_bar",
        "TestService.method_with_args"
    )

def test_key_with_kwargs():
    mock_adapter = create_autospec(RedisSessionAdapter)
    
    class TestService(BaseCachingMixin):
        @BaseCachingMixin.cache_result(key_template='{kwarg1}-{kwarg2}')
        def method_with_kwargs(self, kwarg1=None, kwarg2=None):
            ...

    service = TestService(mock_adapter)
    service.method_with_kwargs(kwarg1="hello", kwarg2="world")
    
    mock_adapter.cache_key.assert_called_once_with(
        "TestService.method_with_kwargs.hello-world",
        "TestService.method_with_kwargs"
    )

def test_key_with_mixed_args_kwargs():
    mock_adapter = create_autospec(RedisSessionAdapter)
    
    class TestService(BaseCachingMixin):
        @BaseCachingMixin.cache_result(key_template='{arg}_{kwarg}')
        def mixed_method(self, arg, kwarg=None):
            ...

    service = TestService(mock_adapter)
    service.mixed_method("positional", kwarg="keyword")
    
    mock_adapter.cache_key.assert_called_once_with(
        "TestService.mixed_method.positional_keyword",
        "TestService.mixed_method"
    )

def test_custom_prefix_override():
    mock_adapter = create_autospec(RedisSessionAdapter)
    
    class TestService(BaseCachingMixin):
        @BaseCachingMixin.cache_result(
            key_template='test',
            prefix='CustomPrefix.{func.__name__}'
        )
        def custom_prefix_method(self):
            ...

    service = TestService(mock_adapter)
    service.custom_prefix_method()
    
    mock_adapter.cache_key.assert_called_once_with(
        "TestService.custom_prefix_method.test",
        "CustomPrefix.custom_prefix_method"  
    )

def test_complex_key_formatting():
    mock_adapter = create_autospec(RedisSessionAdapter)
    
    class TestService(BaseCachingMixin):
        @BaseCachingMixin.cache_result(key_template='{self.__class__.__name__}_{arg}')
        def self_referencing_method(self, arg):
            ...

    service = TestService(mock_adapter)
    service.self_referencing_method("value")
    
    mock_adapter.cache_key.assert_called_once_with(
        "TestService.self_referencing_method.TestService_value",
        "TestService.self_referencing_method"
    )

def test_missing_template_variable_raises():
    mock_adapter = create_autospec(RedisSessionAdapter)
    
    class TestService(BaseCachingMixin):
        @BaseCachingMixin.cache_result(key_template='{missing_var}')
        def problematic_method(self):
            ...

    service = TestService(mock_adapter)
    
    with pytest.raises(KeyError):
        service.problematic_method()

def test_empty_key_components():
    mock_adapter = create_autospec(RedisSessionAdapter)
    
    class TestService(BaseCachingMixin):
        @BaseCachingMixin.cache_result(key_template='')
        def empty_key_method(self):
            ...

    service = TestService(mock_adapter)
    service.empty_key_method()
    
    mock_adapter.cache_key.assert_called_once_with(
        "TestService.empty_key_method.",
        "TestService.empty_key_method"
    )

def test_result_passes_through_dto_on_cache_miss():
    mock_adapter = create_autospec(RedisSessionAdapter)
    DummyService.set_session_adapter(mock_adapter)
    
    dto_data = {"field_1": 42, "field_2": "dto-value"}
    mock_adapter.get.return_value = None
    mock_adapter.cache_key.return_value = "DummyService.service_method.key"
    
    service = DummyService(mock_adapter)
    result = service.service_method(dto_data)

    assert isinstance(result, DummyDTO)
    assert result.field_1 == 42
    assert result.field_2 == "dto-value"
    mock_adapter.set.assert_called_once()

def test_cache_result_without_dto_list():
    mock_adapter = create_autospec(RedisSessionAdapter)
    
    class NoDtoService(BaseCachingMixin):
        @BaseCachingMixin.cache_result(key_template='no_dto_key', dtos=[])
        def method(self, val):
            return {"value": val}

    mock_adapter.get.return_value = None
    mock_adapter.cache_key.return_value = "NoDtoService.method.no_dto_key"

    service = NoDtoService(mock_adapter)
    result = service.method("something")

    assert result == {"value": "something"}
    mock_adapter.set.assert_called_once_with("NoDtoService.method.no_dto_key", {"value": "something"})

