import logging
import multiprocessing
import json
import structlog
import asyncio

class FieldLog:
    """
    Класс для сбора и управления значениями полей.

    Attributes:
        fields (list): Список имен полей.
        values (dict): Словарь значений полей.

    Methods:
        set_value(field, value): Устанавливает значение для поля.
        is_complete(): Проверяет, заполнены ли все поля.
        to_dict(): Возвращает значения полей в виде словаря.
    """
    PROG = "PROG"
    DONE = "DONE"

    def __init__(self, fields):
        self.fields = fields
        self.values = {field: None for field in fields}

    def set_value(self, field, value):
        if field in self.fields:
            if self.values[field] is not None:
                print(f"Поле '{field}' уже заполнено. Объект не собран.")
                return self.PROG
            self.values[field] = value
        else:
            raise ValueError(f"Поле '{field}' не существует.")

        if self.is_complete():
            return self.DONE
        return self.PROG

    def is_complete(self):
        return all(value is not None for value in self.values.values())

    def to_dict(self):
        return self.values

def setup_logger(queue, result_queue):
    """Настройка логгера для обработки сообщений из очереди."""
    logging.basicConfig(
        format='%(message)s',
        level=logging.INFO,
    )
    
    structlog.configure(
        processors=[
            structlog.processors.KeyValueRenderer(key_order=['event']),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
    )

    logger = structlog.get_logger()
    collected_logs = {}

    while True:
        try:
            message = queue.get()
            event_type = message['event_type']
            data = message['data']

            if event_type not in collected_logs:
                collected_logs[event_type] = FieldLog(fields=['message', 'index'])

            log = collected_logs[event_type]

            if 'message' in data:
                log.set_value('message', data['message'])
            if 'index' in data:
                log.set_value('index', data['index'])

            logger.info("Received message", **message)

            if log.is_complete():
                result_queue.put({event_type: log.to_dict()})
                collected_logs[event_type] = FieldLog(fields=['message', 'index'])

        except Exception as e:
            logger.error('Error', error=str(e))

def start_logger_process(queue, result_queue):
    """Запуск процесса логгера."""
    process = multiprocessing.Process(target=setup_logger, args=(queue, result_queue))
    process.start()
    return process

log_queue = multiprocessing.Queue()
result_queue = multiprocessing.Queue()
logger_process = start_logger_process(log_queue, result_queue)

def log_message(event_type, data):
    """Функция для отправки сообщения в логгер."""
    log_queue.put({'event_type': event_type, 'data': data})

async def async_function_1():
    for i in range(10):
        log_message('event_type_1', {'message': f'Async Function 1 - Message {i}'})
        await asyncio.sleep(0.1)

async def async_function_2():
    for i in range(10):
        log_message('event_type_1', {'index': i})
        await asyncio.sleep(0.2)

async def main():
    await asyncio.gather(async_function_1(), async_function_2())

if __name__ == '__main__':
    try:
        asyncio.run(main())
    finally:
        while not result_queue.empty():
            collected_data = result_queue.get()
            json_output = json.dumps(collected_data, indent=4)
            print(json_output)
