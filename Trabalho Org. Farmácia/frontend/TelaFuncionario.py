import tkinter as tk
from tkinter import messagebox
import sys
import os

# Adiciona o diretório pai ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.FuncionarioBanco import FuncionarioBanco
from frontend.TelaFarmacia import TelaFarmacia
from backend.FarmaciaBanco import FarmaciaBanco

class TelaFuncionario:
    def __init__(self, master):
        self.master = master
        self.master.title("Funcionário")
        self.funcionario_banco = FuncionarioBanco()
        self.new_window = None  # Inicializa como None

        # Campos de entrada
        self.label_username = tk.Label(master, text="Username:")
        self.label_username.grid(row=0, column=0, padx=5, pady=5)
        self.entry_username = tk.Entry(master)
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)

        self.label_senha = tk.Label(master, text="Senha:")
        self.label_senha.grid(row=1, column=0, padx=5, pady=5)
        self.entry_senha = tk.Entry(master, show="*")
        self.entry_senha.grid(row=1, column=1, padx=5, pady=5)

        self.button_login = tk.Button(master, text="Login", command=self.realizar_login)
        self.button_login.grid(row=2, columnspan=2, pady=5)

        self.button_farmacia = tk.Button(master, text="Abrir Farmácia", command=self.abrir_tela_farmacia, state=tk.DISABLED)
        self.button_farmacia.grid(row=3, column=0, padx=5, pady=5)

    def realizar_login(self):
        username = self.entry_username.get().strip()
        senha = self.entry_senha.get().strip()

        if not username or not senha:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
            return

        funcionario = self.funcionario_banco.get_funcionario_by_username(username)

        if funcionario and funcionario.senha == senha:
            messagebox.showinfo("Login", "Login realizado com sucesso!")
            self.button_farmacia.config(state=tk.NORMAL)  # Ativa o botão de Farmácia
            self.limpar_campos()  # Limpa os campos de entrada
        else:
            messagebox.showerror("Erro", "Username ou senha incorretos.")

    def abrir_tela_farmacia(self):
        if self.new_window is None or not self.new_window.winfo_exists():
            self.new_window = tk.Toplevel(self.master)
            TelaFarmacia(self.new_window)
            self.new_window.protocol("WM_DELETE_WINDOW", self.voltar)
        else:
            self.new_window.lift()  # Se a janela já estiver aberta, traz para o foco

    def voltar(self):
        if self.new_window:
            self.new_window.destroy()  # Fecha a tela da farmácia
            self.new_window = None  # Reseta a referência
        self.master.deiconify()  # Mostra a tela de funcionário
        self.limpar_campos()  # Limpa os campos ao voltar

    def limpar_campos(self):
        self.entry_username.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = TelaFuncionario(root)
    root.mainloop()
