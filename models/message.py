

from db_config import get_db_connection


class Message:

    def __init__(self, id, name, email, content):
        self.id = id
        self.name = name
        self.email = email
        self.content = content

    
    """ convert db a object """
    @classmethod
    def from_row(clase, row):
        if not row:
            return None
        
        return clase(
            id=row["id"],
            name=row["name"],
            email=row["email"],
            content=row["message"]  
        )

    
    """ object a dict """
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "message": self.content
        }

    


    @classmethod
    def get_all(clase):
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT * FROM messages ORDER BY id DESC")
            rows = cursor.fetchall()

            cursor.close()

            """ convert chaque file en object """
            return [clase.from_row(row) for row in rows]
        
        finally:
            conn.close()

    


    @classmethod
    def create(clase, name, email, content):
        conn = get_db_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)",
                (name, email, content)
            )

            conn.commit()
            new_id = cursor.lastrowid

            cursor.close()

            return clase(new_id, name, email, content)
        
        finally:
            conn.close()