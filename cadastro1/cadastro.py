import bcrypt
from psycopg2 import sql
import psycopg2 as pg2
from database.conexao import criar_conexao, fechar_conexao

def cadastro_usuario(conn):
    emails = []
    senhas = []
    hash_senhas = []
    conn, curr = criar_conexao()
    if not conn or not curr:
        print("Erro no cursour ou na conexão, tente novamento.")
        return False
    try:
        while True:
            opc = input("Digite 1 para adicionar valores à lista, 2 para sair e executar a função: ").strip()
            
            if opc == "1":
                email = input("Adicione o email: ").strip()
                senha = input("Adicione a senha: ").strip()
                if email and senha:
                    emails.append(email)
                    senhas.append(senha)
                else:
                    print("Email e senha não podem estar vazios.")
            
            elif opc == "2":
                print("Saindo da função e executando o programa.")
                break            
            else:
                print("Opção inválida. Digite 1 ou 2.")
        
        for email in emails:
            curr.execute("SELECT email FROM leitor WHERE email = %s", (email,))
            if curr.fetchone():
                print(f"Erro: O email {email} já está cadastrado.")
                emails.remove(email)

        for senha in senhas:
            if not isinstance(senha, str):
                raise ValueError("Todas as senhas devem ser strings.")
            salt = bcrypt.gensalt(rounds=12)
            hash_da_senha = bcrypt.hashpw(senha.encode("UTF-8"), salt)
            hash_senhas.append(hash_da_senha.decode("UTF-8"))
        
        placeholders = sql.SQL(", ").join(sql.SQL("(%s, %s)") for _ in emails)
        query = sql.SQL("INSERT INTO leitor (email, hash_senha) VALUES {values}").format(
            values=placeholders
        )
        values = [(email, hash_senha) for email, hash_senha in zip(emails, hash_senhas)]
        flat_values = [item for sublist in values for item in sublist]
        
        curr.execute(query, flat_values)
        conn.commit()
        print(f"{len(emails)} dados inseridos com sucesso.")
        return True    
    except ValueError as ve:
        print(f"Erro de valor: {ve}")    
    except pg2.Error as e:
        print(f"Erro no banco de dados: {e}")
        conn.rollback()    
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")    
    finally:
        print("Processo finalizado.")
        curr.close()
        fechar_conexao()

