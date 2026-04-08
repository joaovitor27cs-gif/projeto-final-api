class formula1:
    def __init__ (self,numero_carro,nome_motorista,sigla_motorista,time_motorista,pontos):
        self.numero_carro=numero_carro
        self.nome_motorista=nome_motorista
        self.sigla_motorista=sigla_motorista
        self.time_motorista=time_motorista
        self.pontos=pontos
    def __str__(self):
        return f"nome do motorista: {self.nome_motorista}, sigla do motorista: {self.sigla_motorista}, time:{self.time_motorista}, pontos: {self.pontos}"