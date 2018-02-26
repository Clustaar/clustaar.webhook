import pytest
from clustaar.webhook.filters import StepID, JSONKeyEquals, JSONKeyIn
from tests.utils import FACTORY


class TestCall(object):
    def test_returns_an_equals_filter_if_id_is_a_str(self):
        filter = StepID("123")
        assert isinstance(filter, JSONKeyEquals)

    def test_returns_an_equals_filter_if_id_is_a_list(self):
        filter = StepID(["123"])
        assert isinstance(filter, JSONKeyIn)

    def test_raise_error_if_invalid_argument(self):
        with pytest.raises(TypeError):
            StepID(1)
