import pysftp
import fnmatch

from config.settings import TRUELINK_SFTP_HOST, TRUELINK_SFTP_USER
from utils.utils import write_key_file

KEY_PATH = write_key_file()

# Supress warning about trusting all host keys - bad practice!
import warnings
warnings.filterwarnings('ignore','.*Failed to load HostKeys.*')


def list_all_files():
    # Trust all host keys - bad practice!
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    # Get connection
    sftp = pysftp.Connection(host=TRUELINK_SFTP_HOST, username=TRUELINK_SFTP_USER, private_key=KEY_PATH, cnopts=cnopts)

    # filter away directorires and files without file extensions
    filelist = [ f for f in sftp.listdir() if fnmatch.fnmatch(f, '*.*') ]
    return filelist, sftp