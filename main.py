import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

### options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_argument("user-data-dir=selenium")
mobile_emulation = {
    "deviceMetrics": { "width": 414, "height": 736, "pixelRatio": 3.0 },
    "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
}
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
chrome_options.add_argument("--disable-gpu");
chrome_options.add_argument("--disable-extensions");
chrome_options.add_experimental_option("useAutomationExtension", False);
chrome_options.add_argument("--proxy-server='direct://'");
chrome_options.add_argument("--proxy-bypass-list=*");
chrome_options.add_argument('--lang=en_US')
chrome_options.add_argument("--window-size=1366,768");
chrome_options.add_argument("--start-maximized");
chrome_options.add_argument("--disable-dev-shm-usage")
### options end

print('setting up driver.')
driver = webdriver.Chrome('./chromedriver', options=chrome_options)
print('done.')
driver.get('https://www.instagram.com/p/CEXItsJDVOP/')
#driver.get('https://www.instagram.com')
print('got page.')

print('sleeping...')
time.sleep(5)
print('sleep ended.')

print('taking screenshot.')
driver.save_screenshot("screenshot.png")

time.sleep(10000)

driver.quit()
