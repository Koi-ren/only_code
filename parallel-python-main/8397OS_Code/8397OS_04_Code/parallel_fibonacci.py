#coding: utf-8

import logging, threading

from queue import Queue

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(message)s')

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

'''
로거 가져오기
logger = logging.getLogger()
getLogger()를 호출하여 기본 로거 인스턴스를 가져옵니다. 이 로거를 통해 로그 메시지를 기록할 수 있습니다.

로거 수준 설정
logger.setLevel(logging.DEBUG)
로거의 로그 레벨을 DEBUG로 설정합니다. 이는 DEBUG 레벨 이상의 모든 로그 메시지를 기록하겠다는 의미입니다. 로그 레벨의 순서는 DEBUG, INFO, WARNING, ERROR, CRITICAL입니다.

포맷터 설정
formatter = logging.Formatter('%(asctime)s - %(message)s')
로그 메시지의 형식을 설정합니다. 여기서는 로그 메시지에 타임스탬프와 메시지만 포함하도록 설정했습니다. 예를 들어, %(asctime)s는 로그가 기록된 시간을 나타내고, %(message)s는 실제 로그 메시지를 나타냅니다.

스트림 핸들러 생성 및 설정
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
StreamHandler를 생성하여 로그 메시지를 콘솔에 출력할 수 있도록 합니다. 이 핸들러의 로그 레벨을 DEBUG로 설정하고, 앞서 정의한 포맷터를 핸들러에 설정합니다.

핸들러 추가
logger.addHandler(ch)
설정된 핸들러를 로거에 추가합니다. 이를 통해 로거는 로그 메시지를 콘솔에 출력하게 됩니다.
'''

fibo_dict = {}
shared_queue = Queue()
input_list = [3, 10, 5, 7] #simulates user input

queue_condition = threading.Condition()


def fibonacci_task(condition):
    with condition:
        while shared_queue.empty(): 
            logger.info("[%s] - waiting for elements in queue..." % 
                        threading.current_thread().name)
            condition.wait()
        else:
            value = shared_queue.get()
            a, b = 0, 1
            for item in range(value):
                a, b = b, a + b
                fibo_dict[value] = a
            shared_queue.task_done()
            logger.debug("[%s] fibonacci of key [%d] with result [%d]" %
                        (threading.current_thread().name, value, fibo_dict[value]))

def queue_task(condition):
    logging.debug('Starting queue_task...')
    with condition:
        for item in input_list:
            shared_queue.put(item)
        logging.debug("Notifying fibonacci_task threads that the queue is ready to consume..")
        condition.notify_all()

threads = [threading.Thread(
            daemon=True, target=fibonacci_task, args=(queue_condition,)) for i in range(4)]

'''
args에서 queue_condition뒤에 ','가 붙는 이유는 args가 반드시 단일값이 아닌 
반드시 반복가능한 객체(iterable)이여야하기 때문
따라서 튜플 형식이나 리스트 형식으로 값을 전달해야 한다.

위 코드에서는 튜플형식으로 값을 인가했지만 리스트 형식으로 값을 전달한다면,
리스트의 가변성(mutable) 성질 때문에 데이터의 무결성이 위협받는다.

따라서 불변성(immutable) 성질을 가진 튜플을 사용하는 것이 안전하며,
또한 튜플은 리스트보다 메모리가 가벼워 더 빠르게 계산되기에 
성능면이나 안전면에서 튜플을 사용하는 것이 적극 권장된다.
'''

[thread.start() for thread in threads]

prod = threading.Thread(name='queue_task_thread', daemon=True,
                         target=queue_task, args=(queue_condition,))
prod.start()

[thread.join() for thread in threads]

logger.info("[%s] - Result: %s" % (threading.current_thread().name, fibo_dict))
