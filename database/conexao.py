import psycopg2
from psycopg2 import extras

host = "localhost"
port = "5432"
database = "postgres"
user = "postgres"
password = "senha_qualquer"

def criar_conexao():
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        print("Conexão com o banco de dados realizada com sucesso!")


        cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
        print("Cursor criado com sucesso!")
        
        return conn, cursor
    except psycopg2.Error as e:
        print(f"Erro ao conectar ao banco de dados ou criar o cursor: {e}")
        return None, None
def fechar_conexao(conn):
    if conn:
        conn.close()
        print("Conexão com o banco de dados fechada com sucesso.")
