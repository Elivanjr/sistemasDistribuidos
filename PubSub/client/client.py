import socket
import json
from datetime import datetime

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def conectarServidor():
    ip = input("Digite o endereço de IP: ")
    porta = int(input("Digite a porta: "))

    try:
        cliente.connect((ip, porta))
        print("Deu bom")
        return cliente

    except OSError:
        print("Não deu bom")
        cliente.close()
        return None


def assinarTopico(clienteSocket):
    topic = input("Assine um topico existente: ")

    if not topic:
        print("Cade o topico rapaz...")
        return

    mensagem = {"action": "subscribe", "event": evento}


# def removeAssinatura()


def publicarEvento(clienteSocket, clienteId):
    topico = input("Tópico: ")
    # bota um se nao receber nada assim como a linha 36
    if not topico:
        print("Cade o topico rapaz?")
        return

    descricao = input("Descrição: ")

    evento = {
        "topico": topico,
        "descricao": descricao,
        "timestamp": datetime.now(),
        "author_id": clienteId,
    }

    mensagem = {"action": "publish", "event": evento}

    enviaMensagem(clienteSocket, mensagem)

    print("Evento enviado ao servidor!")


# def encerrarConexao():
#   conexao.close()


def recebeMensagem(clienteSocket):
    dados = clienteSocket.recv(1024)
    if not dados:
        raise ConnectionError("Matei sua conexão")
    mensagem = json.loads(dados.decode("utf-8"))
    return mensagem


def enviaMensagem(clienteSocket, contexto):
    pass


conectarServidor()

