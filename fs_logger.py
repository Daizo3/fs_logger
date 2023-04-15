# fs_logger.py

import csv
import datetime
from pathlib import Path
import os

FILE_LIST_IN = 'filelist.csv'   # file list in fullpath
CSV_HEADER= ["at","fullpath","name","size","timestamp"]
LOG_FILE_BASE_NAME='fs_log'
LOG_FILE_DIRECTORY='.\\fs_log'
MAX_LOG_FILE = 24   # keeps 24 months of log

def get_info(fullpath: str):
    """
        get file information with current time
        current time, fullpath, name, size, timestamp
    """
    info=[]
    ct = datetime.datetime.now()
    info.append(ct)
    info.append(fullpath)

    if not os.path.exists(fullpath):
        info.append('NA')
        info.append(0)
        info.append('NA')
        return info
    
    fp = Path(fullpath)
    info.append(fp.name)
    info.append(os.path.getsize(fp))
    ts = datetime.datetime.fromtimestamp(fp.stat().st_mtime)
# 2023-04-15 replaced to above
#    ts = datetime.datetime.fromtimestamp(fp.stat().st_ctime)
    info.append(ts)
    return info


def log_filename() -> str:
    """
        get log csv file name with yyyy-mm date data
    """

    filename = datetime.date.today().isoformat()[:7] + ' ' + LOG_FILE_BASE_NAME + '.csv'
    fullpath = LOG_FILE_DIRECTORY + '\\' + filename
    return fullpath

def check_log_directory():
    """
        check log directory exists and make it if it is not exist
    """
    if os.path.exists(LOG_FILE_DIRECTORY):
        return
    os.mkdir(LOG_FILE_DIRECTORY)


def main():
    """
        file size logger. log size and timestamp by files specified in FILE_LIST_IN.
    """

    # get file list
    with open(FILE_LIST_IN,'r',encoding='utf-8') as fin:
        cin = csv.reader(fin)
        files = [row for row in cin]

    # get file information
    logs=[]
    for file in files:
        info = get_info(file[0])
        logs.append(info)

    # set up log csv file
    fs_log = log_filename()

    write_header = False
    if not os.path.exists(fs_log):
        write_header=True

    # write out to log csv file
    with open(fs_log,'a',encoding='utf-8') as fout:
        cout = csv.writer(fout,lineterminator='\n')
        if write_header:            
            cout.writerow(CSV_HEADER)
        cout.writerows(logs)

def remove_oldest_log():
    """
        remove the oldest log if number of log is more than MAX_LOG_FILE
        created: 2023/03/25
    """
    files = os.listdir(LOG_FILE_DIRECTORY)
    if len(files)<=MAX_LOG_FILE:
        return
    files.sort()
    os.remove(LOG_FILE_DIRECTORY + '\\' + files[0])

if __name__ == '__main__':
    print('This is fs_logger, thanks.')
    main()
    remove_oldest_log()
