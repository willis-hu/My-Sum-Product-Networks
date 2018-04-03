Sum-Product-Networks

Reference:
Sum-Product Networks: A New Deep Architecture, Hoifung Poon and Pedro Domingos



原项目作者已删除项目，项目中两项bug已修复。
#### BUG

1. allocateSumNode(),分配相同地址的SumNode。
2. initUnitRegion()，counts赋值错误。

使用解析:
1. Dataset.py
  - col是表示一列数据的矩阵，计算得到的img表示该列中每行数据占的比例。img的一列数据之和为1。

2. 步骤
  - 对于coarseRegion进行记录。
  - 记录fineRegion，分为PixelRegion和FineRegion。PixelRegion记录行差和列差均为1的区域。PixelRegion相当于用顶点标记的单位区域。
  - 对于PixelRegion，会进行一个__initUnitRegion方法的操作。
  - 行、列差递增，记录各个不同行列差的区域。
  - 再一次增加rowStepSize和colStepSize，记录64*64区域中所有的fineRegion。

3. region
  - region.coarseRegionId记录行差或者列差大于4的区域，即大于4*4的区域。总计18240个coarseRegion。即记录64*64图片中所有大于4*4的区域。
  - 显示时先显示列，后显示行。
  - initialize
    - 对于大于4*4的区域，每个区域分配20个sum节点，依次计算(0,4,0,8)到(60,64,56,64),端点按4增加。对整个64*64只分配1个节点。
    - 对于小于4*4的区域，每个分配20个sum节点。端点按4批次增加。若区域边为1，则标注为单位区域,分配4个sum节点。region.values记录每个实例中该区域左上角的数值。并对value进行排序。region.means记录每个实例该位置的均值，从大到小排列。variance记录每个实例该位置的方差。counts记录该位置实例个数。
  - MAPinference
    - 将instance值输入到对应region中，每个region记录该区域左上角的值。区域均为1*1大小。
    - 每个节点的logvalue记录该(-((value - mean)^2) / 2)。4个sumNode与4个mean值对应。
    - region.decompOption记录该区域的最优分解。

NOTE:
SPN两个特征：
    1. 每个节点有自己的语义。
    2. 能进行推导的概率图模型。

P节点相当于神经网络中的 ***激活函数***。

三种概率图模型对比：
  - 贝叶斯网络，intractable推导。
  - 马尔可夫网。intractable推导。
  - SPN。tractable推导。

SPN显示了多个随机变量之间的 ***联合分布*** 。

一个概率图表示：![概率图](H:\a_huqigen\Markdown笔记\图片\spn-概率图.png)
可以理解为：一个人选择购买衣服，看中了两件衣服，一件上衣一件裤子。找三个专家来评判买或者不买,A,B精通买上衣，C精通买裤子。找专家的过程包括：掷骰子，决定找AC或者BC，A给出的意见是20%不买，80%买。B给出的意见是10%不买，90%买。C给出的意见是40%不买，60%买。那么最终买全套或者买裤子或者买上衣的概率计算，可以通过在spn上的推导获得。

SPN中，sum节点代表着 **隐变量**，product节点代表 **因式分解**。

SPN中的学习可以分为 **权重学习** 和 **结构学习**，结构学习中包括 **变量分离** 和 **样本聚类** 。

先给SPN中的边权重一个稀疏先验，之后再通过梯度下降法更新权重。在已知权重时，每个节点上的值是可以计算得到的，根据梯度更新公式∂S(x)/∂wij =(∂S(x)/∂Si(x))Sj(x),可以自上而下更新权重的值。
