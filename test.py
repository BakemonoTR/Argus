import subprocess
import os
import hashlib

API_KEY = os.environ.get('API_KEY')
password = hashlib.sha256(os.environ.get('PASSWORD').encode()).hexdigest()

def get_user(user_id):
    query = "SELECT * FROM users WHERE id = %s"
    return db.execute(query, (user_id,))

def find_duplicates(items):
    duplicates = []
    for i in items:
        for j in items:
            if i == j:
                duplicates.append(i)
    return duplicates

def a(x, y):
    return x+y