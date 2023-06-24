# SIMPLE SQL Injection Tester

This tool is a Python script that can be used to test SQL injection vulnerabilities in web applications. The tool generates a list of SQL injection payloads and injects them into the specified URL. The tool then checks the HTTP response for error messages that indicate a successful SQL injection attack.

## Disclaimer

Use this tool at your own risk. The tool is intended for security testing purposes only. The author of this tool is not responsible for any illegal or unauthorized use of the tool.

## Installation

1. Install Python 3.x from the official website: https://www.python.org/downloads/
2. Clone this repository or download the ZIP file and extract it to a directory.
3. Open a terminal or command prompt and navigate to the directory where the tool is located.
4. Install the required Python packages by running the following command: `pip install -r requirements.txt`

## Usage

```
python sql_injection_tester.py -u <url> [-t <tamper_script>] [-p <payload>] [--list-tampers] [--list-payloads] [-pn <payloads_number>]
```

### Required Arguments

* `-u/--url`: The URL to test.

### Optional Arguments

* `-t/--tamper`: The name of the tamper script to use. Tamper scripts can be used to modify the injection payloads before they are sent to the server.
* `-p/--payload`: Specify a custom payload to use instead of the default list of payloads.
* `--list-tampers`: List the available tamper scripts.
* `--list-payloads`: List the available payloads.
* `-pn/--payloads-number`: Specify the number of payloads to test.

### Example 1

```
python sql_injection_tester.py -u http://example.com/index.php?id=1 -t base64encode --payloads-number 10
```
### Example 2

```
python sql_injection_tester.py -u http://example.com/index.php?id=1 -t randomcase -p ' OR 1=1 -- -
```


This will test the URL `http://example.com/index.php?id=1` with the first 10 payloads from the default list of payloads, after encoding them with the `base64encode` tamper script.

## Output

The tool outputs the results of the injection test to the console and saves them in an HTML file called `result.html`. The HTML file contains a list of all the URLs that were tested and whether or not they resulted in a successful SQL injection attack. If an attack was successful, the error message that was returned by the server is also included.

### Notice
# the tool still young, when you find issues please help fixing


## Donations

If you find this tool useful and would like to support its development, you can make a donation using Ethereum (ETH):

ETH Wallet Address: 0x68699b4F7965A2347C2d61139856a2B7A40Bc41c

Your support is greatly appreciated!

## Algeria 🇩🇿🇩🇿
