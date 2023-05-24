# 导入Serial模块
import serial
# 导入time模块
import time
import serial.tools.list_ports

# 解析指令
def read_massage():
    uart_message = ser.readline().decode('GBK')
    print(uart_message)
    if uart_message == 'start':
        ser.write(b'satbled_one\n')
    elif uart_message == 'satbled_one':
        ser.write(b'read_one\n')
    elif uart_message == 'read_one':
        ser.write(b'satbled_two\n')
    elif uart_message == 'satbled_two':
        ser.write(b'read_two\n')
    elif uart_message == 'read_two':
        ser.write(b'satbled_thr\n')
    elif uart_message == 'satbled_thr':
        ser.write(b'read_thr\n')
    elif uart_message == 'read_thr':
        ser.write(b'stabled_one\n')

# 如果不清楚当前的串口设备，pyserial 也提供了相应的 api

ports = list(serial.tools.list_ports.comports(include_links=False))
for port in ports:
    print(str(port)[0:4], '\ndatatype:',type(port))

# windows系统下打开串口
port_name_1 = "com7"
ser = serial.Serial(port=port_name_1, baudrate=115200, timeout=0.01, parity=serial.PARITY_NONE, bytesize=8)
if ser.isOpen():
    print("ser.name:", ser.name)
    print("ser.port:", ser.port)
    print(ser.portstr)
else:
    print("Connect_Error!")

start_time = time.time()

# 收发数据
ser.write(b"start")

ser.write(b'hello\n')
print(ser.in_waiting)
data = ser.readline().decode('gbk')
print(ser.in_waiting)
print(data)
print(ser.in_waiting)
print(ser.out_waiting)

end_time = time.time()

# 测试

# 关闭串口
ser.close()


print("Running_Time:", (end_time - start_time))
