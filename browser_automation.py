from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import os


def download_spreadsheet():
    print("Initializing the Chrome driver")
    options = Options()
    options.headless = False
    options.add_argument("--window-size=1920,1080")

    download_dir = os.path.expanduser("~/Downloads/AssetTigerDownloads")
    os.makedirs(download_dir, exist_ok=True)

    # Enable downloading in headless mode
    preferences = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", preferences)
    options.add_argument("--no-sandbox")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        print("Navigating to the Asset Tiger login page")
        driver.get("https://www.assettiger.com/login")

        print("Locating the login form and entering credentials")
        username_field = driver.find_element(By.ID, "Email")
        password_field = driver.find_element(By.ID, "Password")

        username_field.send_keys("steveanthony999@gmail.com")
        password_field.send_keys("bf3x!qLdassettiger")

        wait = WebDriverWait(driver, 10)

        print("Waiting for the sign-in button to be clickable")
        sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-primary') and @type='submit']")))
        print("Clicking the sign-in button")
        sign_in_button.click()
        print("Logging in")

        # Check if the dashboard page is reached
        print("Checking if logged in successfully")
        wait.until(EC.url_to_be("https://www.assettiger.com/dashboard"))
        print("Login successful, navigating to the Export page")
        driver.get("https://www.assettiger.com/export")
        print("Navigated to the Export page")

        export_type_dropdown_element = wait.until(EC.element_to_be_clickable((By.ID, "ExportType")))
        print("Selecting 'Assets' from the dropdown")
        export_type_dropdown = Select(export_type_dropdown_element)
        export_type_dropdown.select_by_value("1")
        print("Selected 'Assets'")

        print("Checking 'All Columns' checkbox")
        try:
            # Wait for the checkbox element to be present in the DOM
            all_columns_checkbox_element = wait.until(EC.presence_of_element_located((By.ID, "chkAll")))
            print("Found 'All Columns' checkbox")

            try:
                # Try clicking the checkbox directly
                all_columns_checkbox_element.click()
                print("Checked 'All Columns' checkbox")
            except Exception as click_exception:
                print(f"Direct click failed: {click_exception}, trying JavaScript click.")
                # If direct click fails, use JavaScript to click the checkbox
                driver.execute_script("arguments[0].click();", all_columns_checkbox_element)
                print("Checked 'All Columns' checkbox via JavaScript")

        except Exception as e:
            print(f"Failed to find or interact with the checkbox: {e}")

        print("Clicking the Export button")
        export_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'btn-primary') and @name='SubmitType' and @value='Export']")))
        print("Fou d the Export button")
        export_button.click()
        print("Clicked the Export button")

        print("Starting sleep")
        time.sleep(3)
        print("Ending sleep")

        print("Download initiated")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        print("Quitting")
        driver.quit()

    return "Download complete"


if __name__ == "__main__":
    download_spreadsheet()
