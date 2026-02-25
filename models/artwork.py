


from db_config import get_db_connection




class Artwork:

    def __init__(self, id, title, description, category, created_at):
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.created_at = created_at



    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM artworks ORDER BY id DESC")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows



    @staticmethod
    def create(title, description, category):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO artworks (title, description, category) VALUES (%s, %s, %s)",
            (title, description, category)
        )

        conn.commit()
        new_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return new_id



    @staticmethod
    def update(artwork_id, title, description, category):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE artworks SET title=%s, description=%s, category=%s WHERE id=%s",
            (title, description, category, artwork_id)
        )

        conn.commit()
        cursor.close()
        conn.close()



    @staticmethod
    def delete(artwork_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM artworks WHERE id=%s", (artwork_id,))

        conn.commit()
        cursor.close()
        conn.close()