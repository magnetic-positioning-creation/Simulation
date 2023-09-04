# 别动这文件，谁动我跟谁急
# 驱动和采样系统
# 响应式触发
import threading
import time
import serial


def emd_rxd(com_emd, com_sen):
    while True:
        time.sleep(0.001)
        if com_emd.in_waiting:
            message = com_emd.readline().decode('gbk')
            print(message)
            send_to_sen(message, com_sen)


def send_to_sen(message, com_sen):
    if message == 'Stable_1st_Finish\r\n':
        com_sen.write(b'Read_1st\r\n')
    if message == 'Stable_2nd_Finish\r\n':
        com_sen.write(b'Read_2nd\r\n')
    if message == 'Stable_3rd_Finish\r\n':
        com_sen.write(b'Read_3rd\r\n')


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
        time.sleep(1)
        # com_emd.write(b'Stable_1st\r\n')
        com_emd.write(b'MagneticEnd\r\n')
    if message == 'MagneticEndFinish\r\n':
        print('-' * 100)


def interaction(com):
    while True:
        line = input('>>> ').strip() + '\r\n'
        com.write(line.encode('GBK'))


def main():
    try:
        # 通讯串口配置
        port_name_sen = "com4"  # 传感器
        port_name_emd = "com7"  # 驱动
        sen = serial.Serial(port=port_name_sen, baudrate=115200, timeout=0.01, parity=serial.PARITY_NONE, bytesize=8)
        emd = serial.Serial(port=port_name_emd, baudrate=115200, timeout=0.01, parity=serial.PARITY_NONE, bytesize=8)
        print(emd)
        print(sen)
        print('-' * 160)

        emd_r = threading.Thread(target=emd_rxd, args=(emd, sen,))
        sen_r = threading.Thread(target=sen_rxd, args=(sen, emd,))
        robot = threading.Thread(target=interaction, args=(emd,))
        # emd.write(b'MagneticBegin\r\n')

        emd_r.start()
        sen_r.start()
        robot.start()

        emd_r.join()
        sen_r.join()
        robot.join()

    except Exception as e:
        print('[error]', e)


if __name__ == '__main__':
    main()
