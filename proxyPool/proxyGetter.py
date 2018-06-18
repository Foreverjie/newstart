from .proxyStore import RedisClient
from .proxyCrawler import Crawler
from .setting import *
from .tester import Tester
import sys

class Getter():
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        '''
        判断是否达到了代理池限制
        :return:
        '''
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False
