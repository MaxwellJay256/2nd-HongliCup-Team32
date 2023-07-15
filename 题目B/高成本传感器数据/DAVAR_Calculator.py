import csv
import numpy
from matplotlib import pyplot as plt

def Allan(_list, n):
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

def DisplayGraph(graph, _title, ylist):
    graph.set(title=_title, xlabel='Time(s)')
    graph.set_ylabel('DAVAR', loc='top')
    graph.axis([timeStart, timeEnd, yMin, yMax])
    graph.plot(timeAxis, ylist)
    graph.spines['top'].set_visible(False)
    graph.spines['right'].set_visible(False)
    graph.grid(linewidth=0.2)

if __name__ == '__main__':
    filename = "High quality sensor 05.csv"
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
    
    # 计算DAVAR
    n = 1
    windowWidth = 50
    DAVAR_accX = numpy.asarray(DAVAR(accx, n, windowWidth))
    DAVAR_accY = numpy.asarray(DAVAR(accy, n, windowWidth))
    DAVAR_accZ = numpy.asarray(DAVAR(accz, n, windowWidth))

    DAVAR_gyroX = numpy.asarray(DAVAR(gyrox, n, windowWidth))
    DAVAR_gyroY = numpy.asarray(DAVAR(gyroy, n, windowWidth))
    DAVAR_gyroZ = numpy.asarray(DAVAR(gyroz, n, windowWidth))

    sampleTime = GetSampleTime(time)
    sampleNum = len(DAVAR_accX)
    timeAxis = numpy.linspace(0, sampleNum*sampleTime, sampleNum, True)
    
    # 绘图
    timeStart = 0
    timeEnd = time[-1]
    yMin = -0.005
    yMax = 0.40
    xInterval = 50
    figure1, (graph_AccX, graph_AccY, graph_AccZ) = plt.subplots(nrows=3, ncols=1, sharex=True, sharey=True)

    DisplayGraph(graph_AccX, 'Acceleration X', DAVAR_accX)
    DisplayGraph(graph_AccY, 'Acceleration Y', DAVAR_accY)
    DisplayGraph(graph_AccZ, 'Acceleration Z', DAVAR_accZ)
    plt.xticks(timeAxis[::xInterval])
    #figure.tight_layout()
    plt.suptitle(filename[0:-4])
    plt.show()

    yMin = -0.0001
    yMax = 0.02
    figure2, (graph_GyroX, graph_GyroY, graph_GyroZ) = plt.subplots(nrows=3, ncols=1, sharex=True, sharey=True)
    DisplayGraph(graph_GyroX, 'Gyroscope X', DAVAR_gyroX)
    DisplayGraph(graph_GyroY, 'Gyroscope Y', DAVAR_gyroY)
    DisplayGraph(graph_GyroZ, 'Gyroscope Z', DAVAR_gyroZ)
    plt.xticks(timeAxis[::xInterval])
    plt.suptitle(filename[0:-4])
    plt.show()