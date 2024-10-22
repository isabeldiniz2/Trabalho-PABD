import psycopg2

#o código é uma base sólida para a criação de uma tela de farmácia em uma aplicação.

def conectar_db():
    try:
        return psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="pabd",
            host='localhost',
            port=5432
        )
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
    
#Conexão com o Banco: Tenta se conectar ao banco de dados usando as credenciais fornecidas.
#Tratamento de Erros: Se ocorrer um erro, ele imprime uma mensagem e retorna None.

class FarmaciaBanco:
    def criar_tabela_farmacia(self):
        conn = conectar_db()
        if conn is None:
            return
        
        with conn:
            with conn.cursor() as cursor:
                create_farmacia_table = '''
                CREATE TABLE IF NOT EXISTS Farmacia (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    crm_funcionario INT REFERENCES Funcionario(CRM),
                    cod_remedio INT REFERENCES Remedio(cod)
                );
                '''
                cursor.execute(create_farmacia_table)
                print("Tabela Farmacia criada com sucesso.")
                
    #Uso de Cursor: O uso de with garante que o cursor e a conexão sejam fechados automaticamente após o uso.

    def inserir_dados(self, nome, crm_funcionario, cod_remedio):
        conn = conectar_db()
        if conn is None:
            return
        
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO Farmacia (nome, crm_funcionario, cod_remedio) VALUES (%s, %s, %s);", 
                               (nome, crm_funcionario, cod_remedio))
                print("Dados inseridos na tabela Farmacia com sucesso.")
                
    #Parâmetros de Inserção: Utiliza parâmetros (%s) para evitar injeção de SQL.

    def atualizar_dados(self, id, novo_nome):
        conn = conectar_db()
        if conn is None:
            return
        
        with conn:
            with conn.cursor() as cursor:
                cmd_sql = '''
                UPDATE Farmacia
                SET nome = %s WHERE id = %s;
                '''
                cursor.execute(cmd_sql, (novo_nome, id))
                print("Dados atualizados na tabela Farmacia com sucesso.")

    def get_all_farmacias(self):
        conn = conectar_db()
        if conn is None:
            return []
        
        with conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute("SELECT * FROM Farmacia;")
                    return cursor.fetchall()
                except Exception as e:
                    print(f"Erro ao obter farmácias: {e}")
                    return []
                
    #Recuperação de Dados: Retorna todos os registros da tabela Farmacia. Se houver um erro, imprime uma mensagem e retorna uma lista vazia.
    
    def verificar_farmacia_existente(self, nome, crm_funcionario, cod_remedio):
        conn = conectar_db()
        if conn is None:
            return False
        
        with conn:
            with conn.cursor() as cursor:
                cursor.execute('''SELECT COUNT(*) FROM Farmacia 
                                  WHERE nome = %s AND crm_funcionario = %s AND cod_remedio = %s;''',
                               (nome, crm_funcionario, cod_remedio))
                count = cursor.fetchone()[0]
                return count > 0
            
    #Verificação de Existência: Verifica se uma farmácia com os mesmos dados já existe na tabela, retornando True ou False.
