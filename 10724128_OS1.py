import os
import time
import queue
import threading
import multiprocessing
from datetime import datetime
def PrintCommand() :
    print( "**********************************************************" ) 
    print( "***** OS Projece 1 : Multi-Process V.S. Multi-Thread *****" ) 
    print( "*****------------------------------------------------*****" ) 
    print( "***** 0. EXIT                                        *****" )
    print( "***** 1. 方法1                                       *****" ) 
    print( "***** 2. 方法2                                       *****" ) 
    print( "***** 3. 方法3                                       *****" ) 
    print( "***** 4. 方法4                                       *****" ) 
    print( "請輸入指令:", end='' )
# end PrindCommand()

def LoadFile( filename):
    filename = filename + ".txt"
    if os.path.isfile(filename) :
        return True
    else :
        print("###" + filename + "does not exist!!! ###")
        return False
# end LoadFile()


data = []
mul_data =[]
t1 = 0.0
t2 = 0.0
now_time = ""

def StoreFile(filename):
    data.clear()
    with open(filename, 'r') as file:
        for line in file:
            line = line.rstrip()
            num = int(line)
            data.append(num)
# end StroeFile()


def Job( temp_data, q):
    n = len(temp_data)
    sorted = False
    for _ in range(n) :
        sorted = True                
        for j in range(n-1):              
            if temp_data[j] > temp_data[j+1]:        
                temp_data[j], temp_data[j+1] = temp_data[j+1], temp_data[j]
                sorted = False
        if sorted:
            break

    q.put(temp_data)
# end Job()

def Merge(q1, q2, q):
    lenof_q1 = len(q1)
    lenof_q2 = len(q2)
    temp_q1, temp_q2 = 0, 0
    sort_list = []
    while temp_q1 < lenof_q1 and temp_q2 < lenof_q2 :
        if q1[temp_q1] < q2[temp_q2]:
            sort_list.append( q1[temp_q1] )
            temp_q1 += 1
        else :
            sort_list.append( q2[temp_q2] )
            temp_q2 += 1
    
    if temp_q1 != lenof_q1 :
        sort_list.extend(q1[temp_q1:lenof_q1])
    else :
        sort_list.extend(q2[temp_q2:lenof_q2])

    q.put(sort_list)

def BubbleSort():
    global t1,t2
    global now_time
    n = len(data)
    sorted = False
    t1 = time.time()
    for _ in range(n) :
        sorted = True                
        for j in range(n-1):              
            if data[j] > data[j+1]:        
                data[j], data[j+1] = data[j+1], data[j]
                sorted = False
        if sorted:
            break
    t2 = time.time()
    now_time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

# end BubbleSort()

def WriteFile(filename, com, output_data ):
    t2 = time.time()
    filename = filename + "_output" + com + ".txt" 
    with open(filename, "w") as f :
        for i in output_data:
            f.write(str(i) + '\n')
        temp = "CPU Time : "+ str(t2 - t1) + " seconds"
        f.write(temp + '\n')
        temp = "Output Time : " + now_time
        f.write(temp + '\n')
# end WriteFile()


def SepList( sepNum ):
    n = len(data) 
    lenOfcont = len(data)
    sep_ls = []
    for i in range(sepNum):
        temp = []
        for j in range(i, lenOfcont, sepNum):
            temp.append(data[j])
        sep_ls.append(temp)

    return sep_ls

if __name__ == '__main__':
    PrintCommand()
    com = input()
    while com != "0":
        if com == "1" :
            print("輸入要執行的檔案: ", end = '')
            filename = input()
            while( LoadFile(filename) != True ):
                print("輸入要執行的檔案: ", end = '')
                filename = input()
            StoreFile(filename + ".txt")
            BubbleSort()
            WriteFile(filename,com, data)
        elif com == "2" :
            m_threads = []
            print("輸入要執行的檔案: ", end = '')
            filename = input()
            while( LoadFile(filename) != True ):
                print("輸入要執行的檔案: ", end = '')
                filename = input()
            StoreFile(filename + ".txt")

            sepNum = int(input("請輸入要切成幾分: "))
            sep_list = SepList(sepNum) # get the processed seprated list
            threads = []
            t1 = time.time()
            q = queue.Queue()
            for i in range(sepNum):
                threads.append(threading.Thread(target = Job, args = (sep_list[i], q)))

            count, k = 0, 0
            while count < sepNum or k < sepNum - 1 :
                if count < sepNum:
                    threads[count].start()
                    count += 1
                if q.qsize() >= 2:
                    q1 = q.get()
                    q2 = q.get()
                    m = threading.Thread(target = Merge, args = (q1, q2, q) )
                    m.start()
                    m_threads.append(m)
                    k += 1

            for i in m_threads:
                i.join()

            now_time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
            WriteFile(filename, com, q.get() )

        elif com == "3":
            m_process = []
            print("輸入要執行的檔案: ", end = '')
            filename = input()
            while( LoadFile(filename) != True ):
                print("輸入要執行的檔案: ", end = '')
                filename = input()
            StoreFile(filename + ".txt")

            sepNum = int(input("請輸入要切成幾分: "))
            sep_list = SepList(sepNum) # get the processed seprated list

            manager = multiprocessing.Manager()
            q = manager.Queue(sepNum)
            processes = []
            t1 = time.time()
            for i in range(sepNum):
                processes.append(multiprocessing.Process(target = Job, args = (sep_list[i], q)))
                processes[i].start()
            for i in processes:
                i.join()
            k = 0
            while k < sepNum - 1 :
                if q.qsize() >= 2:
                    q1 = q.get()
                    q2 = q.get()
                    p = multiprocessing.Process(target = Merge, args = (q1, q2, q) )
                    p.start()
                    m_process.append(p)
                    k += 1
            for i in m_process:
                i.join()
            t2 = time.time()
            now_time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
            WriteFile(filename, com, q.get() )
        elif com == "4":
            print("輸入要執行的檔案: ", end = '')
            filename = input()
            while( LoadFile(filename) != True ):
                print("輸入要執行的檔案: ", end = '')
                filename = input()
            StoreFile(filename + ".txt")

            sepNum = int(input("請輸入要切成幾分: "))
            sep_list = SepList(sepNum) # get the processed seprated list
            t1 = time.time()
            q = queue.Queue()
            for i in range(sepNum):
                Job(sep_list[i], q)
            k = 0
            while k < sepNum - 1 :
                if q.qsize() >= 2:
                    q1 = q.get()
                    q2 = q.get()
                    Merge(q1,q2,q)
                    k += 1
            t2 = time.time()
            now_time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
            WriteFile(filename, com, q.get() )
        else :
            print( "指令不存在，請從新輸入" )
        PrintCommand()
        com = input()
