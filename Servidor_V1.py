import os
import rpyc
from rpyc.utils.server import ThreadedServer
from collections import defaultdict

DIRETORIO_ARQUIVOS = "Servidor_Arquivos"
if not os.path.exists(DIRETORIO_ARQUIVOS):
    os.makedirs(DIRETORIO_ARQUIVOS)
ARQUIVO_REGISTROS = "registros.txt"

class ServicoArquivos(rpyc.Service):
    def __init__(self):
        self.registro_interesses = defaultdict(list)
        self.carregar_registros()

    def on_connect(self, conexao):
        print("Cliente conectado")

    def on_disconnect(self, conexao):
        print("Cliente desconectado")

    def exposed_registrar_cliente(self, nome_cliente):
        print(f"Cliente registrado: {nome_cliente}")
        return nome_cliente

    def exposed_listar_arquivos(self):
        return os.listdir(DIRETORIO_ARQUIVOS)

    def exposed_enviar_arquivo(self, nome_arquivo, dados_arquivo):
        caminho_arquivo = os.path.join(DIRETORIO_ARQUIVOS, nome_arquivo)
        with open(caminho_arquivo, 'wb') as f:
            f.write(dados_arquivo)
        print(f"{nome_arquivo} foi enviado com sucesso!")
        return f"{nome_arquivo} foi enviado com sucesso!"

    def exposed_baixar_arquivo(self, nome_cliente, nome_arquivo, host, porta):
        caminho_arquivo = os.path.join(DIRETORIO_ARQUIVOS, nome_arquivo)
        if not os.path.exists(caminho_arquivo):
            print(f"Arquivo {nome_arquivo} não encontrado. Registrando interesse para {nome_cliente}.")
            self.registrar_interesse(nome_cliente, nome_arquivo, host, porta)
            return None
        
        with open(caminho_arquivo, 'rb') as f:
            dados_arquivo = f.read()
        return dados_arquivo

    def exposed_verificar_interesses(self, nome_cliente):
        arquivos_disponiveis = set(os.listdir(DIRETORIO_ARQUIVOS))
        interesses_cliente = []
        for nome_arquivo, clientes in list(self.registro_interesses.items()):
            for cliente in clientes:
                if cliente['nome'] == nome_cliente and nome_arquivo in arquivos_disponiveis:
                    interesses_cliente.append(nome_arquivo)
        
        return interesses_cliente

    def exposed_remover_interesse(self, nome_cliente, nome_arquivo):
        if nome_arquivo in self.registro_interesses:
            self.registro_interesses[nome_arquivo] = [cliente for cliente in self.registro_interesses[nome_arquivo] if cliente['nome'] != nome_cliente]
            if not self.registro_interesses[nome_arquivo]:
                self.registro_interesses.pop(nome_arquivo)
            self.atualizar_arquivo_registros()

    def registrar_interesse(self, nome_cliente, nome_arquivo, host, porta):
        self.registro_interesses[nome_arquivo].append({"nome": nome_cliente, "host": host, "porta": int(porta)})
        self.atualizar_arquivo_registros()

    def carregar_registros(self):
        if os.path.exists(ARQUIVO_REGISTROS):
            with open(ARQUIVO_REGISTROS, 'r') as registros:
                for linha in registros:
                    nome_cliente, nome_arquivo, host, porta = linha.strip().split(',')
                    self.registro_interesses[nome_arquivo].append({"nome": nome_cliente, "host": host, "porta": int(porta)})

    def atualizar_arquivo_registros(self):
        with open(ARQUIVO_REGISTROS, 'w') as registros:
            for nome_arquivo, clientes in self.registro_interesses.items():
                for cliente in clientes:
                    registros.write(f"{cliente['nome']},{nome_arquivo},{cliente['host']},{cliente['porta']}\n")

if __name__ == "__main__":
    servidor = ServicoArquivos()
    servidor_thread = ThreadedServer(servidor, port=8080)
    print("Servidor iniciado. Aguardando conexões...")
    servidor_thread.start()