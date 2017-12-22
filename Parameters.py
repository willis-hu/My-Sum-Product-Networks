# coding=utf-8
class Parameters:
    # image attributes
    # 记录图片的属性，分辨率
    imageWidth = 64
    imageHeight = 64
    baseResolution = 4
    # region attributes
    numSumNodePerRegion = 20
    numSumNodePerPixel = 4
    # dataset attributes
    testSetSize = 50
    # learning attributes
    maxIteration = 30
    batchSize = 50
    prior = 1
    thresholdForConvergence = 0.1
