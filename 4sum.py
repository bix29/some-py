# -*- coding:utf-8 -*-


#
# 排序求和
#
def fourSum( targetList, sum=0):
    # 先对目标 list 进行一次排序,并获取其长度
    targetList.sort()
    lstLen = len(targetList)

    # 存放最终结果
    res = []


    if lstLen < 4:
         print('False')

    #第一层固定两个元素
    for i in range(lstLen - 2):
        for j in range(i+1, lstLen):
            # 计算出此差值，即为第二层需要查到的两元素的和需要满足的条件
            tmpSum1 = sum - targetList[i] - targetList[j]
            tmpMin = j + 1
            tmpMax = lstLen - 1
            # 第二层，采用双指针移动，寻找两个元素的和为第一层计算出的结果
            while tmpMin < tmpMax:
                tmpSum2 = targetList[tmpMin] + targetList[tmpMax]
                tmpRes = [targetList[i], targetList[j], targetList[tmpMin], targetList[tmpMax]]
                # 找到合适的元素记录并移动指针寻找下一组
                if tmpSum2 == tmpSum1  and tmpRes not in res:
                    res.append(tmpRes)
                    tmpMin += 1
                    tmpMax -= 1
                # 和偏小，讲小值的指针右移（即增加小值）
                elif tmpSum2 < tmpSum1:
                    tmpMin += 1
                # 和偏大， 减小大值
                else:
                    tmpMax -= 1

    if len(res) > 0:
        print(res)
    else:
        print('False')



#
# 大文件筛选
#




# 测试代码

if __name__ == '__main__':
    testList = [1, 2, 4, 0, 5, 3]
    fourSum(testList)
    testList = [1, 2, -2, 0, 5, -1]
    fourSum(testList)

