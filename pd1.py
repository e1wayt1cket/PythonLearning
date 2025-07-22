import numpy as np
a=np.arange(0,12).reshape(3,4)
a1=a.sum(axis=None)
a2=a.mean(axis=0)        # 每列
a3=a.std(), a.var(), a.min(), a.max()
a4=a.argmin(), a.argmax()
a5=np.median(a, axis=1)
a6=np.percentile(a, 50, axis=0)
print(a1,a2,a3,a4,a5,a6)