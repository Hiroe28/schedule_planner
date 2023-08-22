

# イベントデータを保持するディクショナリ
events_db = {}


def create_event(event_name, memo, dates):
    event_id = len(events_db) + 1
    events_db[event_id] = {
        'name': event_name,
        'memo': memo,
        'dates': dates,
        'participants': {}
    }
    return event_id


def get_event(event_id):
    return events_db.get(event_id)


def add_participant(event_id, name, availability, comment):
    events_db[event_id]['participants'][name] = {
        'availability': availability,
        'comment': comment
    }


def remove_participant(event_id, name):
    if name in events_db[event_id]['participants']:
        del events_db[event_id]['participants'][name]
