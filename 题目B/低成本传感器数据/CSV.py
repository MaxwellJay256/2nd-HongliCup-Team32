import csv

# 写入文件
# newline=""：使两行之间没有空行
# encoding 指定字符集编码
with open('demo.csv', 'w', newline="") as datacsv:
    csvwriter = csv.writer(datacsv, dialect = ("excel"))
    csvwriter.writerow(['A','B','C','D'])
    csvwriter.writerow(['1','2','3','4'])
    csvwriter.writerow(['1','2','3','4'])

## 读取文件
f = open('demo.csv', 'r')
csvreader = csv.reader(f)
#print(next(csvreader)) # 读取现在所处的一行
#print(next(csvreader))
for i in csvreader:
    print(i)

import pandas as pd
filename = 'low-cost sensor A 01.csv'
df = pd.read_csv(filename)
print(df.head()) # head最多显示5行数据

data = df.head()
data.to_csv('demo1.csv', index=False)