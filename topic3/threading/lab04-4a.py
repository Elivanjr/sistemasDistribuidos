import threading
import time

def contar(id: int, num: list, mutex):
    while num[0]<=100:
        with mutex:
            print(f'Thread {id} contou número: {num[0]}')
            num[0] += 1
        time.sleep(1)

threads = []
num = [1]
mutex = threading.Lock()

for i in range(3):
    threads.append(threading.Thread(target=contar, args=(i, num, mutex)))

for t in threads:
    t.start()

for t in threads:
    t.join()

print("Contagem encerrada")