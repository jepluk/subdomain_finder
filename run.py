import requests, socket
from bs4 import BeautifulSoup as bs

p = '\x1b[38;5;255m'; h = '\x1b[38;5;46m'; m = '\x1b[38;5;160m'; o = '\x1b[38;5;220m'
def subdomain(url, base='https://rapiddns.io/', block=[]):
    #url = url.replace('https://','').replace('www.','').replace('http://','')
    request = bs(requests.get(base +'/subdomain/'+ url).text, 'html.parser')
    page = request.find_all('a', href=lambda x: x and f'/subdomain/{url}?page=' in x)
    
    for page_ in page:
        patch = page_['href']
        web = bs(requests.get(base + patch).text, 'html.parser')

        for td in web.find_all('td'):
            string = td.text
            if string not in block:
                if string.endswith(url): 
                    try: ip = h + socket.gethostbyname(string)
                    except socket.gaierror: ip = m +'none'
    
                    try: 
                        server = requests.get('https://'+ string).headers.get('Server')
                        if server is None: server = m +'undefined'
                        else: server = h + server
                    except requests.RequestException: server = m +'undefined'
                
                    print(f'{o}{string}{p}|{ip}{p}|{server}')
                    block.append(string)


if __name__ == "__main__":
    url = input(f'\n\n{p}Url ({m}ex: line.me{p}):{h} ')
    print(p +'-'*60)
    subdomain(url)

