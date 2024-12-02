from cadastro1.login import autenticacao, usuario_logado
from cadastro1.login import autenticacao
from database.conexao import criar_conexao, fechar_conexao
import psycopg2 as pg2
from psycopg2 import sql

def selects(comando1: list, tabela1: str, condicao: str = None):
    conn, curr = criar_conexao()
    if not conn or not curr:
        print("Falha ao criar a conexão. Encerrando o processo.")
        return False
    if not autenticacao(usuario_logado):
        print("Usuário não logado.")
        return None
    try:
        colunas = sql.SQL(", ").join(map(sql.Identifier, comando1))
        tabela = sql.Identifier(tabela1)

        if condicao:
            query = sql.SQL("SELECT {colunas} FROM {tabela} WHERE {condicao}").format(
                colunas=colunas,
                tabela=tabela,
                condicao=sql.SQL(condicao)  
            )
        else:
            query = sql.SQL("SELECT {colunas} FROM {tabela}").format(
                colunas=colunas,
                tabela=tabela
            )

        curr.execute(query)
        resultado = curr.fetchall()

        print("Aqui estão os resultados listados:")
        for linha in resultado:
            print(linha)
        return resultado
    except pg2.Error as e:
        print(f"Erro na função: {e}")
        return None

    finally:
        curr.close()
        fechar_conexao