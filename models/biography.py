


from db_config import get_db_connection


class Biography:

    def __init__(self, id, user_id, content):
        self.id = id
        self.user_id = user_id
        self.content = content

   

    """ db object """
    @classmethod
    def from_row(cls, row):
        if not row:
            return None

        return cls(
            id=row["id"],
            user_id=row["user_id"],
            content=row["content"]
        )


    """ object a dict """
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "content": self.content
        }

   

    @classmethod
    def get_by_user_id(cls, user_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM biography WHERE user_id=%s", (user_id, ))

            row = cursor.fetchone()

            cursor.close()

            return cls.from_row(row)
        
        finally:
            conn.close()




    """ creer o faire la mise a jour, si deja existe """
    def save(self):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()

            """ voir si y a des données """
            cursor.execute("""
                INSERT INTO biography (user_id, content)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE content = VALUES(content)
                """, 
                (self.user_id, self.content)
            )

            conn.commit()

            if cursor.lastrowid:
                self.id = cursor.lastrowid
                
            cursor.close()

        finally:
            conn.close()