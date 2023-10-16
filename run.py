import sys, re, socket, json, urllib3

req = lambda url, **kwargs: urllib3.PoolManager(timeout=int(sys.argv[2])).request('GET', url, **kwargs)

def scan_subdomain(api="https://rapiddns.io/", block=[]):
    pages = [f'{api}/subdomain/{sys.argv[1]}']
    for url in pages:
        response = req(url)

        try:
            next_url = re.search('<a href="(.*?)" class="page-link " aria-label="Next ">', response.data.decode('utf-8')).group(1)
            pages.append(api + next_url)
        except AttributeError:
            pass

        for subdomain in re.findall(r'<td>(.*?'+sys.argv[1]+'.*?)</td>', response.data.decode('utf-8')):
            if subdomain in block: continue

            block.append(subdomain)
            send = sendr(subdomain)

            address = addressr(subdomain)
            status = send[0]
            server = send[1]

            print(f'{status}\t{address}\t{subdomain} ~ {server}')

 
def addressr(subdomain):
    try: 
        return socket.gethostbyname(subdomain)
    except:
        return '!none'

def sendr(subdomain):
    try:
        response = req(subdomain)
        status = response.status

        server = response.headers.get('server')
        if server is None:
            server = '!none'

        return (str(status), server)
    except:
        return ('!none','!none')

if __name__ == "__main__":
    if len(sys.argv) == 3:
        print('\n\nStatus\tAddress\t\tSubdomain ~ Server')
        print('-'*60)
        scan_subdomain()
    else:
        print('Failure. Ex: python run.py <domain> <timeout>')
