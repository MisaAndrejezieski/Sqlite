import sqlite3

class GerenciadorDeProducao:
    def __init__(self, db_nome):
        self.conn = sqlite3.connect(db_nome)
        self.c = self.conn.cursor()
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                quantidade INTEGER NOT NULL
            )
        ''')

    def adicionar_produto(self, nome, quantidade):
        self.c.execute("INSERT INTO produtos (nome, quantidade) VALUES (?, ?)", (nome, quantidade))
        self.conn.commit()

    def atualizar_produto(self, id, nome, quantidade):
        self.c.execute("UPDATE produtos SET nome = ?, quantidade = ? WHERE id = ?", (nome, quantidade, id))
        self.conn.commit()

    def deletar_produto(self, id):
        self.c.execute("DELETE FROM produtos WHERE id = ?", (id,))
        self.conn.commit()

    def visualizar_produtos(self):
        self.c.execute("SELECT * FROM produtos")
        return self.c.fetchall()

    def fechar_conexao(self):
        self.conn.close()

# Uso da classe
gerenciador = GerenciadorDeProducao('producao.db')

while True:
    print("1. Adicionar produto")
    print("2. Atualizar produto")
    print("3. Deletar produto")
    print("4. Visualizar produtos")
    print("5. Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == '1':
        nome = input("Digite o nome do produto: ")
        quantidade = int(input("Digite a quantidade do produto: "))
        gerenciador.adicionar_produto(nome, quantidade)
    elif opcao == '2':
        id = int(input("Digite o ID do produto que deseja atualizar: "))
        nome = input("Digite o novo nome do produto: ")
        quantidade = int(input("Digite a nova quantidade do produto: "))
        gerenciador.atualizar_produto(id, nome, quantidade)
    elif opcao == '3':
        id = int(input("Digite o ID do produto que deseja deletar: "))
        gerenciador.deletar_produto(id)
    elif opcao == '4':
        produtos = gerenciador.visualizar_produtos()
        for produto in produtos:
            print(produto)
    elif opcao == '5':
        break
    else:
        print("Opção inválida. Tente novamente.")

gerenciador.fechar_conexao()
