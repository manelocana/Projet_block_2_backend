

from db_config import get_db_connection




def init_database():
    conn = get_db_connection()
    cursor = conn.cursor()


    # creer la database si n'existe pas
    cursor.execute("CREATE DATABASE IF NOT EXISTS projet_block2;")
    cursor.execute("USE projet_block2;")



    # Table users
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



    # Table artworks (fk=users)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artworks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        category VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
            ON DELETE CASCADE
    );
    """)



    # Table biography (fk=users)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS biography (
        id INT PRIMARY KEY,
        user_id INT UNIQUE,
        content TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
            ON DELETE CASCADE
    );
    """)



    # Creer une table inicial pour la biography
    cursor.execute("""
    INSERT IGNORE INTO biography (id, content) 
        VALUES (1, '');
    """)



    # Table messages (contact) (fk=users)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NULL,
        name VARCHAR(150),
        email VARCHAR(150),
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
            ON DELETE SET NULL
    );
    """)

    conn.commit()
    cursor.close()
    conn.close()

    print("DB correct")

if __name__ == "__main__":
    init_database()