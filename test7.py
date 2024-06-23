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

# Function to scroll and extract profile URLs
def scroll_and_extract_profiles(driver):
    profile_data = []  # Use a list to store profile names and URLs
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # Adjust based on page load time
        
        profiles = driver.find_elements(By.XPATH, "//a[contains(@href, '/in/') and contains(@class, 'app-aware-link')]")
        for profile in profiles:
            profile_url = profile.get_attribute("href")
            profile_name_element = profile.find_element(By.XPATH, ".//span[contains(@class, 'name')]")
            profile_name = profile_name_element.text if profile_name_element else "Unknown"
            if profile_url and "linkedin.com/in/" in profile_url:
                profile_data.append([profile_name, profile_url])
        
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

    return profile_data

# Scroll and extract profile data
profile_data = scroll_and_extract_profiles(driver)

# Save profile data to a CSV file
with open('profile_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Profile Name', 'Profile URL'])
    writer.writerows(profile_data)

print(f"Extracted {len(profile_data)} profiles.")
print("Profile data saved to profile_data.csv")

# Close the driver
driver.quit()
