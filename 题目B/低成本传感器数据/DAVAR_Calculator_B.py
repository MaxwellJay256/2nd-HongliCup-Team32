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

def GetSampleTime(timelist):
    "获取时间列表的平均取样时间间隔"
    sampleNum = len(timelist)
    timeInterval = [timelist[j+1] - timelist[j] for j in range(0, sampleNum-1)]
    _timeInterval = numpy.asarray(timeInterval)
    avgSampleTime = numpy.mean(_timeInterval)
    return avgSampleTime

def DisplayGraph(graph, _title, ylist, timeList, timeStart, timeEnd):
    graph.set(title=_title, xlabel='Time(s)') # 标题、x轴标签
    graph.set_ylabel('DAVAR', loc='top') # y轴标签
    graph.axis([timeStart, timeEnd, yMin, yMax])
    graph.plot(timeList, ylist)
    graph.spines['top'].set_visible(False) # 删除上方边界线
    graph.spines['right'].set_visible(False) # 删除右侧边界线
    graph.grid(linewidth=0.2) # 生成网格线

if __name__ == '__main__':
    time1 = [] # Acc时间节点
    time2 = [] # Gyro时间节点
    accx = [] # x轴加速度
    accy = [] # y轴加速度
    accz = [] # z轴加速度
    gyrox = [] # x轴角速度
    gyroy = [] # y轴角速度
    gyroz = [] # z轴角速度

    # 读取.csv文件
    filename1 = "low-cost sensor B 10 Acc.csv"
    with open(filename1, mode="r", newline="", encoding="utf8") as f:
        reader = csv.reader(f)
        header = next(reader) # 文件的第一行是列名行
        for row in reader:
            time1.append(float(row[0]))
            accx.append(float(row[1]))
            accy.append(float(row[2]))
            accz.append(float(row[3]))
    filename2 = 'low-cost sensor B 10 Gyro.csv'
    with open(filename2, mode="r", newline="", encoding="utf8") as f:
        reader = csv.reader(f)
        header = next(reader) # 文件的第一行是列名行
        for row in reader:
            time2.append(float(row[0]))
            gyrox.append(float(row[1]))
            gyroy.append(float(row[2]))
            gyroz.append(float(row[3]))
    
    # 计算DAVAR
    n = 2
    windowWidth = 20
    DAVAR_accX = numpy.asarray(DAVAR(accx, n, windowWidth))
    DAVAR_accY = numpy.asarray(DAVAR(accy, n, windowWidth))
    DAVAR_accZ = numpy.asarray(DAVAR(accz, n, windowWidth))

    DAVAR_gyroX = numpy.asarray(DAVAR(gyrox, n, windowWidth))
    DAVAR_gyroY = numpy.asarray(DAVAR(gyroy, n, windowWidth))
    DAVAR_gyroZ = numpy.asarray(DAVAR(gyroz, n, windowWidth))

    sampleTime1 = GetSampleTime(time1)
    sampleNum1 = len(DAVAR_accX)
    timeAxis1 = numpy.linspace(0, sampleNum1*sampleTime1, sampleNum1, True)
    sampleTime2 = GetSampleTime(time2)
    sampleNum2 = len(DAVAR_gyroX)
    timeAxis2 = numpy.linspace(time2[0], sampleNum2*sampleTime2, sampleNum2, True)
    
    # 绘图
    timeStart1 = time1[0]
    timeEnd1 = time1[-1]
    yMin = -0.001
    yMax = 0.5
    xInterval = 60
    figure1, (graph_AccX, graph_AccY, graph_AccZ) = plt.subplots(nrows=3, ncols=1, sharex=True, sharey=True)
    DisplayGraph(graph_AccX, 'Acceleration X', DAVAR_accX, timeAxis1, timeStart1, timeEnd1)
    DisplayGraph(graph_AccY, 'Acceleration Y', DAVAR_accY, timeAxis1, timeStart1, timeEnd1)
    DisplayGraph(graph_AccZ, 'Acceleration Z', DAVAR_accZ, timeAxis1, timeStart1, timeEnd1)
    plt.xticks(timeAxis1[::xInterval])
    #figure.tight_layout()
    plt.suptitle(filename1[0:20])
    plt.show()

    timeStart2 = time2[0]
    timeEnd2 = time2[-1]
    yMin = -0.000
    yMax = 0.07
    figure2, (graph_GyroX, graph_GyroY, graph_GyroZ) = plt.subplots(nrows=3, ncols=1, sharex=True, sharey=True)
    DisplayGraph(graph_GyroX, 'Gyroscope X', DAVAR_gyroX, timeAxis2, timeStart2, timeEnd2)
    DisplayGraph(graph_GyroY, 'Gyroscope Y', DAVAR_gyroY, timeAxis2, timeStart2, timeEnd2)
    DisplayGraph(graph_GyroZ, 'Gyroscope Z', DAVAR_gyroZ, timeAxis2, timeStart2, timeEnd2)
    plt.xticks(timeAxis2[::xInterval])
    plt.suptitle(filename2[0:20])
    plt.show()