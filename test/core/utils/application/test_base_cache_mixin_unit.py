from kombu.exceptions import BaseExceptionType
import pytest
from unittest.mock import create_autospec
from pydantic import BaseModel
from core.utils.application.base_cache_mixin import BaseCachingMixin
from core.utils.infrastructure.adapters.redis import RedisSessionAdapter

class DummyDTO(BaseModel):
    field_1: int = 0
    field_2: str = 'string'

class DummyService(BaseCachingMixin):
    @BaseCachingMixin.cache_result(key_template='some_arg', dtos=[DummyDTO])
    def service_method(self, some_args: dict) -> DummyDTO:
        return DummyDTO(**some_args)

class DummyAdapter:
    def __init__(self):
        self.cache_key = lambda key, prefix="cache": str()
        self.get = lambda key, default=None, deserialize=True: DummyDTO()
        self.set = lambda key, data, expire=60, serialize=True: None

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

def test_session_adapter_injection():
    mixin = BaseCachingMixin(DummyAdapter)
    assert isinstance(mixin.session_adapter, DummyAdapter)

    mixin = BaseCachingMixin(DummyAdapter())
    assert isinstance(mixin.session_adapter, DummyAdapter)

    with pytest.raises():
        BaseCachingMixin(None)
