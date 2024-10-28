from random import randint
import threading
import time

lock = threading.Lock()

class Bank(threading.Thread):

    def __init__(self):
        super().__init__()
        self.balance = 0
        self.lock = lock


    def deposit(self):
        for _ in range(100):
            n = randint(50, 500)
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
            self.balance += n
            print(f'Пополнение: {n}. Баланс: {self.balance}')
            time.sleep(0.001)


    def take(self):
        for _ in range(100):
            m = randint(50, 500)
            print(f'Запрос на {m}')
            if m <= self.balance:
                self.balance -= m
                print(f'Снятие: {m}. Баланс: {self.balance}')
            else:
                print('Запрос отклонён, недостаточно средств')
                self.lock.acquire()
            time.sleep(0.001)


bk = Bank()

th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()

th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')