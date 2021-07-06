import os

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


def fileRotation(savePathPrimary, savePathChecksum):
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
