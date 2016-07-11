""" TODO TODO TODO TODO
CAN MULTIPLE @CLASSMETHOD BE REPLACED WITH @STATICMETHOD
"""
import logging
import os


class InputData(object):

    def read(self):
        raise NotImplementedError


class GenericInputData(InputData):

    def read(self):
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, config):
        raise NotImplementedError


class PathInputData(GenericInputData):

    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        return open(self.path).read()

    @classmethod
    def generate_inputs(cls, config):
        data_dir = config['data_dir']
        for name in os.listdir(data_dir):
            if(os.path.isfile(name)):
                yield cls(os.path.join(data_dir, name))


class GenericWorker(object):

    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError

    @classmethod
    def create_workers(cls, input_class, config):
        workers = []
        for input_data in input_class.generate_inputs(config):
            workers.append(cls(input_data))
        return workers


class LineCountWorker(GenericWorker):

    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result


def execute(workers):
    from threading import Thread
    threads = [Thread(target=w.map) for w in workers]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    first, rest = workers[0], workers[1:]
    for worker in rest:
        first.reduce(worker)
    return first.result


def mapreduce(worker_class, input_class, config):
    workers = worker_class.create_workers(input_class, config)
    return execute(workers)

if __name__ == '__main__':
    from log_config import LogConfig
    LogConfig.init_log()
    log = logging.getLogger(__name__)
    src_dir = os.environ.get('HOME')
    config = {'data_dir': src_dir}
    result = mapreduce(LineCountWorker, PathInputData, config)
    log.info('Counted {} lines'.format(result))
