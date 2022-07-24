import logging
import os.path
from logging import handlers

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 获取绝对路径
BASE_URL = 'http://user-p2p-test.itheima.net/'
DB_URL = "52.83.144.39"
DB_USERNAME = "root"
DB_PASSWORD = "Itcast_p2p_20191228"
DB_MEMBER = 'czbk_member'
DB_FINANCE = 'czbk_finance'

# 日志初始化
def init_log_config():
    # 1.初始化日志对象
    logger = logging.getLogger()
    # 2.设置日志级别（>INFO）
    logger.setLevel(logging.INFO)
    # 3.创建日志处理器（控制台&文件）
    sh = logging.StreamHandler()
    # logfile = BASE_DIR + "log" + os.sep + "log{}.log".format("%Y%m%D %H%M%S")
    logfile = BASE_DIR + os.sep + "log" + os.sep + "log1.log"
    fh = handlers.TimedRotatingFileHandler(logfile, when='M', interval=5, backupCount=5, encoding='utf-8')

    # 4.创建格式化器，设置日志格式
    fmt = '%(asctime)s %(levelname)s [%(name)s] [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s'
    formatter = logging.Formatter(fmt)
    # 5.将格式化器添加到日志器中
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)

    # 6.把日志处理器添加到日志对象
    logger.addHandler(sh)
    logger.addHandler(fh)


