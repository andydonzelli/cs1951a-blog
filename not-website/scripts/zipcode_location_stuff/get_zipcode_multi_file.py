import glob
import pathlib
import subprocess
import os
import time

RIDE_PARTS_FOLDER_ABS_PATH = pathlib.Path('/home/ec2-user/all_rides_256_csvs')
RIDE_PARTS_FILE_PATHS = []

for file_path in RIDE_PARTS_FOLDER_ABS_PATH.glob('*.csv'): 
    RIDE_PARTS_FILE_PATHS.append(str(file_path))

script = "/home/ec2-user/scripts/add_zipcode_to_rides_in_csv.py"
processes = set()
max_processes = 80

for csv_file in RIDE_PARTS_FILE_PATHS:
    processes.add(subprocess.Popen(['python3', script, csv_file]))
    if len(processes) >= max_processes:
        os.wait()
        processes.difference_update([p for p in processes if p.poll() is not None])
