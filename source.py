import ftplib
import os

host = 'v4rts.beget.tech'
user = 'v4rts_test'
password = '1234Bb!'
savePathPrimary = '/Users/macuser/desktop/FTP-FileMonitoring/primaryfiles'
savePathChecksum = '/Users/macuser/desktop/FTP-FileMonitoring/checksumFiles'
con = ftplib.FTP(host, user, password)
con.cwd('/Fba')  

filenames = con.nlst()


for item in filenames:
    host_file = os.path.join(savePathPrimary, item)
    
    try:
        with open(host_file, 'wb') as local_file:
            con.retrbinary('RETR ' + item, local_file.write)
    except ftplib.error_perm:
        pass
 

con.cwd('/FbaSha') 

filenames = con.nlst()


for item in filenames:
    host_file = os.path.join(savePathChecksum, item)
    
    try:
        with open(host_file, 'wb') as local_file:
            con.retrbinary('RETR ' + item, local_file.write)
    except ftplib.error_perm:
        pass

con.quit()


file_list = os.listdir(savePathPrimary)
full_list = [os.path.join(savePathPrimary, i) for i in file_list]
time_sorted_list = sorted(full_list, key = os.path.basename)
print(time_sorted_list)