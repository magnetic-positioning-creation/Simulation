import serial # 导入模块
import time

file_handle = open('D:/User/Elec_Contest_2023.3.16/uart_test.txt', 'w')
try:
    # 端口号，根据自己实际情况输入，可以在设备管理器查看
    port = "COM3"
    # 串口波特率，根据自己实际情况输入
    bps = 115200
    # 超时时间,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
    time = 0.005
    # 打开串口，并返回串口对象
    uart = serial.Serial(port, bps, bytesize=8, timeout=time)

    # 串口接收一个字符串
    print('连接状态:', uart.isOpen())

    while True:
        str = uart.readline()
        if str != b'':
            # print(str) # 打印源码
            print(str.decode('GBK'))
            file_handle.writelines(str.decode('GBK'))

        time.sleep(1)
        uart.write(b'Read\r\n')





except Exception as result:
    print("******error******：", result)
