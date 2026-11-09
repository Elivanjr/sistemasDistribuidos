import socket
import json
from datetime import datetime

#acao no json vai ser: publica, assina, remove, sai

def menu():
    print("\nCliente Pub/Sub")
    print("1) Conectar Servidor")
    print("2) Publicar Evento")
    print("3) Assinar Tópico")
    print("4) Remover Assinatura")
    print("5) Encerrar Conexão")
    print("0) Sair")    
    return input("Escolha uma opção: ").strip()


def conectarServidor():
    ip = input("Digite o endereço de IP: ")
    porta = int(input("Digite a porta: "))
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        cliente.connect((ip, porta))
        volta = recebeMensagem(cliente)
        uuid = volta["uuid"]
        print(f"Deu bom, logo UUID -> {uuid}")
        return cliente, uuid

    except OSError:
        print("Não deu bom, tente novamente")
        cliente.close()
        return None


def assinarTopico(clienteSocket):
    topic = input("Assine um topico existente: ")

    if not topic:
        print("Cade o topico rapaz...")
        return

    mensagem = {"acao": "assina", "topico": topic}
    enviaMensagem(clienteSocket, mensagem)
    print("Assinatura concluida.")


def removeAssinatura(clienteSocket):
    topic = input("Remover assinatura de que tópico? ")
    
    if not topic:
        print("Cade o topico rapaz...")
        return
    
    mensagem = {"acao": "remove", "topico": topic}
    enviaMensagem(clienteSocket, mensagem)
    print("Assinatura removida.")


def publicarEvento(clienteSocket, clienteId):
    topico = input("Tópico: ")
    if not topico:
        print("Cade o topico rapaz...")
        return

    descricao = input("Descrição: ")

    mensagem = {
        "acao": "publica",
        "topico": topico,
        "descricao": descricao,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "author_id": clienteId,
    }

    enviaMensagem(clienteSocket, mensagem)
    print("Evento enviado ao servidor!")


def encerrarConexao(clienteSocket):
    mensagem = {"acao": "sai"}
    enviaMensagem(clienteSocket, mensagem)
    clienteSocket.close()


def recebeMensagem(clienteSocket):
    dados = b""
    while True:
        byte = clienteSocket.recv(1)
        if not byte:
            raise ConnectionError("Servidor matou sua conexão")
        if byte == b"\n":
            break
        dados += byte
    return json.loads(dados.decode("utf-8"))


def enviaMensagem(clienteSocket, contexto):
    dados = (json.dumps(contexto, ensure_ascii=False) + "\n").encode("utf-8")
    clienteSocket.sendall(dados)


def main():
    sock = None
    clienteId = None

    while True:
        opcao = menu()

        if opcao == "1":
            if sock:
                print("Existe conexão ativa.")
                continue
            resultado = conectarServidor()
            if resultado:
                sock, clienteId = resultado

        elif opcao in ("2", "3", "4", "5"):
            if not sock:
                print("Precisa se conectar ao server primeiro.")
                continue

            if opcao == "2":
                publicarEvento(sock, clienteId)
            elif opcao == "3":
                assinarTopico(sock)
            elif opcao == "4":
                removeAssinatura(sock)
            elif opcao == "5":
                encerrarConexao(sock)
                sock = None
                clienteId = None
        
        elif opcao == "0":
            print("Vai pela sombra")
            break

        
if __name__ == "__main__":
    main()
