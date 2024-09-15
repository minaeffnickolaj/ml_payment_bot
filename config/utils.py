import configparser

def read_config():
    config = configparser.ConfigParser()
    try:
        config.read('config.ini')

        if not config.has_section('database'):
            raise Exception('Database section not found in config.ini')
        if not config.has_section('pyrogram'):
            raise Exception('Pyrogram section not found in config.ini')
        if not config.has_section('techwizapi'):
            raise Exception('Techwizapi section not found in config.ini')
        if not config.has_section('payment_server'):
            raise Exception('Payment server section not found in config.ini')

        database_url = config['database']['url']
        database_user = config['database']['user']
        database_password = config['database']['password']
        database_name = config['database']['name']
        database_port = config['database']['port']
        pyrogram_api_id = config['pyrogram']['api_id']
        pyrogram_api_hash = config['pyrogram']['api_hash']
        pyrogram_bot_token = config['pyrogram']['bot_token']
        techwizapi_url = config['techwizapi']['url']
        techwizapi_key = config['techwizapi']['api_key']
        techwizapi_shop_id = config['techwizapi']['shop_id']
        payment_port = config['payment_server']['port']

        return (database_url, database_user, database_password, database_name, database_port, pyrogram_api_id,
                pyrogram_api_hash, pyrogram_bot_token, techwizapi_url, techwizapi_key, techwizapi_shop_id, payment_port)

    except FileNotFoundError:
        print('config.ini not found')
        raise
    except configparser.Error as e:
        print(f'Error reading config.ini: {e}')
        raise
    except ValueError as e:
        print(f'Configuration error reading config.ini: {e}')
        raise

    return config

