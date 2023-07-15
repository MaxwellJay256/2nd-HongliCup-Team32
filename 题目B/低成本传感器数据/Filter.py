import csv
import numpy
from matplotlib import pyplot as plt

def AverageFilter(list, windowWidth): # 均值滤波
    "list：要滤波的列表；windowWidth：取均值所用的样本数"
    length = len(list)
    filteredList = []
    for index in range(0, length - windowWidth):
        datatemp = numpy.asarray(list[index:index + windowWidth])
        avg = numpy.mean(datatemp)
        filteredList.append(avg)
        del(datatemp)
    return filteredList

def MedianFilter(list, windowWidth): # 中值滤波
    "list：要滤波的列表；windowWidth：取均值所用的样本数"
    length = len(list)
    filteredList = []
    for index in range(0, length - windowWidth):
        datatemp = numpy.asarray(list[index:index + windowWidth])
        avg = numpy.median(datatemp)
        filteredList.append(avg)
        del(datatemp)
    return filteredList

def GetSampleTime(timelist):
    "获取时间列表的平均取样时间间隔"
    sampleNum = len(timelist)
    timeInterval = [timelist[j+1] - timelist[j] for j in range(0, sampleNum-1)]
    _timeInterval = numpy.asarray(timeInterval)
    avgSampleTime = numpy.mean(_timeInterval)
    return avgSampleTime

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

    # 对加速度中值滤波
    windowWidth = 25
    filteredAccX = AverageFilter(accx, windowWidth)
    sampleTime = GetSampleTime(time)
    sampleNum = len(accx)
    timeAxis1 = numpy.linspace(0, sampleNum*sampleTime, sampleNum, True)
    timeAxis2 = numpy.linspace(0, (sampleNum-windowWidth)*sampleTime, sampleNum-windowWidth, True)

    # 绘图
    plt.subplot(2,1,1)
    plt.plot(timeAxis1, accx)
    plt.title("Acceleration X")
    plt.subplot(2,1,2)
    plt.plot(timeAxis2, filteredAccX)
    plt.title("Filtered Acceleration X")
    plt.suptitle(filename[0:-4])
    plt.show()