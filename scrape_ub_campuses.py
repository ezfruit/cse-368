"""import requests

from bs4 import BeautifulSoup

def scrape_ub_campuses():
    url = "https://www.buffalo.edu/home/ub_at_a_glance/our-campuses.html"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    campuses_info = []
    
    # Find all campus sections (they are typically wrapped in unstructuredpage divs)
    campus_sections = soup.find_all('div', class_='unstructuredpage')
    
    for section in campus_sections:
        # Find the title within this section
        title_div = section.find('div', class_='title section')
        if not title_div:
            continue
            
        name = title_div.find('h2')
        if not name:
            continue
            
        # Find the corresponding text section that follows the title
        text_section = section.find('div', class_='text parbase section')
        description = None
        if text_section:
            # Find the paragraph within the text section
            description = text_section.find('p')
            
        if name and description:
            campuses_info.append({
                'name': name.get_text(strip=True),
                'description': description.get_text(strip=True) if description else 'Description not found'
            })
    
    return campuses_info

if __name__ == "__main__":
    campuses = scrape_ub_campuses()
    if campuses:
        print("UB Campuses Information:")
        for campus in campuses:
            print(f"\nName: {campus['name']}")
            print(f"Description: {campus['description']}")
    else:
        print("No campus information found")"""

import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class CampusInfo:
    name: str
    subtitle: Optional[str] = None
    description: Optional[str] = None
    fun_facts: List[Dict[str, str]] = field(default_factory=list)
    links: List[Dict[str, str]] = field(default_factory=list)

def get_fun_facts(section):
    fun_facts = []
    # Find the Fun Facts section
    fun_facts_title = section.find('span', string=lambda x: x and 'Fun Facts' in x)
    if fun_facts_title:
        # Get the parent section that contains all fun facts
        facts_container = fun_facts_title.find_parent('div', class_='parsys_column')
        if facts_container:
            # Find all fact titles
            fact_titles = facts_container.find_all('span', class_='teaser-title')
            for title in fact_titles:
                # Get the description from the next text section
                desc_div = title.find_parent('div', class_='calltoaction').find_next_sibling('div', class_='text')
                if desc_div and desc_div.find('p'):
                    fun_facts.append({
                        'title': title.get_text(strip=True),
                        'description': desc_div.find('p').get_text(strip=True)
                    })
    return fun_facts

def get_description(section):
    desc_div = section.find('div', class_='text parbase section')
    if desc_div and desc_div.find('p'):
        return desc_div.find('p').get_text(strip=True)
    return None

def get_links(section):
    links = []
    link_list = section.find('div', class_='list parbase section')
    if link_list:
        for link in link_list.find_all('a', class_='teaser-primary-anchor'):
            title = link.find('span', class_='teaser-title')
            if title:
                links.append({
                    'text': title.get_text(strip=True),
                    'url': link.get('href', '')
                })
    return links

def scrape_ub_campuses():
    url = "https://www.buffalo.edu/home/ub_at_a_glance/our-campuses.html"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    campuses = {}

    # Process provided HTML content directly
    html_content = soup.decode()
    soup = BeautifulSoup(html_content, 'html.parser')
    
    for campus_name in ['North Campus', 'South Campus', 'Downtown Campus']:
        campus = CampusInfo(name=campus_name)
        
        # Find the main section for this campus
        campus_header = soup.find('h2', string=lambda x: x and campus_name in x)
        if campus_header:
            main_section = campus_header.find_parent('div', class_='unstructuredpage')
            if main_section:
                # Get subtitle
                subtitle = main_section.find('h2', id=lambda x: x and 'title' in x and 'cop' in x)
                if subtitle:
                    campus.subtitle = subtitle.get_text(strip=True)
                
                # Get description
                campus.description = get_description(main_section)
                
                # Get fun facts
                campus.fun_facts = get_fun_facts(main_section)
                
                # Get links
                campus.links = get_links(main_section)
                
        campuses[campus_name] = campus
    
    return campuses

def print_campus_info(campuses):
    for campus in campuses.values():
        print(f"\n{'='*50}")
        print(f"Campus: {campus.name}")
        print(f"{'='*50}")
        
        if campus.subtitle:
            print(f"\nSubtitle: {campus.subtitle}")
        
        if campus.description:
            print(f"\nDescription:\n{campus.description}")
        
        if campus.fun_facts:
            print("\nFun Facts:")
            for fact in campus.fun_facts:
                print(f"\n- {fact['title']}")
                print(f"  {fact['description']}")
        
        if campus.links:
            print("\nLinks:")
            for link in campus.links:
                print(f"- {link['text']}: {link['url']}")

if __name__ == "__main__":
    campuses = scrape_ub_campuses()
    if campuses:
        print_campus_info(campuses)
    else:
        print("No campus information found")
