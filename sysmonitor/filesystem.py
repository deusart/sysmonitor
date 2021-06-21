import logging
import sysmonitor.files as files
import os, csv, logging

# Setting
logging.basicConfig(filename='log/app.log', filemode='w',format='[%(levelname)s][%(name)s][%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.info('Module Loaded')

def get_space_state(root_disk = 'C:\\'):
    logging.debug(f'Reading from {root_disk}')
    fileslist = []
    for dirpath, dirnames, filenames in os.walk(root_disk):
        fileslist.append(files.get_folder_info(root_disk, dirpath, dirnames, filenames))
        for file in filenames:
            fileslist.append(files.get_file_info(root_disk, dirpath, file))
    
    root = root_disk.replace(':\\','')
    csv_file = f"./storage/{root}_root.csv"
    csv_columns = ['root', 'name','path','parent','file_type','format','level','dirs_count','files_count','size','measure','created_at','updated_at']
    
    logging.debug(f'{len(fileslist)} lines prepared to be saved')
    with open(csv_file, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
        writer.writeheader()
        try:
            for line in fileslist:
                writer.writerow(line)
        except:
            logging.error(line)

    csv_file = f"./storage/{root}_root_total.csv"
    csv_columns = ['root', 'total','used','free']
    total_info = files.get_total_space(root_disk)

    with open(csv_file, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
        writer.writeheader()
        try:
            writer.writerow(total_info)
        except:
            logging.error(line)

# def get_total_space(root_disk = 'C:\\'):
#     total = psutil.disk_usage(root_disk).total / measure_index
#     used = psutil.disk_usage(root_disk).used / measure_index
#     free = psutil.disk_usage(root_disk).free / measure_index
#     with open(csv_file, 'w', encoding='utf-8') as csv_file: