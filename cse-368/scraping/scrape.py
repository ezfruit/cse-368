from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import csv
import time

service = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=service)

with open("UB_Residential_Calendar.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Semester", "Date", "Details"])
    try:
        driver.get("https://www.buffalo.edu/campusliving/for-current-students/residential-calendar.html")
        time.sleep(2)
        buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'collapsible-button')]")
        for button in buttons:
            semester = button.text
            button.click()
            time.sleep(2)
            date_and_details = driver.find_elements(By.XPATH, "//div[contains(@class, 'text parbase section')]//li")
            for i in date_and_details:
                text = i.text
                if text != '' and ':' in text:
                    [date, details] = text.split(':', 1)
                    writer.writerow([semester, date, details])
                    time.sleep(0.1)
    finally:
        driver.quit()

