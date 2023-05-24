import serial
import time


try:
    # 通讯串口配置
    port_name_sen = "com7"     # 传感器
    port_name_emd = "com4"     # 驱动
    port_name_robot = "com3"   # 机械臂
    sen = serial.Serial(port=port_name_sen, baudrate=115200, timeout=0.01, parity=serial.PARITY_NONE, bytesize=8)
    emd = serial.Serial(port=port_name_emd, baudrate=115200, timeout=0.01, parity=serial.PARITY_NONE, bytesize=8)
    robot = serial.Serial(port=port_name_robot, baudrate=115200, timeout=0.01, parity=serial.PARITY_NONE, bytesize=8)
    print(sen)
    print(emd)
    print(robot)

    print('-'*160)

    # 启动
    n = 0

    while n < 20:
        time.sleep(0.1)
        robot.write(b'robotbegin')
        print(1)
        while True:
            time.sleep(0.001)
            data = robot.read_all().strip()
            if data == b'robotbegin':
                print('received')
                break

        time.sleep(0.001)

        emd.write(b'MagneticBegin\r\n')
        if emd.in_waiting:
            message = emd.readline().decode('gbk')
            # print(message)
            if message == 'Stable_1st_Finish\r\n':
                sen.write(b'Read_1st\r\n')
            if message == 'Stable_2nd_Finish\r\n':
                sen.write(b'Read_2nd\r\n')
            if message == 'Stable_3rd_Finish\r\n':
                sen.write(b'Read_3rd\r\n')
            # emd.flushInput()

        if sen.in_waiting:
            message = sen.readline().decode('gbk')
            # print(message)
            if message == 'Read_1st_Finish\r\n':
                emd.write(b'Stable_2nd\r\n')
            if message == 'Read_2nd_Finish\r\n':
                emd.write(b'Stable_3rd\r\n')
            if message == 'Read_3rd_Finish\r\n':
                emd.write(b'Stable_1st\r\n')
            # if message[9:0] == 'FinishRead':  # TODO:修改指令
            if 'FinishRead' in message:
                print(n)
                emd.write(b'MagneticEnd\r\n')
                with open(file='D:/User/509/dataset/dataset_v0.2.txt', mode='a') as f:
                    f.write(str(n))
                    f.write(message)
                    n = n + 1
                time.sleep(1)
                emd.write(b'MagneticBegin\r\n')
            # sen.flushInput()

    emd.write(b'MagneticEnd\r\n')
    emd.close()
    sen.close()

except Exception as e:
    print('error', e)
