import serial
import threading

class Com_Class:
    # 初始化
    def __init__(self, port, baud):
        self.port = port
        self.baud = baud
        self.comSerial = None
        self.run = False        # 串口运行状态
        self.open()             # 打开串口函数
        if self.run:
            self.thread1 = threading.Thread()
            self.thread2 = threading.Thread()
            self.thread1.start()
            self.thread2.start()
            self.thread1.join()
            self.thread2.join()
            self.close()

    def open(self):
        try:
            self.comSerial = serial.Serial(port=self.port, baudrate=self.baud, bytesize=8)
            self.run = True
            print(self.comSerial)
        except Exception as e:
            print('Uart_Error', e)

    def close(self):
        self.comSerial.close()

    def receiveData(self):
        while self.run:
            receive_data = self.comSerial.read(self.comSerial.inWaiting()).decode("gbk")
            n = 0
            if receive_data:
                print('RX:%s', receive_data)
            n = n + 1
            if n > 10:
                break


if __name__ == "__main__":
    print('test')
    print("__main__ :", threading.current_thread)
    test = Com_Class('com7', 115200)
