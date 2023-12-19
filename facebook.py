from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import time

driver = webdriver.Chrome()

config = {
    # reel or new feed
    'jobs': [
        {
            'name': 'new_feeds',
            'time': 50
        },
        {
            'name': 'like',
            'delay-time': 5
        }
    ]
}

{
    con:
    acc
}

accounts = [
    {
    "uid": "61552572046652",
    "password": "tonghai87um",
    "fa_secret": "47PLGEIQFMPTH3MHL4AU6NVRAGSSKPQ3"
    },
    {
    "uid": "61552572046652",
    "password": "nonghoa5x0c",
    "fa_secret": "PGUD3JFWP3IMKHPTLQFKW2JUYLAKZVNY"
    },
    {
    "uid": "61552797154523",
    "password": "lodu4raRAY",
    "fa_secret": "UJXOWHGRO2M5DNGTSICYU23L7GIWHZNW"
    },
    {
    "uid": "61553087692402",
    "password": "hocat2kzl",
    "fa_secret": "KXA7HGHXBY6AQGMRVSN2UJL74PCTAWIS"
    },
]


def login():
    # Navigate to the Facebook login page
    driver.get("https://www.facebook.com")

    # Find the username and password input fields and the login button using their respective attributes
    username_input = driver.find_element(By.ID, "email")
    password_input = driver.find_element(By.ID, "pass")
    login_button = driver.find_element(By.NAME, "login")


    # Enter your Facebook credentials
    username_input.send_keys(accounts[3]["uid"])
    password_input.send_keys(accounts[3]["password"])

    # Click the login button
    login_button.click()

    # Find the appovals_code field and checkPointSubmitbutton after click
    appovals_code_input = driver.find_element(By.ID, "approvals_code")
    checkPointSubmitbutton = driver.find_element(By.ID, "checkpointSubmitButton")

    # GET 2FA Code
    two_fa_code = get_2FA_Code(accounts[3]["fa_secret"])

    # Enter 2FA Code
    appovals_code_input.send_keys(two_fa_code)

    # Click the CPS_button
    checkPointSubmitbutton.click()

    # Find checkbox
    try:
        checkBox = driver.find_element(By.XPATH, "//div[@class='uiInputLabel clearfix uiInputLabelLegacy']/label")
        # click check box
        checkBox.click()
    except Exception as error:
        print(error)

    # find and click another CPS_Button
    try:
        checkPointSubmitbutton = driver.find_element(By.ID, "checkpointSubmitButton")
        checkPointSubmitbutton.click()
    except Exception as error:
        print(error)

    # Scroll down continuously
    scroll_down_continuous(driver, scroll_delay=2, num_scrolls=1)

    # find the first like_button and click it
    # try:
    #     like_button = driver.find_element(By.XPATH, "//div[@aria-label='Thích']")
    #     like_button.click()
    # except Exception as error:
    #     print(error)

    # # sleep in 2 seconds
    # time.sleep(2)

    # # find the first comment box and comment on it
    # try:
    #     # //div[@aria-label='Viết bình luận']
    #     show_comment_box_button = driver.find_element(By.XPATH, "//div[@aria-label='Viết bình luận']")
    #     show_comment_box_button.click()

    #     # Find comment box
    #     comment_box = driver.find_element(By.XPATH, "//div[@aria-label='Viết bình luận...']/p")
    #     # Enter comment contents
    #     comment_box.send_keys("<3")

    #     # Find comment button
    #     comment_button = driver.find_element(By.XPATH, "//div[@aria-label='Bình luận' and @role='button']")
    #     # Click
    #     comment_button.click()
    # except Exception as error:
    #     print(error)

    try:
        # like_buttons = driver.find_elements(By.XPATH, "//div[@aria-label='Thích']")
        # data-visualcompletion="css-img"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Thích']")))
        like_buttons = driver.find_elements(By.XPATH, "//div[@aria-label='Thích']")
        print("count:", len(like_buttons))

        for like_button in like_buttons:
            like_button.click()
    except Exception as error:
        print(error)

    # Allow some time for the login to complete (you might need to adjust this based on your internet speed)
    time.sleep(1000)

    # You can add further actions here, such as navigating to another page or interacting with elements on the page

    # Close the browser window
    driver.quit()

def get_2FA_Code(fa_secret: str):
    # URL with with the query param fa_scret
    url = f"https://2fa.live/tok/{fa_secret}"

    # A GET request to the API
    response = requests.get(url)

    # Return 2FA Code
    response_json = response.json()
    return response_json["token"]

def scroll_down_continuous(driver, scroll_delay=2, num_scrolls=None):
    # Define the scroll script
    scroll_script = "window.scrollTo(0, document.body.scrollHeight);"

    try:
        scroll_count = 0
        while num_scrolls is None or scroll_count < num_scrolls:
            # Execute the scroll script
            driver.execute_script(scroll_script)

            # Interacting

            
            # Wait for a short time to allow the content to load
            time.sleep(scroll_delay)

            scroll_count += 1
    except KeyboardInterrupt:
        # Handle interruption with KeyboardInterrupt (Ctrl+C)
        pass