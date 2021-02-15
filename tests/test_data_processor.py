import csv
import os
from io import StringIO

import pytest
import requests
import pandas as pd
from pandas import DataFrame

from data_jump import data_processor as DP
from data_jump.app import app
import requests_mock


def file_get_contents(filename):
    with open(filename, 'r') as f:
        return f.read()


response_1 = [{"date": "22-01-2021", "impressions": 1376}, {"date": "21-01-2021", "impressions": 1906},
              {"date": "20-01-2021", "impressions": 2818}, {"date": "19-01-2021", "impressions": 1024},
              {"date": "18-01-2021", "impressions": 646}, {"date": "17-01-2021", "impressions": 2885},
              {"date": "16-01-2021", "impressions": 1889}, {"date": "15-01-2021", "impressions": 1534},
              {"date": "14-01-2021", "impressions": 995}, {"date": "13-01-2021", "impressions": 1251}]
fname = os.getcwd() + '/input_data/small.csv'
response_2 = file_get_contents(os.getcwd() + '/input_data/small.csv')

SERVICE_ENDPOINTS = {
    'Service X': 'http://test.com/abc/1234',
    'Service Y': 'http://test.com/def/5678'
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
        service_2_name = list(SERVICE_ENDPOINTS)[1]
        service_2_url = SERVICE_ENDPOINTS[service_2_name]
        kwargs['mock'].get(service_1_url,
                           headers={
                               "content-type": "application/json;charset=UTF-8",
                           },
                           json=response_1)
        kwargs['mock'].get(service_2_url,
                           headers={
                               "content-type": "text/csv;charset=UTF-8",
                           },
                           body=fname)
        data_processor = DP.DataProcessor(SERVICE_ENDPOINTS.items())
        data = data_processor.get_data_from_endpoints()
        assert data == [response_1, response_2]

    def test_combine_dataframes(self):
        data_frames: list = []
        for segment in [response_1, response_1]:
            data_frames.append(pd.DataFrame(segment))

        concatenated_data_frames: DataFrame = pd.concat(data_frames, ignore_index=True)

        data_processor = DP.DataProcessor(SERVICE_ENDPOINTS.items())
        combined_data: DataFrame = data_processor.combine_dataframes([response_1, response_1])
        assert combined_data.to_string() == concatenated_data_frames.to_string()

    def test_find_sum_and_mean(self):
        data_frames: list = []
        for segment in [response_1, response_1]:
            data_frames.append(pd.DataFrame(segment))

        concatenated_data_frames: DataFrame = pd.concat(data_frames, ignore_index=True)
        data_processor = DP.DataProcessor(SERVICE_ENDPOINTS.items())
        output = data_processor.find_sum_and_mean(concatenated_data_frames)

        assert output == {'mean': 1632.4, 'sum': 32648}
