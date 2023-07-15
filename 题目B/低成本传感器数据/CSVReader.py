import csv
import numpy
from matplotlib import pyplot as plt

def Allan(_list, n=1):
    "list: 要处理的列表；n：分组步长"
    list = numpy.asarray(_list)
    length = len(list)
    K = length // n # 分组数
    sigma = []
    
    for i in range(0, length-1, n):
        s = slice(i,i+n)
        global listtemp
        listtemp = list[s]
        avg = numpy.mean(listtemp)
        sigma.append(avg)
    del(listtemp)
    sum = 0
    for j in range(0, K-2):
        sum += (sigma[j+1]-sigma[j]) ** 2
    delta = sum / 2 / (K - 1)
    return delta

def DAVAR(_dataList, n, windowWidth):
    "_dataList：要处理的列表；_timeList：对应的时间列表；n：Allan方差的分组步长；windowWidth：每个时间点左右各取样数量；time：要观察的时间长度"
    # startTime = _timeList[0]
    # tau = GetSampleTime(_timeList)
    AllanList = []
    length = len(_dataList)
    for index in range(windowWidth, length - windowWidth):
        datatemp = _dataList[index - windowWidth:index + windowWidth]
        Allantemp = Allan(datatemp, n)
        AllanList.append(Allantemp)
        del(datatemp)
    
    return AllanList # 最终，AllanList中将含(length-2windowWidth+1)个元素

def CutList(_dataList, _timeList, time):
    "将列表按时间切片"
    tau = GetSampleTime(_timeList)
    lines = time // tau
    returnList = _dataList[0:lines]
    return returnList

def GetSampleTime(timelist):
    "获取时间列表的平均取样时间间隔"
    sampleNum = len(timelist)
    timeInterval = [timelist[j+1] - timelist[j] for j in range(0, sampleNum-1)]
    _timeInterval = numpy.asarray(timeInterval)
    avgSampleTime = numpy.mean(_timeInterval)
    return avgSampleTime

if __name__ == '__main__':
    filename = "low-cost sensor A 01.csv"
    time = [] # 时间节点
    accx = []
    accy = []
    accz = [] # z轴的加速度
    gyrox = []
    gyroy = []
    gyroz = [] # z轴的角速度

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
    
    # 绘图
    # sampleTime = GetSampleTime(time)
    # DAVAR_accX = numpy.asarray(DAVAR(accx, 2, 10))
    # sampleNum = len(DAVAR_accX)
    # timeAxis = numpy.linspace(0, sampleNum*sampleTime, sampleNum, True)
    # plt.plot(timeAxis,DAVAR_accX)
    # plt.show()
    print(accx, '\n', accy)