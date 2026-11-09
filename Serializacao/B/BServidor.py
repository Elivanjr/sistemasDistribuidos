# b) PICKLE: reconstrói o dict, tipos preservados
import socket
import pickle
HOST = "127.0.0.1"
PORT = 5000

def receber_tudo(conn):
    """Lê até o cliente fechar o envio (shutdown)."""
    partes = []
    while True:
        bloco = conn.recv(4096)
        if not bloco:
            break
        partes.append(bloco)
    return b"".join(partes)

def imprimir(produto):
    print("--- Produto recebido ---")
    for campo, valor in produto.items():
        print(f"{campo}: {valor} ({type(valor).__name__})")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"Servidor aguardando em {HOST}:{PORT}...")
        conn, addr = s.accept()
        with conn:
            dados = receber_tudo(conn)
    produto = pickle.loads(dados)  # só use com clientes SEGUROS!!!
    imprimir(produto)


if __name__ == "__main__":
    main()
