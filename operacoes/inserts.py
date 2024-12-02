from cadastro1.login import autenticacao, usuario_logado
import psycopg2 as pg2
from psycopg2 import sql
from database.conexao import criar_conexao, fechar_conexao

def inserts(tabela: str, colunas: list):
    insert_values = []
    conn, curr = criar_conexao() 
    if not conn or not curr:
        print("Falha ao criar a conexão. Encerrando o processo.")
        return False
    
    if not autenticacao(usuario_logado):
        print("Usuário não logado.")
        return None
    
    while True:
        try:
            opc = int(input("Digite 1 para adicionar valores à lista, ou 2 para sair: "))
            if opc == 1:
                valores = input(f"Digite os valores para {len(colunas)} colunas, separados por vírgula: ").split(",")
                if len(valores) != len(colunas):
                    print(f"Erro: você deve informar exatamente {len(colunas)} valores.")
                    continue
                insert_values.append(tuple(valores))  
            elif opc == 2:
                if not insert_values:  
                    print("Nenhum valor foi adicionado. Encerrando.")
                    return False
                break
            else:
                print("Escolha uma opção válida.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")

    colunas_sql = sql.SQL(", ").join(sql.Identifier(col) for col in colunas)
    placeholders = sql.SQL(", ").join(sql.Placeholder() for _ in colunas)

    query = sql.SQL("INSERT INTO {tabela} ({colunas}) VALUES ({placeholders})").format(
        tabela=sql.Identifier(tabela),
        colunas=colunas_sql,
        placeholders=placeholders
    )
    
    try:
        for linha in insert_values:
            curr.execute(query, linha)
        conn.commit()
        print(f"{len(insert_values)} linha(s) inserida(s) com sucesso!")
        return True

    except pg2.Error as e:
        print(f"Erro ao inserir dados: {e}")
        conn.rollback() 
        return False
    finally:
        curr.close()
        fechar_conexao(conn)
