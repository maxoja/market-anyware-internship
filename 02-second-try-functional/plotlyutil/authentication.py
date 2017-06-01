from plotly.tools import set_credentials_file

def login(user_id=0):
    set_credentials_file(username(user_id), api_key(user_id))
    
def username(user_id):
    return ['maxoja', 'wasdzz'][user_id]

def api_key(user_id):
    return ['fW2JzfFO3YkOI2DD02uv', 'l8NjTxVKOn4xUpMaRK0E'][user_id]