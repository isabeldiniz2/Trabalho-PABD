import psycopg2
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

#sys e os: Usadas para manipulação do sistema de arquivos e configuração de caminhos.
#Adiciona o diretório pai ao sys.path para importar a classe Funcionario de um módulo específico.

from backend.Funcionario import Funcionario

class FuncionarioBanco:
    def __init__(self):
        pass
    
#O construtor está vazio por enquanto, mas pode ser expandido no futuro para incluir configurações adicionais.Servindo para ser chamado de classe e 
#estabelecer suas devidas funções na tabela funcionario
    
    def conectar_db(self):
        return psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='pabd',
            host='localhost',
            port=5432
        )

    def criar_tabela_funcionario(self):
        db_connection = self.conectar_db()
        db_cursor = db_connection.cursor()
        
        create_funcionario_table = '''
        CREATE TABLE IF NOT EXISTS Funcionario (
            CRM int PRIMARY KEY,
            nome VARCHAR(50) NOT NULL,
            username VARCHAR(50),
            senha VARCHAR(60)
        ); '''
        
        try:
            db_cursor.execute(create_funcionario_table)  
            db_connection.commit()

            # Inserindo funcionários de exemplo
            self.inserir_dados(151515, 'Belzinha', 'beldiniz', '1234589')
            self.inserir_dados(345678, 'Raul', 'raulxl', '12345')

            print("Tabela Funcionario criada e dados inseridos com sucesso.")
        except Exception as e:
            print(f"Erro ao criar tabela ou inserir dados: {e}")
        finally:
            db_cursor.close()
            db_connection.close()
    
    def inserir_dados(self, crm, nome, username, senha):
        db_connection = self.conectar_db()
        db_cursor = db_connection.cursor()
        
        cmd_sql = '''
        INSERT INTO Funcionario (CRM, nome, username, senha) VALUES (%s, %s, %s, %s);
        '''
        
        #try: Executa o código que pode gerar uma exceção.
        #except: Captura e lida com a exceção, imprimindo uma mensagem de erro.
        #finally: Executa sempre, garantindo que os recursos (como cursores e conexões) sejam fechados.
        
        try:
            db_cursor.execute(cmd_sql, (crm, nome, username, senha))
            db_connection.commit()
            print("Funcionário adicionado com sucesso.")
        except Exception as e:
            print(f"Erro ao adicionar funcionário: {e}")
        finally:
            db_cursor.close()
            db_connection.close()

    def atualizar_dados(self, novo_nome, novo_username, nova_senha, crm):
        db_connection = self.conectar_db()
        db_cursor = db_connection.cursor()
        
        cmd_sql = '''
        UPDATE Funcionario
        SET nome = %s, username = %s, senha = %s
        WHERE CRM = %s;
        '''
        
        db_cursor.execute(cmd_sql, (novo_nome, novo_username, nova_senha, crm))
        db_connection.commit()
        db_cursor.close()
        db_connection.close()
        print("Dados atualizados na tabela Funcionario com sucesso.")

    def remover_funcionario(self, crm):
        db_connection = self.conectar_db()
        db_cursor = db_connection.cursor()
        
        cmd_sql = '''
        DELETE FROM Funcionario WHERE CRM = %s;
        '''
        
        try:
            db_cursor.execute(cmd_sql, (crm,))
            db_connection.commit()
            print("Funcionário removido com sucesso.")
        except Exception as e:
            print(f"Erro ao remover funcionário: {e}")
        finally:
            db_cursor.close()
            db_connection.close()

    def get_funcionario_by_username(self, username_farm):
        db_connection = None
        db_cursor = None
        func = None
        
        try:    
            db_connection = self.conectar_db()
            db_cursor = db_connection.cursor()
            cmd_sql = "SELECT * FROM Funcionario WHERE username = %s;"
            db_cursor.execute(cmd_sql, (username_farm,))
            lista_exibir = db_cursor.fetchone()
            
            if lista_exibir is not None:
                nome_funcionario = lista_exibir[1]
                username_funcionario = lista_exibir[2]
                id_funcionario = lista_exibir[0]
                senha_funcionario = lista_exibir[3]
                func = Funcionario(nome_funcionario, username_funcionario, id_funcionario, senha_funcionario)
                print(lista_exibir)
            else:
                func = None

        except Exception as e:
            print(f"Erro ao consultar o funcionário: {e}")
        finally:
            db_cursor.close()
            db_connection.close()
            return func
        
    #Busca um funcionário pelo username e retorna um objeto Funcionario.
        
    def get_all_funcionarios(self):
        db_connection = self.conectar_db()
        db_cursor = db_connection.cursor()
        funcionarios = []

        try:
            db_cursor.execute("SELECT * FROM Funcionario;")
            funcionarios = db_cursor.fetchall()  # Obtém todos os registros
        except Exception as e:
            print(f"Erro ao obter funcionários: {e}")
        finally:
            db_cursor.close()
            db_connection.close()
        
        return funcionarios
    #Obtém todos os registros da tabela Funcionario e os retorna como uma lista.
