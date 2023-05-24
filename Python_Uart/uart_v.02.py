# 专门测试 驱动 emd 通讯串口
import serial
import time

# 数据保存地址
save_file_path = "xxx"

try:
    # 通讯串口配置
    port_name_emd = "com3"     # 驱动

    emd = serial.Serial(port=port_name_emd, baudrate=115200, timeout=0.01, parity=serial.PARITY_NONE, bytesize=8)
    if emd.isOpen():
        print("驱动_emd_成功连接")
        print(emd)



    # 启动
    emd.write(b'Stable_1st\r\n')

    time.sleep(0.001)
    if emd.in_waiting:
        message = emd.readline().decode('gbk')
        print(message)




except Exception as e:
    print('error', e)

