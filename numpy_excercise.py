# coding=gbk
import numpy as np
"""
ndarray����ָ�����ݵ�ָ�룬dtype��shape�����Ԫ�飨stride��ǰ������ǰά����һ��Ԫ����Ҫ������ֽ�����
"""
#����ndarray
a = np.array([1,2,3])
a = np.array((1,2,3))#���Դ����κ�����
a = np.arange(4)#(0,1,2,3)

a = np.array([[1,2],[3,4]])
a = np.array([1,2,3,4,5],ndmin=2)#[[1,2,3,4,5]]
a = np.array([1,2,3],dtype=complex)#[1.+0.j 2.+0.j 3.+0.j]

a = np.zeros((3,4))
a = np.ones((3,4))
a = np.linspace(0,2*np.pi,5)
a = np.logspace(1.0,  2.0, num =  10)

#��Ƭ
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
������Ϣ��dtype��������, sizeԪ�ظ���, shape��״, itemsize���ݴ�С, ndim, nbytes
"""
"""
���������� reshape, + - * /(������Ԫ�ؼ���)��dot ��� 
"""
a = np.arange(12).reshape(3,4)
b = np.arange(12).reshape(3,4)
print(a<b)
a = np.arange(9).reshape(3,3)
b = np.array([[1,0,0],[0,1,0],[0,0,1]])
print(b.dot(a))
"""
��������� sum min max cumsum
"""
print(a[1].sum())
print(a.cumsum())
"""
��������
"""
a=np.arange(0,100,10)
b=[4,3,5]
print(a[b])#��ȡ�ض�Ԫ�� ��ʽ����

#��������   �����鴫�ݸ��漰���������
import matplotlib.pyplot as plt
a = np.linspace(0, 2 * np.pi, 50)
b = np.sin(a)
plt.plot(a,b)
mask = b >= 0
plt.plot(a[mask], b[mask], 'bo')
mask = (b >= 0) & (a <= np.pi / 2)
plt.plot(a[mask], b[mask], 'go')
plt.show()

#ȱʡ����
a = np.arange(0,100,10)
c = a[a>=50]
print(c)

#where ����
a = np.arange(0,100,10)
b = np.where(a<50)
print(b)[0]

#ͳ�ƺ���
np.amax(a,0) #����������Сֵ
np.amin(a,1)
np.ptp(a)    #������Ԫ�ص����ֵ����Сֵ

#��������ˢѡ


