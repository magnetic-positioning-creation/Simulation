# 别动这文件，谁动我跟谁急
# 驱动和采样系统
# 响应式触发
import threading
import time
import serial


def emd_rxd(com_emd, com_sen, com_robot):
    while True:
        time.sleep(0.001)
        if com_emd.in_waiting:
            message = com_emd.readline().decode('gbk')
            print(message)
            send_to_sen(message, com_sen, com_robot)


def send_to_sen(message, com_sen, com_robot):
    if message == 'Stable_1st_Finish\r\n':
        com_sen.write(b'Read_1st\r\n')
    if message == 'Stable_2nd_Finish\r\n':
        com_sen.write(b'Read_2nd\r\n')
    if message == 'Stable_3rd_Finish\r\n':
        com_sen.write(b'Read_3rd\r\n')
    if message == 'MagneticEndFinish\r\n':
        com_robot.write(b'robotbegin')
        print('-' * 100)


def sen_rxd(com_sen, com_emd):
    while True:
        time.sleep(0.001)
        if com_sen.in_waiting:
            message = com_sen.readline().decode('gbk')
            print(message)
            send_to_emd(message, com_emd)


def send_to_emd(message, com_emd):
    if message == 'Read_1st_Finish\r\n':
        com_emd.write(b'Stable_2nd\r\n')
    if message == 'Read_2nd_Finish\r\n':
        com_emd.write(b'Stable_3rd\r\n')
    if message == 'Read_3rd_Finish\r\n':
        com_emd.write(b'Stable_1st\r\n')
    if 'FinishRead' in message:
        with open(file='D:/User/509/dataset/dataset_20230526_2.txt', mode='a') as f:
            f.write(message)
        time.sleep(1)
        com_emd.write(b'MagneticEnd\r\n')


def interaction(com):
    while True:
        line = input('>>> ').strip() + '\r\n'
        com.write(line.encode('GBK'))


def robot_rx(com_robot, com_emd):
    while True:
        time.sleep(0.001)
        if com_robot.in_waiting:
            message = com_robot.readline()
            print(message)
            robot_send_to_emd(message, com_emd)


def robot_send_to_emd(message, com_emd):
    if message == b'robotdone\n':
        com_emd.write(b'MagneticBegin\r\n')


def main():
    try:
        # 通讯串口配置
        port_name_sen = "com7"  # 传感器
        port_name_emd = "com4"  # 驱动
        port_name_robot = "com3"
        sen = serial.Serial(port=port_name_sen, baudrate=115200, timeout=0.01, parity=serial.PARITY_NONE, bytesize=8)
        emd = serial.Serial(port=port_name_emd, baudrate=115200, timeout=0.01, parity=serial.PARITY_NONE, bytesize=8)
        robot = serial.Serial(port=port_name_robot, baudrate=115200, timeout=0.01, parity=serial.PARITY_NONE, bytesize=8)
        print(emd)
        print(sen)
        print(robot)
        print('-' * 160)

        emd_r = threading.Thread(target=emd_rxd, args=(emd, sen, robot))
        sen_r = threading.Thread(target=sen_rxd, args=(sen, emd,))
        robot_r = threading.Thread(target=robot_rx, args=(robot, emd))

        # 启动
        robot.write(b'robotbegin\n')
        time.sleep(1)

        emd_r.start()
        sen_r.start()
        robot_r.start()

        emd_r.join()
        sen_r.join()
        robot_r.join()

    except Exception as e:
        print('[error]', e)


if __name__ == '__main__':
    main()
