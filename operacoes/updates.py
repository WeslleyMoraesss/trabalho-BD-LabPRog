from cadastro1.login import autenticacao, usuario_logado
import psycopg2 as pg2
from psycopg2 import sql
from database.conexao import criar_conexao, fechar_conexao


def updates(tabela4: str, coluna2: str, condicao3: str):
    conn, curr = criar_conexao()
    if not conn or not curr:
        print("Falha ao criar a conexão. Encerrando o processo.")
        return False
    
    if not autenticacao(usuario_logado):
        print("Usuário não logado.")
        return None
    try:
        consulta = sql.SQL("UPDATE {tabela4} SET {coluna2} WHERE {condicao3}").format(
            tabela4=sql.Identifier(tabela4),   
            coluna2=sql.Identifier(coluna2),    
            condicao3=sql.SQL(condicao3)        
        )

        curr.execute(consulta)
        conn.commit()  
        print(f"Tabela {tabela4} foi alterada com sucesso.")
        return True

    except pg2.Error as e:
        print(f"Erro na função: {e}")
        conn.rollback()  
        return False
    finally:
        curr.close()
        fechar_conexao()