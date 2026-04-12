


from db_config import get_db_connection


class Biography:

    def __init__(self, id, user_id, content):
        self.id = id
        self.user_id = user_id
        self.content = content

   

    """ db object """
    @classmethod
    def from_row(clase, row):
        if not row:
            return None

        return clase(
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
    def get_by_user_id(clase, user_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM biography WHERE user_id=%s", (user_id, ))

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return clase.from_row(row)



    """ creer o faire la mise a jour, si deja existe """
    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        """ voir si y a des données """
        cursor.execute(
            "SELECT id FROM biography WHERE user_id=%s",
            (self.user_id,)
        )

        existing = cursor.fetchone()

        if existing:
            cursor.execute(
                "UPDATE biography SET content=%s WHERE user_id=%s",
                (self.content, self.user_id)
            )

        else:
            cursor.execute(
                "INSERT INTO biography (user_id, content) VALUES (%s, %s)",
                (self.user_id, self.content)
            )
            self.id = cursor.lastrowid

        conn.commit()
        cursor.close()
        conn.close()