# c) JSON: serializa o dict em texto UTF-8
import socket
import json
HOST = "127.0.0.1"
PORT = 5000

def ler_produto():
    return {
        "codigo": int(input("Código: ")),
        "nome": input("Nome: "),
        "preco": float(input("Preço: ")),
        "quantidade": int(input("Quantidade: ")),
    }

def main():
    produto = ler_produto()
    dados = json.dumps(produto).encode("utf-8")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(dados)
        s.shutdown(socket.SHUT_WR)  # avisa que terminou de enviar
    print("Cadastro enviado.")


if __name__ == "__main__":
    main()
