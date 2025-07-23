my_dict={'alice':'87', 'bob':'90', 'charlie':'85'}
name=input('plz type the name you want to check:')
total=0
if name in my_dict:
    print(my_dict[name])
else:
    print('plz type correct name')
for value in my_dict.values():
    total+=int(value)
average=total/len(my_dict)
print(f'summary is {total},average is {average}')