def addition(num1,num2):
    return num1+num2
def subtraction(num1,num2):
    return num1-num2
def multiplication(num1,num2):
    return num1*num2
def division(num1,num2):
    return num1/num2
print('==计算器==' '1.加法 2.减法 3.乘法 4.除法')
choice=int(input('选择:'))
num1=float(input('请输入第一个数:'))
num2=float(input('请输入第二个数:'))
if choice==1:
    print(f'结果:{num1}+{num2} = {addition(num1,num2)}')
    con=input('是否继续计算? (y/n): ')
    if con.lower() == 'y':  
        num1=float(input('请输入第一个数:'))
        num2=float(input('请输入第二个数:'))
        print(f'结果:{num1}+{num2} = {addition(num1,num2)}')
elif choice==2:
    print(f'结果:{num1}-{num2} = {subtraction(num1,num2)}')
    con=input('是否继续计算? (y/n): ')
    if con.lower() == 'y':
        num1=float(input('请输入第一个数:'))
        num2=float(input('请输入第二个数:'))
        print(f'结果:{num1}-{num2} = {subtraction(num1,num2)}')
elif choice==3:
    print(f'结果:{num1}*{num2} = {multiplication(num1,num2)}')
    con=input('是否继续计算? (y/n): ')
    if con.lower() == 'y':
        num1=float(input('请输入第一个数:'))
        num2=float(input('请输入第二个数:'))
        print(f'结果:{num1}*{num2} = {multiplication(num1,num2)}')
elif choice==4:
    if num2 == 0:
        print("错误: 除数不能为零")
    else:
        print(f'结果:{num1}/{num2} = {division(num1,num2)}')
    con=input('是否继续计算? (y/n): ')
    if con.lower() == 'y':
        num1=float(input('请输入第一个数:'))
        num2=float(input('请输入第二个数:'))
        if num2 == 0:
            print("错误: 除数不能为零")
        else:
            print(f'结果:{num1}/{num2} = {division(num1,num2)}')
else:
    print('无效的选择，请重新运行程序')