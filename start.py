import os
from subprocess import Popen, PIPE
import multiprocessing
import time
import random

# список запущенных процессов
p_list = []
root_dir = os.path.abspath('.')
SERVER_PATH = os.path.join(root_dir, 'server', 'main.py')
CLIENT_PATH = os.path.join(root_dir, 'client', 'main.py')

while True:
    user = input("Запустить сервер и клиентов (s) / Выйти (q)")
    cmd_for_start_server = ['xterm', '-e', 'python3', SERVER_PATH]
    cmd_for_start_client_reader = ['xterm', '-e', 'python3', CLIENT_PATH, '-r']
    cmd_for_start_client_writer = ['xterm', '-e', 'python3', CLIENT_PATH, '-w']
    if user == 's':
        # запускаем сервер
        # Запускаем серверный скрипт и добавляем его в список процессов
        p_list.append(Popen(cmd_for_start_server,
                            shell=False, stdin=PIPE, stdout=PIPE, close_fds=True))
        print('Сервер запущен')
        # ждем на всякий пожарный
        time.sleep(2)
        print(len(p_list))
        # запускаем клиентов на чтение случайное число
        for _ in range(random.randint(1, 10)):
            # Запускаем клиентский скрипт для чтения и добавляем его в список процессов
            p_list.append(Popen(cmd_for_start_client_reader,
                                shell=False, stdin=PIPE, stdout=PIPE, close_fds=True))
        print('Клиенты на чтение запущены')
        # запускаем клиента на запись случайное число
        for _ in range(random.randint(1, 5)):
            # Запускаем клиентский скрипт и добавляем его в список процессов
            p_list.append(Popen(cmd_for_start_client_writer,
                                shell=False, stdin=PIPE, stdout=PIPE,
                                close_fds=True))
        print('Клиенты на запись запущены')
    elif user == 'q':
        print('Открыто процессов {}'.format(len(p_list)))
        for p in p_list:
            print('Закрываю {}'.format(p))
            p.kill()
        p_list.clear()
        print('Выхожу')
        break