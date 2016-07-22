""" This modules gives an easy to use logging configuration
class.  The goal is to give a logging API like
LogSetup.init_log()
LogSetup.initLog(log_file='myapp.log')
LogSetup.initLog(log_dir='path/to/myapp/', log_file='myapp.log')

Inheritance can add log settings to the default configuration

A custom file handle is used to manually rotate logfiles.
It appends the current timestamp to the logfile instead
of an arbirary number
This allows logfile to be rotated on call instead of size
or age.
"""
import logging
import logging.config
from logging.handlers import BaseRotatingHandler
from datetime import datetime
import os.path


class LogRotateException(Exception):
    pass


class DatedRotatingFileHandle(BaseRotatingHandler):
    """ Handler for rolling over logfiles with the current date.
    Similar to Java's log4j RollingFileAppender.
    The logfile is appended with a timestamp instead of a
    number assigned by RotatingFileHandler.  This make it easy
    to find a logfile for a specific day when looking through
    archives

    It also allows logfiles to be rotated by call instead of
    reaching a threshold.  This is ideal when one logfile should
    be created per execution.
    """

    def __init__(self, filename, dateformat=None, mode='a',
                 encoding=None, delay=False):
        """ Set the rotating file format, isoformat is used
        by default
        """
        super().__init__(filename, mode, encoding, delay)
        self.dateformat = dateformat
        if dateformat and '/' in dateformat:
            print("Replacing / in {} dateformat with -"
                  .format(self.dateformat))
            self.dateformat = self.dateformat.replace('/', '-')

    def doRollover(self):
        """ Appends the current timestamp to logfile
        """
        if self.stream:
            self.stream.close()
            self.stream = None

        # Format the current time
        time = datetime.now()
        if self.dateformat:
            time_postfix = time.strftime(self.dateformat)
        else:
            time_postfix = time.isoformat()

        # Append the current time to the logfile
        dated_file = self.rotation_filename(
            "{}.{}".format(self.baseFilename,
                           time_postfix)
        )

        # Sanity check to confirm nothing can be overwritten
        if os.path.exists(dated_file):
            raise LogRotateException(
                "Logfile already exists, but datetime should be unique")

        self.rotate(self.baseFilename, dated_file)

    def shouldRollover(self, record):
        """ Never roll over a file unless called
        """
        return 0


class LogConfig(object):
    date_format = "%d/%b/%Y-%H:%M:%S"
    log_dir = 'logs'
    log_file = 'test.log'
    detailed_format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    simple_format = '%(name)-12s %(levelname)-8s %(message)s'
    handler_class = BaseRotatingHandler

    @classmethod
    def rollover(cls):
        """ Rollover all file handlers. Do not do this from a thread or subprocess
        """
        for handler in logging.getLogger().handlers:
            if isinstance(handler, cls.handler_class):
                handler.doRollover()

    @classmethod
    def log_config(cls):
        return {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'detailed': {
                    'format': cls.detailed_format,
                    'dateformat': cls.date_format,
                },
                'simple': {
                    'format': cls.simple_format,
                    'dateformat': cls.date_format,
                }
            },
            'handlers': {
                'console': {
                    'level': 'DEBUG',
                    'formatter': 'simple',
                    'class': 'logging.StreamHandler',
                },
                'file': {
                    'level': 'INFO',
                    'formatter': 'detailed',
                    'class': 'log_config.DatedRotatingFileHandle',
                    'filename': os.path.join(cls.log_dir,
                                             cls.log_file),
                    'mode': 'a',
                },
            },
            'loggers': {
                '': {
                    'handlers': ['console', 'file'],
                    'level': 'DEBUG'
                },
            }
        }

    @classmethod
    def init_log(cls, log_dir=None, log_file=None):
        cls.log_dir = log_dir if log_dir else cls.log_dir
        cls.log_file = log_file if log_file else cls.log_file
        logging.config.dictConfig(cls.log_config())


class Setup(LogConfig):
    """ This is an example for overriding the base
    logging configuration.
    """
    log_dir = 'logs'
    log_file = '123.log'
    disable = False
    simple_format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'

    @classmethod
    def log_config(cls):
        config = super(Setup, cls).log_config()
        config['handlers']['file']['level'] = 'DEBUG'
        config['handlers']['file']['dateformat'] = "%d/%b/%Y-%H:%M:%S"
        return config

if __name__ == '__main__':

    LogConfig.init_log()
    log = logging.getLogger(__name__)
    log.debug('debug test')
    log.info('info test')
    log.error('error test')

    Setup.init_log()
    log = logging.getLogger(__name__)
    log.debug('debug test 2')
    log.info('info test 2')
    log.error('error test 2')
    log.info('hello 3')
    LogConfig.rollover()

    LogConfig.init_log(log_file='custom.log')
    log.debug('debug test 2')
    log.info('info test 2')
    log.error('error test 2')

    LogConfig.rollover()
