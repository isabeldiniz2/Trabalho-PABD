import tkinter as tk
from tkinter import messagebox
import sys
import os

# Adiciona o diretório pai ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.FarmaciaBanco import FarmaciaBanco  # Importação correta

class TelaFarmacia:
    def __init__(self, master):
        self.master = master
        self.master.title("Gerenciador de Farmácias")

        # Inicializa o banco de dados
        self.farmacia_banco = FarmaciaBanco()
        self.farmacia_banco.criar_tabela_farmacia()  # Garante que a tabela exista

        # Criação de widgets
        self.label_nome = tk.Label(master, text="Nome da Farmácia:")
        self.label_nome.grid(row=0, column=0)

        self.entry_nome = tk.Entry(master)
        self.entry_nome.grid(row=0, column=1)

        self.label_crm = tk.Label(master, text="CRM do Funcionário:")
        self.label_crm.grid(row=1, column=0)

        self.entry_crm = tk.Entry(master)
        self.entry_crm.grid(row=1, column=1)

        self.label_cod = tk.Label(master, text="Código do Remédio:")
        self.label_cod.grid(row=2, column=0)

        self.entry_cod = tk.Entry(master)
        self.entry_cod.grid(row=2, column=1)

        self.button_cadastrar = tk.Button(master, text="Cadastrar", command=self.cadastrar_farmacia)
        self.button_cadastrar.grid(row=3, columnspan=2)

        self.listbox_farmacias = tk.Listbox(master)
        self.listbox_farmacias.grid(row=4, columnspan=2)

        # Botão para abrir a tela de remédios
        self.button_remedios = tk.Button(master, text="Acessar Remédios", command=self.abrir_tela_remedio)
        self.button_remedios.grid(row=5, columnspan=2, pady=5)

        self.atualizar_lista_farmacias()

    def cadastrar_farmacia(self):
        nome = self.entry_nome.get()
        crm_funcionario = self.entry_crm.get()
        cod_remedio = self.entry_cod.get()

        if nome and crm_funcionario and cod_remedio:
            if self.farmacia_banco.verifica_farmacia_existente(nome, crm_funcionario, cod_remedio):
                messagebox.showwarning("Aviso", "Farmácia já cadastrada com esses dados.")
                return

            try:
                self.farmacia_banco.inserir_dados(nome, crm_funcionario, cod_remedio)
                self.atualizar_lista_farmacias()
                self.limpar_campos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao cadastrar farmácia: {e}")
        else:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")

    def atualizar_lista_farmacias(self):
        self.listbox_farmacias.delete(0, tk.END)
        try:
            for farmacia in self.farmacia_banco.get_all_farmacias():
                id_farmacia = farmacia[0]
                nome_farmacia = farmacia[1]
                self.listbox_farmacias.insert(tk.END, f"ID: {id_farmacia}, Nome: {nome_farmacia}")
        except Exception as e:
            print(f"Erro ao atualizar lista de farmácias: {e}")

    def abrir_tela_remedio(self):
        # Verifica se uma farmácia foi selecionada
        selected_index = self.listbox_farmacias.curselection()
        if not selected_index:
            messagebox.showwarning("Atenção", "Selecione uma farmácia antes de acessar os remédios.")
            return
        
        # Obtém a farmácia selecionada
        selected_farmacia = self.listbox_farmacias.get(selected_index)
        id_farmacia = selected_farmacia.split(",")[0].split(":")[1].strip()  # Obtém o ID da farmácia selecionada

        # Obtém os dados da farmácia
        farmacia = self.farmacia_banco.get_all_farmacias()
        for f in farmacia:
            if f[0] == int(id_farmacia):
                nome_farmacia = f[1]
                crm_funcionario = f[2]
                cod_remedio = f[3]

                # Verifica se os dados da farmácia estão completos
                if nome_farmacia and crm_funcionario and cod_remedio:
                    if not hasattr(self, 'new_window') or not self.new_window.winfo_exists():
                        self.master.withdraw()
                        from frontend.TelaRemedio import TelaRemedio
                        self.new_window = tk.Toplevel(self.master)
                        TelaRemedio(self.new_window, self)
                        self.new_window.protocol("WM_DELETE_WINDOW", self.voltar)
                    else:
                        self.new_window.deiconify()
                    return
                else:
                    messagebox.showwarning("Atenção", "A farmácia selecionada possui dados incompletos.")
                    return
        
        messagebox.showwarning("Atenção", "A farmácia selecionada não foi encontrada.")

    def voltar(self):
        if hasattr(self, 'new_window') and self.new_window.winfo_exists():
            self.new_window.destroy()
            self.master.deiconify()

    def limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_crm.delete(0, tk.END)
        self.entry_cod.delete(0, tk.END)

# Aplicação Principal
if __name__ == "__main__":
    root = tk.Tk()
    app = TelaFarmacia(root)
    root.mainloop()
