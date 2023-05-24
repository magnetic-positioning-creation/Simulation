import serial
import time

# 数据保存地址
save_file_path = "xxx"

try:
    # 通讯串口配置
    port_name_sen = "com7"     # 传感器
    port_name_emd = "com3"     # 驱动
    sen = serial.Serial(port=port_name_sen, baudrate=115200, timeout=0.01, parity=serial.PARITY_NONE, bytesize=8)
    emd = serial.Serial(port=port_name_emd, baudrate=115200, timeout=0.01, parity=serial.PARITY_NONE, bytesize=8)
    if sen.isOpen():
        print(sen)
    if emd.isOpen():
        print(emd)

    # 启动
    emd.write(b'Stable_1st\r\n')

    # 接收数据并通讯
    while True:
        time.sleep(0.1)
        if emd.in_waiting:
            message = emd.readline(emd.in_waiting).decode('gbk')
            if message == "Stable_1st_Finish\r\n":     # 已核对
                sen.write(b'Read_1st\r\n')

            if message == "Stable_2nd_Finish\r\n":     # 已核对
                sen.write(b'Read_2nd\r\n')

            if message == "Stable_3rd_Finish\r\n":     # 已核对
                sen.write(b'Read_3rd\r\n')

            # if message == "MagneticEndFinish\r\n":     # 给机械臂发送指令，移动到下一个指定位置

        time.sleep(0.1)
        if sen.in_waiting:
            message = sen.readline(sen.in_waiting).decode('gbk')
            if message == "Read_1st_Finish\r\n":
                emd.write(b'Stable_2nd\r\n')

            if message == "Read_2nd_Finish\r\n":
                emd.write(b'Stable_3rd\r\n')

            if message == "Read_3rd_Finish\r\n":
                emd.write(b'Stable_1st')

            if message[9:0] == "FinishRead":
                emd.write(b'MagneticEnd\r\n')
                # 保存数据
                file_handle = open(save_file_path, mode='a+')
                file_handle.write(message)
                file_handle.close()


except Exception as e:
    print('error', e)

# w 只能操作写入  r 只能读取   a 向文件追加
# w+ 可读可写   r+可读可写    a+可读可追加
# wb+写入进制数据
# w模式打开文件，如果而文件中有数据，再次写入内容，会把原来的覆盖掉
