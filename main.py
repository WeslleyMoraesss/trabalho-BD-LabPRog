from database.conexao import criar_conexao, fechar_conexao
from cadastro1.cadastro import cadastro_usuario
from cadastro1.login import login_usuario
from operacoes.create import criar_tabela
from operacoes.delete import delete
from operacoes.inserts import inserts
from operacoes.updates import updates
from operacoes.joins import joins
from operacoes.ilike import operador_com_ILIKE
from operacoes.listagem import listag_ord_crescen
from operacoes.selects import selects

usuario_logado = False

def menu_principal():
    print("""
=== Menu Principal ===
1. Cadastro de usuário
2. Login
3. Criar tabela
4. Inserir dados
5. Atualizar dados
6. Deletar dados
7. Consultar dados (SELECT)
8. Consultar com ILIKE
9. Listar dados ordenados
10. Realizar JOIN
0. Sair
    """)


def main():
    conn = criar_conexao() 
    usuario_logado = None  

    while True:
        menu_principal()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastro_usuario(conn)

        elif opcao == "2":
            usuario_logado = login_usuario(conn)

        elif opcao == "3" and usuario_logado:
            criar_tabela()

        elif opcao == "4" and usuario_logado:
            tabela = input("Digite o nome da tabela: ")
            colunas = input("Digite as colunas separadas por vírgula: ").split(",")
            inserts(tabela, colunas)

        elif opcao == "5" and usuario_logado:
            tabela = input("Digite o nome da tabela: ")
            coluna = input("Digite a coluna a ser atualizada e o novo valor (exemplo: nome='novo_valor'): ")
            condicao = input("Digite a condição para atualizar (exemplo: id=1): ")
            updates(tabela, coluna, condicao)

        elif opcao == "6" and usuario_logado:
            tabela = input("Digite o nome da tabela: ")
            condicao = input("Digite a condição para deletar (exemplo: id=1): ")
            delete(tabela, condicao)

        elif opcao == "7" and usuario_logado:
            colunas = input("Digite as colunas a selecionar separadas por vírgula: ").split(",")
            tabela = input("Digite o nome da tabela: ")
            condicao = input("Digite a condição (ou deixe em branco): ")
            selects(colunas, tabela, condicao)

        elif opcao == "8" and usuario_logado:
            tabela = input("Digite o nome da tabela: ")
            termo1 = input("Digite o primeiro termo de busca: ")
            termo2 = input("Digite o segundo termo de busca: ")
            operador_com_ILIKE(tabela, termo1, termo2)

        elif opcao == "9" and usuario_logado:
            colunas = input("Digite as colunas a listar separadas por vírgula: ").split(",")
            tabela = input("Digite o nome da tabela: ")
            coluna_ordem = input("Digite a coluna para ordenação: ")
            listag_ord_crescen(colunas, tabela, coluna_ordem)

        elif opcao == "10" and usuario_logado:
            tabela = input("Digite as colunas a selecionar separadas por vírgula: ")
            comando1 = input("Digite o nome da primeira tabela para o JOIN: ")
            comando2 = input("Digite o nome da segunda tabela para o JOIN: ")
            chave = input("Digite a chave do JOIN (exemplo: t1.id=t2.id_tabela1): ")
            condicao = input("Digite a condição (ou deixe em branco): ")
            joins(tabela, comando1, comando2, chave, condicao)

        elif opcao == "0":
            print("Encerrando o programa...")
            break

        else:
            print("Opção inválida ou operação não permitida sem login.")

    fechar_conexao(conn)  

if __name__ == "__main__":
    main()
