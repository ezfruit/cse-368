from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
#*** I used the current lastest version of chromedriver: 130.0.6723.116 which is attached to the current folder.
#if a down grade of version is needed it might break some functions in my code
#***

# I used selenium to get a database of all the bus routes on campus for Fall 2024. It doesn't separate from north to south for now.
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
website = "https://www.buffalo.edu/parking/getting-around-UB/bus/bus-schedules/fall-semester.html"
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(website)
north = "Departures From North Campus"
south = "Departures From South Campus"
bus_buttons = driver.find_elements(By.XPATH, "//button[@class='collapsible-button']")
with open("UB_bus_schedules.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    schedule_div = ""
    for bus in bus_buttons:
        driver.execute_script("arguments[0].scrollIntoView(true);", bus) #scolling unti the bus schedule that needs to be click is clicked
        time.sleep(0.5)
        try:
            if bus.get_attribute("aria-expanded") == "false":
                bus.click()
                time.sleep(0.2)
                operation = driver.find_elements(By.TAG_NAME, "h3")
                schedule_div = driver.find_elements(By.XPATH, "//div[@class='table parbase section']")   
        except Exception as e:   
            print("bus schedule was not clickable")
    driver.execute_script("window.scrollTo(0, 0);")
    schedule_div = driver.find_elements(By.XPATH, "//div[@class='table parbase section']")   
    for schedule in schedule_div:

            op = operation[schedule_div.index(schedule)]
            op = op.text
            driver.execute_script("arguments[0].scrollIntoView(true);", schedule) #scolling unti the bus schedule that needs to be click is clicked
            # time.sleep(0.5)
            table = schedule.find_element(By.XPATH, ".//table[@border='1']")
            caption = table.find_element(By.TAG_NAME, "caption").text     
            writer.writerow([caption,op, "Bus Schedule"])
            lis = table.find_elements(By.TAG_NAME, "tr")

            for col in range(0, len(lis)):
                    if( col == 0 or col == 1):
                        temp = []
                        times = lis[col].find_elements(By.TAG_NAME, "th")
                        for head in times:
                            temp.append(head.text.strip())
                        if(len(temp) == 0):
                            temp = []
                            times = lis[col].find_elements(By.TAG_NAME,"td")
                            for time in times:
                                temp.append(time.text.strip())
                            writer.writerow(temp)
                        else:  
                            writer.writerow(temp)
                    else:
                        temp = []
                        times = lis[col].find_elements(By.TAG_NAME,"td")
                        for time in times:
                            temp.append(time.text.strip())
                        writer.writerow(temp)

            


driver.quit()
