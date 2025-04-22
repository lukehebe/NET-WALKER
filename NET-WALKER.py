import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse
import sys
import json
import re
import time
from email_validator import validate_email, EmailNotValidError

def arguments():
    parser = argparse.ArgumentParser(description="NET-WALKER - OSINT Email & Phone Number Grabber")
    parser.add_argument(
        "-t", "--target",
        required=True,
        help="Target URL to start the crawl (e.g., https://example.com)"
    )
    parser.add_argument(
        "-d", "--depth",
        type=int,
        default=1,
        help="Maximum depth for link crawling (e.g., 1 = target page only, 2 = target + linked pages)"
    )
    parser.add_argument(
        "-s", "--scope",
        choices=["domain", "subdomains", "all"],
        default="domain",
        help="Scraping scope: 'domain' (same domain), 'subdomains' (include subdomains), 'all' (no restrictions)"
    )
    parser.add_argument(
        "-o", "--output-file",
        default="results.json",
        help="Output file for harvested data (e.g., results.json)"
    )
    parser.add_argument(
        "-r", "--rate-limit",
        type=float,
        default=0.5,
        help="Delay between requests in seconds (e.g., 0.5)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "-D", "--data-type",
        choices=["emails", "phones", "both"],
        default="both",
        help="Data to scrape: 'emails', 'phones', or 'both' (default: both)"
    )
    parser.add_argument(
        "--user-agent",
        default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        help="Custom User-Agent for HTTP requests"
    )
    return parser.parse_args()

def is_in_scope(url, target_domain, scope):
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return False
    if scope == "domain":
        return parsed.netloc == target_domain
    elif scope == "subdomains":
        return parsed.netloc == target_domain or parsed.netloc.endswith("." + target_domain)
    return True

def scrape_data(text, data_type):
    emails, phones = [], []
    if data_type in ["emails", "both"]:
        email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        raw_emails = re.findall(email_regex, text, re.IGNORECASE)
        for email in raw_emails:
            try:
                validate_email(email, check_deliverability=False)
                emails.append(email)
            except EmailNotValidError:
                pass
    if data_type in ["phones", "both"]:
        phone_regex = r'\b(?:\+1\s?)?(?:\(\d{3}\)\s?|\d{3}[-.]?)\d{3}[-.]?\d{4}\b'
        phones = re.findall(phone_regex, text)
    return emails, phones

def save_results(emails, phones, output_file, data_type):
    data = {}
    if data_type in ["emails", "both"]:
        data["emails"] = list(set(emails))
    if data_type in ["phones", "both"]:
        data["phone_numbers"] = list(set(phones))
    try:
        with open(output_file, "w") as f:
            json.dump(data, f, indent=4)
        print(f"[$$$] LOOT saved to {output_file}")
    except IOError as e:
        print(f"[-] Error saving to {output_file}: {e}")
        sys.exit(1)

def crawl(url, args, visited, depth=0, emails=None, phones=None):
    if emails is None:
        emails = []
    if phones is None:
        phones = []
    if depth > args.depth or url in visited:
        return emails, phones
    visited.add(url)
    if args.verbose:
        print(f"[*] Crawling {url} (Depth: {depth})")
    
    try:
        headers = {"User-Agent": args.user_agent}
        response = requests.get(url, timeout=5, headers=headers)
        response.raise_for_status()
        time.sleep(args.rate_limit)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract selected data
        page_emails, page_phones = scrape_data(response.text, args.data_type)
        emails.extend(page_emails)
        phones.extend(page_phones)
        
    except requests.RequestException as e:
        if args.verbose:
            print(f"[-] Error crawling {url}: {e}")
        return emails, phones
    
    if args.verbose and page_emails:
        print(f"[+] Found emails: {list(set(page_emails))}")
    if args.verbose and page_phones:
        print(f"[+] Found phones: {list(set(page_phones))}")
    
    if depth < args.depth:
        target_domain = urlparse(args.target).netloc
        for link in soup.find_all("a", href=True):
            next_url = urljoin(url, link["href"])
            if is_in_scope(next_url, target_domain, args.scope) and next_url not in visited:
                sub_emails, sub_phones = crawl(next_url, args, visited, depth + 1, emails, phones)
                emails.extend(sub_emails)
                phones.extend(sub_phones)
    
    return emails, phones

def print_banner():
    banner = r"""
     _   _ ______ _______  __          __     _      _  ________ _____
 | \ | |  ____|__   __| \ \        / /\   | |    | |/ /  ____|  __ \
 |  \| | |__     | |_____\ \  /\  / /  \  | |    | ' /| |__  | |__) |
 | . ` |  __|    | |______\ \/  \/ / /\ \ | |    |  < |  __| |  _  /
 | |\  | |____   | |       \  /\  / ____ \| |_ _ | |____| | \ \
 |_| \_|______|  |_|        \/  \/_/    \_\______|_|\_\______|_|  \_\

    """
    print(banner)

def main():
    print_banner()
    args = arguments()
    
    
    if not args.target.startswith(("http://", "https://")):
        args.target = "https://" + args.target
    
    print(f"[+] Starting NET-WALKER on {args.target} (Data: {args.data_type})")
    visited = set()
    emails, phones = crawl(args.target, args, visited)
       
    if emails or phones:
        save_results(emails, phones, args.output_file, data_type=args.data_type)
    else:
        print(f"[!] No {args.data_type} found")
    
    print(f"[+] Crawling complete. Visited {len(visited)} URLs")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[-] Stopped by user")
        sys.exit(0)
