import numbers



def converter(num):
    if isinstance(num, numbers.Number):
        '{:.14f}'.format(num)

# print(['{}: {:.14f}'.format(k,i) for k,i in dic.items()
#         if isinstance(i, numbers.Number)])