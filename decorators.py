from functools import wraps


class Log:
    """
    Класс декоратор для логирования функций
    """

    def __init__(self, logger):
        # запоминаем логгер, чтобы можно было использовать разные
        self.logger = logger

    def __call__(self, func):
        """
        Определяем __call__ для возможности вызова экземпляра как декоратора
        :param func: функция которую будем декорировать
        :return: новая функция
        """

        @wraps(func)
        def decorated(*args, **kwargs):
            # Выполняем функцию и получаем результат
            result = func(*args, **kwargs)
            message = "{} - {} - ".format(decorated.__module__, decorated.__name__)
            if args:
                message += 'args: {} '.format(args)
            if kwargs:
                message += 'kwargs: {} '.format(kwargs)
            if result:
                message += '= {}'.format(result)

            self.logger.info(message)
            return result

        return decorated
