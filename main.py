from sysmonitor import filesystem
import logging
logging.basicConfig(level='DEBUG')

filesystem.get_space_state('E:\\')
filesystem.get_space_state('D:\\')
filesystem.get_space_state('C:\\')