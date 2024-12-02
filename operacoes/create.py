from cadastro1.login import autenticacao, usuario_logado
import psycopg2 as pg2
from psycopg2 import sql
from database.conexao import criar_conexao, fechar_conexao


def criar_tabela():
    conn, curr = criar_conexao()
    if not conn or not curr:
        print("Falha ao criar a conexão. Encerrando o processo.")
        return False

    if not autenticacao(usuario_logado):
        print("Usuário não logado.")
        return None

    try:
        table_name = input("Digite o nome da tabela: ").strip()
        if not table_name:
            print("O nome da tabela não pode estar vazio.")
            return False

        colunas = []
        while True:
            opc = input('Digite 1 para adicionar coluna, 2 para finalizar: ').strip()
            if opc == '1':
                coluna = input("Digite o nome da coluna: ").strip()
                tipo = input("Digite o tipo de dado (ex: VARCHAR, INT): ").strip()
                if coluna and tipo:
                    colunas.append(f"{coluna} {tipo}")
                else:
                    print("Nome da coluna e tipo de dado não podem estar vazios.")
            elif opc == '2':
                print("Finalizando a entrada de colunas...")
                break
            else:
                print("Opção inválida. Tente novamente.")

        if not colunas:
            print("Nenhuma coluna foi definida. Tabela não será criada.")
            return False

        query = f"CREATE TABLE {table_name} ({', '.join(colunas)});".format(
            table_name = sql.Identifier()
        )

        curr.execute(query)
        conn.commit()
        print(f"Tabela '{table_name}' criada com sucesso!")
        return True

    except pg2.Error as e:
        print(f"Erro ao criar a tabela no banco de dados: {e}")
        conn.rollback()
        return False

    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return False

    finally:
        curr.close()
        fechar_conexao(conn)
