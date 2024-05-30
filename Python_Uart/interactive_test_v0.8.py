"""对单个电磁铁进行采样"""
# 别动这文件，谁动我跟谁急
# 驱动和采样系统
# 响应式触发
import threading
import time
import serial
import datetime

now = datetime.datetime.now()
start = time.time()
Save_File_Path = 'D:/User/test_3_2023.9.22+.txt'

robotdone_counter = 0


def emd_rxd(com_emd, com_sen, com_robot, send_counter):
    """
    电磁场驱动接收端
    :param com_emd:电磁场驱动设备串口端口号-用于接收
    :param com_sen:采样设备串口端口号-用于发送
    :param com_robot:机械臂设备窗口端口号-用于发送
    :param send_counter:用于周期计数
    :return:none
    """
    while True:
        time.sleep(0.001)
        if com_emd.in_waiting:
            message = com_emd.readline().decode('gbk')
            print(message)
            send_to_sen(message, com_sen, com_robot, send_counter)


def send_to_sen(message, com_sen, com_robot, send_counter):
    # TODO：对于不同电磁铁测试的时候不需要直接改变电路，就无需改变代码，避免了较为繁琐的烧录过程
    if message == 'Stable_1st_Finish\r\n':
        com_sen.write(b'Read_1st\r\n')
    # if message == 'Stable_2nd_Finish\r\n':
    #     com_sen.write(b'Read_2nd\r\n')
    # if message == 'Stable_3rd_Finish\r\n':
    #     com_sen.write(b'Read_3rd\r\n')
    if message == 'MagneticEndFinish\r\n':
        com_robot.write(b'robotbegin\r\n')
        send_counter = send_counter + 1
        print('-' * 100)


def sen_rxd(com_sen, com_emd, send_counter, receive_counter):
    while True:
        time.sleep(0.001)
        if com_sen.in_waiting:
            message = com_sen.readline().decode('gbk')
            print(message)
            send_to_emd(message, com_emd, send_counter, receive_counter)


def send_to_emd(message, com_emd, send_counter, receive_counter):
    if message == 'Read_1st_Finish\r\n':
        com_emd.write(b'Stable_1st\r\n')
    # if message == 'Read_1st_Finish\r\n':
    #     com_emd.write(b'Stable_2nd\r\n')
    # if message == 'Read_2nd_Finish\r\n':
    #     com_emd.write(b'Stable_3rd\r\n')
    # if message == 'Read_3rd_Finish\r\n':
    #     com_emd.write(b'Stable_1st\r\n')
    if 'FinishRead' in message:
        with open(file=Save_File_Path, mode='a') as f:
            f.write(str(robotdone_counter))
            f.write('&')
            f.write(message)
        end = time.time()
        receive_counter = receive_counter + 1
        print('Send_Counter:', send_counter, 'Receive_Counter:',  receive_counter, '\n')
        print('Time:', round(end-start, 3), 'secs\r\n')
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
    if message == b'robotdone\r\n':
        global robotdone_counter
        robotdone_counter += 1
        print(robotdone_counter)
        com_emd.write(b'MagneticBegin\r\n')


def main():
    # counter
    send_counter = 1
    receive_counter = 0
    try:
        # 通讯串口配置
        port_name_sen = "com3"      # 传感器
        port_name_emd = "com5"      # 驱动
        port_name_robot = "com8"    # 机械臂
        sen = serial.Serial(port=port_name_sen, baudrate=115200, timeout=0.01, parity=serial.PARITY_NONE, bytesize=8)
        emd = serial.Serial(port=port_name_emd, baudrate=115200, timeout=0.01, parity=serial.PARITY_NONE, bytesize=8)
        robot = serial.Serial(port=port_name_robot, baudrate=115200, timeout=0.01, parity=serial.PARITY_NONE, bytesize=8)
        print(emd)
        print(sen)
        print(robot)
        print('-' * 160)

        emd_r = threading.Thread(target=emd_rxd, args=(emd, sen, robot, send_counter,))
        sen_r = threading.Thread(target=sen_rxd, args=(sen, emd, send_counter, receive_counter,))
        robot_r = threading.Thread(target=robot_rx, args=(robot, emd, ))

        # 日志记录
        with open(file=Save_File_Path, mode='a') as f:
            f.write(str(now))
        # 启动
        robot.write(b'robotbegin\r\n')

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
