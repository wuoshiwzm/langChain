import sys, os
from loguru import logger

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir = os.path.join(root_dir, "logs")

if not os.path.exists(log_dir):
    os.mkdir(log_dir)

#   Trace < Debug < Info < Success < Warning < Error < Critical

# 把日志输出到控制台上
class MyLogger:
    def __init__(self):
        self.logger = logger
        self.logger.remove()
        self.logger.add(sys.stdout, level='DEBUG',
                        format='<green>{time:YYYY-MM-DD HH:mm:ss}</green> | }'
                        '{process.name}'
                        'thread.name'
                        '<cyan>{module}</cyan> - <cyan>{line}</cyan>}'
                        ':<cyan>{line}</cyan>'
                        '<level>{level}</level>'
                        '<level>{message}</level>',
                        )

        # 输出到文件的格式，注释下面的add, 则关闭日志写入

    def get_logger(self):
        return self.logger

logger = MyLogger().get_logger()