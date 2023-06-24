import os
import requests
import random
import importlib.util
import argparse
import sys
import time
from urllib.parse import urlparse
from colorama import Fore, Style
from bs4 import BeautifulSoup

def get_error_message(response):

    return response.text.strip()

def scrape_html(url):
    response = requests.get(url)
    return response.text

def search_for_errors(html, error_patterns):
    soup = BeautifulSoup(html, 'html.parser')
    error_messages = []

    for pattern in error_patterns:
        elements = soup.find_all(text=lambda text: pattern in text)
        if elements:
            error_messages.extend(elements)

    return error_messages

def inject_payloads(url, payloads, tamper_script=None, payloads_number=None):
    results = []


    initial_response = requests.get(url)
    required_headers = initial_response.headers


    parsed_url = urlparse(url)
    referer_header = parsed_url.netloc


    if payloads_number:
        payloads = payloads[:payloads_number]

    for payload in payloads:
        injected_url = url + payload
        print(f"Trying payload: {payload}")

        if tamper_script is not None:
            tampered_payload = tamper_payload(payload, tamper_script)
            injected_url = url + tampered_payload
            print(f"Tampered payload: {tampered_payload}")


        user_agent = get_random_user_agent()


        headers = {
            "Referer": referer_header,
            "User-Agent": user_agent
        }
        response = requests.get(injected_url, headers=headers)
        print(response.headers)
        error_message = get_error_message(response)

        if is_sql_error(error_message):
            result = {
                "url": injected_url,
                "status_code": response.status_code,
                "error_message": error_message,
            }
            results.append(result)
            print(f"SQL error detected in URL: {injected_url}")


        time.sleep(4)

        print("Status Code:", end=" ")
        print_status_code(response.status_code)

    return results

def print_status_code(status_code):
    if status_code == 200:
        print(Fore.GREEN + str(status_code) + Style.RESET_ALL)
    elif status_code == 400:
        print(Fore.RED + str(status_code) + Style.RESET_ALL)
    elif status_code == 404:
        print(Fore.YELLOW + str(status_code) + Style.RESET_ALL)
    elif status_code == 500:
        print(Fore.MAGENTA + str(status_code) + Style.RESET_ALL)
    elif status_code == 403:
        print(Fore.CYAN + str(status_code) + Style.RESET_ALL)
    elif status_code == 401:
        print(Fore.BLUE + str(status_code) + Style.RESET_ALL)
    elif status_code == 503:
        print(Fore.YELLOW + Style.BRIGHT + str(status_code) + Style.RESET_ALL)
    elif status_code >= 300:
        print(Fore.CYAN + str(status_code) + Style.RESET_ALL)
    elif status_code >= 406:
        print(Fore.RED + str(status_code) + Style.RESET_ALL)
    else:
        print(str(status_code))

def is_sql_error(error_message):
    error_patterns_file = "error_patterns.txt"
    with open(error_patterns_file, "r") as file:
        error_patterns = [line.strip() for line in file]

    return any(pattern in error_message for pattern in error_patterns)

def tamper_payload(payload, tamper_script):
    tamper_module = load_tamper_script(tamper_script)
    return tamper_module.tamper(payload)

def load_tamper_script(tamper_script):
    tamper_directory = "tamper_scripts"
    tamper_module_path = os.path.join(tamper_directory, f"{tamper_script}.py")

    if not os.path.exists(tamper_module_path):
        raise ValueError(f"Tamper script '{tamper_script}' not found")

    spec = importlib.util.spec_from_file_location(tamper_script, tamper_module_path)
    tamper_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tamper_module)

    if not hasattr(tamper_module, "tamper"):
        raise ValueError(
            f"Tamper script '{tamper_script}' is missing the 'tamper' function"
        )

    return tamper_module

def list_tampers():
    tamper_directory = "tamper_scripts"
    tamper_files = os.listdir(tamper_directory)
    tampers = [
        os.path.splitext(file)[0] for file in tamper_files if file.endswith(".py")
    ]
    print("Available tamper scripts:")
    for tamper in tampers:
        print(tamper)
        
def list_payloads():
    payloads_file = "payloads.txt"
    with open(payloads_file, "r") as file:
        payloads = [line.strip() for line in file]

    print("Available payloads:")
    for payload in payloads:
        print(payload)


def read_payloads_from_file():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    payloads_file = os.path.join(script_directory, "payloads.txt")
    with open(payloads_file, "r") as file:
        payloads = [line.strip() for line in file]
    return payloads

def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",

    ]
    return random.choice(user_agents)

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", help="Specify the URL")
parser.add_argument("-t", "--tamper", help="Specify the tamper script to use")
parser.add_argument("-p", "--payload", help="Specify a custom payload")
parser.add_argument("-pn", "--payloads-number", type=int, help="How many payloads? from 1 to 1592")
parser.add_argument(
    "--list-tampers", action="store_true", help="List available tamper scripts"
)
parser.add_argument(
    "--list-payloads", action="store_true", help="List available payloads(1592)"
)
args = parser.parse_args()

if args.list_tampers:
    list_tampers()
    sys.exit()
    
if args.list_payloads:
    list_payloads()
    sys.exit()

if not args.url:
    parser.error("URL is required. Please provide a URL using the -u/--url argument.")

payloads = read_payloads_from_file()
if args.payload:
    payloads = [args.payload]

if args.payloads_number:
    payloads = payloads[:args.payloads_number]

results = inject_payloads(args.url, payloads, tamper_script=args.tamper)

with open("result.html", "w") as file:
    file.write("<html><body>")
    for result in results:
        file.write(f"<h3>URL: {result['url']}</h3>")
        file.write(f"<p>Status Code: {result['status_code']}</p>")
        if is_sql_error(result['error_message']):
            file.write(f"<p>Error Message: {result['error_message']}</p>")
        file.write("<hr>")
    file.write("</body></html>")

for result in results:
    print(f"URL: {result['url']}")
    print(f"Status Code: {result['status_code']}")
    if is_sql_error(result['error_message']):
        print(f"Error Message: {result['error_message']}")
    print("------------")

if is_sql_error(results[-1]['error_message']):
    print(f"SQL error detected in URL: {results[-1]['url']}")

print("Injection completed. Results are saved in 'result.html' file.")
print("please consider helping us improve ETH: 0x68699b4F7965A2347C2d61139856a2B7A40Bc41c")
