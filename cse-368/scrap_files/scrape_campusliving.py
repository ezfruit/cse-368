from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

driver = webdriver.Firefox()


url = 'https://www.buffalo.edu/campusliving.html'
driver.get(url)


def scrape_links():
    urls = []
    
    try:

        links = driver.find_elements(By.XPATH, "//a[contains(@class, 'cta-button')]")
        
        for link in links:
            link_url = link.get_attribute('href')
            link_text = link.text.strip()


            if link_url:
                urls.append([link_text, link_url])

    except Exception as e:
        print(f"Error scraping links: {e}")

  
    try:
        links = driver.find_elements(By.XPATH, "//a[contains(@class, 'teaser-primary-anchor')]")
        
        for link in links:
            link_url = link.get_attribute('href')
            link_text = link.text.strip() 

            if link_url:
                urls.append([link_text, link_url])

    except Exception as e:
        print(f"Error scraping links: {e}")

    return urls


all_urls = []

all_urls.extend(scrape_links())

with open('cta_and_teaser_buttons_urls.csv', mode='w', newline='') as file:
    data_writer = csv.writer(file)
    data_writer.writerow(['Link Text', 'URL']) 
    data_writer.writerows(all_urls) 


driver.quit()

