from influxdb import InfluxDBClient
import configparser


class DBLoader:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        self._host = config['DATABASE']['host']
        self._port = config['DATABASE']['port']
        self._username = config['DATABASE']['username']
        self._password = config['DATABASE']['password']
        self._database = config['DATABASE']['database']

    def _get_connection(self):
        client = InfluxDBClient(self._host, self._port, self._username, self._password, self._database)
        client.switch_database(self._database)
        return client

    def _create_influxdb_json(self, dataframe, measurement_name, time_column_name):
        influxdb_json = []
        for _, row in dataframe.iterrows():
            measurement = {
                'measurement': measurement_name,
                'tags': {},
                'time': row[time_column_name],
                'fields': {}
            }
            for column in dataframe.columns:
                if column != time_column_name:
                    measurement['fields'][column] = row[column]
            influxdb_json.append(measurement)
        return influxdb_json

    def load_data(self, dataframe, measurement_name, time_column_name):
        connection = self._get_connection()

        influx_json = self._create_influxdb_json(dataframe, measurement_name, time_column_name)

        connection.drop_measurement(measurement_name)
        connection.write_points(influx_json)
