from db.connection import get_connection

with get_connection() as conn:
    with conn.cursor() as cursor:
        cursor.execute("""
            ALTER USER 'tosokcokr'@'%' 
            IDENTIFIED WITH mysql_native_password BY 'tosokcokr##^^';
        """)
        cursor.execute("FLUSH PRIVILEGES;")
        cursor.close()
    conn.commit()