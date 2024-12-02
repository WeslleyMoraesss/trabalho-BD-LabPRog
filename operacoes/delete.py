from cadastro1.login import autenticacao, usuario_logado
import psycopg2 as pg2
from psycopg2 import sql
from cadastro1.login import autenticacao
from database.conexao import criar_conexao, fechar_conexao

def delete(tabela6: str, condicao4):
    conn, curr = criar_conexao()
    
    if not conn or not curr:
        print("Falha ao criar a conexão. Encerrando o processo.")
        return False
    if not autenticacao(usuario_logado):
        print("Usuário não logado.")
        return None

    try:
        if condicao4:
            execute = sql.SQL("DELETE FROM {tabela6} WHERE {condicao4}").format(
                tabela6=sql.Identifier(tabela6),
                condicao4=sql.SQL(condicao4)
            )
        else:
            execute = sql.SQL("DELETE FROM {tabela6}").format(
                tabela6=sql.Identifier(tabela6)
            )
        
        curr.execute(execute)
        conn.commit()
        print(f"Registros da tabela {tabela6} deletados com sucesso!")
        return True
    
    except pg2.Error as e:
        print(f"Erro na função: {e}")
        conn.rollback()
        return False
    finally:
        curr.close()
        fechar_conexao()