import random

t = []

for i in range(1024):
    n = random.randint(-1000,1000)
    t.append(n)
print(t)
t.sort()
print("-------------------------------------------------------")
i=0
while i < len(t):
    if (t[i] <= 0):
        t.pop(i) # Возвращает элемент [на указанной позиции], удаляя его из списка.
    else:
        i+=1
print(t)


