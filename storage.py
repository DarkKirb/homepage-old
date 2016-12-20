import pickle
import os
def get(name, num):
    if not num < count (name):
        raise IndexError
    storagename="data/%s-%i.pickle"%(name,num/50)
    f=open(storagename, "rb")
    data=pickle.load(f)
    f.close()
    if not isinstance(data, list):
        raise ValueError
    return data[num%50]

def put(name, num, val):
    if not num < count (name):
        raise IndexError
    storagename="data/%s-%i.pickle"%(name,num/50)
    f=open(storagename, "rb")
    data=pickle.load(f)
    f.close()
    if not isinstance(data, list):
        raise ValueError
    data[num%50]=val
    f=open(storagename, "wb")
    pickle.dump(data,f,-1)
    f.close()
def append(name, val):
    num=count(name)
    storagename="data/%s-%i.pickle"%(name,num/50)
    data=[]
    try:
        f=open(storagename, "rb")
        data=pickle.load(f)
        f.close()
    except:
        pass
    data.append(val)
    f=open(storagename, "wb")
    pickle.dump(data,f,-1)
    f.close()
def count(name):
    path = "data/"
    files = [i for i in os.listdir(path) if os.path.isfile(os.path.join(path,i))
            and name in i]
    storagename="data/%s-%i.pickle"%(name,len(files)-1)
    count=(len(files)-1)*50
    if len(files) == 0:
        return 0
    f=open(storagename, "rb")
    count = count + len(pickle.load(f))
    f.close()
    return count
