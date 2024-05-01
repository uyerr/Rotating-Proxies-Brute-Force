# About

This script was created with the aim of practising scripting, use of libraries and proxies. 
The use of free proxies is discouraged as they *can* be malicious or most commonly work horrifically wrong.
The program will not run properly due to parameters/variables being hardcoded as it was not intended to be used.
Its only objective is showcase what can be done in <100 lines of code .

## How it works

1. The script browses free-proxy-list.net and stores only the proxies with Https availability in a list. 
2. It then checks that each proxy is working by sending a request to ipinfo.io/json. If the connection is established (status_code == 200) the proxy is appended to a list.
3. Using the top 100 most popular passwords located in passwordlist.txt, the script iterates through the file, sending a request to the target website using the first proxy in the list. After trying a password, the counter goes up by 1 and the next proxy is used.
4. If using free proxies it is probable there won't be 100 of them. Solved by repeating proxies (not optimal though). 

## Disclaimer

This program is intended for practice purposes only. It is designed to help the creator learn and enhance skills in programming. The creator of this program doses not endorse or condone the use of this program for any malicious, harmful, or illegal activities. Any misuse of this program for unethical purposes is strictly prohibited.