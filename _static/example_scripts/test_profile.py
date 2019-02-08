import profile

def funcShort():
    for i in range(1000):
        pass

def funcLong():
    for i in range(1000):
        s = '%i'%(i*i + (i+2)**2)

def func2():
    for i in range(1000):
        funcShort()
        funcLong()

profile.run("func2()")


