import pyrebase

FIREBASE_CONFIG_FILE = './neydi-api/firebase/config.json'


def _load_config():
    with open(FIREBASE_CONFIG_FILE) as file_data:
        import json
        json_data = json.load(file_data)
        return json_data


def _get_firebase():
    config = _load_config()
    firebase = pyrebase.initialize_app(config)
    return firebase


def add_query(token, query):
    firebase = _get_firebase()
    db = firebase.database()


def new_user(token, email, public, private):
    firebase = _get_firebase()
    db = firebase.database()
    data = {
        "token": str(token),
        "email": email,
        "public": str(public)
    }
    result = db.child("users").push(data)
    return result
