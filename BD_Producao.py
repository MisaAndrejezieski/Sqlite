import sqlite3
import tkinter as tk
from tkinter import messagebox

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
        try:
            self.c.execute("INSERT INTO produtos (nome, quantidade) VALUES (?, ?)", (nome, quantidade))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            return False

    def atualizar_produto(self, id, nome, quantidade):
        try:
            self.c.execute("UPDATE produtos SET nome = ?, quantidade = ? WHERE id = ?", (nome, quantidade, id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            return False

    def deletar_produto(self, id):
        try:
            self.c.execute("DELETE FROM produtos WHERE id = ?", (id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            return False

    def visualizar_produtos(self):
        self.c.execute("SELECT * FROM produtos")
        return self.c.fetchall()

    def fechar_conexao(self):
        self.conn.close()

class Aplicativo:
    def __init__(self, gerenciador):
        self.gerenciador = gerenciador
        self.root = tk.Tk()
        self.root.title("Gerenciador de Produção")

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.label_nome = tk.Label(self.frame, text="Nome do Produto:")
        self.label_nome.pack(side=tk.LEFT)
        self.entry_nome = tk.Entry(self.frame)
        self.entry_nome.pack(side=tk.LEFT)

        self.label_quantidade = tk.Label(self.frame, text="Quantidade:")
        self.label_quantidade.pack(side=tk.LEFT)
        self.entry_quantidade = tk.Entry(self.frame)
        self.entry_quantidade.pack(side=tk.LEFT)

        self.button_adicionar = tk.Button(self.frame, text="Adicionar Produto", command=self.adicionar_produto)
        self.button_adicionar.pack(side=tk.LEFT)

        self.button_atualizar = tk.Button(self.frame, text="Atualizar Produto", command=self.atualizar_produto)
        self.button_atualizar.pack(side=tk.LEFT)

        self.button_deletar = tk.Button(self.frame, text="Deletar Produto", command=self.deletar_produto)
        self.button_deletar.pack(side=tk.LEFT)

        self.button_visualizar = tk.Button(self.frame, text="Visualizar Produtos", command=self.visualizar_produtos)
        self.button_visualizar.pack(side=tk.LEFT)

    def adicionar_produto(self):
        nome = self.entry_nome.get()
        quantidade = int(self.entry_quantidade.get())
        if self.gerenciador.adicionar_produto(nome, quantidade):
            messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
        else:
            messagebox.showerror("Erro", "Ocorreu um erro ao adicionar o produto.")

    def atualizar_produto(self):
        id = int(input("Digite o ID do produto que deseja atualizar: "))
        nome = self.entry_nome.get()
        quantidade = int(self.entry_quantidade.get())
        if self.gerenciador.atualizar_produto(id, nome, quantidade):
            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
        else:
            messagebox.showerror("Erro", "Ocorreu um erro ao atualizar o produto.")

    def deletar_produto(self):
        id = int(input("Digite o ID do produto que deseja deletar: "))
        if self.gerenciador.deletar_produto(id):
            messagebox.showinfo("Sucesso", "Produto deletado com sucesso!")
        else:
            messagebox.showerror("Erro", "Ocorreu um erro ao deletar o produto.")

    def visualizar_produtos(self):
        produtos = self.gerenciador.visualizar_produtos()
        messagebox.showinfo("Produtos", "\n".join(map(str, produtos)))

    def run(self):
        self.root.mainloop()

gerenciador = GerenciadorDeProducao('producao.db')
app = Aplicativo(gerenciador)
app.run()
gerenciador.fechar_conexao()
