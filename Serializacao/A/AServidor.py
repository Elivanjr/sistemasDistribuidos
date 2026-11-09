# a) SEM serialização: o servidor precisa saber a ordem e os tipos dos campos
import socket

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
    codigo, nome, preco, quantidade = dados.decode("utf-8").split(";")
    # Sem serialização: toda conversão de tipo é manual
    produto = {
        "codigo": int(codigo),
        "nome": nome,
        "preco": float(preco),
        "quantidade": int(quantidade),
    }
    imprimir(produto)


if __name__ == "__main__":
    main()
