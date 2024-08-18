Trabalho Prático 02 - Middlewares
Arquitetura Cliente-Servidor
Java RMI, Eventos e Notificações

Aplicação de transferência de arquivos em uma arquitetura cliente-servidor.
▪ Utilizar a middleware Java RMI (Remote Invocation Method) ou Pyro 4/5
(Python Remote Objects) ou RPyC (Remote Python Call) para prover a
comunicação entre os clientes e o servidor da aplicação.

Métodos disponíveis no Servidor:
▪ Fazer upload de arquivos para serem compartilhados;
▪ Consultar informações sobre os arquivos disponíveis;
▪ Fazer download de arquivos disponíveis;
▪ Registrar interesse em arquivos não disponíveis no momento da consulta.
Para isso o cliente deve informar o arquivo desejado, sua referência de objeto
remoto e por quanto tempo será válido esse registro. Servidor armazena
esses interesses. Cada vez que um novo arquivo estiver disponível, o
servidor checa a lista de interesses e envia notificações aos clientes
interessados na ocorrência do evento em questão. Esse envio de notificação
ocorrerá via chamada de métodos (isto é, o servidor invocará um método do
cliente para enviar a notificação).
▪ Cancelar registro de interesse.

Método disponível no Cliente:
▪ Notificar evento: cliente receberá notificações assíncronas de eventos
(arquivos) que sejam do seu interesse.
