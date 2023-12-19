import configparser

read_config = configparser.ConfigParser()
read_config.read('settings.ini')

mongo_host = read_config['settings']['mongo_host']  # Query to mongo
postgres_query = read_config['settings']['postgres_query'] # Query to pqsl
