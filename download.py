import ftplib
import os

def FTPdownload(savePath, con):
	filenames = con.nlst()
	for item in filenames:
		host_file = os.path.join(savePath, item)
		try:
			with open(host_file, 'wb') as local_file:
				con.retrbinary('RETR ' + item, local_file.write)
		except ftplib.error_perm:
			pass

def download(host, user, password, savePathPrimary, savePathChecksum):
	con = ftplib.FTP(host, user, password)
	con.cwd('/Fba')  
	FTPdownload(savePathPrimary, con)
	con.cwd('/FbaSha') 
	FTPdownload(savePathChecksum, con)