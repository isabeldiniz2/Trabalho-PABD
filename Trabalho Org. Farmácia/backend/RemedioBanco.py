import psycopg2
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.Remedio import Remedio

class RemedioBanco:
    def __init__(self):
        self.remedios = []  # Inicializa a lista de remédios
        self.criar_tabela_remedio()  # Certifique-se de que a tabela é criada ao instanciar a classe

    def conectar_db(self):
        return psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="pabd",
            host='localhost',
            port=5432
        )

    def criar_tabela_remedio(self):
        db_connection = self.conectar_db()
        db_cursor = db_connection.cursor()

        create_remedio_table = '''
        CREATE TABLE IF NOT EXISTS Remedio (
            cod INT PRIMARY KEY,
            nome VARCHAR(50) NOT NULL,
            tipo VARCHAR(50),
            quantidade INT
        ); '''
        
        db_cursor.execute(create_remedio_table)
        db_connection.commit()

        # Inserindo um remédio de exemplo apenas uma vez
        try:
            db_cursor.execute("INSERT INTO Remedio (cod, nome, tipo, quantidade) VALUES (%s, %s, %s, %s);", 
                              (1, 'Dipirona', 'Analgésico', 100))
            db_cursor.execute("INSERT INTO Remedio (cod, nome, tipo, quantidade) VALUES (%s, %s, %s, %s);", 
                              (2, 'Ibuprofeno', 'Antiinflamatório', 50))
            db_connection.commit()
        except psycopg2.errors.UniqueViolation:
            print("Os remédios de exemplo já estão inseridos.")

        db_cursor.close()
        db_connection.close()
        print("Tabela Remedio criada e dados inseridos com sucesso.")

    def get_all_remedio(self):
        with self.conectar_db() as db_connection:
            with db_connection.cursor() as db_cursor:
                cmd_sql = "SELECT * FROM Remedio;"
                db_cursor.execute(cmd_sql)
                lista_remedios = db_cursor.fetchall()

                # Limpa a lista antes de preenchê-la novamente
                self.remedios.clear()
                
                # Adicionando remédios do banco de dados
                for codigo, nome, tipo, quantidade in lista_remedios:
                    remedio_arm = Remedio(nome, quantidade, tipo, codigo)
                    self.remedios.append(remedio_arm)

                return self.remedios  # Retorna a lista de remédios

    def insert_new_remedio(self, nome, quantidade, tipo, codigo):
        db_connection = self.conectar_db()
        db_cursor = db_connection.cursor()
        cmd_sql = "INSERT INTO Remedio (cod, nome, quantidade, tipo) VALUES (%s, %s, %s, %s);"

        db_cursor.execute(cmd_sql, (codigo, nome, quantidade, tipo))
        db_connection.commit()
        db_cursor.close()
        db_connection.close()
        print("Novo remédio inserido com sucesso.")

    def verificar_remedio_existente(self, codigo_remedio):
        db_connection = self.conectar_db()
        db_cursor = db_connection.cursor()
        
        cmd_sql = "SELECT COUNT(*) FROM Remedio WHERE cod = %s;"
        db_cursor.execute(cmd_sql, (codigo_remedio,))
        
        existe = db_cursor.fetchone()[0] > 0
        
        db_cursor.close()
        db_connection.close()
        
        return existe

    def get_remedio_por_codigo(self, codigo):
        for remedio in self.remedios:
            if remedio.codigo == codigo:
                return remedio
        return None

    def atualizar_dados(self, codigo, novo_nome, nova_quantidade, novo_tipo):
        db_connection = self.conectar_db()
        db_cursor = db_connection.cursor()
        
        cmd_sql = '''
        UPDATE Remedio
        SET nome = %s, quantidade = %s, tipo = %s
        WHERE cod = %s;
        '''
        
        db_cursor.execute(cmd_sql, (novo_nome, nova_quantidade, novo_tipo, codigo))
        db_connection.commit()
        db_cursor.close()
        db_connection.close()
        print("Dados atualizados na tabela Remedio com sucesso.")

    def remover_remedio(self, codigo):
        db_connection = self.conectar_db()
        db_cursor = db_connection.cursor()
        
        cmd_sql = "DELETE FROM Remedio WHERE cod = %s;"
        db_cursor.execute(cmd_sql, (codigo,))
        db_connection.commit()
        
        db_cursor.close()
        db_connection.close()
        print("Remédio removido com sucesso.")
