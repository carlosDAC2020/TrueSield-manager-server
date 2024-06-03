import psycopg2

# Configura la conexión
host = 'trueshield.cl0mwigse4do.us-east-1.rds.amazonaws.com'
dbname = 'postgres'
user = 'postgres'
password = 'j2uPsPyhcqb3tPyNdrbu'

# Conecta a la base de datos
conn = psycopg2.connect(
    host=host,
    dbname=dbname,
    user=user,
    password=password
)

# Crea una nueva base de datos
try:
    with conn.cursor() as cursor:
        cursor.execute('CREATE DATABASE FKNDetector;')
        conn.commit()

        # Recupera la lista de bases de datos existentes
        cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
        databases = cursor.fetchall()
        print("Bases de datos existentes:")
        for db in databases:
            print(db[0])
except psycopg2.Error as e:
    print("Error al crear o consultar la base de datos:", e)
finally:
    conn.close()
