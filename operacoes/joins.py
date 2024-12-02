from cadastro1.login import autenticacao, usuario_logado
import psycopg2 as pg2
from psycopg2 import sql
from database.conexao import criar_conexao, fechar_conexao


def joins(tabela3: str, comando2: str, comando3: str, keys: str, condicao2: str = None):
    conn, curr = criar_conexao() 
    if not conn or not curr:
        print("Falha ao criar a conexão. Encerrando o processo.")
        return False
    
    if not autenticacao(usuario_logado):
        print("Usuário não logado.")
        return None
    
    try:
        if condicao2:
            consulta2 = sql.SQL("SELECT {tabela3} FROM {comando2} JOIN {comando3} ON {keys} WHERE {condicao2}").format(
                tabela3=sql.Identifier(tabela3),  
                comando2=sql.Identifier(comando2),  
                comando3=sql.Identifier(comando3),  
                keys=sql.SQL(keys),  
                condicao2=sql.SQL(condicao2)  
            )
        else:
            consulta2 = sql.SQL("SELECT {tabela3} FROM {comando2} JOIN {comando3} ON {keys}").format(
                tabela3=sql.Identifier(tabela3),
                comando2=sql.Identifier(comando2),
                comando3=sql.Identifier(comando3),
                keys=sql.SQL(keys) 
            )

        curr.execute(consulta2)
        result = curr.fetchall()

        for l in result:
            print(l)
        return True
    
    except pg2.Error as e:
        print(f"Erro na função: {e}")
        return False
    finally:
        curr.close()
        fechar_conexao()