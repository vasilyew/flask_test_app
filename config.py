import json

class AppConfig:
    db_connection = ''
    debug = False
    suPassword = ''
    sessionLifetime = 0

def init_config():
    with open('appconfig.json', 'r') as f:
        jf = f.read()
        res = json.loads(jf)
        AppConfig.db_connection = res['dbConnection']
        AppConfig.debug = res['debug']
        AppConfig.suPassword = res['suPassword']
        AppConfig.sessionLifetime = res['sessionLifetime']