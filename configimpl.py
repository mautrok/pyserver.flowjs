import configparser

config= configparser.RawConfigParser(allow_no_value=True)
#decomment this line for unix system
#config.read('conf/pyserverconfig.ini')
config.read('conf/pyserverconfigWin.ini')
