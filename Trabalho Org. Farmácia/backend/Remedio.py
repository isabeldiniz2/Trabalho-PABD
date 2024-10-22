class Remedio:

    def __init__(self, nome, quantidade, tipo, codigo):
        self.nome = nome
        self.tipo = tipo
        self.quantidade = quantidade
        self.codigo = codigo

    def __str__(self):
        return f"Remédio: {self.nome}, Tipo: {self.tipo}, Quantidade: {self.quantidade}, Código: {self.codigo}"
    
    #Este método retorna uma string que representa o objeto de forma legível.
    #Ele é chamado automaticamente quando você usa print() em um objeto Remedio, facilitando a visualização das informações do remédio.
    
    def __repr__(self):
        return self.__str__()
    
    #Neste caso, ele retorna a mesma string que __str__, o que é útil para garantir que ambas as representações sejam consistentes.
    
    def get_nome(self):
        return self.nome
    #este é um método getter que permite acessar o nome do remédio de fora da classe. Ele retorna o valor do atributo nome.
