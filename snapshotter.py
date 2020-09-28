from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Snapshotter:
    driver = None

    def __init__(self):
        ### options
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")  # this option should be at the top.
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

        print('Scraper: setting up driver.')
        self.driver = webdriver.Chrome('./chromedriver', options=chrome_options)
        print('Scraper: driver setup done.')

    def snapshot_post(self, urlId, destinationPath):
        url = 'https://www.instagram.com/p/' + urlId
        self.driver.get(url)
        print('snapshot_post: got page ' + url + '.')

        print('snapshot_post: taking screenshot.')
        self.driver.save_screenshot(destinationPath)

    def save_snapshot(self):
        return