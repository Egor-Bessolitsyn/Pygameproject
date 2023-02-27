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

m = [[0 for i in range(24)] for _ in range(24)]

start = 2, 2
end = 7, 15
m[start[0]][start[1]] = 1


def make_step(k):
    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j] == k:
                if i > 0 and m[i - 1][j] == 0 and a[i - 1][j] == 0:
                    if j < 23 and m[i - 1][j + 1] == 0 and a[i - 1][j + 1] == 0:
                        m[i - 1][j] = k + 1
                        # m[i - 1][j + 1] = k + 1
                if j > 0 and m[i][j - 1] == 0 and a[i][j - 1] == 0:
                    if i < 23 and m[i + 1][j - 1] == 0 and a[i + 1][j - 1] == 0:
                        m[i][j - 1] = k + 1
                        # m[i + 1][j - 1] = k + 1
                if i < len(m) - 2 and m[i + 1][j] == 0 and a[i + 1][j] == 0 and not a[i + 2][j]:
                    if j < 22 and m[i + 1][j + 1] == 0 and a[i + 1][j + 1] == 0 and not a[i + 2][j + 1]:
                        m[i + 1][j] = k + 1
                        # m[i + 1][j + 1] = k + 1
                if j < len(m[i]) - 2 and m[i][j + 1] == 0 and a[i][j + 1] == 0 and not a[i][j + 2]:
                    if i < 22 and m[i + 1][j + 1] <= k + 1 and a[i + 1][j + 1] == 0 and not a[i + 1][j + 2]:
                        m[i][j + 1] = k + 1
                        # m[i + 1][j + 1] = k + 1


k = 0
while m[end[0]][end[1]] == 0:
    k += 1
    make_step(k)

for i in m:
    print(i)

i, j = end
k = m[i][j]
The_Path = [(i, j)]
while k > 1:
    if i > 0 and j < 23 and m[i - 1][j] == k - 1:
        i, j = i - 1, j
        The_Path.append((i, j))
        k -= 1
    elif j > 0 and i < 23 and m[i][j - 1] == k - 1:
        i, j = i, j - 1
        The_Path.append((i, j))
        k -= 1
    elif i < len(m) - 1 and m[i + 1][j] == k - 1:
        i, j = i + 1, j
        The_Path.append((i, j))
        k -= 1
    elif j < len(m[i]) - 1 and m[i][j + 1] == k - 1:
        i, j = i, j + 1
        The_Path.append((i, j))
        k -= 1

The_Path = The_Path[::-1]
print(The_Path)
