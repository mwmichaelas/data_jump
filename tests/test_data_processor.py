import csv
import sys
import os

from data_jump.app import app
from data_jump.data_processor import DataProcessor

sys.path.append(os.path.join(os.path.dirname(__file__),os.pardir,"data_jump"))


import pytest
import pandas as pd
from pandas import DataFrame

import requests_mock


def file_get_contents(filename):
    with open(filename, 'r') as f:
        return f.read()


response_1 = [{"date": "22-01-2021", "impressions": 1376}, {"date": "21-01-2021", "impressions": 1906},
              {"date": "20-01-2021", "impressions": 2818}, {"date": "19-01-2021", "impressions": 1024},
              {"date": "18-01-2021", "impressions": 646}, {"date": "17-01-2021", "impressions": 2885},
              {"date": "16-01-2021", "impressions": 1889}, {"date": "15-01-2021", "impressions": 1534},
              {"date": "14-01-2021", "impressions": 995}, {"date": "13-01-2021", "impressions": 1251}]

SERVICE_ENDPOINTS = {
    'Service X': 'http://test.com/abc/1234'
}


class TestDataProcessor:

    @pytest.fixture
    def app_context(self):
        with app.app_context():
            yield

    @requests_mock.Mocker(kw='mock')
    def test_get_data_from_endpoints(self, **kwargs):
        service_1_name = list(SERVICE_ENDPOINTS)[0]
        service_1_url = SERVICE_ENDPOINTS[service_1_name]
        kwargs['mock'].get(service_1_url,
                           headers={
                               "content-type": "application/json;charset=UTF-8",
                           },
                           json=response_1)
        data_processor = DataProcessor(SERVICE_ENDPOINTS.items())
        data = data_processor.get_data_from_endpoints()
        assert data == [response_1]

    def test_combine_dataframes(self):
        data_frames: list = []
        for segment in [response_1, response_1]:
            data_frames.append(pd.DataFrame(segment))

        concatenated_data_frames: DataFrame = pd.concat(data_frames, ignore_index=True)

        data_processor = DataProcessor(SERVICE_ENDPOINTS.items())
        combined_data: DataFrame = data_processor.combine_dataframes([response_1, response_1])
        assert combined_data.to_string() == concatenated_data_frames.to_string()

    def test_find_sum_and_mean(self):
        data_frames: list = []
        for segment in [response_1, response_1]:
            data_frames.append(pd.DataFrame(segment))

        concatenated_data_frames: DataFrame = pd.concat(data_frames, ignore_index=True)
        data_processor = DataProcessor(SERVICE_ENDPOINTS.items())
        output = data_processor.find_sum_and_mean(concatenated_data_frames)

        assert output == {'mean': 1632.4, 'sum': 32648}
