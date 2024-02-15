import httpx, json, re, fade, sys, time, m3u8
from Cryptodome.Cipher import AES
from colorama import Fore, Style, init
init()

# Fancy stuff.. ?

def prp(text):
    print(fade.pinkred(text))

def error(text):
    return f"{Style.BRIGHT}{Fore.RED}[!]{Fore.WHITE} {text}{Style.RESET_ALL}"

def slow_print(text: str, speed: float):
    for x in text:
        sys.stdout.write(x)
        sys.stdout.flush()
        time.sleep(speed)
    sys.stdout.write("\n")

print(fade.pinkred("""
██   ██ ██████  ██      
██   ██ ██   ██ ██    Simple to use download script for hanime.tv  
███████ ██   ██ ██      Developed by github.com/u6f AKA xin
██   ██ ██   ██ ██      
██   ██ ██████  ███████   
"""))

with open("config.json") as file:
    config = json.load(file)
file.close()

def hvid(slug: str):
    r = httpx.get("https://hanime.tv/api/v8/video?id="+slug).json()
    return r

try:
    url = sys.argv[1]
except:
    exit(error("Invalid usage! Example: python dl.py https://hanime.tv/videos/hentai/hajimete-no-hitozuma-6"))

if not re.compile(r"https://hanime\.tv/videos/hentai/([A-Za-z0-9]+(-[A-Za-z0-9]+)+)", re.IGNORECASE).match(url):
    exit(error("Invalid URL!"))

slug = url.split("/")[5]
info = hvid(slug)
print(f"{Style.BRIGHT}{Fore.BLUE}[-]{Fore.WHITE} ", end="")
slow_print(f"Getting hentai information... {Style.RESET_ALL}", 0.03)
if info['hentai_video']['is_censored'] == True:
    censored = f"{Fore.RED}True{Style.RESET_ALL}"
else:
    censored = f"{Fore.GREEN}False{Style.RESET_ALL}"
print(f"{Style.BRIGHT}{Fore.GREEN}[!]{Fore.WHITE} ", end="")     
slow_print(f"{Fore.WHITE}Name: {info['hentai_video']['name']}", 0.05)
print(f"{Style.BRIGHT}{Fore.GREEN}[!]{Fore.WHITE} ", end="")
slow_print(f"Censored: {censored}", 0.05)
streams = info['videos_manifest']['servers'][0]['streams']
print(error("Pick a resolution"))
for i in range(len(streams)):
    res = streams[i]['height']
    if res != "1080":
        print(f"{Style.BRIGHT}{Fore.BLUE}[{i}]{Fore.WHITE} ", end="")
        slow_print(f"{res}p", 0.05)
print(f"{Style.BRIGHT}{Fore.GREEN}[>]{Fore.WHITE} ", end="")        
choice = int(input(""))
try:
    stream_url = streams[choice]['url']
    print(f"{Style.BRIGHT}{Fore.GREEN}[!]{Fore.WHITE} ", end="")
    slow_print(f"File size: {streams[choice]['filesize_mbs']}MB", 0.03)
    print(f"{Style.BRIGHT}{Fore.GREEN}[!]{Fore.WHITE} ", end="")
    file_name = "%s-%sp.mp4" % (slug, res)
    slow_print(f"File name: {file_name}", 0.03)
    print(f"{Style.BRIGHT}{Fore.BLUE}[-]{Fore.WHITE} ", end="")
    slow_print(f"Starting download... {Style.RESET_ALL}", 0.03)
    x = 0
    parsed = m3u8.loads(httpx.get(stream_url).text)
    urls = parsed.segments.uri
    key = AES.new(httpx.get(parsed.keys[0].uri).content, AES.MODE_CBC)
    with open(file_name, "ab") as video:
        for url in urls:
            while True:
                try:
                    data = key.decrypt(httpx.get(url).content)
                    video.write(data)
                    x += 1
                    sys.stdout.write(f"\r{Style.BRIGHT}{Fore.YELLOW}[?]{Fore.WHITE} Progress {x}/{len(urls)}")
                    sys.stdout.flush()
                    break
                except:
                    pass
    print("\n")
    print(f"{Style.BRIGHT}{Fore.MAGENTA}[+]{Fore.WHITE} ", end="")
    slow_print(f"Finished downloading! {Style.RESET_ALL}", 0.03)
except:
    exit(error("Wrong option!"))

# print(f"{Style.BRIGHT}{Fore.BLUE}[-]{Fore.WHITE} ", end="")