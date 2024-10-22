import requests
from bs4 import BeautifulSoup
import re

def scrape_ub_campuses():
    # URL of the campuses page
    url = "https://www.buffalo.edu/home/ub_at_a_glance/our-campuses.html"
    
    # Send GET request
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return
    
    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the main content section
    campuses_info = []
    
    # Look for campus sections
    campus_sections = soup.find_all('div', class_='title section')  # Update class name if necessary
    print(f"Found {len(campus_sections)} campus sections.")  # Debugging output

    for section in campus_sections:
        name = section.find(['h2', 'h3'])
        description = section.find(['p', 'div'], class_='description')  # Adjust class if necessary
        if name:
            campuses_info.append({
                'name': name.get_text(strip=True),
                'description': description.get_text(strip=True) if description else 'Description not found'
            })
            print(f"Name: {name.get_text(strip=True)}")  # Debugging output
            print(f"Description: {description.get_text(strip=True) if description else 'Description not found'}")  # Debugging output
    
    # If no structured data found, try to get basic information
    if not campuses_info:
        main_content = soup.find('div', class_='page-content') or soup.find('main')
        if main_content:
            text_content = main_content.get_text()
            # Look for mentions of different campuses
            campus_patterns = ['North Campus', 'South Campus', 'Downtown Campus']
            for pattern in campus_patterns:
                if pattern in text_content:
                    context = get_context_around_campus(text_content, pattern)
                    campuses_info.append({
                        'name': pattern,
                        'description': context
                    })
    
    return campuses_info

def get_context_around_campus(text, campus_name):
    """Get the surrounding context for a campus mention"""
    try:
        start = text.index(campus_name)
        end = min(start + 200, len(text))
        context = text[start:end].split('.')[0] + '.'
        return context.strip()
    except ValueError:
        return 'Context not found'

if __name__ == "__main__":
    campuses = scrape_ub_campuses()
    if campuses:
        print("UB Campuses Information:")
        for campus in campuses:
            print(f"\nName: {campus['name']}")
            print(f"Description: {campus['description']}")
    else:
        print("No campus information found")
