


from db_config import get_db_connection





class Message:

    @staticmethod
    def create(name, email, message):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)",
            (name, email, message)
        )

        conn.commit()
        cursor.close()
        conn.close()

        

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM messages ORDER BY id DESC")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows