# webScraper

**webScraper** is a simple automated multitool for scraping websites, focusing on gathering information such as `robots.txt`, `sitemap.xml`, admin page discovery, subdomain enumeration, and DNS querying. The tool is written in Python and supports concurrency for faster enumeration and scraping tasks.

## Features
- Retrieve and save the `robots.txt` of a website.
- Retrieve and save the `sitemap.xml`.
- Discover potential admin pages using a wordlist.
- Enumerate subdomains using a wordlist.
- Perform DNS queries.
- Search for CMS based on the Wappalizer api
- Search for CVE based on the gathered CMS

## Installation
1. Clone the repository:
```bash
git clone https://github.com/laisoJS/webScraper.git
```
2. Install required dependencies:
```bash
pip install -r requirements.txt
```
3. Create a .env file:
You need to request an API key from nist.gov website:
https://nvd.nist.gov/developers/request-an-api-key
```bash
touch .env
echo "<Your API key" > .env
```

## Usage
To use the scraper, run it with the following options:
### Basic Usage:
```bash
python main.py <domain> [options]
```
### Sample Command Breakdown:
```bash
python main.py example.com -a wordlists/admin_pages.txt -s wordlists/subdomains.txt -c 10 -v
```
- `exemple.com`: The domain to scrape
- -a wordlists/admin_pages.txt: Use the admin_pages.txt wordlist for admin page discovery.
- -s wordlists/subdomains.txt: Use the subdomains.txt wordlist for subdomain enumeration.
- -c 10: Set concurrency to 10 tasks running simultaneously.
- -v: Enable verbose mode for detailed output.

| Argument | Description | Example |
|--|--|--|
| `<domain>`| The domain to scrape (without `http`/`https`). | `example.com` |
| `-a`, `--admin` | Path to a wordlist file for admin page discovery. | `-a wordlists/admin_pages.txt` |
| `-s`, `--subs` | Path to a wordlist file for subdomain enumeration. | `-s wordlists/subdomains.txt` |
| `-c`, `--concurrency` | Set the maximum concurrency level for asynchronous tasks. Default: 10. | `-c 20` |
| `-v`, `--verbose` | Enable verbose output to get detailed information about the process. | `-v` |

## Output
The output files will be saved in an output/ directory. The tool generates the following files based on the tasks executed:

- `robots.txt` from the target domain.
- `sitemap.xml` from the target domain.
- `admin.txt` containing discovered admin pages.
- `subdomains.txt` containing discovered subdomains.
- `cms.json` containing the name, version and category for the gathered cms
- `cve.json` containing a list of cve found by cms name and version
- `DNS.json` containing the DNS methods and the response of it
- `links.txt` containing the links of the website
- `sitemap_urls.txt` containing parsed urls from the sitemap.xml
- `forms.json` containing gathered form from pages

## Contributing
Feel free to submit issues and pull requests to improve this tool. Contributions are welcome!

## License
This project is licensed under the MIT License.

