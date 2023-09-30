import tkinter as tk
from tkinter import ttk, messagebox

class Livro:
    def __init__(self, livro_id, titulo, autor, ano_publicacao):
        self.livro_id = livro_id
        self.titulo = titulo
        self.autor = autor
        self.ano_publicacao = ano_publicacao
        self.__status = "disponível"

    def __set_status(self, status):
        if status in ["disponível", "emprestado"]:
            self.__status = status

    def emprestar(self):
        if self.__status == "disponível":
            self.__set_status("emprestado")
            return True
        else:
            return False

    def devolver(self):
        if self.__status == "emprestado":
            self.__set_status("disponível")
            return True
        else:
            return False

    def __str__(self):
        return f"ID: {self.livro_id}, Título: {self.titulo}, Autor: {self.autor}, Ano: {self.ano_publicacao}, Status: {self.__status}"


class LivroImpresso(Livro):
    def __init__(self, livro_id, titulo, autor, ano_publicacao, numero_paginas):
        super().__init__(livro_id, titulo, autor, ano_publicacao)
        self.numero_paginas = numero_paginas


class LivroDigital(Livro):
    def __init__(self, livro_id, titulo, autor, ano_publicacao, formato):
        super().__init__(livro_id, titulo, autor, ano_publicacao)
        self.formato = formato


class Membro:
    def __init__(self, membro_id, nome, endereco, telefone):
        self.membro_id = membro_id
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.livros_emprestados = []

    def emprestar_livro(self, livro):
        if livro.emprestar():
            self.livros_emprestados.append(livro)
            return True
        else:
            return False

    def devolver_livro(self, livro):
        if livro in self.livros_emprestados and livro.devolver():
            self.livros_emprestados.remove(livro)
            return True
        else:
            return False

    def __str__(self):
        return f"ID: {self.membro_id}, Nome: {self.nome}, Livros Emprestados: {[livro.titulo for livro in self.livros_emprestados]}"


class Biblioteca:
    def __init__(self):
        self.livros = []
        self.membros = []

    def adicionar_livro(self, livro):
        self.livros.append(livro)

    def remover_livro(self, livro_id):
        livro = next((l for l in self.livros if l.livro_id == livro_id), None)
        if livro:
            self.livros.remove(livro)
            return True
        return False

    def adicionar_membro(self, membro):
        self.membros.append(membro)

    def remover_membro(self, membro_id):
        membro = next((m for m in self.membros if m.membro_id == membro_id), None)
        if membro:
            self.membros.remove(membro)
            return True
        return False

    def listar_livros(self):
        for livro in self.livros:
            print(livro)

    def listar_membros(self):
        for membro in self.membros:
            print(membro)


# Exemplo de uso
biblioteca = Biblioteca()

livro_impresso = LivroImpresso(1, "O Senhor dos Anéis", "J.R.R. Tolkien", 1954, 1000)
livro_digital = LivroDigital(2, "Duna", "Frank Herbert", 1965, "PDF")

biblioteca.adicionar_livro(livro_impresso)
biblioteca.adicionar_livro(livro_digital)

membro = Membro(1, "Alice", "Rua A, 123", "111-2222")

biblioteca.adicionar_membro(membro)

membro.emprestar_livro(livro_impresso)

biblioteca.listar_livros()
biblioteca.listar_membros()


class App:

    def __init__(self, root):
        self.biblioteca = Biblioteca()

        self.root = root
        self.root.title('Sistema de Biblioteca')

        self.tree = ttk.Treeview(self.root, columns=('ID', 'Título', 'Autor', 'Ano', 'Status'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Título', text='Título')
        self.tree.heading('Autor', text='Autor')
        self.tree.heading('Ano', text='Ano')
        self.tree.heading('Status', text='Status')
        self.tree.pack(pady=20)

        self.add_button = ttk.Button(self.root, text='Adicionar Livro', command=self.add_book_popup)
        self.add_button.pack()

        self.remove_button = ttk.Button(self.root, text='Remover Livro', command=self.remove_book)
        self.remove_button.pack()

        self.update_list()

    def add_book_popup(self):
        popup = tk.Toplevel()
        popup.title("Adicionar Livro")

        ttk.Label(popup, text="Título:").grid(row=0, column=0, padx=10, pady=10)
        titulo_entry = ttk.Entry(popup)
        titulo_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(popup, text="Autor:").grid(row=1, column=0, padx=10, pady=10)
        autor_entry = ttk.Entry(popup)
        autor_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(popup, text="Ano de Publicação:").grid(row=2, column=0, padx=10, pady=10)
        ano_entry = ttk.Entry(popup)
        ano_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(popup, text="Número de Páginas:").grid(row=3, column=0, padx=10, pady=10)
        paginas_entry = ttk.Entry(popup)
        paginas_entry.grid(row=3, column=1, padx=10, pady=10)

        def on_add():

            try:
                titulo = titulo_entry.get()
                autor = autor_entry.get()
                ano = int(ano_entry.get())
                paginas = int(paginas_entry.get())

                if titulo and autor:
                    livro = LivroImpresso(len(self.biblioteca.livros) + 1, titulo, autor, ano, paginas)
                    self.biblioteca.adicionar_livro(livro)
                    self.update_list()
                    popup.destroy()  # Fecha o popup
                else:
                    messagebox.showerror("Erro", "Título e Autor são obrigatórios!")
            except ValueError:
                messagebox.showerror("Erro", "Ano e número de páginas devem ser números!")

        add_button = ttk.Button(popup, text="Adicionar", command=on_add)
        add_button.grid(row=4, column=0, columnspan=2, pady=20)

    def remove_book(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showerror("Erro", "Selecione um livro para remover!")
            return
        for item in selected_items:
            livro_id = self.tree.item(item)['values'][0]
            self.biblioteca.remover_livro(livro_id)
        self.update_list()

    def update_list(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for livro in self.biblioteca.livros:
            self.tree.insert('', 'end', values=(
            livro.livro_id, livro.titulo, livro.autor, livro.ano_publicacao, livro._Livro__status))


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()


