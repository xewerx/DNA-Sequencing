str11 = 'EEEGABC'
str22 = 'ABCDEEE'

count = 0

def gen_weight(str1, str2):
    for x in range(len(str1)):
        if str2.startswith(str1[0+x:len(str1)]):
            return len(str1[0+x:len(str1)])
    return 0

print(gen_weight(str11, str22))