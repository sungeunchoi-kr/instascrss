from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from PIL import Image
import re
import time
import bannerremover

class Snapshotter:
    driver = None
    last_run_time = 0

    def __init__(self):
        ### options
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")  # this option should be at the top.
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("user-data-dir=selenium")
        mobile_emulation = {
            "deviceMetrics": { "width": 414, "height": 788, "pixelRatio": 3.0 },
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

        # if it has been an hour since the previous snapshot, then run
        # the bannerremover.
        print('last_run_time={}'.format(self.last_run_time))
        if time.time() - self.last_run_time > 60*60:
            print('running bannerremover because it has been more ' +
                  'than an hour since the last snapshot.')
            bannerremover.run()
            self.last_run_time = time.time()
            print('bannerremover returned.')

            # get the page again because the timing below matters.
            self.driver.get(url)
            print('snapshot_post: got page ' + url + '.')

        # this amount of sleep is necessary for the scroll bars on the right to
        # disappear but for the "like" button notification wordcloud to not 
        # show up yet.
        time.sleep(0.200)
        print('snapshot_post: taking screenshot.')
        self.driver.save_screenshot(destinationPath)

        reduce_factor = 3
        img = Image.open(destinationPath)
        reduced_dimension = (img.size[0]//reduce_factor, img.size[1]//reduce_factor)
        print('snapshot_post: reduced_dimension=' + str(reduced_dimension))
        img2 = img.resize(reduced_dimension, Image.ANTIALIAS)
        img2.save(destinationPath)

    def convert_shortcode(self, shortcode):
        url = 'https://www.instagram.com/p/' + shortcode
        self.driver.get(url)
        print('convert_shortcode: got page ' + url + '.')

        print(self.driver.page_source)
        media_id = resolve_post_url_to_media_id(self.driver.page_source)
        print('convert_shortcode: found media_id=' + str(media_id) + '.')
        return media_id

    def save_snapshot(self):
        return

def resolve_post_url_to_media_id(pageHtml):
    try:
        match = re.search('content="instagram://media\?id=(.+?)"', pageHtml).group(1)
        return match
    except AttributeError:
        return None

