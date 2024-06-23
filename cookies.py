import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors=yes')
options.add_argument("--log-level=3")

# Setting up service
service = Service(ChromeDriverManager().install(), log_output='nul')

# Creating a webdriver instance
driver = webdriver.Chrome(service=service, options=options)

# Open LinkedIn's login page
driver.get("https://linkedin.com/uas/login")

# Wait for the page to load
time.sleep(5)

# Enter username and password
username = driver.find_element(By.ID, "username")
username.send_keys("ayushi.121102@gmail.com")  # Replace with your LinkedIn email
pword = driver.find_element(By.ID, "password")
pword.send_keys("Tripti.soni@123")  # Replace with your LinkedIn password

# Click the login button
driver.find_element(By.XPATH, "//button[@type='submit']").click()

# Wait for login to complete
time.sleep(5)

# Save cookies to a file
with open("linkedin_cookies.pkl", "wb") as file:
    pickle.dump(driver.get_cookies(), file)

print("Cookies have been saved.")
driver.quit()
