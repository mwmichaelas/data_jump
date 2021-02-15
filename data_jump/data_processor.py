import csv
import pandas as pd
import requests

from pandas import DataFrame


class DataProcessor:

    def __init__(self, endpoints):
        self.endpoints: dict = endpoints

    def get_data_from_endpoints(self) -> list:
        data: list = []
        for service_name, url in self.endpoints:
            try:
                response: requests = requests.get(url)
                data = self.append_data_to_list(data, response)
            except requests.ConnectionError:
                raise ConnectionError
        return data

    def append_data_to_list(self, output, response):
        content_type: str = response.headers.get('content-type')
        if 'application/json' in content_type:
            output.append(response.json())
        elif 'text/csv' in content_type:
            columns: list = ['date', 'impression']
            csv_data: csv = pd.read_csv(response.url, header=None, index_col=False, names=columns,
                                        sep=',', squeeze=True, skiprows=1).to_dict('records')
            output.append(csv_data)
        return output

    def combine_dataframes(self, data) -> DataFrame:
        data_frames: list = []
        for segment in data:
            data_frames.append(pd.DataFrame(segment))

        for i in range(1, len(data_frames)):
            data_frames[i].columns = data_frames[0].columns

        concatenated_data_frames: DataFrame = pd.concat(data_frames, ignore_index=True)

        return concatenated_data_frames

    def find_sum_and_mean(self, data: pd.DataFrame) -> dict:
        impressions_sum: int = data['impressions'].sum()
        impressions_mean: int = data['impressions'].mean()

        return {'mean': float(impressions_mean), 'sum': int(impressions_sum)}
