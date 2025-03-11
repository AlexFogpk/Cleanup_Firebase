import os
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials, firestore

# Читаем ключ Firebase из переменной окружения "FIREBASE_CREDENTIALS"
firebase_credentials = os.getenv("FIREBASE_CREDENTIALS")
if not firebase_credentials:
    raise ValueError("Environment variable FIREBASE_CREDENTIALS is not set.")

# Записываем содержимое переменной в файл firebase.json
with open("firebase.json", "w") as f:
    f.write(firebase_credentials)

# Инициализация Firebase
cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def delete_old_messages():
    cutoff_date = datetime.utcnow() - timedelta(days=90)
    users_ref = db.collection("users")
    deleted_count = 0

    for user_doc in users_ref.stream():
        history_ref = user_doc.reference.collection("history")
        old_messages = history_ref.where("timestamp", "<", cutoff_date).stream()
        for msg in old_messages:
            msg.reference.delete()
            deleted_count += 1

    print(f"Deleted {deleted_count} old messages.")

if __name__ == "__main__":
    delete_old_messages()
