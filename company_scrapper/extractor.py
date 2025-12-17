"""
Data Extraction Module
Extracts structured company information from parsed HTML content.
Handles identity, contacts, pricing, services, and business details.
"""

from urllib.parse import urlparse
from .utils import extract_emails, extract_phones, is_social_link
import re

# Keywords used to identify priority pages to crawl
# These help find important company pages like pricing, careers, about, etc.
PRIORITY_KEYWORDS = [
    "about", "company", "products", "solutions",
    "industries", "pricing", "contact", "careers",
    "innovations", "about us", "blog", "news",
    "features", "services", "why", "use cases",
    "updates", "resources", "case studies",
    "contact", "contact us", "get in touch", "support",
    "help", "faq", "integrations", "partners",
    "jobs", "job", "hiring", "work with us", "join us",
    "team", "our team", "leadership"
]

def extract_identity(soup, url):
    """
    Extract company identity information (name, website, tagline).
    
    Args:
        soup (BeautifulSoup): Parsed HTML object
        url (str): Current page URL
        
    Returns:
        dict: Company name, website URL, and tagline
    """
    title = soup.title.string if soup.title else ""
    h1 = soup.find("h1")
    
    # Extract domain name from URL as fallback
    domain = urlparse(url).netloc.replace("www.", "").split(".")[0]
    
    # Extract company name from title (usually comes after | or -)
    company_name = domain.capitalize()
    if title:
        # Parse title to get company name
        parts = [p.strip() for p in title.replace(" | ", "|").replace(" - ", "-").split("|")]
        if len(parts) > 1:
            company_name = parts[-1]
        else:
            parts = title.split("-")
            if len(parts) > 1:
                company_name = parts[-1].strip()
            else:
                company_name = title.strip()

    return {
        "company_name": company_name,
        "website": url,
        "tagline": (h1.text.strip() if h1 else "")
    }

def extract_links(soup):
    return [a["href"] for a in soup.find_all("a", href=True)]

def filter_priority_pages(links):
    selected = []
    for link in links:
        for key in PRIORITY_KEYWORDS:
            if key in link.lower():
                selected.append(link)
                break
    return list(set(selected))

def extract_contacts(text):
    return {
        "emails": extract_emails(text),
        "phones": extract_phones(text)
    }

def extract_company_description(text):
    """Extract what the company does from the text"""
    if not text:
        return ""
    
    # Get first few sentences from the text that likely contain company description
    sentences = text.split('.')[:5]  # First 5 sentences
    description = '. '.join(sentences).strip()
    
    # Clean up and limit to 500 characters
    description = re.sub(r'\s+', ' ', description)
    if len(description) > 500:
        description = description[:500] + "..."
    
    return description

def extract_services_and_products(text):
    """Extract services, products, and offerings from text"""
    if not text:
        return []
    
    services = []
    
    # Common service/product keywords
    keywords = [
        "service", "product", "solution", "tool", "platform",
        "feature", "offering", "plan", "package", "subscription",
        "software", "application", "api", "integration", "plugin"
    ]
    
    # Split text into words and find lines containing service/product keywords
    lines = text.split('\n')
    for line in lines[:50]:  # Check first 50 lines
        line_lower = line.lower().strip()
        if not line_lower or len(line_lower) < 10:
            continue
        
        # Check if line mentions services/products
        for keyword in keywords:
            if keyword in line_lower and len(line) > 15 and len(line) < 200:
                services.append(line.strip())
                break
    
    # Remove duplicates and return unique services
    return list(set(services))[:10]  # Return max 10 services

def extract_pricing(text):
    """Extract detailed pricing information"""
    if not text:
        return {}
    
    pricing_info = {
        "tiers": [],
        "prices": [],
        "trial_available": False,
        "free_option": False
    }
    
    text_lower = text.lower()
    
    # Check for free option
    if "free" in text_lower:
        pricing_info["free_option"] = True
    
    # Check for trial
    if "trial" in text_lower or "free trial" in text_lower:
        pricing_info["trial_available"] = True
    
    # Extract pricing tiers
    tier_keywords = ["starter", "basic", "pro", "premium", "enterprise", "business", "professional"]
    for tier in tier_keywords:
        if tier in text_lower:
            pricing_info["tiers"].append(tier.capitalize())
    
    # Extract prices - match both with $ and without
    # First try to get prices with $
    price_pattern = r'\$[\d,]+(?:\.\d{2})?(?:/(?:month|year))?'
    prices_with_dollar = re.findall(price_pattern, text)
    
    # Also get prices without $ that are followed by /month or /year
    price_pattern_no_dollar = r'(?<![a-zA-Z])\d{2,5}(?:\.\d{2})?/(?:month|year)'
    prices_no_dollar = re.findall(price_pattern_no_dollar, text)
    
    # Also get standalone prices (just dollars)
    price_pattern_standalone = r'(?<!\$)\b\d{2,5}(?:\.\d{2})?\b(?![\d/])'
    prices_standalone = re.findall(price_pattern_standalone, text)
    
    # Combine and normalize all prices
    all_prices = set()
    
    # Add prices that already have $
    for price in prices_with_dollar:
        all_prices.add(price)
    
    # Add prices without $ and normalize them
    for price in prices_no_dollar:
        if not price.startswith('$'):
            price = '$' + price
        all_prices.add(price)
    
    # Add standalone prices with $
    for price in prices_standalone:
        if len(price) > 0 and price.isdigit() or ('.' in price):
            price = '$' + price
            all_prices.add(price)
    
    # Convert set to sorted list and limit to 5
    pricing_info["prices"] = sorted(list(all_prices))[:5]
    
    # Remove duplicates from tiers
    pricing_info["tiers"] = list(set(pricing_info["tiers"]))
    
    return pricing_info

def extract_target_customers(text):
    """Extract target customers/industries"""
    if not text:
        return []
    
    customers = []
    
    # Common industry/customer keywords
    keywords = [
        "enterprise", "startup", "sme", "small business", "mid-market",
        "enterprise", "healthcare", "finance", "retail", "education",
        "manufacturing", "technology", "agency", "team", "business",
        "professional", "developer", "freelancer", "consultant"
    ]
    
    text_lower = text.lower()
    for keyword in keywords:
        if keyword in text_lower:
            customers.append(keyword.capitalize())
    
    # Remove duplicates
    return list(set(customers))

def extract_business_info(text):
    """Extract comprehensive business information"""
    return {
        "services": extract_services_and_products(text),
        "pricing": extract_pricing(text),
        "target_customers": extract_target_customers(text)
    }

def categorize_social_links(links):
    socials = {}
    for link in links:
        l = link.lower()
        if "linkedin" in l:
            socials["linkedin"] = link
        elif "twitter" in l or "x.com" in l:
            socials["twitter"] = link
        elif "facebook" in l:
            socials["facebook"] = link
        elif "instagram" in l:
            socials["instagram"] = link
        elif "youtube" in l:
            socials["youtube"] = link
    return socials