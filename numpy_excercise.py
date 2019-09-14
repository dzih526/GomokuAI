# coding=gbk
import numpy as np
"""
ndarray对象：指向数据的指针，dtype，shape，跨度元组（stride，前进道当前维度下一个元组需要跨过的字节数）
"""
#创建ndarray
a = np.array([1,2,3])
a = np.array((1,2,3))#可以传递任何序列
a = np.arange(4)#(0,1,2,3)

a = np.array([[1,2],[3,4]])
a = np.array([1,2,3,4,5],ndmin=2)#[[1,2,3,4,5]]
a = np.array([1,2,3],dtype=complex)#[1.+0.j 2.+0.j 3.+0.j]

a = np.zeros((3,4))
a = np.ones((3,4))
a = np.linspace(0,2*np.pi,5)
a = np.logspace(1.0,  2.0, num =  10)

#切片
a = np.array([[11, 12, 13, 14, 15],
              [16, 17, 18, 19, 20],
              [21, 22, 23, 24, 25],
              [26, 27, 28 ,29, 30],
              [31, 32, 33, 34, 35]])
print(a[0,1:4])
print(a[1:3,0])
print(a[::2,::2])
print(a[:,1])

"""
数组信息：dtype数据类型, size元素个数, shape形状, itemsize数据大小, ndim, nbytes
"""
"""
基本操作符 reshape, + - * /(都是逐元素计算)，dot 点积 
"""
a = np.arange(12).reshape(3,4)
b = np.arange(12).reshape(3,4)
print(a<b)
a = np.arange(9).reshape(3,3)
b = np.array([[1,0,0],[0,1,0],[0,0,1]])
print(b.dot(a))
"""
特殊运算符 sum min max cumsum
"""
print(a[1].sum())
print(a.cumsum())
"""
索引进阶
"""
a=np.arange(0,100,10)
b=[4,3,5]
print(a[b])#获取特定元素 花式索引

#布尔屏蔽   将数组传递个涉及数组的条件
import matplotlib.pyplot as plt
a = np.linspace(0, 2 * np.pi, 50)
b = np.sin(a)
plt.plot(a,b)
mask = b >= 0
plt.plot(a[mask], b[mask], 'bo')
mask = (b >= 0) & (a <= np.pi / 2)
plt.plot(a[mask], b[mask], 'go')
plt.show()

#缺省索引
a = np.arange(0,100,10)
c = a[a>=50]
print(c)

#where 函数
a = np.arange(0,100,10)
b = np.where(a<50)
print(b)[0]

#统计函数
np.amax(a,0) #沿轴的最大最小值
np.amin(a,1)
np.ptp(a)    #数组中元素的最大值与最小值

#排序、条件刷选


