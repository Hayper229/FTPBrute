grep -oP 'addr="(\d+\.\d+\.\d+\.\d+)"' results.txt | sed 's/addr="//g; s/"//g' > results_clean.txt
