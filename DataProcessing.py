import os
import numpy
import matplotlib.pyplot as plt


# 读取数据
sensor_data_path = os.path.join('sensorData.txt')
sensor_data = numpy.loadtxt(sensor_data_path, delimiter='\n')
# print(sensor_data)


# 使用matplotlib绘制图像
plt.figure()
plt.plot(sensor_data)
plt.xlabel('Time')
plt.ylabel('Sensor Data')
plt.show()
