import csv
import numpy as np
from matplotlib import pyplot as plt

def Allan(_list, n):
    "list: 要处理的列表；n：分组步长"
    list = np.asarray(_list)
    length = len(list)
    K = length // n # 分组数
    sigma = []
    
    for i in range(0, length-1, n):
        s = slice(i,i+n)
        global listtemp
        listtemp = list[s]
        avg = np.mean(listtemp)
        sigma.append(avg)
    del(listtemp)
    sum = 0
    for j in range(0, K-2):
        sum += (sigma[j+1]-sigma[j]) ** 2
    delta = sum / 2 / (K - 1)
    return delta

def DAVAR(_dataList, n, windowWidth):
    "_dataList：要处理的列表；_timeList：对应的时间列表；n：Allan方差的分组步长；windowWidth：每个时间点左右各取样数量；time：要观察的时间长度"
    AllanList = []
    length = len(_dataList)
    for index in range(windowWidth, length - windowWidth):
        datatemp = _dataList[index - windowWidth:index + windowWidth]
        Allantemp = Allan(datatemp, n)
        AllanList.append(Allantemp)
        del(datatemp)
    return AllanList # 最终，AllanList中将含(length-2windowWidth+1)个元素

def GetSampleTime(timelist):
    "获取时间列表的平均取样时间间隔"
    sampleNum = len(timelist)
    timeInterval = [timelist[j+1] - timelist[j] for j in range(0, sampleNum-1)]
    _timeInterval = np.asarray(timeInterval)
    avgSampleTime = np.mean(_timeInterval)
    return avgSampleTime

class Kalman_Filter: # Kalman滤波器
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

def DisplayGraph(graph, _title, ylist, filtered_ylist):
    graph.set(title=_title, xlabel='Time(s)') # 标题、x轴标签
    graph.set_ylabel('DAVAR', loc='top') # y轴标签
    graph.axis([timeStart, timeEnd, yMin, yMax])
    l1, = graph.plot(timeAxis, ylist, label=_title)
    l2, = graph.plot(timeAxis, filtered_ylist, label='Filtered '+_title)
    graph.legend(handles=[l1,l2]) # 生成图例
    graph.spines['top'].set_visible(False) # 删除上方边界线
    graph.spines['right'].set_visible(False) # 删除右侧边界线
    graph.grid(linewidth=0.2) # 生成网格线

if __name__ == '__main__':
    filename = "low-cost sensor A 04.csv"
    time = [] # 时间节点
    accx = [] # x轴加速度
    accy = [] # y轴加速度
    accz = [] # z轴加速度
    gyrox = [] # x轴角速度
    gyroy = [] # y轴角速度
    gyroz = [] # z轴角速度

    # 读取.csv文件
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

    # Kalman滤波
    AccX_Filter = Kalman_Filter(0.001, 0.1) # 生成Kalman滤波器
    AccY_Filter = Kalman_Filter(0.001, 0.1)
    AccZ_Filter = Kalman_Filter(0.001, 0.1)
    GyroX_Filter = Kalman_Filter(0.001, 0.1)
    GyroY_Filter = Kalman_Filter(0.001, 0.1)
    GyroZ_Filter = Kalman_Filter(0.001, 0.1)

    filteredAccX = []
    filteredAccY = []
    filteredAccZ = []
    filteredGyroX = []
    filteredGyroY = []
    filteredGyroZ = []
    for i in range (0, len(time)):
        filteredAccX.append(AccX_Filter.Kalman(accx[i]))
        filteredAccY.append(AccY_Filter.Kalman(accy[i]))
        filteredAccZ.append(AccZ_Filter.Kalman(accz[i]))
        filteredGyroX.append(GyroX_Filter.Kalman(gyrox[i]))
        filteredGyroY.append(GyroY_Filter.Kalman(gyroy[i]))
        filteredGyroZ.append(GyroZ_Filter.Kalman(gyroz[i]))

    # 计算DAVAR
    n = 2
    windowWidth = 10
    DAVAR_AccX = np.asarray(DAVAR(accx, n, windowWidth))
    DAVAR_AccY = np.asarray(DAVAR(accy, n, windowWidth))
    DAVAR_AccZ = np.asarray(DAVAR(accz, n, windowWidth))
    DAVAR_Filtered_AccX = np.asarray(DAVAR(filteredAccX, n, windowWidth))
    DAVAR_Filtered_AccY = np.asarray(DAVAR(filteredAccY, n, windowWidth))
    DAVAR_Filtered_AccZ = np.asarray(DAVAR(filteredAccZ, n, windowWidth))

    n = 2
    windowWidth = 10
    DAVAR_GyroX = np.asarray(DAVAR(gyrox, n, windowWidth))
    DAVAR_GyroY = np.asarray(DAVAR(gyroy, n, windowWidth))
    DAVAR_GyroZ = np.asarray(DAVAR(gyroz, n, windowWidth))
    DAVAR_Filtered_GyroX = np.asarray(DAVAR(filteredGyroX, n, windowWidth))
    DAVAR_Filtered_GyroY = np.asarray(DAVAR(filteredGyroY, n, windowWidth))
    DAVAR_Filtered_GyroZ = np.asarray(DAVAR(filteredGyroZ, n, windowWidth))

    sampleTime = GetSampleTime(time)
    sampleNum = len(DAVAR_AccX)
    timeAxis = np.linspace(0, sampleNum*sampleTime, sampleNum, True)

    # 绘图
    timeStart = 0
    timeEnd = time[-1]
    yMin = -0.005
    yMax = 0.16
    xInterval = 60 # x轴刻度间隔
    figure1, (graph_AccX, graph_AccY, graph_AccZ) = plt.subplots(nrows=3, ncols=1, sharex=True, sharey=True)

    DisplayGraph(graph_AccX, 'Acceleration X', DAVAR_AccX, DAVAR_Filtered_AccX)
    DisplayGraph(graph_AccY, 'Acceleration Y', DAVAR_AccY, DAVAR_Filtered_AccY)
    DisplayGraph(graph_AccZ, 'Acceleration Z', DAVAR_AccZ, DAVAR_Filtered_AccZ)
    plt.xticks(timeAxis[::xInterval])
    plt.suptitle(filename[0:-4])
    plt.show()

    yMin = -0.0001
    yMax = 0.005
    figure2, (graph_GyroX, graph_GyroY, graph_GyroZ) = plt.subplots(nrows=3, ncols=1, sharex=True, sharey=True)
    DisplayGraph(graph_GyroX, 'Gyroscope X', DAVAR_GyroX, DAVAR_Filtered_GyroX)
    DisplayGraph(graph_GyroY, 'Gyroscope Y', DAVAR_GyroY, DAVAR_Filtered_GyroY)
    DisplayGraph(graph_GyroZ, 'Gyroscope Z', DAVAR_GyroZ, DAVAR_Filtered_GyroZ)
    plt.xticks(timeAxis[::xInterval])
    plt.suptitle(filename[0:-4])
    plt.show()