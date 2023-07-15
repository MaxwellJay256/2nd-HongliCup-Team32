import numpy

def Allan(_list, n):
    "list: 要处理的列表；n：分组步长"
    list = numpy.asarray(_list)
    length = len(list)
    K = length // n # 分组数
    sigma = []
    
    for i in range(0, length-1, n):
        s = slice(i,i+n)
        avg = numpy.mean(list[s])
        sigma.append(avg)
    for j in range(0, i):
        sum += (sigma[j+1]-sigma[j]) ** 2
    delta = sum / 2 / (K - 1)
    return delta

def GetAllan(y, tau0=1):
    N = len(y)
    NL = N 
    Tau = [] # 保存不同的tau
    Sigma = [] # 保存不同tau下的Allan方差值
    Err = []
    for k in numpy.arange(1, 800):
        sigma_k = numpy.sqrt(1/(2*(NL-1)) * numpy.sum(numpy.power(y[1:NL]-y[0:NL-1], 2))) # Allan的时域表达式
        Sigma.append(sigma_k)
        tau_k = 2 ** (k-1) * tau0 # 将取样时间加倍，tau2 = 2tau1
        Tau.append(tau_k)
        err = 1 / numpy.sqrt(2* (NL-1))
        Err.append(err)
        NL = numpy.floor(NL/2)
        NL = int(NL) 
        if NL < 3: 
            break
        y = 1/2 * (y[0:2*NL:2] + y[1:2*NL:2]) # 对应的序列长度减半
    return Sigma, Tau