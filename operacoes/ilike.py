from cadastro1.login import autenticacao, usuario_logado
from database.conexao import criar_conexao, fechar_conexao
import psycopg2 as pg2
from psycopg2 import sql
from cadastro1.login import autenticacao

def operador_com_ILIKE(tabela: str, termo1: str, termo2: str):
    conn, curr = criar_conexao()
    if not conn or not curr:
        print("Falha ao criar a conexão. Encerrando o processo.")
        return False
    if not autenticacao(usuario_logado):
        print("Usuário não logado.")
        return False

    colunas = []
    while True:
        try:
            opc = int(input("Digite 1 para adicionar coluna, 2 para sair: "))
            if opc == 1:
                conteudo = input("Digite o nome da coluna: ").strip()
                if conteudo:
                    colunas.append(conteudo)
                else:
                    print("Nome da coluna não pode ser vazio.")
            elif opc == 2:
                print("Saindo da adição de colunas.")
                break
            else:
                print("Opção inválida. Digite 1 ou 2.")
        except ValueError:
            print("Erro: Por favor, digite um número válido.")

    if not colunas:
        print("Nenhuma coluna foi adicionada.")
        return False
    try:
        curr = conn.cursor()

        columns = sql.SQL(", ").join(sql.Identifier(col) for col in colunas)
        consulta = sql.SQL(
            "SELECT {columns} FROM {tabela} WHERE titulo ILIKE %s OR subtitulo ILIKE %s"
        ).format(
            columns=columns,
            tabela=sql.Identifier(tabela)
        )
        curr.execute(consulta, (termo1 + '%', termo2 + '%'))
        resultados = curr.fetchall()
        if not resultados:
            print("Nenhum resultado foi encontrado.")
            return False
        print(f"Aqui estão os resultados da tabela '{tabela}':")
        for linha in resultados:
            print(linha)
        return True

    except pg2.Error as e:
        print(f"Erro no banco de dados: {e}")
        return False
    finally:
        curr.close()
        fechar_conexao()