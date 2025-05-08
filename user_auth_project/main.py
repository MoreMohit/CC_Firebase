from flask import Flask, request, render_template, redirect
import firebase_admin
from firebase_admin import auth, credentials
from google.cloud import datastore

app = Flask(__name__)

# Firebase Admin SDK initialization
cred = credentials.Certificate("firebase/firebase_config.json")
firebase_admin.initialize_app(cred)

# Initialize Datastore client
datastore_client = datastore.Client()

@app.route('/')
def index():
    return render_template('login.html')  # Your login page

@app.route('/verify', methods=['POST'])
def verify():
    id_token = request.form.get('idToken')

    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        email = decoded_token.get('email')

        # Store in Datastore
        entity_key = datastore_client.key('User', uid)  # Kind = User
        entity = datastore.Entity(key=entity_key)
        entity.update({
            'email': email,
            'uid': uid
        })
        datastore_client.put(entity)

        return render_template('success.html', email=email)

    except Exception as e:
        return f"Token verification failed: {str(e)}", 403

if __name__ == '__main__':
    app.run(debug=True)
