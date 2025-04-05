from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv

# Setup headless Chrome
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://www.shl.com/solutions/products/product-catalog/"
driver.get(url)

# ✅ Wait for the assessment table to load
try:
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
    )
except:
    print("❌ Timeout: Table did not load.")
    driver.quit()
    exit()

rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
print(f"✅ Found {len(rows)} assessments.")

data = []

for row in rows:
    try:
        name_element = row.find_element(By.CSS_SELECTOR, "td:first-child a")
        name = name_element.text.strip()
        link = name_element.get_attribute("href")

        remote_dot = row.find_elements(By.CSS_SELECTOR, "td:nth-child(2) span")
        adaptive_dot = row.find_elements(By.CSS_SELECTOR, "td:nth-child(3) span")
        remote = "Yes" if remote_dot else "No"
        adaptive = "Yes" if adaptive_dot else "No"

        test_type_boxes = row.find_elements(By.CSS_SELECTOR, "td:nth-child(4) span")
        test_types = ", ".join([box.text.strip() for box in test_type_boxes])

        duration = "Unknown"  # placeholder

        data.append({
            "Assessment Name": name,
            "URL": link,
            "Remote Testing Support": remote,
            "Adaptive/IRT Support": adaptive,
            "Duration": duration,
            "Test Type": test_types
        })

        print(f"✔️ Scraped: {name}")

    except Exception as e:
        print(f"❌ Skipped a row due to error: {e}")

driver.quit()

if data:
    with open("shl_assessments.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print("✅ CSV saved as 'shl_assessments.csv'")
else:
    print("⚠️ No data scraped.")
