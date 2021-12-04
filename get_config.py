from configparser import ConfigParser

PATH = "CONFIG/config.conf"
#Read config.ini file
config_object = ConfigParser()
config_object.read(PATH)

#Get the password
serverinfo = config_object["SERVERCONFIG"]
HOST = serverinfo['host']
PORT = int(serverinfo['port'])
TIMEOUT= int(serverinfo['timeout'])
CONNECTIONS = int(serverinfo['connections'])
MAX_REQUEST = int(serverinfo['requests'])
FORMAT = serverinfo['FORMAT']
IP = serverinfo['ipaddr']
TIMEOUT= int(serverinfo['timeout'])
BUFFER = int(serverinfo['buffer'])

