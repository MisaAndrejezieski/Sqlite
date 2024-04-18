import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

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
        style = ttk.Style()
        style.theme_use('clam')

        self.frame_botoes = ttk.Frame(self.root)
        self.frame_botoes.pack(side=tk.TOP)
        #self.frame = ttk.Frame(self.root)--troca pelo código acima:
        #self.frame.pack()

# move todos os widgets relacionados aos botões e campos de entrada para o novo frame.
        self.label_nome = ttk.Label(self.frame_botoes, text="Nome do Produto:")
        self.label_nome.pack(side=tk.LEFT)
        self.entry_nome = ttk.Entry(self.frame_botoes)
        self.entry_nome.pack(side=tk.LEFT)

        self.label_quantidade = ttk.Label(self.frame_botoes, text="Quantidade:")
        self.label_quantidade.pack(side=tk.LEFT)
        self.entry_quantidade = ttk.Entry(self.frame_botoes)
        self.entry_quantidade.pack(side=tk.LEFT)

        self.label_id = ttk.Label(self.frame_botoes, text="ID do Produto (para atualizar/deletar):")
        self.label_id.pack(side=tk.LEFT)
        self.entry_id = ttk.Entry(self.frame_botoes)
        self.entry_id.pack(side=tk.LEFT)

        self.button_adicionar = ttk.Button(self.frame_botoes, text="Adicionar Produto", command=self.adicionar_produto)
        self.button_adicionar.pack(side=tk.LEFT)

        self.button_atualizar = ttk.Button(self.frame_botoes, text="Atualizar Produto", command=self.atualizar_produto)
        self.button_atualizar.pack(side=tk.LEFT)

        self.button_deletar = ttk.Button(self.frame_botoes, text="Deletar Produto", command=self.deletar_produto)
        self.button_deletar.pack(side=tk.LEFT)

        self.button_visualizar = ttk.Button(self.frame_botoes, text="Visualizar Produtos", command=self.visualizar_produtos)
        self.button_visualizar.pack(side=tk.LEFT)


        #self.listbox = tk.Listbox(self.root)
        #self.listbox.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        #self.listbox = tk.Listbox(self.root)
        #self.listbox.pack()

    def adicionar_produto(self):
        nome = self.entry_nome.get()
        quantidade = int(self.entry_quantidade.get())
        if self.gerenciador.adicionar_produto(nome, quantidade):
            messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
        else:
            messagebox.showerror("Erro", "Ocorreu um erro ao adicionar o produto.")

    def atualizar_produto(self):
        id = int(self.entry_id.get())
        nome = self.entry_nome.get()
        quantidade = int(self.entry_quantidade.get())
        if self.gerenciador.atualizar_produto(id, nome, quantidade):
            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
        else:
            messagebox.showerror("Erro", "Ocorreu um erro ao atualizar o produto.")

    def deletar_produto(self):
        id = int(self.entry_id.get())
        if self.gerenciador.deletar_produto(id):
            messagebox.showinfo("Sucesso", "Produto deletado com sucesso!")
        else:
            messagebox.showerror("Erro", "Ocorreu um erro ao deletar o produto.")

    def visualizar_produtos(self):
        self.listbox.delete(0, tk.END)
        produtos = self.gerenciador.visualizar_produtos()
        for produto in produtos:
            id, nome, quantidade = produto
        self.listbox.insert(tk.END, f"ID: {id}, Nome: {nome}, Quantidade: {quantidade}")

    
    def run(self):
        self.root.mainloop()

gerenciador = GerenciadorDeProducao('producao.db')
app = Aplicativo(gerenciador)
app.run()
gerenciador.fechar_conexao()
