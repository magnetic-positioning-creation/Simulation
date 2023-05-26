import threading
import time


def func_1():
    while True:
        print(1)
        time.sleep(1)


def func_2():
    while True:
        print(2)
        time.sleep(0.5)


def func_3():
    while True:
        print(3)
        time.sleep(2)


def func_4():
    while True:
        print(4)
        time.sleep(1.5)


def main():
    thread1 = threading.Thread(target=func_1)
    thread2 = threading.Thread(target=func_2)
    thread3 = threading.Thread(target=func_3)
    thread4 = threading.Thread(target=func_4)
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()


if __name__ == '__main__':
    print('-'*100)
    main()