from configparser import ConfigParser

#Get the configparser object
config_object = ConfigParser()

PATH = "CONFIG/config.conf"
PORT = 8000
TIMEOUT = 300
MAX_CONNECTIONS = 10
MAX_REQUEST = 100
BUFFER = 1024
config_object["SERVERCONFIG"] = {
    "host": '127.0.0.1',
    "port": PORT,
    "timeout": TIMEOUT,
    "FORMAT": "utf-8",
    "ipaddr": "8.8.8.8",
    'connections': MAX_CONNECTIONS,
    'requests': MAX_REQUEST,
    'buffer': BUFFER,
    'ServerRoot': 'HTTPServer'
}

#Write the above sections to config.ini file
with open(PATH, 'w') as conf:
    config_object.write(conf)