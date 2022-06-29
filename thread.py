from random import randint
import threading as th
from datetime import datetime
import multiprocessing



def multi(l1, l2):
    list_proc = []
    lst = ['primeiro', 'sugundo']
    for index, i in enumerate(range(2)):
        proc = multiprocessing.Process(target=primreiro, args=[l1, lst[index]])
        list_proc.append(proc)


    for proc in list_proc:
        proc.start()

    for proc in list_proc:
        proc.join()




def parallel(l1, l2):
    th1 = th.Thread(target=primreiro, args=[l1, 'primeiro'])
    th2 = th.Thread(target=primreiro, args=[l2, 'segundo'])

    th1.start()
    th2.start()

    th1.join()
    th2.join()




def simple(l1, l2):

    primreiro(l1, 'primeiro')
    primreiro(l2, 'segundo')




def primreiro(lista, label):
    print(label)
    for i in range(10000000):
        lista.append(randint(1,1000001))


def segundo(lista):
    print('segundo')
    for i in range(3000000):
        lista.append(randint(1000001,2000001))


l1 =[]
l2 =[]



# print(l_final)
start = datetime.now()

multi(l1, l2)
# parallel(l1, l2)
# simple(l1, l2)

end = datetime.now()

print(f'clock_time {end-start}')