


from db_config import get_db_connection
import hashlib



password = "1234"
hashed = hashlib.sha256(password.encode()).hexdigest()



conn = get_db_connection()
cursor = conn.cursor()

cursor.execute("""
INSERT INTO users (username, email, password, role)
VALUES (%s, %s, %s, %s)
""", ("admin", "admin@example.com", hashed, "admin"))

conn.commit()
cursor.close()
conn.close()

print("Usuario admin creado")



