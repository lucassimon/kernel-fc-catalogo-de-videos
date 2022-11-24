import pytest

from kernel_catalogo_videos.core.application.use_case import UseCase


def test_raises_error_when_method_execute_is_not_implemented():

    with pytest.raises(TypeError) as assert_error:
        # pylint: disable=abstract-class-instantiated
        UseCase()

    assert (
        assert_error.value.args[0]
        == "Can't instantiate abstract class UseCase with abstract method execute"
    )
