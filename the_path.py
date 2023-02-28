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

a = [[0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
     [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
     [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
     [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
     [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
     [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
     [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
     [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1],
     [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1],
     [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
     [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
     [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
     [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
     [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
     [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
     [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1],
     [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1],
     [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
     [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
     [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
     [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
     [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
     [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
     [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]]

m = [[0 for i in range(24)] for _ in range(24)]

start = 13, 8
end = 9, 12
m[start[0]][start[1]] = 1
visited_old = [(start)]
visited_new = []


def make_step(k):
    for cell in visited_old:
        i, j = cell[0], cell[1]
        if m[i][j] == k:
            if i > 0 and j < len(m[i]) - 1 and m[i - 1][j] == 0 and a[i - 1][j] == 0 and not a[i - 1][j + 1]:
                # if j < 23 and m[i - 1][j + 1] == 0 and a[i - 1][j + 1] == 0:
                m[i - 1][j] = k + 1
                visited_new.append((i - 1, j))
                    # m[i - 1][j + 1] = k + 1
            if j > 0 and i < 23 and m[i][j - 1] == 0 and a[i][j - 1] == 0 and not a[i + 1][j - 1]:
                # if i < 23 and m[i + 1][j - 1] == 0 and a[i + 1][j - 1] == 0:
                m[i][j - 1] = k + 1
                visited_new.append((i, j - 1))
                    # m[i + 1][j - 1] = k + 1
            if i < len(m) - 2 and j < 23 and m[i + 1][j] == 0 and a[i + 1][j] == 0 and not a[i + 2][j] and not a[i + 1][j + 1]  and not a[i + 2][j + 1]:
                # if j < 22 and m[i + 1][j + 1] == 0 and a[i + 1][j + 1] == 0 and not a[i + 2][j + 1]:
                m[i + 1][j] = k + 1
                visited_new.append((i + 1, j))
                    # m[i + 1][j + 1] = k + 1
            if j < len(m[i]) - 2 and i < 23 and m[i][j + 1] == 0 and a[i][j + 1] == 0 and not a[i][j + 2] and not a[i + 1][j + 1] and not a[i + 1][j + 2]:
                # if i < 22 and m[i + 1][j + 1] <= k + 1 and a[i + 1][j + 1] == 0 and not a[i + 1][j + 2]:
                m[i][j + 1] = k + 1
                visited_new.append((i, j + 1))
                    # m[i + 1][j + 1] = k + 1

k = 0
while m[end[0]][end[1]] == 0:
    k += 1
    make_step(k)
    visited_old = visited_new[:]
    visited_new = []
    # for i in m:
    #     for j in i:
    #         print('{:4}'.format(j), end=' ')
    #     print()
    # print()

for i in m:
    for j in i:
        print('{:4}'.format(j), end=' ')
    print()

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
