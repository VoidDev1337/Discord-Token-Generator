from msilib.schema import CreateFolder
import os, httpx, websocket, base64, json, random, time, threading, ctypes, datetime, string, requests
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style
from base64 import b64encode



with open('config.json') as config_file:config = json.load(config_file)
solved = 0
genned = 0
errors = 0
genStartTime = time.time()


def TitleWorkerr():
    global genned, solved, errors, verified 
    ctypes.windll.kernel32.SetConsoleTitleW(f'Space Generator | Generated : {genned} | Errors : {errors} | Solved : {solved} | Total : {round(genned + errors)}')

class Logger:
    def CenterText(var:str, space:int=None): # From Pycenter
        if not space:
            space = (os.get_terminal_size().columns - len(var.splitlines()[int(len(var.splitlines())/2)])) / 2
        return "\n".join((' ' * int(space)) + var for var in var.splitlines())
    
    def Success(text):
        lock = threading.Lock()
        lock.acquire()
        print(f'[{Fore.GREEN}${Fore.WHITE}] {text}')
        lock.release()
    
    def Error(text):
        lock = threading.Lock()
        lock.acquire()
        print(f'[{Fore.RED}-{Fore.WHITE}] {text}')
        lock.release()
    
    def Question(text):
        lock = threading.Lock()
        lock.acquire()
        print(f'[{Fore.BLUE}?{Fore.WHITE}] {text}')
        lock.release()
    
    def Console():
        os.system('cls')
        text = """
                      ███████╗██████╗  █████╗  ██████╗███████╗    ████████╗ ██████╗ ██╗  ██╗███████╗███╗   ██╗███████╗
                      ██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝    ╚══██╔══╝██╔═══██╗██║ ██╔╝██╔════╝████╗  ██║██╔════╝
                      ███████╗██████╔╝███████║██║     █████╗         ██║   ██║   ██║█████╔╝ █████╗  ██╔██╗ ██║███████╗
                      ╚════██║██╔═══╝ ██╔══██║██║     ██╔══╝         ██║   ██║   ██║██╔═██╗ ██╔══╝  ██║╚██╗██║╚════██║
                      ███████║██║     ██║  ██║╚██████╗███████╗       ██║   ╚██████╔╝██║  ██╗███████╗██║ ╚████║███████║
                      ╚══════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝       ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝
                                                                                                """        
        faded = ''
        red = 40
        for line in text.splitlines():
            faded += (f"\033[38;2;{red};0;220m{line}\033[0m\n")
            if not red == 255:
                red += 15
                if red > 255:
                    red = 255
        print(Logger.CenterText(faded))


class Utils(object):
    @staticmethod
    def GenerateBornDate():
        year=str(random.randint(1997,2001));month=str(random.randint(1,12));day=str(random.randint(1,28))
        if len(month)==1:month='0'+month
        if len(day)==1:day='0'+day
        return year+'-'+month+'-'+day
    
    @staticmethod
    def RandomCharacter(y):
        return ''.join(random.choice(string.ascii_letters) for x in range(y))
    
    @staticmethod
    def CreateEmail():
        return f"{Utils.RandomCharacter(8)}{random.choice(config['email_domains'])}"
    
    @staticmethod
    def GetVerifyToken(email):
        return httpx.get(f'{config["email_server_link"]}{email}').text
    
    @staticmethod
    def GetUsername():
        usernames = open("input/usernames.txt", encoding="cp437").read().splitlines()
        return random.choice(usernames)
    
    @staticmethod
    def GetProxy():
      with open('input/proxies.txt', "r") as f:
        return random.choice(f.readlines()).strip()
    
    @staticmethod
    def GetFormattedProxy(proxy):
        if '@' in proxy:
            return proxy
        elif len(proxy.split(':')) == 2:
            return proxy
        else:
            if '.' in proxy.split(':')[0]:
                return ':'.join(proxy.split(':')[2:]) + '@' + ':'.join(proxy.split(':')[:2])
            else:
                return ':'.join(proxy.split(':')[:2]) + '@' + ':'.join(proxy.split(':')[2:])
    
    @staticmethod
    def PostTokenInWebhook(token):
        for webhook in config["webhook_urls"]:
            try:
                httpx.post(webhook, json={ "username": "Space Generator", "content": token})
            except Exception as e:
                pass
    

class CreateWebsocket(object):
    def __init__(self, token:str):
        ws = websocket.WebSocket()
        ws.connect('wss://gateway.discord.gg/?v=6&encoding=json')
        response = ws.recv()
        event = json.loads(response)
        auth = {'op': 2, 'd': {'token': token, 'capabilities': 61, 'properties': {'os': 'Windows', 'browser': 'Chrome', 'device': '',  'system_locale': 'en-GB', 'browser_user_agent': config['useragent'], 'browser_version': '90.0.4430.212', 'os_version': '10', 'referrer': '', 'referring_domain': '', 'referrer_current': '', 'referring_domain_current': '', 'release_channel': 'stable', 'client_build_number': '85108', 'client_event_source': 'null'}, 'presence': {'status': random.choice(['online', 'dnd', 'idle']), 'since': 0, 'activities': [{ "name": "Custom Status", "type": 4, "state": 'Void Loves Cord', "emoji": '🐱' }], 'afk': False}, 'compress': False, 'client_state': {'guild_hashes': {}, 'highest_last_message_id': '0', 'read_state_version': 0, 'user_guild_settings_version': -1}}};
        ws.send(json.dumps(auth))

class SolveCaptcha(object):
    def init(proxy, site_url, site_key, thread_id, can_solve_in_one_click, solver_address=None):
        global solved
        captcha_key = httpx.post(solver_address, json={
            "site_key": "4c672d35-0701-42b2-88c3-78380b0db560",
            "site_url": "https://discord.com/",
            "proxy_url": 'python0001:x4rTHLZJEoVeAdW3@geo.litespeed.cc:12323'
        }, timeout=None).text

        if "P0_" in captcha_key:
            solved += 1
            TitleWorkerr()
            #Logger.Success("Solved Captcha")
            return captcha_key
        else:
            return False
        



def GenerateToken(key, proxy, thread_id):
    try:
        global genned, solved, errors, verified

        client = httpx.Client(http2=True,timeout=3, proxies={"all://": f"http://{proxy}"})
    
        response = client.get("https://discord.com/register", headers={'user-agent': config['useragent']}, timeout=20)

        dcfduid = response.headers['Set-Cookie'].split('__dcfduid=')[1].split(';')[0]
        sdcfduid = response.headers['Set-Cookie'].split('__sdcfduid=')[1].split(';')[0]
        cookie_header = f'__dcfduid={dcfduid}; __sdcfduid={sdcfduid}'

        registerheaders  = { "Host":"discord.com", "User-Agent": config['useragent'], "Accept":"*/*", "Accept-Language":"en-US,en;q=0.5", "Accept-Encoding":"gzip,", "Content-Type":"application/json", "X-Track": config['x_super_properties'], "X-Fingerprint": config['x_fingerprint'], "Origin":"https://discord.com", "Alt-Used":"discord.com", "Connection":"keep-alive", "Referer":"https://discord.com/", 'Cookie': cookie_header, "Sec-Fetch-Dest":"empty", "Sec-Fetch-Mode":"cors", "Sec-Fetch-Site":"same-origin", "TE":"trailers"}
        account_email = Utils.CreateEmail()
        account_password = "SpaceGenxD!!??"
        account_username = Utils.GetUsername() + ' | .gg/tokenverse'
    
        payload = { "email": account_email, "password": account_password, "date_of_birth": Utils.GenerateBornDate(), "username": account_username, "consent": True, "captcha_key": key, 'fingerprint': config['x_fingerprint'], "invite": config['invite_code']}

        response = client.post('https://discord.com/api/v9/auth/register', headers=registerheaders, json=payload, timeout=20)

        if response.status_code == 201:
            token = response.json()['token']
            Logger.Success(f"Created Token : {token}")
            genned = genned + 1
            TitleWorkerr()
            CreateWebsocket(token)
            #Utils.PostTokenInWebhook(token)
        else:
            TitleWorkerr()
            if 'captcha' in response.text:
                errors = errors + 1
                Logger.Error('Invalid Captcha Response, Retrying...')
            else:
                errors = errors + 1
                Logger.Error(response.json())
    except Exception as e:
        TitleWorkerr()
        errors = errors + 1
        Logger.Error(e)


def StartThread(thread_id,solver_address=None):
    while True:
        try:
            proxy =  Utils.GetProxy()
            proxy_raw = proxy
            proxy_formated = Utils.GetFormattedProxy(proxy_raw)
            if solver_address == None:
                solver_address = config["solver_address"]
            key = SolveCaptcha.init(proxy_formated,   "https://discord.com/register" , "4c672d35-0701-42b2-88c3-78380b0db560",thread_id, False ,solver_address)

            if key != False and key != 0 and key !="0":
                threading.Thread(target=GenerateToken,args=[key,proxy_formated,thread_id] ).start()

        except Exception as e:
            Logger.Error(e)

def StartGenerator():
    global threads
    
    try:
        Logger.Console()
        Logger.Question("How many threads do you want ? ")
        threads = int(input(''))
    except:
        Logger.Error("Please enter a valid number")
        os._exit(1)

    thread_running = threads
        
    with ThreadPoolExecutor(max_workers=threads) as exe:
        for x in range(threads):
            exe.map(StartThread,[x])

StartGenerator()