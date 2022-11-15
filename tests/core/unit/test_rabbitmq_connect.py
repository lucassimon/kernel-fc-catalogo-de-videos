# Python
from unittest.mock import patch


# Third
import pytest

# Apps
from kernel_catalogo_videos.core.infrastructure.rabbitmq import RabbitMQ


@pytest.mark.integration
@pytest.mark.skip
def test_check_amqp_uri(blocking_connection_mock, url_parameters_mock):
    pass
