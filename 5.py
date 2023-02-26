import pprint
a = []
with open('data/Map8.txt') as file:
    for i in file.readlines():
        b = []
        for j in range(len(i.rstrip())):
            if i[j] not in ['T', 't']:
                if int(i[j]) == 0:
                    b.append(0)
                else:
                    b.append(1)
            else:
                b.append(0)
        a.append(b)
pprint.pprint(a)
