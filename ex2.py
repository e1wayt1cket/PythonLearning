import copy
lst1 = [[1, 2], [3, 4]]
lst2 = lst1          # 浅拷贝
lst3 = copy.deepcopy(lst1)  
lst1[0][0] = 99
# 深拷贝
# 修改 lst1[0][0] = 99
# 打印 lst2 与 lst3 观察差异
print (lst2)
print (lst3)