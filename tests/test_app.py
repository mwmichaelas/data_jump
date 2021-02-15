import pytest
import requests
from data_jump.app import app
import requests_mock


class TestApp:

    @pytest.fixture
    def app_context(self):
        with app.app_context():
            yield

    @requests_mock.Mocker(kw='mock')
    def test_home_function(self, **kwargs):
        mean_and_sum = {'mean': 1632.4, 'sum': 32648}
        kwargs['mock'].get('http://127.0.0.1/',
                           headers={
                               "content-type": "application/json;charset=UTF-8",
                           },
                           json=mean_and_sum)
        response = requests.get('http://127.0.0.1/')
        assert response.json() == mean_and_sum
