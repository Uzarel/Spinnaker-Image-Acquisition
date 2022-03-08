import configparser

def get_config():
    # Reding configuration file
    config = configparser.ConfigParser()
    with open('config.ini') as file:
        config.readfp(file)
    return config