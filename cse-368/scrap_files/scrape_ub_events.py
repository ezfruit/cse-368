from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv


driver = webdriver.Firefox()

url = 'https://calendar.buffalo.edu/'
driver.get(url)

def scrape_events():
    events = []
    
 
    date_header = driver.find_element(By.XPATH, "//div/h3").text

    event_articles = driver.find_elements(By.XPATH, "//article[@itemtype='http://schema.org/Event']")
    
    for event in event_articles:
        name = event.find_element(By.XPATH, ".//span[@itemprop='name']").text
        date_time = event.find_element(By.TAG_NAME, 'p').text
        event_url = event.find_element(By.XPATH, ".//a[@itemprop='url']").get_attribute('href')
        
        
        events.append([name, date_header + ', ' + date_time, event_url])
    
    return events

all_events = []


while True:
    all_events.extend(scrape_events())

    links = driver.find_elements(By.XPATH, "//div[@class='event-pagination']/ul/li/a")
    next_page = None
    for link in links:
        if 'next page' in link.get_attribute('title'):
            next_page = link
            break

    if next_page:
        next_page.click() 
        time.sleep(2)  # Wait for the page to load
    else:
        #print("No more pages available.")
        break


with open('ub_events.csv', mode='w', newline='') as file:
    data = csv.writer(file)
    data.writerow(['Event Name', 'Date and Time', 'URL'])
    data.writerows(all_events)

#print("Event data saved to events.csv successfully.")

driver.quit()