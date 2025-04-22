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

Ethical Use Disclaimer

NET-WALKER is intended for authorized security testing and OSINT tasks only. You must obtain explicit permission from the website owner before scraping any site. Unauthorized scraping may violate:

Website terms of service
Data protection laws (e.g., GDPR, CCPA)
Computer fraud laws (e.g., CFAA in the U.S.)
Always ensure compliance with local and international laws. The author is not responsible for misuse of this tool.
