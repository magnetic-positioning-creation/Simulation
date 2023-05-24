import time
i = 0
t_start = 0
t_end = 0
while i < 100:
    t = time.time()
    if i == 0:
        t_start = int(round(t*1000000))
        continue
    if i == 99:
        t_end = int(round(t*1000000))
        continue
    i += 1


print(t_start)
print(t_end)

# 00 - 1679573729811528
# 99 - 1679573729812526
