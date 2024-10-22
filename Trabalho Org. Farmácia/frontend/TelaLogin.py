import tkinter as tk
from tkinter import messagebox
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.UsuarioBanco import UsuarioBanco
from frontend.TelaFuncionario import TelaFuncionario

def on_entry_click(event, entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, tk.END)  # Apaga a dica
        entry.config(fg='black')  # Altera a cor do texto para preto

def on_focusout(event, entry, placeholder):
    if entry.get() == '':
        entry.insert(0, placeholder)  # Restaura a dica
        entry.config(fg='grey')  # Altera a cor do texto para cinza

def buttonPressUsuario():
    nome = textbNomeUsuario.get()
    senha = textbSenha.get()

    if not nome or nome == "Digite seu nome":
        messagebox.showwarning("Aviso", "Nome não pode estar vazio.")
        return

    if usuario_banco.verifica_usuario(nome, senha):
        messagebox.showwarning("Aviso", "Usuário já cadastrado.")
        return

    try:
        usuario_banco.insert_new_usuario(nome, senha)
        complete_lista_nomes_usuarios()
        messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
        usuario_window.destroy()  # Fecha a tela de cadastro
        abrir_tela_login(nome, senha)  # Abre a tela de login
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao inserir usuário: {e}")

def complete_lista_nomes_usuarios():
    listbox_usuarios.delete(0, tk.END)
    for usuario in usuario_banco.get_all_usuarios():
        listbox_usuarios.insert(tk.END, usuario['nome'])

def abrir_tela_login(nome, senha):
    login_window = tk.Toplevel()
    login_window.geometry("300x200")
    login_window.title("Tela de Login")

    label_nome = tk.Label(login_window, text="Nome:")
    label_nome.pack()

    entry_nome = tk.Entry(login_window)
    entry_nome.pack()
    entry_nome.insert(0, nome)  # Preenche com o nome cadastrado

    label_senha = tk.Label(login_window, text="Senha:")
    label_senha.pack()

    entry_senha = tk.Entry(login_window, show="*")
    entry_senha.pack()

    button_login = tk.Button(login_window, text="Login",
                              command=lambda: realizar_login(entry_nome.get(), entry_senha.get(), login_window))
    button_login.pack()

def realizar_login(nome, senha, login_window):
    if usuario_banco.verifica_usuario(nome, senha):
        messagebox.showinfo("Sucesso", "Login bem-sucedido!")
        login_window.destroy()  # Fecha a tela de login
        abrir_tela_funcionario()  # Abre a tela de funcionários
    else:
        messagebox.showerror("Erro", "Nome ou senha inválidos.")

def abrir_tela_funcionario():
    funcionario_window = tk.Toplevel()
    TelaFuncionario(funcionario_window)  # Abre a tela de funcionários
    funcionario_window.protocol("WM_DELETE_WINDOW", lambda: (funcionario_window.destroy(), root.deiconify()))  # Fecha a tela principal ao fechar

def run_usuario():
    global textbNomeUsuario
    global textbSenha
    global listbox_usuarios
    global usuario_banco
    global usuario_window

    usuario_banco = UsuarioBanco()

    usuario_window = tk.Toplevel()
    usuario_window.geometry("400x300")
    usuario_window.title("Cadastro de Usuários")

    listbox_usuarios = tk.Listbox(usuario_window)
    listbox_usuarios.grid(row=0, column=0)

    button_usuario = tk.Button(usuario_window, text='Cadastrar Usuário', command=buttonPressUsuario)
    button_usuario.grid(row=0, column=1)

    textbNomeUsuario = tk.Entry(usuario_window, fg='grey')
    textbNomeUsuario.grid(row=1, column=0)
    textbNomeUsuario.insert(0, "Digite seu nome")
    textbNomeUsuario.bind('<FocusIn>', lambda event: on_entry_click(event, textbNomeUsuario, "Digite seu nome"))
    textbNomeUsuario.bind('<FocusOut>', lambda event: on_focusout(event, textbNomeUsuario, "Digite seu nome"))

    textbSenha = tk.Entry(usuario_window, show="*")
    textbSenha.grid(row=2, column=0)
    textbSenha.insert(0, "Senha")
    textbSenha.bind('<FocusIn>', lambda event: on_entry_click(event, textbSenha, "Senha"))
    textbSenha.bind('<FocusOut>', lambda event: on_focusout(event, textbSenha, "Senha"))

# Criação da janela principal
root = tk.Tk()
root.geometry("300x200")
root.title("Tela Principal")

button_open_usuario = tk.Button(root, text='Abrir Cadastro de Usuários', command=run_usuario)
button_open_usuario.pack()

# Inicia o loop principal do Tkinter
root.mainloop()
