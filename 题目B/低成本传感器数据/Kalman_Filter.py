import numpy as np
import matplotlib.pyplot as plt
import csv

class Kalman_Filter:
    def __init__(self, Q, R): # 构造函数
        self.Q = Q
        self.R = R

        self.P_k_k1 = 1
        self.Kg = 0
        self.P_k1_k1 = 1
        self.x_k_k1 = 0
        self.ADC_OLD_Value = 0
        self.Z_k = 0
        self.kalman_adc_old=0

    def Kalman(self, ADC_Value):
        self.Z_k = ADC_Value

        if ( abs(self.kalman_adc_old - ADC_Value) >= 60 ):
            self.x_k1_k1 = ADC_Value * 0.382 + self.kalman_adc_old * 0.618
        else:
            self.x_k1_k1 = self.kalman_adc_old;

        self.x_k_k1 = self.x_k1_k1
        self.P_k_k1 = self.P_k1_k1 + self.Q
        self.Kg = self.P_k_k1 / (self.P_k_k1 + self.R)

        kalman_adc = self.x_k_k1 + self.Kg * (self.Z_k - self.kalman_adc_old)
        self.P_k1_k1 = (1 - self.Kg) * self.P_k_k1
        self.P_k_k1 = self.P_k1_k1

        self.kalman_adc_old = kalman_adc
        return kalman_adc

def GetSampleTime(timelist):
    "获取时间列表的平均取样时间间隔"
    sampleNum = len(timelist)
    timeInterval = [timelist[j+1] - timelist[j] for j in range(0, sampleNum-1)]
    _timeInterval = np.asarray(timeInterval)
    avgSampleTime = np.mean(_timeInterval)
    return avgSampleTime

if __name__ == '__main__':
    # 读取csv文件
    filename = "low-cost sensor A 04.csv"
    time = [] # 时间节点
    accx = [] # x轴加速度
    accy = [] # y轴加速度
    accz = [] # z轴加速度
    gyrox = [] # x轴角速度
    gyroy = [] # y轴角速度
    gyroz = [] # z轴角速度

    with open(filename, mode="r", newline="", encoding="utf8") as f:
        reader = csv.reader(f)
        header = next(reader) # 文件的第一行是列名行            
        for row in reader:
            time.append(float(row[0]))
            accx.append(float(row[1]))
            accy.append(float(row[2]))
            accz.append(float(row[3]))
            gyrox.append(float(row[4]))
            gyroy.append(float(row[5]))
            gyroz.append(float(row[6]))
    
    # 卡尔曼滤波
    AccX_Filter = Kalman_Filter(0.001, 0.1)
    AccY_Filter = Kalman_Filter(0.001, 0.1)
    AccZ_Filter = Kalman_Filter(0.001, 0.1)
    GyroX_Filter = Kalman_Filter(0.001, 0.1)
    GyroY_Filter = Kalman_Filter(0.001, 0.1)
    GyroZ_Filter = Kalman_Filter(0.001, 0.1)

    sampleTime = GetSampleTime(time)
    sampleNum = len(time)
    timeAxis = np.linspace(0, sampleNum*sampleTime, sampleNum, True)

    filteredAccX = []
    filteredAccY = []
    filteredAccZ = []
    filteredGyroX = []
    filteredGyroY = []
    filteredGyroZ = []
    for i in range (0, sampleNum):
        filteredAccX.append(AccX_Filter.Kalman(accx[i]))
        filteredAccY.append(AccY_Filter.Kalman(accy[i]))
        filteredAccZ.append(AccZ_Filter.Kalman(accz[i]))
        filteredGyroX.append(GyroX_Filter.Kalman(gyrox[i]))
        filteredGyroY.append(GyroY_Filter.Kalman(gyroy[i]))
        filteredGyroZ.append(GyroZ_Filter.Kalman(gyroz[i]))

    # 绘图
    l1, = plt.plot(timeAxis, accx, label="Acceleration X")
    l2, = plt.plot(timeAxis, filteredAccX, label="Kalman Filtered Acceleration X")
    plt.title(filename[0:-4])
    plt.xlabel("Time(s)")
    plt.ylabel("Acceleration X(m/s²)")
    plt.legend(handles=[l1,l2])
    plt.grid()
    plt.show()

    l1, = plt.plot(timeAxis, accy, label="Acceleration Y")
    l2, = plt.plot(timeAxis, filteredAccY, label="Kalman Filtered Acceleration Y")
    plt.title(filename[0:-4])
    plt.xlabel("Time(s)")
    plt.ylabel("Acceleration Y(m/s²)")
    plt.legend(handles=[l1,l2])
    plt.grid()
    plt.show()

    l1, = plt.plot(timeAxis, accz, label="Acceleration Z")
    l2, = plt.plot(timeAxis, filteredAccZ, label="Kalman Filtered Acceleration Z")
    plt.title(filename[0:-4])
    plt.xlabel("Time(s)")
    plt.ylabel("Acceleration Z(m/s²)")
    plt.legend(handles=[l1,l2])
    plt.grid()
    plt.show()

    l1, = plt.plot(timeAxis, gyrox, label="Gyroscope X")
    l2, = plt.plot(timeAxis, filteredGyroX, label="Kalman Filtered Gyroscope X")
    plt.title(filename[0:-4])
    plt.xlabel("Time(s)")
    plt.ylabel("Gyroscope X(rad/s)")
    plt.legend(handles=[l1,l2])
    plt.grid()
    plt.show()

    l1, = plt.plot(timeAxis, gyroy, label="Gyroscope Y")
    l2, = plt.plot(timeAxis, filteredGyroY, label="Kalman Filtered Gyroscope Y")
    plt.title(filename[0:-4])
    plt.xlabel("Time(s)")
    plt.ylabel("Gyroscope Y(rad/s)")
    plt.legend(handles=[l1,l2])
    plt.grid()
    plt.show()

    l1, = plt.plot(timeAxis, gyroz, label="Gyroscope Z")
    l2, = plt.plot(timeAxis, filteredGyroZ, label="Kalman Filtered Gyroscope Z")
    plt.title(filename[0:-4])
    plt.xlabel("Time(s)")
    plt.ylabel("Gyroscope Z(rad/s)")
    plt.legend(handles=[l1,l2])
    plt.grid()
    plt.show()