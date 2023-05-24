import serial
import time

try:
    # 通讯串口配置
    port_name_sen = "com7"     # 传感器
    port_name_emd = "com4"     # 驱动
    port_name_robot = "com3"   # 机械臂
    sen = serial.Serial(port=port_name_sen, baudrate=115200, timeout=0.01, parity=serial.PARITY_NONE, bytesize=8)
    emd = serial.Serial(port=port_name_emd, baudrate=115200, timeout=0.01, parity=serial.PARITY_NONE, bytesize=8)
    robot = serial.Serial(port='COM3', baudrate=115200, timeout=0.01, parity=serial.PARITY_NONE, bytesize=8)
    print(sen)
    print(emd)
    print(robot)

    print('-'*160)

    # 启动
    time.sleep(1)
    robot.write(b'robotbegin')
    n = 1
    while True:
        while True:
            time.sleep(0.0001)
            if robot.in_waiting:
                message = robot.read_all().strip()
                print(message)
                if message == b'robotdone':
                    emd.write(b'MagneticBegin\r\n')
                    robot.flushInput()
                    break

        while True:
            time.sleep(0.0001)
            if emd.in_waiting:
                message = emd.readline().decode('gbk')
                print(message)
                if message == 'Stable_1st_Finish\r\n':
                    sen.write(b'Read_1st\r\n')
                if message == 'Stable_2nd_Finish\r\n':
                    sen.write(b'Read_2nd\r\n')
                if message == 'Stable_3rd_Finish\r\n':
                    sen.write(b'Read_3rd\r\n')
                emd.flushInput()

            if sen.in_waiting:
                message = sen.readline().decode('gbk')
                print(message)
                if message == 'Read_1st_Finish\r\n':
                    emd.write(b'Stable_2nd\r\n')
                if message == 'Read_2nd_Finish\r\n':
                    emd.write(b'Stable_3rd\r\n')
                if message == 'Read_3rd_Finish\r\n':
                    emd.write(b'Stable_1st\r\n')
                # if message[9:0] == 'FinishRead':  # TODO:修改指令
                if 'FinishRead' in message:
                    # with open(file='D:/User/509/dataset/dataset.txt', mode='a') as f:
                    #     f.write(str(n))
                    #     f.write(message)
                    n = n + 1
                    time.sleep(1)
                    print(n)
                    break
                sen.flushInput()

        time.sleep(1)

        emd.close()
        sen.close()
        robot.close()

        emd.open()
        sen.open()
        robot.open()

        time.sleep(1)
        robot.write(b'robotbegin\r\n')
        # sen.flushInput()

except Exception as e:
    print('error', e)
