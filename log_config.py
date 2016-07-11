""" This modules gives an easy to use logging configuration
class.  The goal is to give a logging API like
LogSetup.init_log()
LogSetup.initLog(log_file='myapp.log')
LogSetup.initLog(log_dir='path/to/myapp/', log_file='myapp.log')

It also allows inheritance for adding log settins to the
default configuration
"""
import logging
import logging.config
import os.path


class LogConfig(object):
    date_format = "%d/%b/%Y %H:%M:%S"
    log_dir = 'logs'
    log_file = 'test.log'
    detailed_format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    simple_format = '%(name)-12s %(levelname)-8s %(message)s'

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
                    'class': 'logging.FileHandler',
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
    log_dir = 'logs'
    log_file = '123.log'
    disable = False
    simple_format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'

    @classmethod
    def log_config(cls):
        config = super(Setup, cls).log_config()
        config['handlers']['file']['level'] = 'DEBUG'
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

    LogConfig.init_log(log_file='custom.log')
    log.debug('debug test 2')
    log.info('info test 2')
    log.error('error test 2')
