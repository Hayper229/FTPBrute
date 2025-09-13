
Command 1:  masscan --range '86.000.00.00-86.255.255.255' -p21 --rate=20000 --open-only -oX results.txt 

Command 2:  bash filter_ftp.sh  source:   grep -oP 'addr="(\d+\.\d+\.\d+\.\d+)"' results.txt | sed 's/addr="//g; s/"//g' > results_clean.txt

Command 3: cat  results_clean.txt > targets.txt

Command 4: python3 ftp_brute.py

Command 5: cat FTP_results.txt
