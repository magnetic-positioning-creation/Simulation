import serial
import time


try:
    # 通讯串口配置
    # port_name_sen = "com7"     # 传感器
    # port_name_emd = "com4"     # 驱动
    port_name_robot = "com3"   # 机械臂
    # sen = serial.Serial(port=port_name_sen, baudrate=115200, timeout=0.01, parity=serial.PARITY_NONE, bytesize=8)
    # emd = serial.Serial(port=port_name_emd, baudrate=115200, timeout=0.01, parity=serial.PARITY_NONE, bytesize=8)
    robot = serial.Serial(port='COM3', baudrate=115200, timeout=0.01, parity=serial.PARITY_NONE, bytesize=8)
    # print(sen)
    # print(emd)
    print(robot)

    print('-'*160)

    while True:
        time.sleep(1)
        robot.write(b'robotbegin')
        print(1)

except Exception as e:
    print('error', e)
