from cadastro1.login import autenticacao, usuario_logado
import psycopg2 as pg2
from psycopg2 import sql
from database.conexao import criar_conexao, fechar_conexao


def listag_ord_crescen(comando2: list, tabela2: str, coluna: str):
    conn, curr = criar_conexao()
    if not conn or not curr:
        print("Falha ao criar a conexão. Encerrando o processo.")
        return False
    if not autenticacao(usuario_logado):
        print("Usuário não logado.")
        return None

    try:
        colunas = sql.SQL(", ").join(map(sql.Identifier, comando2))
        tabela = sql.Identifier(tabela2)
        ordem_coluna = sql.Identifier(coluna)

        query = sql.SQL("SELECT {colunas} FROM {tabela} ORDER BY {ordem_coluna} ASC").format(
            colunas=colunas,
            tabela=tabela,
            ordem_coluna=ordem_coluna
        )
        curr.execute(query)
        resultado = curr.fetchall()

        for linha in resultado:
            print(linha)
        return resultado

    except pg2.Error as e:
        print(f"Erro ao executar a consulta: {e}")
        return None

    finally:
        curr.close()
        fechar_conexao()