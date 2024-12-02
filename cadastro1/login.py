import bcrypt
import psycopg2
from database.conexao import criar_conexao, fechar_conexao
from main import usuario_logado

def login_usuario():
    conn, curr = criar_conexao()
    if not conn or not curr:
        print("Falha ao criar a conexão. Encerrando o processo.")
        return False
    global usuario_logado
    
    try:
        print("--------------Login------------------")
        email = input("Digite o email: ").strip()
        senha = input("Digite a senha: ").strip()

        busca = "SELECT senha FROM leitor WHERE email = %s"
        curr.execute(busca, (email,))  
        result = curr.fetchone()

        if result is None:
            print("Nenhum email foi encontrado.")
            return False
        
        hash_armazenado = result[0]

        if bcrypt.checkpw(senha.encode("UTF-8"), hash_armazenado.encode("UTF-8")):
            print("Login feito com sucesso!")
            usuario_logado = True
            return True
        else:
            print("Senha incorreta.")
            return False
        
    except psycopg2.Error as e:
        print(f"Erro no banco de dados: {e}")
        return False
    except Exception as e:
        print(f"Erro: {e}")
        return False
    finally:
        curr.close()
        fechar_conexao(conn)  

def autenticacao(usuario_logado):
    if usuario_logado:
        return True
    else:
        return False