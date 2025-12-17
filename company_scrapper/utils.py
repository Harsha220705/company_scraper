"""
Utility Functions Module
Contains helper functions for text processing, URL handling, and data extraction.
"""

import re
from urllib.parse import urljoin, urlparse

# List of social media domains to identify social links
SOCIAL_DOMAINS = [
    "linkedin.com",
    "twitter.com",
    "x.com",
    "facebook.com",
    "instagram.com",
    "youtube.com"
]

def clean_text(text):
    """
    Clean and normalize text by removing extra whitespace.
    
    Args:
        text (str): Raw text to clean
        
    Returns:
        str: Cleaned text with single spaces
    """
    if not text:
        return ""
    # Replace multiple spaces/newlines with single space
    return re.sub(r"\s+", " ", text).strip()

def extract_emails(text):
    """
    Extract email addresses from text using regex pattern.
    
    Args:
        text (str): Text to search for emails
        
    Returns:
        list: Unique email addresses found
    """
    return list(set(re.findall(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text or ""
    )))

def extract_phones(text):
    """
    Extract phone numbers from text with improved filtering.
    
    Args:
        text (str): Text to search for phone numbers
        
    Returns:
        list: Valid phone numbers found
    """
    if not text:
        return []
    
    # Better regex for phone numbers - matches formats like +1-555-123-4567, (555) 123-4567, etc.
    phone_pattern = r"(?:\+\d{1,3}[-.\s]?)?\(?[0-9]{2,4}\)?[-.\s]?[0-9]{2,4}[-.\s]?[0-9]{4}"
    matches = re.findall(phone_pattern, text)
    
    # Clean and filter duplicates
    phones = []
    seen = set()
    for match in matches:
        # Extract only digits and + for deduplication
        cleaned = re.sub(r'[^\d+]', '', match)
        
        # Filter out short numbers and duplicates
        if len(cleaned) >= 8 and cleaned not in seen:
            # Skip single/double/triple digit numbers (likely noise)
            if not re.match(r'^\d{1,4}$', cleaned):
                phones.append(match.strip())
                seen.add(cleaned)
    
    return phones

def get_internal_links(base_url, links):
    """
    Filter links to only include internal links from the same domain.
    
    Args:
        base_url (str): Base URL of the website
        links (list): List of all links found
        
    Returns:
        list: Internal links only
    """
    internal = set()
    base_domain = urlparse(base_url).netloc

    for link in links:
        full = urljoin(base_url, link)
        # Only include links from same domain
        if urlparse(full).netloc == base_domain:
            internal.add(full)

    return list(internal)

def is_social_link(url):
    """
    Check if a URL is a social media link.
    
    Args:
        url (str): URL to check
        
    Returns:
        bool: True if URL is from social media domain
    """
    return any(domain in url.lower() for domain in SOCIAL_DOMAINS)
    if not text:
        return []
    
    # Better regex for phone numbers
    # Matches patterns like: +1-555-123-4567, (555) 123-4567, +1 555 123 4567, etc.
    phone_pattern = r"(?:\+\d{1,3}[-.\s]?)?\(?[0-9]{2,4}\)?[-.\s]?[0-9]{2,4}[-.\s]?[0-9]{4}"
    matches = re.findall(phone_pattern, text)
    
    # Clean and filter
    phones = []
    seen = set()
    for match in matches:
        # Clean the phone number
        cleaned = re.sub(r'[^\d+]', '', match)  # Keep only digits and +
        
        # Filter out numbers that are too short or are just dates/numbers
        if len(cleaned) >= 8 and cleaned not in seen:
            # Check it's not just random numbers or dates
            if not re.match(r'^\d{1,4}$', cleaned):  # Skip single/double/triple digit numbers
                phones.append(match.strip())
                seen.add(cleaned)
    
    return phones

def get_internal_links(base_url, links):
    internal = set()
    base_domain = urlparse(base_url).netloc

    for link in links:
        full = urljoin(base_url, link)
        if urlparse(full).netloc == base_domain:
            internal.add(full)

    return list(internal)

def is_social_link(url):
    return any(domain in url.lower() for domain in SOCIAL_DOMAINS)