"""
Company Scraper Runner
This module orchestrates the web scraping process for company information.
It fetches pages, extracts data, and saves results to JSON files.
"""

import argparse
import json
from datetime import datetime, timezone
import os
from pathlib import Path

from .fetcher import get_driver, fetch_page
from .parser import parse_html, get_visible_text
from .extractor import (
    extract_identity,
    extract_links,
    filter_priority_pages,
    extract_contacts,
    categorize_social_links,
    extract_company_description,
    extract_business_info
)
from .utils import get_internal_links, is_social_link

# Maximum number of priority pages to crawl per website
MAX_PAGES = 8

def run(url):
    """
    Main function to scrape company information from a website.
    
    Args:
        url (str): The company website URL to scrape
        
    Returns:
        dict: Comprehensive company information including identity, contacts, 
              pricing, services, and pages visited
    """
    driver = get_driver()
    result = {
        "metadata": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "pages_crawled": 0,
            "errors": []
        }
    }

    html, error = fetch_page(driver, url)
    if error or not html:
        result["metadata"]["errors"].append(str(error))
        driver.quit()
        return result

    soup = parse_html(html)
    homepage_text = get_visible_text(soup)

    result["identity"] = extract_identity(soup, url)

    all_text = homepage_text
    social_links = set()

    homepage_links = extract_links(soup)
    internal_links = get_internal_links(url, homepage_links)
    priority_pages = filter_priority_pages(internal_links)

    visited = []
    page_contents = {}

    for page_url in priority_pages[:MAX_PAGES]:
        page_html, err = fetch_page(driver, page_url)
        if not page_html:
            continue

        page_soup = parse_html(page_html)
        page_text = get_visible_text(page_soup)
        all_text += " " + page_text
        visited.append(page_url)
        
        # Store page content and metadata
        page_contents[page_url] = {
            "text_preview": page_text[:500],  # First 500 chars
            "title": page_soup.title.string if page_soup.title else "",
            "headings": [h.text.strip() for h in page_soup.find_all(['h1', 'h2', 'h3'])[:5]]
        }

        for a in page_soup.find_all("a", href=True):
            if is_social_link(a["href"]):
                social_links.add(a["href"])

    result["contacts"] = extract_contacts(all_text)
    result["social_links"] = categorize_social_links(social_links)
    result["description"] = extract_company_description(all_text)
    result["business_info"] = extract_business_info(all_text)

    result["key_pages"] = {
        "visited": visited,
        "page_details": page_contents
    }

    result["metadata"]["pages_crawled"] = 1 + len(visited)
    
    driver.quit()
    print(f"\n{'='*60}")
    print(f"Company: {result['identity']['company_name']}")
    print(f"Website: {result['identity']['website']}")
    print(f"Tagline: {result['identity']['tagline']}")
    print(f"{'='*60}")
    print(f"\nWhat They Do:")
    print(f"{result['description']}")
    print(f"\n{'='*60}")
    print(f"Business Information:")
    if result['business_info']['services']:
        print(f"Services/Products: {', '.join(result['business_info']['services'][:5])}")
    if result['business_info']['target_customers']:
        print(f"Target Customers: {', '.join(result['business_info']['target_customers'])}")
    
    pricing = result['business_info']['pricing']
    if pricing:
        print(f"\nPricing Details:")
        print(f"  Tiers: {', '.join(pricing['tiers']) if pricing['tiers'] else 'N/A'}")
        print(f"  Prices: {', '.join(pricing['prices']) if pricing['prices'] else 'N/A'}")
        print(f"  Free Option: {'Yes' if pricing['free_option'] else 'No'}")
        print(f"  Trial Available: {'Yes' if pricing['trial_available'] else 'No'}")
    
    print(f"\n{'='*60}")
    print(f"\nEmails Found: {result['contacts']['emails']}")
    print(f"Phones Found: {result['contacts']['phones']}")
    print(f"\n{'='*60}")
    print(f"Social Links:")
    for platform, link in result['social_links'].items():
        print(f"  {platform.upper()}: {link}")
    print(f"\n{'='*60}")
    print(f"Pages Visited: {len(visited)}")
    for i, page in enumerate(visited, 1):
        print(f"  {i}. {page}")
    print(f"{'='*60}\n")
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    args = parser.parse_args()

    output = run(args.url)
    
    # Create examples folder if it doesn't exist
    examples_dir = Path(__file__).parent.parent / "examples"
    examples_dir.mkdir(exist_ok=True)
    
    # Generate filename from company name
    company_name = output['identity']['company_name'].lower().replace(" ", "_").replace("/", "_")
    filename = f"{company_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = examples_dir / filename
    
    # Save JSON output
    with open(filepath, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(json.dumps(output, indent=2))
    print(f"\n✓ Saved to: {filepath}")