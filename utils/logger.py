import logging
import os
import os.path as osp
import yaml


class Logger:
    logger = None
    level = None
    fmt = None
    filename = None

    @staticmethod
    def get_logger():
        if not Logger.logger:
            with open(osp.join(osp.dirname(__file__), '..', 'etc', 'logger.yaml'), 'r') as f:
                config = yaml.load(f.read(), Loader=yaml.BaseLoader)
                level_map = {'debug': logging.DEBUG,
                             'info': logging.INFO,
                             'warn': logging.WARN,
                             'warning': logging.WARN,
                             'error': logging.ERROR,
                             'fatal': logging.FATAL,
                             'critical': logging.CRITICAL}

                level = level_map[config['level'].lower()]
                filename = osp.realpath(osp.join(osp.dirname(__file__), '..', 'etc', *osp.split(config['filename'])))
                if not osp.exists(filename):
                    os.makedirs(osp.dirname(filename))
                Logger.init_logger(level=level, fmt=config['fmt'], filename=filename)
                Logger.logger.info(f'log into {filename}')
        return Logger.logger

    @staticmethod
    def update(level=None, fmt: str = None, filename: str = None):
        Logger.init_logger(level=level or Logger.level,
                           fmt=fmt or Logger.fmt,
                           filename=filename or Logger.filename,
                           overwrite=True)
        return Logger.logger

    @staticmethod
    def init_logger(level=logging.INFO,
                    fmt='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',
                    filename: str = None,
                    overwrite=False):
        if Logger.logger and not overwrite:
            return Logger.logger
        logger = logging.getLogger(filename)
        logger.setLevel(level)

        fmt = logging.Formatter(fmt)

        # stream handler
        sh = logging.StreamHandler()
        sh.setLevel(level)
        sh.setFormatter(fmt)
        logger.addHandler(sh)

        if filename:
            # file handler
            fh = logging.FileHandler(filename)
            fh.setLevel(level)
            fh.setFormatter(fmt)
            logger.addHandler(fh)

        logger.setLevel(level)
        Logger.logger = logger
        return logger
