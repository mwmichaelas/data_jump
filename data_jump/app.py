import os
import sys

from flask import Flask
from pandas import DataFrame

from data_jump import app_config
from data_jump.data_processor import DataProcessor

sys.path.append(os.path.join(os.path.dirname(__file__),os.pardir,"data_jump"))

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home_function() -> dict:
    data_processor: DataProcessor = DataProcessor(app_config.SERVICES.items())
    data: list = data_processor.get_data_from_endpoints()
    combined_data: DataFrame = data_processor.combine_dataframes(data)
    return data_processor.find_sum_and_mean(combined_data)


if __name__ == '__main__':
    port: int = 8000
    app.run(host='127.0.0.1', port=port, debug=True)
