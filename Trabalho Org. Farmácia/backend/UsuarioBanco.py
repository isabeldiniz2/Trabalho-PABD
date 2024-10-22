class UsuarioBanco:
    def __init__(self):
        self.usuarios = []  # Lista para armazenar usuários

    def insert_new_usuario(self, nome, senha):
        # Verifica se o usuário já existe antes de inserir
        if self.verifica_usuario(nome, senha):
            raise Exception(f"O usuário '{nome}' já existe.")
        
        usuario = {
            'nome': nome,
            'senha': senha
        }
        self.usuarios.append(usuario)

    def get_all_usuarios(self):
        return self.usuarios

    def verifica_usuario(self, nome, senha):
        # Verifica se o nome e senha correspondem a um usuário cadastrado
        for usuario in self.usuarios:
            if usuario['nome'] == nome and usuario['senha'] == senha:
                return True
        return False
