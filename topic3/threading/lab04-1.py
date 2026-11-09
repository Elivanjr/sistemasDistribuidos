import threading
import time


def ola_mundo(idThread):
    for i in range(10):
        print(f"Thread {idThread}")
        time.sleep(1)


tasks = []

for i in range(10):
    t = threading.Thread(target=ola_mundo, args=(i+1,))
    tasks.append(t)
    t.start()

for t in tasks:
    t.join()

print("ATE MAIS")
