import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def wake_up_streamlit():
    # Use environment secret for the app URL
    url = os.environ.get("STREAMLIT_APP_URL")
    if not url:
        print("❌ Error: STREAMLIT_APP_URL secret is not set.")
        return

    print(f"🚀 Initializing Selenium to ping: {url}")

    # Configure Chrome options for headless execution
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # Setup WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        driver.get(url)
        print("✅ Page loaded successfully.")

        # Wait for either the "Wake up" button OR the app container to appear
        wait = WebDriverWait(driver, 15)
        
        try:
            # Look for the button with specific text content
            wake_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Yes, get this app back up!')]")))
            print("🔔 Wake up button detected! Clipping it now...")
            wake_button.click()
            
            # Wait for the app container to indicate waking is in progress/complete
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='stAppViewContainer']")))
            print("🚀 App is waking up. Verification complete.")
            
        except Exception:
            # Check if the app container is already here (meaning it's already awake)
            if driver.find_elements(By.CSS_SELECTOR, "div[data-testid='stAppViewContainer']"):
                print("❇️ App is already awake. No action needed.")
            else:
                print("⚠️ Neither wake button nor app container found. Check URL or connection.")
                
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        driver.quit()
        print("🔗 Session closed.")

if __name__ == "__main__":
    wake_up_streamlit()
