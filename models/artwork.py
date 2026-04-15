

from db_config import get_db_connection


class Artwork:

    """ constructeur de la clase artowrk """
    def __init__(self, id, user_id, title, description, category, created_at, username=None):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.category = category
        self.created_at = created_at
        self.username = username

    

    """ convertir le dict du db a object artwork """
    @classmethod
    def from_row(cls, row):
        if not row:
            return None
        
        return cls(
            id=row["id"],
            user_id=row["user_id"],
            title=row["title"],
            description=row["description"],
            category=row["category"],
            created_at=row.get("created_at"),
            username=row.get("username")
        )

    """ convertir depuis object a dict (json) """
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "created_at": self.created_at,
            "username": self.username
        }

    

    @classmethod
    def get_all(cls):
        conn = get_db_connection()

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT artworks.*, users.username 
                FROM artworks
                JOIN users ON artworks.user_id = users.id
                ORDER BY artworks.id DESC
            """)

            rows = cursor.fetchall()
            cursor.close()

            """ convertir chaque row a object """
            return [cls.from_row(row) for row in rows]
        
        finally:
            conn.close()

   


    @classmethod
    def get_by_id(cls, artwork_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM artworks WHERE id=%s", (artwork_id,))

            row = cursor.fetchone()

            cursor.close()

            return cls.from_row(row) if row else None
        
        finally:
            conn.close()

    

    @classmethod
    def create(cls, user_id, title, description, category):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO artworks (user_id, title, description, category) VALUES (%s, %s, %s, %s)",
                (user_id, title, description, category)
            )

            conn.commit()
            new_id = cursor.lastrowid

            cursor.close()

            """ return del nouveau object """
            return cls.get_by_id(new_id)
        
        finally:
            conn.close()



    def update(self, title, description, category):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE artworks SET title=%s, description=%s, category=%s WHERE id=%s AND user_id=%s",
                (title, description, category, self.id, self.user_id)
            )

            conn.commit()

            """ mise a jour object in memoire """
            self.title = title
            self.description = description
            self.category = category
            
            cursor.close()

        finally:
            conn.close()

            

    


    def delete(self):
        conn = get_db_connection()
        try:
            cursor = conn.cursor() 

            cursor.execute(
                "DELETE FROM artworks WHERE id=%s AND user_id=%s",
                (self.id, self.user_id)
            )

            conn.commit()
            cursor.close()
        
        finally:
            conn.close() 