from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

# Initialize the WebDriver (using Firefox in this case)
driver = webdriver.Firefox()

# Define the URL you want to scrape
url = 'https://www.buffalo.edu/home/ub_at_a_glance/our-campuses.html'
driver.get(url)

# Wait for the page to load and <p> tags to be present
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'p')))
except Exception as e:
    print(f"Error waiting for page to load: {e}")
    driver.quit()

# Define the function to scrape all <p> tags
def scrape_paragraphs():
    paragraphs = []
    
    try:
        # Find all <p> tags on the page
        p_tags = driver.find_elements(By.TAG_NAME, 'p')
        
        for p_tag in p_tags:
            # Get the text of each <p> tag
            p_text = p_tag.text.strip()
            
            # Only add non-empty paragraphs
            if p_text:
                paragraphs.append([p_text])  # Store the paragraph text as a list
    
    except Exception as e:
        print(f"Error scraping paragraphs: {e}")
    
    return paragraphs

# List to store all the paragraphs
all_paragraphs = []

# Scrape the paragraphs
all_paragraphs.extend(scrape_paragraphs())

# Write the scraped data to a CSV file
with open('ub_campus_paragraphs.csv', mode='w', newline='', encoding='utf-8') as file:
    data_writer = csv.writer(file)
    data_writer.writerow(['Paragraph Text'])  
    data_writer.writerows(all_paragraphs) 

print("Paragraph texts saved to ub_campus_paragraphs.csv successfully.")

# Close the WebDriver
driver.quit()
