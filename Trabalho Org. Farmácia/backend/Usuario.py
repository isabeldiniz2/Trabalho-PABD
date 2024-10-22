import psycopg2
# Função para criar a tabela de usuários
class Usuario:
    def __init__(self):
        self.conectar_db()

    def criar_tabela():
        try:
            conn = psycopg2.connect(
                dbname='postgres',
                user='postgres',
                password='pabd',
                host='localhost',
                port='5432'
            )
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id SERIAL PRIMARY KEY,
                    nome TEXT NOT NULL UNIQUE,
                    senha TEXT NOT NULL
                )
            ''')
            conn.commit()
            print("Tabela criada com sucesso.")

        except Exception as e:
            print(f"Erro ao criar a tabela: {e}")
        finally:
            cursor.close()
            conn.close()

    def inserir_usuario(nome, senha):
        try:
            conn = psycopg2.connect(
                dbname='postgres',
                user='postgres',
                password='pabd',
                host='localhost',
                port='5432'
            )
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO usuarios (nome, senha)
                VALUES (%s, %s)
                ON CONFLICT (nome) DO NOTHING
            ''', (nome, senha))
            
            conn.commit()
            if cursor.rowcount > 0:
                print("Usuário inserido com sucesso.")
            else:
                print(f"Erro: O usuário '{nome}' já existe.")

        except Exception as e:
            print(f"Erro ao inserir usuário: {e}")
        finally:
            cursor.close()
            conn.close()

    def listar_usuarios():
        try:
            conn = psycopg2.connect(
                dbname='postgres',
                user='postgres',
                password='pabd',
                host='localhost',
                port='5432'
            )
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM usuarios')
            usuarios = cursor.fetchall()

            return usuarios

        except Exception as e:
            print(f"Erro ao listar usuários: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    # Cria a tabela
    criar_tabela()

    # Insere alguns usuários
    inserir_usuario('Alice', '123')
    inserir_usuario('Bob', '456')

# Lista os usuários
    usuarios = listar_usuarios()
    for usuario in usuarios:
        print(usuario)
