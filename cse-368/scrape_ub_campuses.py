import requests
from bs4 import BeautifulSoup
import csv

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
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    campuses_info = []
    
    # Find all campus sections (they are typically wrapped in unstructuredpage divs)
    campus_sections = soup.find_all('div', class_='reference2 reference parbase section')
    
    """facts = soup.find_all('div', class_='parsys_column cq-colctrl-6-3')
    for f in facts:
        fa = section.find('div', class_='title section')
        fun_facts = fa.find('h2', class_='h2sectionbar bold-ub-blue')"""
    
    for section in campus_sections:
        
        # Find the title within this section
        title_div = section.find('div', class_='title section')
        print(title_div)

        if not title_div:
            continue
            
        name = title_div.find('h2', class_='h2sectionbar bold-ub-blue')
        #fun_facts = title_div.find('h2', class_='h2sectionbar bold-ub-blue')
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

def save_to_csv(data, filename='ub_campuses.csv'):
    # Define the header
    headers = ['name', 'description']
    
    # Open the file in write mode and save the data
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    campuses = scrape_ub_campuses()
    if campuses:
        print("UB Campuses Information:")
        for campus in campuses:
            print(f"\nName: {campus['name']}")
            print(f"Description: {campus['description']}")
        
        # Save data to CSV
        save_to_csv(campuses)
    else:
        print("No campus information found")
