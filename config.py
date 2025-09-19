from selenium import webdriver

from dotenv import load_dotenv
import logging

def setup():
    """Load environment variables and setup logging"""
    logging.basicConfig(level=logging.INFO)
    load_dotenv()


def get_logger():
    """Setup logging configuration"""
    logger = logging.getLogger(__name__)
    return logger


def get_chrome_options():
    """Configure Chrome options for headless operation"""
    opt = webdriver.ChromeOptions()
    opt.add_argument('--disable-blink-features=AutomationControlled')
    # Recommended way for headless mode
    opt.add_argument('--headless=new')

    # General options for stability, especially in Docker/Linux
    opt.add_argument('--no-sandbox')
    opt.add_argument('--disable-dev-shm-usage')

    ## IMPORTANT
    # These flags are the key to making Meet work in headless
    # 1. Automatically grant permission for microphone and camera
    opt.add_argument("--use-fake-ui-for-media-stream")
    opt.add_argument("--use-fake-device-for-media-stream")

    # Disguise Selenium as a normal browser
    opt.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36')
    opt.add_argument("--disable-blink-features=AutomationControlled")
    opt.add_experimental_option("excludeSwitches", ["enable-automation"])
    opt.add_experimental_option('useAutomationExtension', False)


    # opt.add_argument('--disable-gpu')
    # opt.add_argument('--disable-extensions')
    # opt.add_argument('--disable-plugins')
    # opt.add_argument('--disable-images')
    # opt.add_argument('--disable-javascript')
    # opt.add_argument('--disable-css-animations')
    # opt.add_argument('--window-size=1920,1080')
    # opt.add_argument('--remote-debugging-port=9222')
    # opt.add_argument('--disable-web-security')
    # opt.add_argument('--allow-running-insecure-content')
    opt.add_experimental_option("prefs", {
        "profile.default_content_setting_values.media_stream_mic": 0,
        "profile.default_content_setting_values.media_stream_camera": 0,
        "profile.default_content_setting_values.geolocation": 0,
        "profile.default_content_setting_values.notifications": 0
    })
    # opt.add_experimental_option("excludeSwitches", ["enable-automation"])
    # opt.add_experimental_option('useAutomationExtension', False)
    return opt