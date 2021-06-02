import os.path as osp
import logging
from utils.logger import *

logger = Logger.init_logger(filename=osp.join(osp.dirname(__file__), '..', 'log', 'bankdb.log'))