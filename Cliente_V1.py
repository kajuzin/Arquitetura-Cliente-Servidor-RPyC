import rpyc
import os

class ClienteDeArquivos(rpyc.Service):
    def __init__(self, nome_cliente, servidor="localhost", porta=8080):

        self.nome_cliente = nome_cliente
        self.servidor = servidor
        self.porta = porta
        self.conexao = rpyc.connect(servidor, porta)
        self.conexao.root.registrar_cliente(nome_cliente)
        print(f"Cliente {nome_cliente} conectado ao servidor")

    def listar_arquivos(self):
        return self.conexao.root.listar_arquivos()
    
    def enviar_arquivo(self, caminho_arquivo):
        nome_arquivo = os.path.basename(caminho_arquivo)
        with open(caminho_arquivo, 'rb') as arquivo:
            dados_arquivo = arquivo.read()
        resposta = self.conexao.root.enviar_arquivo(nome_arquivo, dados_arquivo)
        print(resposta)

    def baixar_arquivo(self, nome_arquivo):
        dados_arquivo = self.conexao.root.baixar_arquivo(self.nome_cliente, nome_arquivo, self.servidor, self.porta)
        if dados_arquivo is None:
            print(f"No momento o arquivo solicitado não está disponível. O seu interesse foi registrado para o arquivo {nome_arquivo}.")
            print(f"Você será notificado quando ele estiver disponível.")
            print("")
        else:
            salvar_como = nome_arquivo
            with open(salvar_como, 'wb') as arquivo:
                arquivo.write(dados_arquivo)
            print(f"{nome_arquivo} foi baixado com sucesso como {salvar_como}.")

    def verificar_interesses(self):
        interesses = self.conexao.root.verificar_interesses(self.nome_cliente)
        for nome_arquivo in interesses:
            print(f"O arquivo {nome_arquivo} está disponível.")
            print("")
            escolha = input(f"Deseja baixar o arquivo {nome_arquivo}? (s/n): ")
            if escolha.lower() == 's':
                self.baixar_arquivo(nome_arquivo)
            else:
                print(f"Você optou por desistir do arquivo {nome_arquivo}.")
            self.conexao.root.remover_interesse(self.nome_cliente, nome_arquivo)
        if not interesses:
            print("Não há registros de interesse disponíveis para download no momento.")

    def fechar_conexao(self):
        self.conexao.close()
        print("Conexão encerrada")

if __name__ == "__main__":
    nome_cliente = input("Digite o nome do cliente: ")
    cliente = ClienteDeArquivos(nome_cliente)

    while True:
        print("\nOpções:")
        print("1. Listar arquivos disponíveis no servidor")
        print("2. Fazer upload de um arquivo")
        print("3. Fazer download de um arquivo")
        print("4. Verificar registros de interesse")
        print("5. Sair")
        print("")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            arquivos = cliente.listar_arquivos()
            print("Arquivos disponíveis:")
            for arquivo in arquivos:
                print(arquivo)

        elif escolha == "2":
            caminho_arquivo = input("Digite o caminho completo do arquivo a ser enviado: ")
            cliente.enviar_arquivo(caminho_arquivo)
            print("")


        elif escolha == "3":
            nome_arquivo = input("Digite o nome do arquivo a ser baixado: ")
            cliente.baixar_arquivo(nome_arquivo)
            print("")

        elif escolha == "4":
            cliente.verificar_interesses()

        elif escolha == "5":
            cliente.fechar_conexao()
            break

        else:
            print("Opção inválida. Tente novamente.")
