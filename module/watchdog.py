import os

cwdir = os.getcwd()
os.chdir(os.path.join(cwdir, 'tmp'))

print(os.path.getmtime('hi.txt'))
tmptime = getmtime('hi.txt')


