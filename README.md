# NET-WALKER
NET-WALKER is an OSINT tool for scraping emails and phone numbers from websites, designed for authorized pentesting and reconnaissance tasks. It features error handling, email validation, and customizable crawling options.


Installation

Follow these steps to set up NET-WALKER on your system:

1. Clone the Repository:
git clone https://github.com/lukehebe/NET-WALKER.git
cd NET-WALKER

2. Install Dependencies: Install the required Python packages using pip:
pip install -r requirements.txt

3. Run the Tool:
python3 NET-WALKER.py -t <url> [-d <depth>] [-s <scope>] [-o <output_file>] [-r <rate_limit>] [-v] [-D <data_type>]

Arguments
-t, --target <url>: Target URL to start the crawl (e.g., https://example.com). Required.
-d, --depth <int>: Maximum crawl depth (e.g., 1 for target page only, 2 for linked pages). Default: 1.
-s, --scope <domain|subdomains|all>: Crawling scope. Options: domain (same domain), subdomains (include subdomains), all (no restrictions). Default: domain.
-o, --output-file <file>: Output file for results (JSON format). Default: results.json.
-r, --rate-limit <float>: Delay between requests in seconds. Default: 0.5.
-v, --verbose: Enable verbose output to show crawling progress and found data.
-D, --data-type <emails|phones|both>: Data to scrape. Options: emails, phones, both. Default: both.
--user-agent <string>: Custom User-Agent for HTTP requests. Default: Chrome on Windows.


Ethical Use Disclaimer

NET-WALKER is intended for authorized security testing and OSINT tasks only. You must obtain explicit permission from the website owner before scraping any site. Unauthorized scraping may violate:

Website terms of service
Data protection laws (e.g., GDPR, CCPA)
Computer fraud laws (e.g., CFAA in the U.S.)
Always ensure compliance with local and international laws. The author is not responsible for misuse of this tool.
