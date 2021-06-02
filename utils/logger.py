import logging


class Logger:
    logger = None

    @staticmethod
    def get_logger(level: int = None, filename: str = None):
        if not Logger.logger:
            Logger.init_logger(filename=filename)
        if level:
            assert filename and 'please provide filename as well'
            Logger.logger = None
            Logger.init_logger(level=level, filename=filename)
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
