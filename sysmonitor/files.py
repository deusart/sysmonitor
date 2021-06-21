import os, time, logging, configparser, psutil
# Setting
logging.basicConfig(filename='log/app.log', filemode='w',format='[%(levelname)s][%(name)s][%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.info('Module Loaded')
config = configparser.ConfigParser()
config.read("settings.ini")
filesystem = config['Filesystem']

def _get_name(dirpath):
    if str.find(dirpath,'\\') != -1:    
        if str.find(dirpath,'\\') < len(dirpath)-1:
            return dirpath[str.rindex(dirpath,'\\')+1:]
        else:
            return dirpath
    else:
        return ''

def _get_parent_path(dirpath):
    if str.find(dirpath,'\\') != -1:    
        if str.find(dirpath,'\\') < len(dirpath)-1:
            return dirpath[:str.rindex(dirpath,'\\')]
        else:
            return dirpath
    else:
        return ''

def _get_format(filename):
    if str.find(filename,'.') != -1:
        return filename[str.rindex(filename,'.'):]
    else:
        return ''
        
def _get_level(dirpath):
    path_list = dirpath.split('\\')
    if path_list[1] == '':
        level = 1
    else:
        level = len(path_list)
    return level - 1

def _get_measure_index(measure = filesystem['measure']):
    if measure in ('b', 'bytes'):
        measure_index = 1
    elif measure in ('kb', 'KB'):
        measure_index = 1000
    elif measure.lower() in ('mb', 'MB', 'mb'):
        measure_index = 1000000
    else:
        measure_index = 1    
    return measure_index

def _get_file_size(path, file, measure = filesystem['measure']):
    try:
        measure_index = _get_measure_index(measure)
        filepath = os.path.join(path, file)
        return os.path.getsize(filepath) / measure_index
    except Exception as err:
        logging.error(f'[Path]: {path} [File]: {file} issue ' + str(err))

def _get_time(path, time_type = 'c'):
    try:
        if time_type == 'c':
            return time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime(os.path.getctime(path)))
        if time_type == 'm':
            return time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime(os.path.getmtime(path)))
    except Exception as err:
        logging.error(f'[File]: {path} issue ' + str(err))
    

def get_folder_info(root_disk, dirpath, dirnames, filenames):
    file = {}
    file['root'] = root_disk
    file['name'] = _get_name(dirpath)
    file['path'] = dirpath
    file['parent'] = _get_parent_path(dirpath)
    file['file_type'] = 'folder'
    file['format'] = 'folder'
    file['level'] = _get_level(dirpath) - 1
    file['dirs_count'] = len(dirnames)
    file['files_count'] = len(filenames)
    file['size'] = 0
    file['measure'] = filesystem['measure']
    file['created_at'] = _get_time(dirpath, 'c')
    file['updated_at'] = _get_time(dirpath, 'm')

    return file

def get_file_info(root_disk, dirpath, filename):
    file = {}
    file['root'] = root_disk
    file['name'] = filename
    file['path'] = os.path.join(dirpath, filename)
    file['parent'] = dirpath
    file['file_type'] = 'file'
    file['format'] = _get_format(filename)
    file['level'] = _get_level(dirpath) - 1
    file['dirs_count'] = 0
    file['files_count'] = 0
    file['size'] = _get_file_size(dirpath, filename)
    file['measure'] = filesystem['measure']
    file['created_at'] = _get_time(file['path'], 'c')
    file['updated_at'] = _get_time(file['path'], 'm')

    return file

def get_total_space(root_disk = 'C:\\', measure = filesystem['measure']):
    measure_index = _get_measure_index(measure)
    total_info = {}
    total_info['root'] = root_disk
    total_info['total'] = psutil.disk_usage(root_disk).total / measure_index
    total_info['used'] = psutil.disk_usage(root_disk).used / measure_index
    total_info['free'] = psutil.disk_usage(root_disk).free / measure_index    
    
    return total_info