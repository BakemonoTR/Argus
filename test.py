import subprocess

API_KEY = "sk-1234567890abcdef"
password = "supersecret123"

def get_user(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    return db.execute(query)

def find_duplicates(items):
    duplicates = []
    for i in items:
        for j in items:
            if i == j:
                duplicates.append(i)
    return duplicates

def a(x, y):
    return x+y

# test change