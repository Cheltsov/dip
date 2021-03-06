from datetime import datetime
from os.path import splitext

def get_timestamp_path(instance, filename):
    return 'client/%s%s' %(datetime.now().timestamp(), splitext(filename)[1])
