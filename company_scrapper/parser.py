"""
HTML Parser Module
Processes and extracts text from HTML content using BeautifulSoup.
"""

from bs4 import BeautifulSoup
from .utils import clean_text

def parse_html(html):
    """
    Parse HTML content into a BeautifulSoup object.
    
    Args:
        html (str): Raw HTML string
        
    Returns:
        BeautifulSoup: Parsed HTML object for querying
    """
    return BeautifulSoup(html, "lxml")

def get_visible_text(soup):
    """
    Extract visible text from HTML, removing script/style tags.
    
    Args:
        soup (BeautifulSoup): Parsed HTML object
        
    Returns:
        str: Cleaned visible text from the page
    """
    # Remove script and style tags as they contain non-visible content
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    
    # Get all remaining text and clean it
    text = soup.get_text()
    return clean_text(text)
    return clean_text(soup.get_text(separator=" "))