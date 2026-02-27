


from db_config import get_db_connection




class Biography:

    @staticmethod
    def get():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM biography ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row



    @staticmethod
    def create_or_update(content):
        conn = get_db_connection()
        cursor = conn.cursor()

        # Si ya hay biografía, actualizamos
        cursor.execute("SELECT id FROM biography ORDER BY id DESC LIMIT 1")
        existing = cursor.fetchone()
        if existing:
            cursor.execute("UPDATE biography SET content=%s, updated_at=NOW() WHERE id=%s", (content, existing[0]))
        else:
            cursor.execute("INSERT INTO biography (content) VALUES (%s)", (content,))

        conn.commit()
        cursor.close()
        conn.close()