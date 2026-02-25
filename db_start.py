

from db_config import get_db_connection




def init_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Crear la base de datos si no existe
    cursor.execute("CREATE DATABASE IF NOT EXISTS projet_block2;")
    cursor.execute("USE projet_block2;")

    # Tabla Users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) NOT NULL,
        email VARCHAR(150) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        role ENUM('admin','artist') DEFAULT 'artist',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Tabla Artworks
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artworks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        category VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Tabla Biography
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS biography (
        id INT PRIMARY KEY,
        content TEXT
    );
    """)

    # Insertar una fila vacía para la biografía inicial
    cursor.execute("""
    INSERT IGNORE INTO biography (id, content) VALUES (1, '');
    """)

    # Tabla Messages (contacto)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(150),
        email VARCHAR(150),
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("DB inicializada correctamente")

if __name__ == "__main__":
    init_database()