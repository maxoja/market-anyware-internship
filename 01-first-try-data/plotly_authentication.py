from plotly.tools import set_credentials_file

logged_in = False

username_list = ['maxoja', 'wasdzz']
api_key_list = ['fW2JzfFO3YkOI2DD02uv', 'l8NjTxVKOn4xUpMaRK0E']

def login_plotly ( user_id=0 ) :
    username = username_list[user_id]
    api_key = api_key_list[user_id]
    
    set_credentials_file(username=username, api_key=api_key)
