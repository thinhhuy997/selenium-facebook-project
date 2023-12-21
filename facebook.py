from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import time
from proxy_chrome_driver import get_chromedriver
from auto_action import auto_like, auto_haha, auto_play_video, auto_comment_on_livetream, auto_follow_on_livestream

# driver = webdriver.Chrome()


config = {
    "time_farm": {
        50
    },
    # reel or new feed
    'jobs': [
        {
            'name': 'like',
        }
    ],

    # delay time between jobs
    "delay-time": 20
}

# {
#     con:
#     acc
# }

accounts = [
    # This account using for create the page
    {
    "uid": "61553087692402",
    "password": "hocat2kzl",
    "fa_secret": "KXA7HGHXBY6AQGMRVSN2UJL74PCTAWIS"
    },

    # This account using for comment and like the post of user with uid: 61553087692402
    {
    "uid": "61553041014964",
    "password": "lodu4r6t",
    "fa_secret": "DKJDWFBVU3JEYZPD5IMQAIWT3Q2VMPKY"
    },
    # This account using for comment and like the post of user with uid: 61553087692402
    {
    "uid": "61552852831921",
    "password": "luongduyen4s25",
    "fa_secret": "47APFRLJJFBLYLPRLKUBY6LPGCCXU57F"
    },
    # test
    {
    "uid": "61552636782956",
    "password": "tohuong74l",
    "fa_secret": "XVZRNIQZ2SSPELUVHTWLUVWOZ3EAZ7ML"
    }
]

proxies = [
    {
        "ip": "103.162.31.188",
        "port": "5910",
        "username": "sun95910",
        "password": "7fbtn"
    }
]


user_agent_test = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"

driver = get_chromedriver(use_proxy=False, user_agent=None, host=proxies[0]["ip"], port=proxies[0]["port"], username=proxies[0]["username"], password=proxies[0]["password"])

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

    # Write cookie into file
    # get_cookie_and_write_it_into_file(file_name='fb_cookie.txt')

    # Scroll down continuously
    scroll_down_continuous(driver, scroll_delay=1, num_scrolls=4)

    

    # Open a new tab and interact (like, comment, ...)
    # open_new_tab_and_interact(url='/1182299486268776',like=True, comment=True, delay=5)

    # Watch live stream and interact
    # watch_livestream_and_interact(url='/351720304147664',like=True, comment=True, delay=5)

    
    

    # like some posts with post's count
    # like_some_post(2)

    # comment on some posts
    # comment_some_post(2)

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

def like_some_post(post_count: int):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Thích']")))
        like_buttons = driver.find_elements(By.XPATH, "//div[@aria-label='Thích']")
        print("count:", len(like_buttons))

        count = 0

        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Thích']"))).click()

        for like_button in like_buttons:
            if count <= post_count:
                like_button.click()

                # increase count
                count += 1

                # sleep in 2 seconds
                time.sleep(2)
            else:
                break
    except Exception as error:
        print(error)

def comment_some_post(post_count: int):
    try:
        show_comment_box_buttons = driver.find_elements(By.XPATH, "//div[@aria-label='Viết bình luận']")

        print("show_comment_box_buttons' count:", len(show_comment_box_buttons))

        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Viết bình luận']"))).click()

        
        for s_c_b_button in show_comment_box_buttons:
            # check
            # //div[@aria-label='Đóng']

            # click
            s_c_b_button.click()

            

            # check length of close buttons (2 if is dialog show and other hand)
           
            if len(driver.find_elements(By.XPATH, "//div[@aria-label='Đóng']")) == 2:
                print('TRUE')
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Đóng']"))).click()


                driver.find_elements(By.XPATH, "//div[@aria-label='Đóng']")[1].click()

            

            # sleep in 2 seconds
            time.sleep(2)
        
    except Exception as error:
        print(error)

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

def open_new_tab_and_interact(url='', like=False, comment=False, delay=2):
    time.sleep(2)
    try:
        driver.execute_script(f"window.open('{url}');")
        
        
        # Switch to second tab ~ correspond index is 1 (parent tab is 0)
        # In this case, index 1 corresponds to the second tab (since indexing starts from 0)
        driver.switch_to.window(driver.window_handles[1])


        if like:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Thích']"))).click()
            time.sleep(delay)

        if comment:
            time.sleep(delay)
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Viết bình luận']"))).click()

            # Locate comment box
            comment_box = driver.find_element(By.XPATH, "//div[@aria-label='Viết bình luận...']/p")

            # Enter into comment box
            comment_box.send_keys('Xin chào')

            # Hit ENTER
            comment_box.send_keys(Keys.RETURN)

        
        time.sleep(2)
        
        # close this tab
        # driver.close()

        # Switch back to the parent tab
        # driver.switch_to.window(driver.window_handles[0])

    except Exception as error:
        print(error)

def watch_livestream_and_interact(url='', like=False, comment=False, delay=2):
    time.sleep(delay)

    try:
        # open new tab
        driver.execute_script(f"window.open('{url}');")
        # Switch to second tab ~ correspond index is 1 (parent tab is 0)
        # In this case, index 1 corresponds to the second tab (since indexing starts from 0)
        driver.switch_to.window(driver.window_handles[1])

        # auto_like(driver, delay_action=5)


        # auto_play_video(driver=driver, delay_action=5)

        # auto_haha(driver, delay_action=5)
        # auto_comment_on_livetream(driver=driver, delay_action=5)

        auto_follow_on_livestream(driver, delay_action=5)

        # //div[@aria-label='Phát video']

        # Play video (live stream)
        # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Phát video']"))).click()
        

    except Exception as error:
        print(error)

def get_cookie_and_write_it_into_file(file_name:str):
    cookies = driver.get_cookies()

    fb_cookie_str = ""

    for cookie in cookies:
        fb_cookie_str += cookie['name'] + '=' + cookie['value'] + ';'
    if file_name:
        with open(file_name, 'w') as file:
            # Write fb_cookie_str to the file
            file.write(fb_cookie_str)

        print('Wrote facebook cookie successfully!')