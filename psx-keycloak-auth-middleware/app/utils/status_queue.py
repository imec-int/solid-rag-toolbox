
import queue

global statusQueue
statusQueue = queue.Queue()


def get_status_queue():
    return statusQueue
