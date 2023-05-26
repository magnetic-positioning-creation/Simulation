import serial
import threading
from functools import wraps
from datetime import datetime


# 创建一个装饰器
# 这个装饰器的作用是给捕获或者外发的数据信息添加一个时间戳
def timestamp_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f'[{str(datetime.now())[:-3]}]  ', end='')   # 时间戳的输出格式为：[2022-06-12 13:52:43.806]
        func(*args, **kwargs)
    return wrapper


# 创建一个信息打印函数
# 此函数的作用是将用户的输入或者串口捕获到的输出作打印。
# 同时，调用前面创建的装饰器，为当前的打印添加一个时间戳，以便于工作中 debug 某个时间段的串口日志信息
@timestamp_decorator
def print_line(line, input_type='接收'):
    print(f'[{input_type}] {line}')  # [2022-06-12 14:06:00.491]  [接收] 这个一个串口信息


# 创建一个串口日志捕获函数
# 此函数的作用是实时捕获来自串口的日志信息，同时将其打印
def catch_output(com):
    while True:
        line = com.readline().decode('GBK').strip()  # 从串口中读取每一行日志信息
        # line = com.readline().decode('GB2312').strip()
        print_line(line)

# 创建一个串口输入函数
# 此函数的作用是与串口的另一方作交互，给对方下发预期参数数据
# >>> 给串口下发一个指令参数
# [2022-06-12 14:13:23.786]  [发送] 给串口下发一个指令参数
def send_out_cmd(com):
    while True:
        line = input('>>> ').strip() + '\r\n'
        com.write(line.encode('GBK'))
        # com.write(line.encode('GB2312'))
        print_line(line, '发送')


# 主函数main
def main():
    try:
        com = serial.Serial(port='COM7', baudrate=115200)
        co = threading.Thread(target=catch_output, args=(com,))
        so = threading.Thread(target=send_out_cmd, args=(com,))
        co.start()
        so.start()
        co.join()
        so.join()
        print('terminate...')
    except Exception as e:
        print("[error]", e)


if __name__ == '__main__':
    main()



