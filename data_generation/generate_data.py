from faker import Faker
import psycopg2


fake = Faker()


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "joule_ai_db",
    "user": "joule_ai_user",
    "password": "joule_ai_password",
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def main():
    connection = get_connection()

    print("Connected to Joule AI PostgreSQL database!")

    connection.close()



fake = Faker()


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "joule_ai_db",
    "user": "joule_ai_user",
    "password": "joule_ai_password",
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def main():
    connection = get_connection()

    print("Connected to Joule AI PostgreSQL database!")

    connection.close()


if __name__ == "__main__":
    main()