class Funcionario:

    def __init__(self):
        self.nome  = None
        self.username  = None
        self.CRM  = None
        self.senha  = None
        

    def __init__(self, nome_farm, username_farm, CRM , senha_farm):
        self.nome  = nome_farm
        self.username  = username_farm
        self.CRM  = CRM
        self.senha  = senha_farm
        
    #Método set_nome: Este método é usado para definir (ou atualizar) o nome do funcionário e farmacia.

    def set_nome(self, nome_farm):
        self.nome_farm = nome_farm
    
    def get_nome(self):
        return self.nome
    
    def get_senha(self):
        return self.senha