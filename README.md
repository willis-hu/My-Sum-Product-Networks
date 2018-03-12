Sum-Product-Networks
====================
Author  : Chengcheng Zhao
Contact : chengcheng.zcc@alibaba-inc.com

This package adapts Hoifung Poon's Java code for Sum-Product Networks.
It is purely implemented in Python without any optimization so far. For
now, it is basicly for personal interests, but I hope to get any feedbacks
from anyone who is also interested in Sum-Product Networks.

This package is not well tested, it may contain some bugs.

Enjoy it!

Reference:
Sum-Product Networks: A New Deep Architecture, Hoifung Poon and Pedro Domingos

原项目作者已删除项目，项目中两项bug已修复。
---- BUG

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
