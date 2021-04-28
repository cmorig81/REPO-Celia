import threading
import time

def worker():
    """thread worker function"""
    x = 0
    while True:
        x += 1
        print('Aquí ponemos el sensor de Celia')
        time.sleep(3)
        if x == 10:
            break

threads=[]

t = threading.Thread(target=worker)
threads.append(t)
t.start()