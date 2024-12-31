import requests
import asyncio
import sys
import time
import colorsys
from colorama import init, Fore, Style
from itertools import cycle
import ctypes

init(autoreset=True)

def rbt(text, delay=0.05):
    for line in text.splitlines():
        colored_line = ""
        for i, char in enumerate(line):
            hue = (i / len(line)) * 360
            r, g, b = colorsys.hsv_to_rgb(hue / 360, 1, 1)
            r, g, b = int(r * 255), int(g * 255), int(b * 255)
            colored_line += f"\033[38;2;{r};{g};{b}m{char}\033[0m"
        print(colored_line)
        time.sleep(delay)

ASCII = r"""
███╗░░░███╗░█████╗░░██████╗░██████╗    ██████╗░███████╗██████╗░░█████╗░██████╗░████████╗
████╗░████║██╔══██╗██╔════╝██╔════╝    ██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝
██╔████╔██║███████║╚█████╗░╚█████╗░    ██████╔╝█████╗░░██████╔╝██║░░██║██████╔╝░░░██║░░░
██║╚██╔╝██║██╔══██║░╚═══██╗░╚═══██╗    ██╔══██╗██╔══╝░░██╔═══╝░██║░░██║██╔══██╗░░░██║░░░
██║░╚═╝░██║██║░░██║██████╔╝██████╔╝    ██║░░██║███████╗██║░░░░░╚█████╔╝██║░░██║░░░██║░░░
╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═════╝░╚═════╝░    ╚═╝░░╚═╝╚══════╝╚═╝░░░░░░╚════╝░╚═╝░░╚═╝░░░╚═╝░░░

                                                                 by @xczur3k
"""

rbc = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]

def print_with_rainbow(text, delay=0.05):
    color_cycle = cycle(rbc)
    for line in text.splitlines():
        colored_line = "".join(next(color_cycle) + char for char in line)
        print(colored_line)
        time.sleep(delay)

async def spam_report(message_id, channel_id, amount, token):
    print(f"{Fore.CYAN}[INFO] Spam report started...{Style.RESET_ALL}")
    success_count = 0
    error_count = 0

    try:
        for i in range(amount):
            await asyncio.sleep(1)
            reason = 2
            payload = {
                "message_id": message_id,
                "channel_id": channel_id,
                "reason": reason,
            }
            response = requests.post(
                "https://discord.com/api/v9/report",
                json=payload,
                headers={"authorization": token, "user-agent": "Mozilla/5.0"},
            )
            if response.status_code == 201:
                success_count += 1
                print(
                    f"{Fore.GREEN}[SUCCESS] Report {i + 1} sent successfully.{Style.RESET_ALL}"
                )
            else:
                error_count += 1
                print(
                    f"{Fore.RED}[FAILED] Report {i + 1} failed: {response.status_code} - {response.text}{Style.RESET_ALL}"
                )

        print(f"{Fore.CYAN}[INFO] Spam report finished.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[ERROR] {e}{Style.RESET_ALL}")

def main():
    rbt(ASCII, delay=0.01)

    message_id = input(
        f"{Fore.LIGHTYELLOW_EX}[INPUT] Enter the message ID to report: {Style.RESET_ALL}"
    )
    channel_id = input(
        f"{Fore.LIGHTYELLOW_EX}[INPUT] Enter the channel ID where the message was sent: {Style.RESET_ALL}"
    )
    try:
        amount = int(
            input(
                f"{Fore.LIGHTYELLOW_EX}[INPUT] Enter the number of reports to send: {Style.RESET_ALL}"
            )
        )
    except ValueError:
        print(
            f"{Fore.RED}[ERROR] Invalid number. Please enter an integer.{Style.RESET_ALL}"
        )
        sys.exit(0.01)

    token = input(
        f"{Fore.LIGHTYELLOW_EX}[INPUT] Enter your Discord token: {Style.RESET_ALL}"
    )

    asyncio.run(spam_report(message_id, channel_id, amount, token))

    input(f"{Fore.CYAN}[INFO] Report finished. Press Enter to exit...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
