import requests
import asyncio
import sys
import time
import colorsys
from colorama import init, Fore, Style
from itertools import cycle

init(autoreset=True)

def rbt(text, delay=0.05):
    for line in text.splitlines():
        fancy_line = ""
        for i, char in enumerate(line):
            hue = (i / len(line)) * 360
            r, g, b = colorsys.hsv_to_rgb(hue / 360, 1, 1)
            r, g, b = int(r * 255), int(g * 255), int(b * 255)
            fancy_line += f"\033[38;2;{r};{g};{b}m{char}\033[0m"
        print(fancy_line)
        time.sleep(delay)

ASCII_ART = r"""

• ▌ ▄ ·.  ▄▄▄· .▄▄ · .▄▄ ·     ▄▄▄  ▄▄▄ . ▄▄▄·      ▄▄▄  ▄▄▄▄▄    ▄▄▄▄▄            ▄▄▌  
·██ ▐███▪▐█ ▀█ ▐█ ▀. ▐█ ▀.     ▀▄ █·▀▄.▀·▐█ ▄█▪     ▀▄ █·•██      •██  ▪     ▪     ██•  
▐█ ▌▐▌▐█·▄█▀▀█ ▄▀▀▀█▄▄▀▀▀█▄    ▐▀▀▄ ▐▀▀▪▄ ██▀· ▄█▀▄ ▐▀▀▄  ▐█.▪     ▐█.▪ ▄█▀▄  ▄█▀▄ ██▪  
██ ██▌▐█▌▐█ ▪▐▌▐█▄▪▐█▐█▄▪▐█    ▐█•█▌▐█▄▄▌▐█▪·•▐█▌.▐▌▐█•█▌ ▐█▌·     ▐█▌·▐█▌.▐▌▐█▌.▐▌▐█▌▐▌
▀▀  █▪▀▀▀ ▀  ▀  ▀▀▀▀  ▀▀▀▀     .▀  ▀ ▀▀▀ .▀    ▀█▄▀▪.▀  ▀ ▀▀▀      ▀▀▀  ▀█▄▀▪ ▀█▄▀▪.▀▀▀ 

                                                                 by @xczur3k
"""

def load_file(file_path):
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}[ERROR] File not found: {file_path}{Style.RESET_ALL}")
        sys.exit(1)

async def drop_report(api_url, payload, headers, attempt_num, proxy):
    try:
        response = requests.post(api_url, json=payload, headers=headers, proxies=proxy)
        if response.status_code == 201:
            print(f"{Fore.GREEN}[EZ WIN] Report #{attempt_num} sent. GG.{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}[L] Report #{attempt_num} flopped: {response.status_code} - {response.text}{Style.RESET_ALL}")
            return False
    except Exception as oops:
        print(f"{Fore.RED}[OOPS] Something went kaboom: {oops}{Style.RESET_ALL}")
        return False

async def spam_reports(action_type, report_count, user_tokens, proxy_config, delay_ms):
    print(f"{Fore.CYAN}[HYPE] Spam fest loading...{Style.RESET_ALL}")
    dubs = 0
    flops = 0

    if action_type == "message":
        api_url = "https://discord.com/api/v9/report"
        msg_id = input(f"{Fore.LIGHTYELLOW_EX}[INPUT] Drop the message ID: {Style.RESET_ALL}")
        chan_id = input(f"{Fore.LIGHTYELLOW_EX}[INPUT] Channel ID where it lives: {Style.RESET_ALL}")
        payload_skeleton = {"message_id": msg_id, "channel_id": chan_id, "reason": 2}
    elif action_type == "user":
        api_url = "https://discord.com/api/v9/report"
        usr_id = input(f"{Fore.LIGHTYELLOW_EX}[INPUT] User ID to report: {Style.RESET_ALL}")
        payload_skeleton = {"user_id": usr_id, "reason": 1}
    elif action_type == "guild":
        api_url = "https://discord.com/api/v9/report"
        srv_id = input(f"{Fore.LIGHTYELLOW_EX}[INPUT] Server ID to roast: {Style.RESET_ALL}")
        payload_skeleton = {"guild_id": srv_id, "reason": 4}
    else:
        print(f"{Fore.RED}[NOPE] Wrong choice, buddy. Bye.{Style.RESET_ALL}")
        sys.exit(1)

    token_headers = [{"authorization": tok, "user-agent": "Mozilla/5.0"} for tok in user_tokens]

    for attempt in range(report_count):
        await asyncio.sleep(delay_ms / 1000)
        for idx, headr in enumerate(token_headers):
            print(f"{Fore.LIGHTBLUE_EX}[ACTION] Token {idx + 1}/{len(user_tokens)} ready to go.{Style.RESET_ALL}")
            if await drop_report(api_url, payload_skeleton, headr, attempt + 1, proxy_config):
                dubs += 1
            else:
                flops += 1

    print(f"{Fore.CYAN}[FINAL] {dubs} wins, {flops} fails. Donezo.{Style.RESET_ALL}")

def main():
    rbt(ASCII_ART, delay=0.01)

    print("""
    [1] Report a yapping message
    [2] Report a goofy ahh user
    [3] Report a clowny server
    """)
    action_choice = input(f"{Fore.LIGHTYELLOW_EX}[CHOICE] What you picking: {Style.RESET_ALL}")

    if action_choice == "1":
        action_type = "message"
    elif action_choice == "2":
        action_type = "user"
    elif action_choice == "3":
        action_type = "guild"
    else:
        print(f"{Fore.RED}[WRONG] Bad choice, restarting.{Style.RESET_ALL}")
        sys.exit(1)

    try:
        report_count = int(input(f"{Fore.LIGHTYELLOW_EX}[INPUT] How many times? {Style.RESET_ALL}"))
    except ValueError:
        print(f"{Fore.RED}[FAIL] Only numbers, start it.{Style.RESET_ALL}")
        sys.exit(1)

    try:
        delay_ms = int(input(f"{Fore.LIGHTYELLOW_EX}[INPUT] Delay between reports (in ms)? {Style.RESET_ALL}"))
    except ValueError:
        print(f"{Fore.RED}[FAIL] Only numbers, start it.{Style.RESET_ALL}")
        sys.exit(1)

    user_tokens = load_file("INPUT/tokens.txt")
    proxy_lines = load_file("INPUT/proxy.txt")
    proxy_config = None
    if proxy_lines:
        proxy = proxy_lines[0]
        proxy_split = proxy.split(":")
        proxy_config = {
            "http": f"http://{proxy_split[2]}:{proxy_split[3]}@{proxy_split[0]}:{proxy_split[1]}",
            "https": f"http://{proxy_split[2]}:{proxy_split[3]}@{proxy_split[0]}:{proxy_split[1]}"
        }

    asyncio.run(spam_reports(action_type, report_count, user_tokens, proxy_config, delay_ms))

    input(f"{Fore.CYAN}[DONE] Finished! Press Enter...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
