


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



    @classmethod
    def from_row(clase, row):
        if not row:
            return None

        return clase(
            row["id"],
            row["username"],
            row["email"],
            row["password"],
            row["role"],
            row.get("created_at")
        )

    


    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at
        }

    
    

    @classmethod
    def create(clase, username, email, password, role="artist"):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()

            hashed_password = clase.hash_password(password)

            cursor.execute(
                "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
                (username, email, hashed_password, role)
            )

            conn.commit()
            user_id = cursor.lastrowid

            cursor.close()

            return clase.find_by_id(user_id)

        finally:
            conn.close()
    
    

    @classmethod
    def get_all(clase):
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT id, username, email, role, created_at FROM users ORDER BY id DESC"
            )

            rows = cursor.fetchall()

            cursor.close()

            return [clase.from_row(row) for row in rows]
        
        finally:
            conn.close()




    @classmethod
    def find_by_email(clase, email):
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            row = cursor.fetchone()

            cursor.close()

            return clase.from_row(row)
        
        finally:
            conn.close()

    


    @classmethod
    def find_by_id(clase, user_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            row = cursor.fetchone()

            cursor.close()

            return clase.from_row(row)
        
        finally:
            conn.close()

    

    
    def update(self, username, email, password=None):
        conn = get_db_connection()

        try:
            cursor = conn.cursor()

            if password:
                hashed = self.hash_password(password)

                cursor.execute(
                    "UPDATE users SET username=%s, email=%s, password=%s WHERE id=%s",
                    (username, email, hashed, self.id)
                )
                self.password = hashed
            else:
                cursor.execute(
                    "UPDATE users SET username=%s, email=%s WHERE id=%s",
                    (username, email, self.id)
                )

            conn.commit()

            cursor.close()

            """ mise a jour del object en memoire """
            self.username = username
            self.email = email

        finally:
            conn.close()