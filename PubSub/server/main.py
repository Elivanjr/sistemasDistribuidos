import socket
import json
import threading
import uuid

HOST = "127.0.0.1"
PORTA = 8080

clientes = {}
assinaturas = {}

lockAcao = threading.Lock()
lockEnvio = threading.Lock()


def enviaMensagem(clienteSocket, contexto):
    dados = (json.dumps(contexto, ensure_ascii=False) + "\n").encode("utf-8")
    with lockEnvio:
        clienteSocket.sendall(dados)


def publica(mensagem, autorId):
    topico = mensagem.get("topico", "")
    descricao = mensagem.get("descricao", "")
    timestamp = mensagem.get("timestamp", "")

    print(f"Cliente: {autorId} -> PUBLICA -> tópico {topico} | {descricao}")

    evento = {
        "tipo": "evento",
        "topico": topico,
        "descricao": descricao,
        "timestamp": timestamp,
        "author_id": autorId,
    }

    with lockAcao:
        destinos = [
            (uid, clientes[uid])
            for uid in assinaturas.get(topico, set())
            if uid in clientes
        ]

    for uid, sock in destinos:
        try:
            enviaMensagem(sock, evento)
        except OSError:
            print(f"Falha ao enviar para {uid}, removendo cliente")
            limparAssinatura(uid)


def recebeLinhas(clienteSocket):
    buffer = b""
    while True:
        dados = clienteSocket.recv(4096)
        if not dados:
            return
        buffer += dados
        while b"\n" in buffer:
            linha, buffer = buffer.split(b"\n", 1)
            if linha.strip():
                yield json.loads(linha.decode("utf-8"))


def assina(autorId, topico):
    with lockAcao:
        assinaturas.setdefault(topico, set()).add(autorId)
        print(f"Cliente: {autorId} -> ASSINA -> tópico {topico}")


def remove(autorId, topico):
    with lockAcao:
        if topico in assinaturas:
            assinaturas[topico].discard(autorId)
            if not assinaturas[topico]:
                del assinaturas[topico]


def limparAssinatura(clienteId):
    with lockAcao:
        clientes.pop(clienteId, None)
        for topico in list(assinaturas):
            assinaturas[topico].discard(clienteId)
            if not assinaturas[topico]:
                del assinaturas[topico]


def atendeCliente(sock, endereco):
    clienteId = str(uuid.uuid4())
    with lockAcao:
        clientes[clienteId] = sock
    print(f"Nova conexão de {endereco} -> UUID {clienteId}")

    try:
        enviaMensagem(sock, {"uuid": clienteId})
        for msg in recebeLinhas(sock):
            acao = msg.get("acao")
            if acao == "publica":
                publica(msg, clienteId)
            elif acao == "assina":
                assina(clienteId, msg["topico"])
            elif acao == "remove":
                remove(clienteId, msg["topico"])
            elif acao == "sai":
                break
    except (OSError, ValueError, KeyError):
        pass
    finally:
        limparAssinatura(clienteId)
        sock.close()


def main():
    conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conexao.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    conexao.bind((HOST, PORTA))
    conexao.listen()
    print(f"Ouvindo em {HOST}:{PORTA}")

    while True:
        sock, endereco = conexao.accept()
        threading.Thread(
            target=atendeCliente, args=(sock, endereco), daemon=True
        ).start()


if __name__ == "__main__":
    main()
