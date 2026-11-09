import socket
import json

conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conexao.bind(('127.0.0.1', 8080))
conexao.listen()

print("Ouvindo em 127.0.0.1:8080")

while True:
    cliente, endereco = conexao.accept()
    print(f"Cliente {endereco}")
