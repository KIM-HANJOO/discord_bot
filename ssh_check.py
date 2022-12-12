import paramiko
import os

try :
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddpolicy)
    ssh.connect("192.168.219.101", username = "bp", password = "hanjoo970")

    print("ssh connected")
    print(os.getcwd())
    print(os.listdir(os.getcwd()))


    ssh.close()

except Exception as err :
    print(err)


    
