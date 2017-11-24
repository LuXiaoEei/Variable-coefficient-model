# Variable-coefficient-model
这是用局部线性核估计的方法估计变系数模型的一个例子。
简单的说下这个例子

考虑如下变系数模型：

Y=a0(U)+a1(U)X1+a2(U)X2+esp

>其中U是[0,1]均匀分布，
>
>X1，X2服从是独立同分布的标准正态分布，
>
>esp服从均值是0标准差是0.8的正态分布，
>
>在模拟中，`a0(u)=8exp{-(u-0.5)^2}`;`a1(u)=2cos(2pi*u)`;`a2(u)=5(u-0.5)^2`

在这里采用的是局部线性光滑的方法处理：

大致的意思是对于给定的点d0，任何点d在d0处有泰勒展开，a0(d)=a0(d0)+a0'(do)+尾项

取Epanechnikov核`K(u)=0.75(1-U^2)+`

用改良的的分块交叉验证GCV的方法进行窗宽h的选择

取样本量100。

![image](https://github.com/LuXiaoEei/Variable-coefficient-model/raw/master/估计图.png)

![交叉验证](https://github.com/LuXiaoEei/Variable-coefficient-model/raw/master/MCV交叉验证.png)


