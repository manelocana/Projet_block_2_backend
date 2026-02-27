

import hashlib
from db_config import get_db_connection




class User:
    def __init__(self, id, username, email, password, role, created_at=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.created_at = created_at



    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()



    @staticmethod
    def create(username, email, password, role="artist"):
        conn = get_db_connection()
        cursor = conn.cursor()

        hashed_password = User.hash_password(password)

        cursor.execute(
            "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
            (username, email, hashed_password, role)
        )

        conn.commit()
        user_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return user_id



    @staticmethod
    def get_all_users():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id, username, email, role, created_at FROM users ORDER BY id DESC")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows



    @staticmethod
    def find_by_email(email):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        data = cursor.fetchone()

        cursor.close()
        conn.close()

        if data:
            return User(**data)
        return None
    


    @staticmethod
    def update_user(user_id, username, email):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(""" UPDATE users SET username = %s, email = %s WHERE id = %s """, (username, email, user_id))

        conn.commit()

        cursor.close()
        conn.close()