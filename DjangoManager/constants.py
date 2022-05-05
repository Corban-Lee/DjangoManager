from enum import Enum, auto


class ButtonState(Enum):
    REST = auto()
    HOVER = auto()
    ACTIVE = auto()


THEME_DIR = 'DjangoManager/themes'
IMAGES_DIR = 'DjangoManager/images'
CONFIG_FILENAME = 'config.json'
FILENAME_FORMAT_PREFIX = '%Y-%m-%d %H-%M-%S'
MAX_LOGFILE_AGE_DAYS = 7

# Some WindowsOS styles, required for task bar integration
GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080
