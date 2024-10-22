import tkinter as tk
import sys
import os
from tkinter import messagebox

# Adiciona o diretório pai ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.RemedioBanco import RemedioBanco
from frontend.TelaFarmacia import TelaFarmacia

class TelaRemedio:
    def __init__(self, master, tela_farmacia):
        self.master = master
        self.tela_farmacia = tela_farmacia
        self.master.title("Gerenciador de Remédios")
        self.remedio_banco = RemedioBanco()

        self.criar_widgets()
        self.atualizar_lista_remedios()

    def criar_widgets(self):
        # Labels e Entradas
        labels = ["Nome do Remédio:", "Tipo:", "Quantidade:", "Código:"]
        self.entries = []

        for i, label_text in enumerate(labels):
            label = tk.Label(self.master, text=label_text)
            label.grid(row=i, column=0)
            entry = tk.Entry(self.master)
            entry.grid(row=i, column=1)
            self.entries.append(entry)

        # Botões
        botoes = [
            ("Adicionar Remédio", self.adicionar_remedio),
            ("Atualizar Remédio", self.atualizar_remedio),
            ("Remover Remédio", self.remover_remedio),
            ("Ler Remédio", self.ler_remedio),
            ("Finalizar Sessão", self.finalizar_sessao),
            ("Voltar", self.voltar)
        ]

        for i, (texto, comando) in enumerate(botoes):
            button = tk.Button(self.master, text=texto, command=comando)
            button.grid(row=len(labels) + i, columnspan=2)

        self.listbox_remedios = tk.Listbox(self.master)
        self.listbox_remedios.grid(row=len(labels) + len(botoes), columnspan=2)

    def adicionar_remedio(self):
        nome, tipo, quantidade, codigo = [entry.get() for entry in self.entries]
        
        if self.valida_inputs(nome, tipo, quantidade, codigo):
            self.remedio_banco.insert_new_remedio(nome, int(quantidade), tipo, int(codigo))
            self.atualizar_lista_remedios()
            self.limpar_campos()
            messagebox.showinfo("Sucesso", "Remédio adicionado com sucesso!")
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos corretamente.")

    def atualizar_remedio(self):
        if self.listbox_remedios.curselection():
            codigo = self.get_selected_codigo()
            novo_nome, novo_tipo, nova_quantidade, _ = [entry.get() for entry in self.entries]

            if self.valida_inputs(novo_nome, novo_tipo, nova_quantidade, str(codigo)):
                self.remedio_banco.atualizar_dados(codigo, novo_nome, int(nova_quantidade), novo_tipo)
                self.atualizar_lista_remedios()
                self.limpar_campos()
                messagebox.showinfo("Sucesso", "Remédio atualizado com sucesso!")
            else:
                messagebox.showerror("Erro", "Por favor, preencha todos os campos corretamente.")
        else:
            messagebox.showwarning("Aviso", "Selecione um remédio para atualizar.")

    def remover_remedio(self):
        if self.listbox_remedios.curselection():
            codigo = self.get_selected_codigo()
            self.remedio_banco.remover_remedio(codigo)
            self.atualizar_lista_remedios()
            self.limpar_campos()
            messagebox.showinfo("Sucesso", "Remédio removido com sucesso!")
        else:
            messagebox.showwarning("Aviso", "Selecione um remédio para remover.")

    def finalizar_sessao(self):
        self.master.destroy()

    def atualizar_lista_remedios(self):
        self.listbox_remedios.delete(0, tk.END)
        for remedio in self.remedio_banco.get_all_remedio():
            self.listbox_remedios.insert(tk.END, f"Codigo: {remedio.codigo}, Nome: {remedio.nome}, Tipo: {remedio.tipo}, Qtd: {remedio.quantidade}")

    def get_selected_codigo(self):
        selected_index = self.listbox_remedios.curselection()
        if selected_index:
            return int(self.listbox_remedios.get(selected_index).split(",")[0].split(":")[1].strip())
        return None

    def limpar_campos(self):
        for entry in self.entries:
            entry.delete(0, tk.END)

    def ler_remedio(self):
        if self.listbox_remedios.curselection():
            codigo = self.get_selected_codigo()
            remedio = self.remedio_banco.get_remedio_por_codigo(codigo)

            if remedio:
                detalhes = (f"Código: {remedio.codigo}\n"
                            f"Nome: {remedio.nome}\n"
                            f"Tipo: {remedio.tipo}\n"
                            f"Quantidade: {remedio.quantidade}")
                messagebox.showinfo("Detalhes do Remédio", detalhes)
            else:
                messagebox.showwarning("Aviso", "Remédio não encontrado.")
        else:
            messagebox.showwarning("Aviso", "Selecione um remédio para visualizar os detalhes.")

    def valida_inputs(self, nome, tipo, quantidade, codigo):
        return nome and tipo and quantidade.isdigit() and codigo.isdigit()

    def voltar(self):
        self.master.destroy()
        self.tela_farmacia.master.deiconify()

# Para iniciar a tela
if __name__ == "__main__":
    root = tk.Tk()
    TelaRemedio(root, tela_farmacia=None)
    root.mainloop()
