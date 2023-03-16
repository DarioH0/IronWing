import requests
import colorama
import threading
from queue import Queue

colorama.init()

print("""
||||||                           \`----.__                 ____               
 |||  ||| ||||  |||||| ||| ||||   |       `--._         <=#  , *--,           
 |||   |||     |||  ||| |||  ||| /_             `-.    ,/  / `````            
 |||   |||     |||  ||| |||  |||   \__             (_.'  ,'                   
|||||  |||      ||||||  |||  |||      \__ ......'       \___----^__           
                                   _./               ,'           `.         
 ||               ||      |\     _.'   ___/ )\...._\"   ___           \        
||||     |||     ||||     | \__.'  __.'            `\"\"'   `\"\"`.'\"\"\"`--\       
 |||   ||| |||   |||   ||| \____.-'                                           
 |||   ||| |||   |||   ||||   ||| ||||||     |||||||                          
  ||| |||   ||| |||     |||    |||    |||  |||     |||                        
    |||       |||       |||    |||    |||  |||     |||                        
     |         |       |||||   |||    |||    |||||||||                        
                                                   |||                        
                                             ||||||||
""")
##############################################################################################################

amount = int(input('Proxies: '))
threads = int(input('Threads: '))
proxies = []
checked_proxies = set()

def check_proxy(proxy):
    try:
        response = requests.get('https://google.com/', proxies={"http": proxy, "https": proxy}, timeout=10)
        if response.status_code == 200:
            print(f'{colorama.Fore.LIGHTGREEN_EX}GOOD{colorama.Fore.RESET}', proxy)
            return True
    except:
        pass
    print(f'{colorama.Fore.RED}BAD{colorama.Fore.RESET}', proxy)
    return False

def generate_proxies(num_proxies):
    global proxies
    response = requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&simplified=true")
    if response.status_code == 200:
        proxy_list = response.content.decode().split("\r\n")
        for proxy in proxy_list:
            if proxy not in checked_proxies:
                proxies.append(proxy)
                checked_proxies.add(proxy)
                if len(proxies) >= num_proxies:
                    break

def check_proxies(proxy_queue):
    while not proxy_queue.empty():
        proxy = proxy_queue.get()
        check_proxy(proxy)

##############################################################################################################

print()
generate_proxies(amount)

proxy_queue = Queue()
for proxy in proxies:
    proxy_queue.put(proxy)

threads_list = []
for i in range(threads):
    thread = threading.Thread(target=check_proxies, args=(proxy_queue,))
    threads_list.append(thread)
    thread.start()

for thread in threads_list:
    thread.join()

print('#####################################################')
print('THE END:\n')
print(proxies)
