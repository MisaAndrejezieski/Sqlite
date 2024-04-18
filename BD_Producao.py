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

    def visualizar_produtos(self):
        self.c.execute("SELECT * FROM produtos")
        return self.c.fetchall()

    def fechar_conexao(self):
        self.conn.close()

# Uso da classe
gerenciador = GerenciadorDeProducao('producao.db')
gerenciador.adicionar_produto('Produto A', 100)
gerenciador.adicionar_produto('Produto B', 200)
produtos = gerenciador.visualizar_produtos()
for produto in produtos:
    print(produto)
gerenciador.fechar_conexao()
