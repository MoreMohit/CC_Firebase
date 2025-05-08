from google.cloud import datastore

def store_user_data(uid, email):
    client = datastore.Client()
    key = client.key('User', uid)
    entity = datastore.Entity(key)
    entity.update({
        'uid': uid,
        'email': email
    })
    client.put(entity)
