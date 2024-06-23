import pickle
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome options
options = Options()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors=yes')
options.add_argument("--log-level=3")

# Setup Chrome driver service
service = Service(ChromeDriverManager().install(), log_output='nul')

# Initialize WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Load LinkedIn and add cookies
driver.get("https://linkedin.com")
time.sleep(2)

# Load cookies from file
try:
    with open("linkedin_cookies.pkl", "rb") as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
    driver.refresh()
    time.sleep(5)  # Wait for the page to load after refreshing
except FileNotFoundError:
    print("Cookies file not found. Please log in and save cookies first.")
    driver.quit()
    exit()

# Perform a search for "school" with location filter (India) and companies filter
search_query = "school"
location_filter = "companyHqGeo=%5B%22102713980%22%5D"  # Geo URN for India
search_url = f"https://www.linkedin.com/search/results/companies/?{location_filter}&keywords={search_query}"
driver.get(search_url)
time.sleep(5)  # Adjust based on page load time

# Function to scroll and extract company URLs
def scroll_and_extract_companies(driver):
    company_data = []  # Use a list to store company names and URLs
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # Adjust based on page load time
        
        companies = driver.find_elements(By.XPATH, "//a[contains(@href, '/company/') and contains(@class, 'app-aware-link')]")
        for company in companies:
            company_url = company.get_attribute("href")
            try:
                company_name_element = company.find_element(By.XPATH, ".//span[contains(@class, 'name')]")
                company_name = company_name_element.text
            except:
                company_name = "Unknown"
            
            if company_url and "linkedin.com/company/" in company_url:
                company_data.append([company_name, company_url])
        
        try:
            next_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Next')]")
            if next_button.is_enabled():
                next_button.click()
                time.sleep(5)  # Adjust based on page load time
            else:
                break
        except Exception as e:
            print("Next button not found or not clickable:", e)
            break

        return company_data

# Scroll and extract company data
company_data = scroll_and_extract_companies(driver)

# Save company data to a CSV file
with open('company_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Company Name', 'Company URL'])
    writer.writerows(company_data)

print(f"Extracted {len(company_data)} companies.")
print("Company data saved to company_data.csv")

# Close the driver
driver.quit()


