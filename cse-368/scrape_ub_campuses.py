import requests
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
        print("No campus information found")
