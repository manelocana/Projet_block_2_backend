

from db_config import get_db_connection


class Artwork:

    """ constructeur de la clase """
    def __init__(self, id, user_id, title, description, category, created_at):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.category = category
        self.created_at = created_at

    

    """ convertir le dict du db a object artwork """
    @classmethod
    def from_row(clase, row):
        return clase(
            id=row["id"],
            user_id=row["user_id"],
            title=row["title"],
            description=row["description"],
            category=row["category"],
            created_at=row.get("created_at")
        )

    """ convertir depuis object a dict (json) """
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "created_at": self.created_at
        }

    

    @classmethod
    def get_all(clase):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT artworks.*, users.username 
            FROM artworks
            JOIN users ON artworks.user_id = users.id
            ORDER BY artworks.id DESC
        """)

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        """ convertir chaque row a object """
        return [clase.from_row(row) for row in rows]

   


    @classmethod
    def get_by_id(clase, artwork_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM artworks WHERE id=%s", (artwork_id,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if not row:
            return None

        return clase.from_row(row)

    

    @classmethod
    def create(clase, user_id, title, description, category):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO artworks (user_id, title, description, category) VALUES (%s, %s, %s, %s)",
            (user_id, title, description, category)
        )

        conn.commit()
        new_id = cursor.lastrowid

        cursor.close()
        conn.close()

        """ return del nouveau object """
        return clase.get_by_id(new_id)



    def update(self, title, description, category):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE artworks SET title=%s, description=%s, category=%s WHERE id=%s AND user_id=%s",
            (title, description, category, self.id, self.user_id)
        )

        conn.commit()
        cursor.close()
        conn.close()

        """ mise a jour object in memoire """
        self.title = title
        self.description = description
        self.category = category

    


    def delete(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM artworks WHERE id=%s AND user_id=%s",
            (self.id, self.user_id)
        )

        conn.commit()
        cursor.close()
        conn.close() 