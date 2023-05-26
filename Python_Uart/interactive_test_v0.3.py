import threading
import time
import serial


def emd_rxd(emd):
    while True:
        time.sleep(0.001)
        if emd.in_waiting:
            message = emd.readline().decode('gbk')
            print(message)


def emd_trd(emd, message):
    if message == 'Read_1st_Finish\r\n':
        emd.write(b'Stable_2nd\r\n')
    if message == 'Read_2nd_Finish\r\n':
        emd.write(b'Stable_3rd\r\n')
    if message == 'Read_3rd_Finish\r\n':
        emd.write(b'Stable_1st\r\n')
    if 'FinishRead' in message:
        time.sleep(1)
        print('-' * 100)
    message = ''


def sen_rxd(sen, emd):
    while True:
        time.sleep(0.001)
        if sen.in_waiting:
            message = sen.readline().decode('gbk')
            print(message)


def sen_txd(sen, message):
    if message == 'Stable_1st_Finish\r\n':
        sen.write(b'Read_1st\r\n')
    if message == 'Stable_2nd_Finish\r\n':
        sen.write(b'Read_2nd\r\n')
    if message == 'Stable_3rd_Finish\r\n':
        sen.write(b'Read_3rd\r\n')
    message = ''


def main():
    emd_receive_message = ''
    sen_receive_message = ''
    try:
        # 通讯串口配置
        port_name_sen = "com7"  # 传感器
        port_name_emd = "com4"  # 驱动
        sen = serial.Serial(port=port_name_sen, baudrate=115200, timeout=0.01, parity=serial.PARITY_NONE, bytesize=8)
        emd = serial.Serial(port=port_name_emd, baudrate=115200, timeout=0.01, parity=serial.PARITY_NONE, bytesize=8)
        print(emd)
        print(sen)
        print('-' * 160)

        # 启动
        emd.write(b'MagneticBegin\r\n')
        # 接收
        emd_r = threading.Thread(target=emd_rxd, args=(emd, emd_receive_message))
        sen_r = threading.Thread(target=sen_rxd, args=(sen, sen_receive_message))
        # 发送
        emd_t = threading.Thread(target=emd_trd, args=(emd, sen_receive_message))
        sen_t = threading.Thread(target=sen_txd, args=(sen, emd_receive_message))

        emd_r.start()
        sen_r.start()
        emd_t.start()
        sen_t.start()

        emd_r.join()
        sen_r.join()
        emd_t.join()
        sen_t.join()

    except Exception as e:
        print('[error]', e)


if __name__ == '__main__':
    main()
