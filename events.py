import pickle

DATA_FILE = 'events_db.pkl'

# イベントデータを保持するディクショナリ
events_db = {}


def save_data():
    with open(DATA_FILE, 'wb') as f:
        pickle.dump(events_db, f)


def load_data():
    global events_db
    try:
        with open(DATA_FILE, 'rb') as f:
            events_db = pickle.load(f)
    except FileNotFoundError:
        events_db = {}


def create_event(event_name, memo, dates):
    event_id = len(events_db) + 1
    events_db[event_id] = {
        'name': event_name,
        'memo': memo,
        'dates': dates,
        'participants': {}
    }
    save_data()
    return event_id


def get_event(event_id):
    return events_db.get(event_id)


def add_participant(event_id, name, availability, comment):
    events_db[event_id]['participants'][name] = {
        'availability': availability,
        'comment': comment
    }
    save_data()


def remove_participant(event_id, name):
    if name in events_db[event_id]['participants']:
        del events_db[event_id]['participants'][name]
    save_data()

# アプリケーション開始時にデータを読み込みます
load_data()