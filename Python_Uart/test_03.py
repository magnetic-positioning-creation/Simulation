# 导入Serial模块
import serial
import time
try:
    # windows系统下打开串口
    port_name_1 = "com7"
    ser = serial.Serial(port=port_name_1, baudrate=115200, timeout=0.01, parity=serial.PARITY_NONE, bytesize=8)
    print(ser)

    ser.write(b'begin\n')

    # 接收数据
    n = 100
    while n:

        time.sleep(0.000000000001)
        # 输入缓冲区
        if ser.in_waiting:
            message = ser.read(ser.in_waiting).decode('gbk')
            if message == "begin\n":
                print(n, '-', message)
                ser.write(b'stabled_1st\n')

            if message == "stabled_1st\n":
                print(n, '-', message)
                ser.write(b'Read_1st\n')

            if message == "Read_1st\n":
                print(n, '-', message)
                ser.write(b'stabled_2nd\n')

            if message == "stabled_2nd\n":
                print(n, '-', message)
                ser.write(b'Read_2nd\n')

            if message == "Read_2nd\n":
                print(n, '-', message)
                ser.write(b'stabled_3rd\n')

            if message == "stabled_3rd\n":
                print(n, '-', message)
                ser.write(b'Read_3nd\n')

            if message == "Read_3nd\n":
                print(n, '-', message)
                ser.write(b'begin\n')
        else:
            continue

        n -= 1


except Exception as e:
    print('error', e)
