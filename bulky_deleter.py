import sys
import os
import shutil
from threading import Thread
from time import sleep, perf_counter
import logging
from datetime import datetime as dt

my_args = sys.argv
my_folder = r""
try:
	my_folder = my_args[1]

except Exception:
	print("Please insert name of folder to delete like>python bulky_deleter.py your:\\folder_name")
try:
	if my_args[2] == "size":
		calculate_size = True
	else:
		calculate_size = False
except:
	calculate_size = False

log_filename='deleted_'+ dt.now().strftime('%Y_%m_%d_%H_%M') +'.log'

logger = logging.getLogger("Deleter") 
logger.setLevel(logging.INFO)
fh = logging.FileHandler(log_filename)
fh.setLevel(logging.INFO)
logger.addHandler(fh)
# logger = logging.getLogger(__name__) 

def remove_file(id,fname):

	# print(f"Task {id}:{fname}")
	try:
		os.remove(fname)
		logger.info(f"Task {id}:{fname}")
	except Exception as e:
		print(str(e))


def main():
	"""This is a comman line tool. This script is deleting folder recursively with threading and save log file.
	Please be carefully what you insert in the command line. """

	dirs = [os.path.join(my_folder,filepath) for filepath in os.listdir(my_folder)]
	files = []
	total_size = 0
	for r,d,f in os.walk(my_folder):
		for fl in f:
			fp =os.path.join(my_folder,r,fl) 
			files.append(fp)
			if not os.path.islink(fp) and calculate_size:
				total_size += os.path.getsize(fp)
	start_time = perf_counter()
	print("Folder to delete:" + my_folder)
	logger.info("Folder to delete:" + my_folder)
	if calculate_size:
		print("Folder size:"+str(total_size))
		logger.info("Total size: "+str(total_size))
	logger.info("File deleting")
	threads =[Thread(target = remove_file, args = (numb, filename)) for numb,filename in enumerate(files)]
	for t in threads:
		t.start()
	for t in threads:
		t.join()
	logger.info("deleted " + str(len(files)))
	logger.info("-"*50)


	try:
		shutil.rmtree(my_folder)
	except Exception as e:
		print(str(e))

	end_time = perf_counter()

	print(f"it took {end_time-start_time}")
	print("Log filename: " + log_filename)
	logger.info("Overall time: "+str(end_time-start_time))




if __name__ == '__main__':
	main()

