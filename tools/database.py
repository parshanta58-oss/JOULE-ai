import psycopg2


DB_CONFIG= {
    "host": "localhost",
    "port": 5432,
    "database": "joule_ai_db",
    "user": "joule_ai_user",
    "password": "joule_ai_password",
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)