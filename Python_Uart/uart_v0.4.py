import serial
import time


try:
    # 通讯串口配置
    port_name_sen = "com7"     # 传感器
    port_name_emd = "com4"     # 驱动
    sen = serial.Serial(port=port_name_sen, baudrate=115200, timeout=0.001, parity=serial.PARITY_NONE, bytesize=8)
    emd = serial.Serial(port=port_name_emd, baudrate=115200, timeout=0.001, parity=serial.PARITY_NONE, bytesize=8)
    print(sen)
    print(emd)

    print('-'*160)
    emd.write(b'MagneticBegin\r\n')

    # 启动
    n = 0

    while n < 5:
        time.sleep(0.05)
        emd_num = emd.inWaiting()
        sen_num = sen.inWaiting()
        if emd_num:
            message = emd.readline().decode('gbk')
            print(message)
            if message == 'Stable_1st_Finish\r\n':
                sen.write(b'Read_1st\r\n')
            if message == 'Stable_2nd_Finish\r\n':
                sen.write(b'Read_2nd\r\n')
            if message == 'Stable_3rd_Finish\r\n':
                sen.write(b'Read_3rd\r\n')

        if sen_num:
            message = sen.readline().decode('gbk')
            print(message)
            if message == 'Read_1st_Finish\r\n':
                emd.write(b'Stable_2nd\r\n')
            if message == 'Read_2nd_Finish\r\n':
                emd.write(b'Stable_3rd\r\n')
            if message == 'Read_3rd_Finish\r\n':
                emd.write(b'Stable_1st\r\n')
            if 'FinishRead' in message:
                print(n, '-'*100)
                # emd.write(b'MagneticEnd\r\n')
                emd.write(b'Stable_1st\r\n')
                n = n + 1
        emd.close()
        sen.close()
        sen.open()
        emd.open()

    emd.write(b'MagneticEnd\r\n')

except Exception as e:
    print('error', e)
