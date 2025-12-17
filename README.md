# 🕷️ Company Web Scraper

A powerful web scraping tool that extracts comprehensive business information from company websites using Selenium and BeautifulSoup. Features both CLI and Streamlit UI interfaces.

## 🚀 Live Demo

**Try it now:** [Company Scraper on Streamlit Cloud](https://companyscraper-naqps36tbrf9cv5flcdouy.streamlit.app/)

## 📋 Features

- **🔍 Comprehensive Data Extraction**
  - Company identity (name, website, tagline)
  - Contact information (emails, phone numbers)
  - Pricing details (tiers, prices, free options, trial availability)
  - Social media links (LinkedIn, Twitter, Facebook, Instagram, YouTube)
  - Target customers and business information
  - Company description and services

- **🌐 Multi-Page Crawling**
  - Automatically identifies and crawls priority pages (pricing, careers, about, contact, etc.)
  - Extracts text from up to 8 priority pages
  - Combines data from multiple pages for comprehensive information

- **💾 Data Persistence**
  - Saves all results as JSON files
  - Examples folder stores all previous scrapes
  - Easy to reload and compare results

- **🎨 Beautiful UI**
  - Streamlit web interface for easy access
  - Real-time scraping with progress indicators
  - Recent scrapes sidebar for quick access
  - Beautiful metrics and formatted displays

- **📊 Detailed Output**
  - Company information with metrics
  - Business details and pricing breakdown
  - Contact information
  - Social media links
  - Pages visited
  - Raw JSON data export
  - Download results as JSON

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Chrome browser (for Selenium WebDriver)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Harsha220705/company_scraper.git
cd company_scraper
```

2. **Set up virtual environment**
```bash
python3 -m venv company_scrapper/venv
source company_scrapper/venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r company_scrapper/requirements.txt
```

### Usage

#### Option 1: Command Line Interface

```bash
./company_scrapper/venv/bin/python -m company_scrapper.runner --url https://www.notion.so
```

**Output:**
- Displays formatted company information in terminal
- Saves JSON file to `examples/` folder
- Shows confirmation message with file path

#### Option 2: Streamlit Web UI

```bash
./company_scrapper/venv/bin/streamlit run app.py
```

Then open `http://localhost:8501` in your browser

**Features:**
- Enter any company website URL
- View beautiful formatted results
- Browse recent scrapes
- Download JSON results
- View raw JSON data

## 📁 Project Structure

```
company_scraper/
├── app.py                          # Streamlit UI application
├── company_scrapper/
│   ├── __init__.py
│   ├── runner.py                  # Main orchestration script
│   ├── fetcher.py                 # Selenium WebDriver & page fetching
│   ├── parser.py                  # HTML parsing with BeautifulSoup
│   ├── extractor.py               # Data extraction logic
│   ├── utils.py                   # Utility functions
│   └── requirements.txt           # Dependencies
├── examples/                       # Scraped data results (JSON files)
└── README.md                       # This file
```

## 📦 Dependencies

```
selenium==4.15.2
beautifulsoup4==4.12.2
lxml==4.9.3
requests==2.31.0
webdriver-manager==4.0.1
streamlit==1.28.1
```

## 🔧 How It Works

### 1. **Website Fetching** (`fetcher.py`)
- Uses Selenium WebDriver with Chrome browser
- Automatically manages ChromeDriver using webdriver-manager
- Waits for JavaScript to execute
- Handles page load timeouts gracefully

### 2. **HTML Parsing** (`parser.py`)
- Uses BeautifulSoup with lxml parser
- Extracts visible text from HTML
- Removes script tags and non-visible content

### 3. **Data Extraction** (`extractor.py`)
- **Company Identity**: Extracts from page title and H1 tags
- **Priority Pages**: Identifies important pages using keyword matching
- **Pricing**: Uses regex to find pricing tiers and prices
- **Contacts**: Extracts emails and phone numbers
- **Social Links**: Identifies social media profiles
- **Business Info**: Extracts services, target customers, and descriptions

### 4. **Data Storage** (`runner.py`)
- Combines all extracted data into structured JSON
- Saves to `examples/` folder with timestamp
- Displays formatted summary in terminal
- Shows confirmation with file path

## 📊 Output Format

Each scrape generates a JSON file with this structure:

```json
{
  "metadata": {
    "timestamp": "2025-12-17T08:16:21.387252+00:00",
    "pages_crawled": 9,
    "errors": []
  },
  "identity": {
    "company_name": "Company Name",
    "website": "https://example.com",
    "tagline": "Company tagline"
  },
  "contacts": {
    "emails": ["contact@example.com"],
    "phones": ["+1 (555) 123-4567"]
  },
  "social_links": {
    "linkedin": "https://linkedin.com/company/...",
    "twitter": "https://twitter.com/...",
    "facebook": "https://facebook.com/...",
    "instagram": "https://instagram.com/...",
    "youtube": "https://youtube.com/..."
  },
  "description": "What the company does...",
  "business_info": {
    "services": ["Service 1", "Service 2"],
    "pricing": {
      "tiers": ["Basic", "Pro", "Enterprise"],
      "prices": ["$10/month", "$50/month", "Custom"],
      "free_option": true,
      "trial_available": true
    },
    "target_customers": ["Startup", "Enterprise", "SMB"]
  },
  "key_pages": {
    "visited": [
      "https://example.com/pricing",
      "https://example.com/about",
      "https://example.com/careers"
    ]
  }
}
```

## 🎯 Use Cases

- **Market Research**: Gather competitive intelligence
- **Lead Generation**: Extract contact information
- **Business Analysis**: Understand company offerings and pricing
- **Sales Intelligence**: Identify target customers
- **Content Research**: Collect company descriptions and taglines

## ⚙️ Configuration

### Priority Keywords
Located in `extractor.py`, controls which pages are crawled:
```python
PRIORITY_KEYWORDS = [
    "about", "company", "products", "solutions",
    "pricing", "contact", "careers", "blog", "news",
    "features", "services", "integrations", etc.
]
```

### Max Pages
Located in `runner.py`, controls crawling depth:
```python
MAX_PAGES = 8  # Maximum priority pages to crawl
```

## 🔍 Extraction Methods

### Email Extraction
Uses regex pattern: `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`

### Phone Number Extraction
- Matches patterns with country codes: `+1-555-123-4567`
- Matches parentheses format: `(555) 123-4567`
- Matches with slashes: `555/123/4567`
- Filters out false positives (dates, random numbers)

### Pricing Extraction
- Finds prices with `$` symbol
- Identifies pricing tiers (Basic, Pro, Enterprise, etc.)
- Detects free options and trial availability

## 📝 Example Results

### Notion
- **Company**: Notion
- **Pricing**: Free, $10/month, $20/month, $35/month, $340/month
- **Target Customers**: Startup, Small business, Enterprise, Developer, Team
- **Pages Visited**: 6 (pricing, careers, about, contact, blog, help)

### Mailchimp
- **Company**: Mailchimp
- **Pricing**: Free, $20/month, $300/month, $500/month
- **Emails Found**: support@mailchimp.com
- **Pages Visited**: 8 (features, integrations, services, about, resources)

## 🐛 Troubleshooting

### Browser Window Not Appearing
The browser window is set to visible by default. If it's not appearing:
- Check if you have Chrome browser installed
- Ensure webdriver-manager can download ChromeDriver

### Timeout Errors
- Website taking too long to load
- Increase timeout in `fetcher.py`: `driver.set_page_load_timeout(15)`

### No Results Found
- Website structure may be different
- Try different keywords in `PRIORITY_KEYWORDS`
- Check if website is blocking Selenium

### Module Not Found Errors
- Ensure all dependencies are installed: `pip install -r company_scrapper/requirements.txt`
- Activate virtual environment: `source company_scrapper/venv/bin/activate`

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🔗 Links

- **GitHub Repository**: https://github.com/Harsha220705/company_scraper
- **Issue Tracker**: https://github.com/Harsha220705/company_scraper/issues

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

Made with ❤️ by Harsha
