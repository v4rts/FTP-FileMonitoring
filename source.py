import ftplib
import os
import time
from hashlib import sha256
from download import *
from rotation import *
from diagnostic import *

host = 'v4rts.beget.tech'
user = 'v4rts_test'
password = '1234Bb!'
savePathPrimary = '/Users/macuser/desktop/FTP-FileMonitoring/primaryfiles'
savePathChecksum = '/Users/macuser/desktop/FTP-FileMonitoring/checksumFiles'

while True:
	
	looptime = time.time()

	download(host, user, password, savePathPrimary, savePathChecksum)

	brokenFilesRecovery(savePathPrimary, savePathChecksum)

	fileRotation(savePathPrimary, savePathChecksum)

	looptime = time.time() - looptime
	print("Time for this loop: " + str(looptime) + " seconds") 
	time.sleep(120-looptime)

