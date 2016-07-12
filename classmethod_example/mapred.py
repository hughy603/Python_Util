import logging
import os


class InputData(object):

    def read(self):
        raise NotImplementedError


class PathInputData(InputData):

    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        return open(self.path).read()


class Worker(object):

    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError


class LineCountWorker(Worker):

    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result


def generate_inputs(data_dir):
    for name in os.listdir(data_dir):
        if(os.path.isfile(name)):
            yield PathInputData(os.path.join(data_dir, name))


def create_workers(input_list):
    workers = []
    for input_data in input_list:
        workers.append(LineCountWorker(input_data))
    return workers


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


def mapreduce(data_dir):
    inputs = generate_inputs(data_dir)
    workers = create_workers(inputs)
    return execute(workers)

if __name__ == '__main__':
    from log_config import LogConfig
    LogConfig.init_log()
    log = logging.getLogger(__name__)
    src_dir = os.environ.get('HOME')
    log.info('Counting the number of lines in files in {}'.format(src_dir))
    log.info('There are {} lines in {}'.format(mapreduce(src_dir),src_dir))
