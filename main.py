import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def get_email():
    # load from file .env
    with open('.env', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('email='):
                return line.split('=')[1].strip()
    return None


# Get the email from the .env file
email = get_email()


def get_password():
    # load from file .env
    with open('.env', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('password='):
                return line.split('=')[1].strip()
    return None


# Get the password from the .env file
password = get_password()

# Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)

# Set up the Chrome WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Open a webpage
driver.get("https://jinn.page/th/@SatitChula/home")

# get a that href="https://jinn.page/th/@SatitChula/entry/2BAbxWRsjvCAsXQ6WaQQ/main/cache14"
student_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.XPATH,
         "//a[@href='https://jinn.page/th/@SatitChula/entry/2BAbxWRsjvCAsXQ6WaQQ/main/cache14']")
    )
)

# Click the button
student_button.click()

# wait for class swal2-confirm swal2-styled and text = "OK"
ok_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.XPATH,
         "//*[contains(@class, 'swal2-confirm') and contains(@class, 'swal2-styled') and text()='OK']")
    )
)

# Click the OK button if needed
ok_button.click()

# email input
email_input = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.ID, "email-login-only")
    )
)

# Enter the email
email_input.send_keys(email)
# password input
password_input = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.ID, "password")
    )
)
# Enter the password
password_input.send_keys(password)

# login button btn btn-primary form-control
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.XPATH, "//button[@class='btn btn-primary form-control']")
    )
)
# Click the login button
login_button.click()



# button that text = "ลงทะเบียนวิชาเพิ่มเติม" #section2 > div.row.col-12.g-0.p-1.m-0.mb-5 > div:nth-child(5) > button
register_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.XPATH,
         "//button[.//small[contains(text(), 'ลงทะเบียนวิชาเพิ่มเติม')]"
         " and contains(@class, 'btn-block')"
         " and contains(@class, 'btn-secondary')]"
        )
    )
)
register_button.click()

# register_button = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable(
#         (By.XPATH,
#          "//button[contains(text(), 'ลงทะเบียนวิชาเพิ่มเติม')]")
#     )
# )
# # Click the register button
# register_button.click()

print("press enter to exit", end="")
input()
