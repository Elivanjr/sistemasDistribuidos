import threading
import time
import random
import os

def corredor(nome, limite, posicoes, indice):
    for i in range(limite):
        tempo = random.random()
        time.sleep(tempo)
        posicoes[indice] +=1
        

posicoes = [0] * 5
corredores = ["Maya", "Bruno", "Melissa", "James", "Pablo"]
threads = []
limite = 70

for i in range(5):
    thread = threading.Thread(target=corredor, args=(corredores[i], limite, posicoes, i))
    threads.append(thread)
    thread.start()

while any(thread.is_alive() for thread in threads):
    os.system("clear")

    for i in range(5):
        print(f"{corredores[i]}: {'*' * posicoes[i]} ({posicoes[i]})")

    time.sleep(0.1)

for thread in threads:
    thread.join()