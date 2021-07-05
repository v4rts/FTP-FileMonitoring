import ftplib
import os
import time
from hashlib import sha256

host = 'v4rts.beget.tech'
user = 'v4rts_test'
password = '1234Bb!'
savePathPrimary = '/Users/macuser/desktop/FTP-FileMonitoring/primaryfiles'
savePathChecksum = '/Users/macuser/desktop/FTP-FileMonitoring/checksumFiles'

def FTPdownload(savePath, con):
	filenames = con.nlst()
	for item in filenames:
		host_file = os.path.join(savePath, item)
		try:
			with open(host_file, 'wb') as local_file:
				con.retrbinary('RETR ' + item, local_file.write)
		except ftplib.error_perm:
			pass

def getDirectorySize(dir):
	size = 0
	for path, dirs, files in os.walk(dir):
		for f in files:
			fp = os.path.join(path, f)
			size += os.path.getsize(fp)
	return size

def getSortedFileList(dir):
	file_list = os.listdir(dir)
	full_list = [os.path.join(dir, i) for i in file_list]
	sorted_list = sorted(full_list, key = os.path.basename)
	return sorted_list

def fileDownload(fn, pathFile):
    import ftplib
    ftp = ftplib.FTP('v4rts.beget.tech')
    ftp.login('v4rts_test','1234Bb!')
    ftp.cwd('Fba')
    needFile = os.path.join(pathFile,fn)
    file = open(needFile, 'wb')
    ftp.retrbinary('RETR ' + fn, file.write)
    ftp.quit()

def makeFileArray(path, fileNameArray):
    fileArray = []
    for file in fileNameArray:
        fileArray.append(os.path.join(path, file))
    #sorted_list = sorted(fileArray, key = os.path.basename)
    #return sorted_list
    return fileArray

def brokenFilesRecovery(pathFile, pathCheckSum):
    sha256Make = []
    sha256Download = []
 
    fileArray = makeFileArray(pathFile, os.listdir(pathFile))

    for file in fileArray:
        with open(file, "r") as f:
            fRead = f.read()
            sha256Make.append(sha256(fRead.encode('utf-8')).hexdigest())

    for i in range(0, len(os.listdir(pathFile))):
       sha256Make[i] = sha256Make[i] + " " + os.listdir(pathFile)[i]

    fileArray2 = makeFileArray(pathCheckSum, os.listdir(pathCheckSum))
    
    for file in fileArray2:
        with open(file, "r") as f:
            fRead = f.read()
            sha256Download.append(fRead)

    for i in range(0, len(sha256Make)-1):
    	flag = False
    	for j in range(0, len(sha256Make)-1):
    		if(sha256Make[i] == sha256Download[j]):
    			flag = True
    	if (flag):
    		print("Success. " + os.listdir(pathFile)[i])
    	else:
            print("Does not match. Download " + sha256Make[i])
            fileDownload(os.listdir(pathFile)[i], pathFile)

while True:
	
	looptime = time.time()
	con = ftplib.FTP(host, user, password)

	con.cwd('/Fba')  
	FTPdownload(savePathPrimary, con)
 
	con.cwd('/FbaSha') 
	FTPdownload(savePathChecksum, con)

	brokenFilesRecovery(savePathPrimary, savePathChecksum)

	total_size  = getDirectorySize(savePathPrimary)
	print("Directory size: " + str(total_size) + " bytes")

	while (total_size > 1048576):
		sorted_filelist = getSortedFileList(savePathPrimary)
		sorted_sumlist = getSortedFileList(savePathChecksum)
		os.remove(sorted_filelist[0])
		os.remove(sorted_sumlist[0])
		print("File " +  str(sorted_filelist[0]) +  "deleted")
		total_size  = getDirectorySize(savePathPrimary)
		print("Directory size: " + str(total_size) + " bytes")

	looptime = time.time() - looptime
	print("Time for this loop: " + str(looptime) + " seconds") 
	time.sleep(120-looptime)

