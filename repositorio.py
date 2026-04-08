import sqlite3
import requests
import classe

class Repositorio:
    def __init__(self):
        self.conexao = sqlite3.connect("banco.db")
        self.tabela()
        self.verificar_coluna_pontos()

    # -CRIAÇÃO DA TABELA 
    def tabela(self):
        cursor = self.conexao.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS motoristas(
            numero_carro INTEGER PRIMARY KEY,
            nome_motorista TEXT NOT NULL,
            sigla_motorista TEXT NOT NULL,
            time_motorista TEXT NOT NULL,
            pontos INTEGER DEFAULT 0
        );
        """)
        self.conexao.commit()

    # -COLUNA PONTOS
    def verificar_coluna_pontos(self):
        cursor = self.conexao.cursor()
        cursor.execute("PRAGMA table_info(motoristas)")
        colunas = [coluna[1] for coluna in cursor.fetchall()]
        if "pontos" not in colunas:
            cursor.execute("ALTER TABLE motoristas ADD COLUMN pontos INTEGER DEFAULT 0")
            self.conexao.commit()

    # -CREATE
    def cadastrar_motorista(self, numero, nome, sigla, time, pontos=0):
        try:
            cursor = self.conexao.cursor()
            cursor.execute("""
            INSERT INTO motoristas 
            (numero_carro, nome_motorista, sigla_motorista, time_motorista, pontos)
            VALUES (?, ?, ?, ?, ?)
            """, (numero, nome, sigla, time, pontos))
            self.conexao.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    # -ORDENADO POR PONTOS
    def listar_motoristas(self):
        cursor = self.conexao.cursor()
        cursor.execute("""
        SELECT * FROM motoristas 
        ORDER BY pontos DESC, nome_motorista ASC
        """)
        return cursor.fetchall()

    # -ORDENAR POR NÚMERO
    def buscar_por_numero(self, numero):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT * FROM motoristas WHERE numero_carro = ?", (numero,))
        return cursor.fetchone()

    # -Atualizar
    def atualizar_motorista(self, numero, nome, sigla, time, pontos):
        cursor = self.conexao.cursor()
        cursor.execute("""
        UPDATE motoristas 
        SET nome_motorista = ?, 
            sigla_motorista = ?, 
            time_motorista = ?, 
            pontos = ?
        WHERE numero_carro = ?
        """, (nome, sigla, time, pontos, numero))
        self.conexao.commit()
        return cursor.rowcount > 0

    # -DELETE
    def remover_motorista(self, numero):
        cursor = self.conexao.cursor()
        cursor.execute("DELETE FROM motoristas WHERE numero_carro = ?", (numero,))
        self.conexao.commit()
        return cursor.rowcount > 0

    # -API
    def importar_api(self):
        url = "https://api.openf1.org/v1/drivers"
        try:
            resposta = requests.get(url)
            if resposta.status_code != 200:
                print("Erro na API:", resposta.status_code)
                return -1
            dados = resposta.json()
            count = 0
            for p in dados:
                numero = p.get("driver_number")
                nome = p.get("full_name")
                sigla = p.get("name_acronym")
                equipe = p.get("team_name")
                if numero and nome and sigla and equipe:
                    if self.cadastrar_motorista(numero, nome, sigla, equipe, 0):
                        count += 1
            return count
        except requests.exceptions.RequestException as e:
            print("Erro de conexão:", e)
            return -1
        except Exception as e:
            print("Erro:", e)
            return -1
