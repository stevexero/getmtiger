from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import Select
# from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
# import pandas as pd
# import shutil
# import time
# import os

load_dotenv()


def test_browser_automation():
    print("Testing browser startup...")
    options = Options()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(executable_path='/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://www.google.com")
        print("Page title:", driver.title)  # Prints the title of the page
        return driver.title  # Ensure that this value is returned
    except Exception as e:
        print("Error during browser test:", e)
        raise  # Re-raise the exception to handle it in the Flask route
    finally:
        driver.quit()


# def test_browser_automation():
#     print("Testing browser startup...")
#     options = Options()
#     options.headless = True
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")  # Required if running in limited /tmp filesystems like Docker
#
#     service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service, options=options)
#
#     try:
#         driver.get("https://www.google.com")
#         print("Page title:", driver.title)  # Should print the title of the page, confirm browser load
#         return driver.title
#     except Exception as e:
#         print("Error during browser test:", e)
#     finally:
#         driver.quit()


# def wait_for_download(directory, timeout=30):
#     files_before = set(os.listdir(directory))
#     elapsed_time = 0
#     while elapsed_time < timeout:
#         time.sleep(3)
#         elapsed_time += 3
#         files_after = set(os.listdir(directory))
#         new_files = files_after - files_before
#         if new_files:
#             return os.path.join(directory, new_files.pop())
#     return None


# def download_spreadsheet():
#     print("Initializing the Chrome driver")
#     options = Options()
#     options.headless = True
#     options.add_argument("--window-size=1920,1080")
#
#     download_dir = os.path.expanduser(os.environ.get('ASSET_TIGER_FILEPATH'))
#     os.makedirs(download_dir, exist_ok=True)
#
#     # Enable downloading in headless mode
#     preferences = {
#         "download.default_directory": download_dir,
#         "download.prompt_for_download": False,
#         "download.directory_upgrade": True,
#         "safebrowsing.enabled": True
#     }
#     options.add_experimental_option("prefs", preferences)
#     options.add_argument("--no-sandbox")
#
#     service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service, options=options)
#
#     try:
#         print("Navigating to the Asset Tiger login page")
#         driver.get(os.environ.get('ASSET_TIGER_LOGIN_URL'))
#
#         print("Locating the login form and entering credentials")
#         username_field = driver.find_element(By.ID, "Email")
#         password_field = driver.find_element(By.ID, "Password")
#
#         username_field.send_keys(os.environ.get('ASSET_TIGER_USERNAME'))
#         password_field.send_keys(os.environ.get('ASSET_TIGER_PASSWORD'))
#
#         wait = WebDriverWait(driver, 10)
#
#         print("Waiting for the sign-in button to be clickable")
#         sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-primary') and @type='submit']")))
#         print("Clicking the sign-in button")
#         sign_in_button.click()
#         print("Logging in")
#
#         # Check if the dashboard page is reached
#         print("Checking if logged in successfully")
#         wait.until(EC.url_to_be(os.environ.get('ASSET_TIGER_DASHBOARD_URL')))
#         print("Login successful, navigating to the Export page")
#         driver.get(os.environ.get('ASSET_TIGER_EXPORT_URL'))
#         print("Navigated to the Export page")
#
#         export_type_dropdown_element = wait.until(EC.element_to_be_clickable((By.ID, "ExportType")))
#         print("Selecting 'Assets' from the dropdown")
#         export_type_dropdown = Select(export_type_dropdown_element)
#         export_type_dropdown.select_by_value("1")
#         print("Selected 'Assets'")
#
#         print("Checking 'All Columns' checkbox")
#         try:
#             # Wait for the checkbox element to be present in the DOM
#             all_columns_checkbox_element = wait.until(EC.presence_of_element_located((By.ID, "chkAll")))
#             print("Found 'All Columns' checkbox")
#
#             try:
#                 # Try clicking the checkbox directly
#                 all_columns_checkbox_element.click()
#                 print("Checked 'All Columns' checkbox")
#             except Exception as click_exception:
#                 print(f"Direct click failed: {click_exception}, trying JavaScript click.")
#                 # If direct click fails, use JavaScript to click the checkbox
#                 driver.execute_script("arguments[0].click();", all_columns_checkbox_element)
#                 print("Checked 'All Columns' checkbox via JavaScript")
#
#         except Exception as e:
#             print(f"Failed to find or interact with the checkbox: {e}")
#
#         print("Clicking the Export button")
#         export_button = wait.until(EC.element_to_be_clickable(
#             (By.XPATH, "//button[contains(@class, 'btn-primary') and @name='SubmitType' and @value='Export']")))
#         print("Found the Export button")
#         export_button.click()
#         print("Clicked the Export button")
#
#         # Wait for the download to complete
#         downloaded_file_path = wait_for_download(download_dir)
#         if downloaded_file_path:
#             standard_file_path = os.path.join(download_dir, os.environ.get('ASSET_TIGER_FILENAME'))
#             shutil.move(downloaded_file_path, standard_file_path)
#             print(f"File renamed to {standard_file_path}")
#         else:
#             print("Download did not complete within the expected time frame.")
#
#         print("Download initiated")
#
#     except Exception as e:
#         print(f"An error occurred: {e}")
#
#     finally:
#         print("Quitting")
#         driver.quit()
#
#     return "Download complete"


# def upload_spreadsheet(spreadsheet_path):
#     print("Initializing the Chrome driver")
#     options = Options()
#     options.headless = True
#     options.add_argument("--window-size=1920,1080")
#
#     file_dir = os.path.expanduser(os.environ.get('ASSET_TIGER_FILEPATH'))
#     os.makedirs(file_dir, exist_ok=True)
#
#     # Enable downloading in headless mode
#     preferences = {
#         "download.default_directory": file_dir,
#         "download.prompt_for_download": False,
#         "download.directory_upgrade": True,
#         "safebrowsing.enabled": True
#     }
#     options.add_experimental_option("prefs", preferences)
#     options.add_argument("--no-sandbox")
#
#     service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service, options=options)
#
#     try:
#         print("Navigating to the Asset Tiger login page")
#         driver.get(os.environ.get("ASSET_TIGER_LOGIN_URL"))
#
#         print("Locating the login form and entering credentials")
#         username_field = driver.find_element(By.ID, "Email")
#         password_field = driver.find_element(By.ID, "Password")
#
#         username_field.send_keys(os.environ.get('ASSET_TIGER_USERNAME'))
#         password_field.send_keys(os.environ.get('ASSET_TIGER_PASSWORD'))
#
#         wait = WebDriverWait(driver, 10)
#
#         print("Waiting for the sign-in button to be clickable")
#         sign_in_button = wait.until(
#             EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-primary') and @type='submit']")))
#         print("Clicking the sign-in button")
#         sign_in_button.click()
#         print("Logging in")
#
#         # Check if the dashboard page is reached
#         print("Checking if logged in successfully")
#         wait.until(EC.url_to_be(os.environ.get('ASSET_TIGER_DASHBOARD_URL')))
#         print("Login successful, navigating to the Import page")
#         driver.get(os.environ.get('ASSET_TIGER_IMPORT_URL'))
#         print("Navigated to the Import page")
#
#         # Upload the file
#         print("finding file input element")
#         file_input = driver.find_element(By.ID, "File")
#         print("found file input element")
#         file_input.send_keys(spreadsheet_path)
#
#         # Check for the file input error message
#         error_message_selector = ".field-validation-error[data-valmsg-for='File']"
#         try:
#             error_message = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, error_message_selector)))
#             if error_message.text:
#                 print(f"Error message displayed: {error_message.text}")
#         except TimeoutException:
#             print("No error message - proceeding with file upload")
#
#         # Click the 'Upload File' button
#         print("finding upload button")
#         upload_button = driver.find_element(By.ID, "uploadButton")
#         print("Found upload button")
#         upload_button.click()
#
#         # Wait and click the button that shows the dropdown
#         print("Clicking the dropdown to show options")
#         index_purchase_date_button = wait.until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-id='IndexPurchaseDate']")))
#         index_purchase_date_button.click()
#
#         # Wait and click the 'No Column' option in the dropdown
#         print("Selecting 'No Column'")
#         no_column_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='No Column']")))
#         no_column_option.click()
#
#         # Wait and click the 'Preview' button
#         print("finding preview button")
#         wait.until(EC.element_to_be_clickable((By.ID, "previewButton"))).click()
#         print("Found preview button")
#
#         # Wait and click the 'Import Data' button
#         print("finding importdata button")
#         wait.until(EC.element_to_be_clickable((By.ID, "importdata"))).click()
#         print("Found importdata button")
#
#         # Additional steps or waits might be necessary here to ensure the upload process is complete
#         # Consider also checking for any confirmation messages or status updates on the webpage
#         time.sleep(10)  # Pause for 10 seconds
#
#         # Now you can manually inspect the page to see what's going on.
#         # You can adjust the sleep time as needed for your analysis.
#         print("Resuming the script after the pause.")
#
#     except Exception as e:
#         print(f"An error occurred: {e}")
#
#     finally:
#         driver.quit()
#
#
# existing_asset_ids = ['temp0']


# def generate_unique_asset_id(existing_ids, prefix='temp'):
#     # Generate a unique asset ID by incrementing the last number used
#     last_number = max([int(id.replace(prefix, '')) for id in existing_ids if id.startswith(prefix)] or [0])
#     return f"{prefix}{last_number + 1}"


# def add_user_to_spreadsheet(user_id, user_email, spreadsheet_path):
#     print("Adding THE user to spreadsheet")
#     try:
#         # Load the spreadsheet
#         df = pd.read_excel(spreadsheet_path)
#         print("df: ", end="")
#         print(df)
#
#         # Check if the user_id already exists in the 'Customer ID' column
#         if user_id in df['Customer ID'].values:
#             print(f"User ID {user_id} already exists in the spreadsheet.")
#         else:
#             new_asset_id = generate_unique_asset_id(existing_asset_ids)
#             existing_asset_ids.append(new_asset_id)
#
#             new_row_data = {
#                 'Customer ID': user_id,
#                 'Customer Email': user_email,
#                 'Description': new_asset_id,  # Hard-coded for now
#                 'Asset Tag ID': new_asset_id  # The new unique asset ID
#             }
#
#             for col in df.columns.difference(new_row_data.keys()):
#                 new_row_data[col] = ''
#
#             # Add the user ID to the spreadsheet (append or modify a row as needed)
#             # print("appending user id to spreadsheet")  # doesn't print after this
#             # new_row_data = {col: '' for col in df.columns}  # Set all columns to empty strings
#             # new_row_data['Customer ID'] = user_id  # Set the 'Customer ID' column with the user_id
#             new_row = pd.DataFrame([new_row_data])  # Create a new DataFrame from the dictionary
#             df = pd.concat([df, new_row], ignore_index=True)
#             print("df: ", end="")
#             print(df)
#
#             # Save the modified spreadsheet
#             df.to_excel(spreadsheet_path, index=False)
#             print("df: ", end="")
#             print(df)
#
#             upload_spreadsheet(spreadsheet_path)
#     except Exception as e:
#         print(f"An error occurred: {e}")


# if __name__ == "__main__":
