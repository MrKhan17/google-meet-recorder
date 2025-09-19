from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

from datetime import datetime

from recording import start_recording_async

from google_drive_oauth import GoogleDriveOAuth

import config
import os

config.setup()
logger = config.get_logger()


def google_login(driver, mail_address: str, password: str):
    """Login to Google account"""
    try:
        # Google Account Login ---
        driver.get("https://accounts.google.com/")
        
        # Input Gmail
        # Wait for email field and enter email
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        ).send_keys(mail_address)
        driver.find_element(By.ID, "identifierNext").click()

        # Input Password
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "Passwd"))
        ).send_keys(password)
        driver.find_element(By.ID, "passwordNext").click()

        # Wait for login to complete
        WebDriverWait(driver, 15).until(
            EC.url_contains("myaccount.google.com")
        )
        
        return True
    except Exception as e:
        print(f"Login failed: {e}")
        return False
    
def upload_to_drive(file_path: str, folder_name: str = "Meeting Recordings"):
    """Upload file to Google Drive"""
    try:
        google_oauth = GoogleDriveOAuth()
        
        # Create or get folder
        folder = google_oauth.create_folder(folder_name)
        
        # Generate timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        drive_filename = f"meeting_recording_{timestamp}.mp3"
        
        
        folder_id = folder['id'] if folder else None
        print(folder_id)
        result = google_oauth.upload_file(file_path, folder_id=folder_id, file_name=drive_filename)
        
        return result
    except Exception as e:
        print(f"Upload error: {e}")
        return None

async def record_meeting(meeting_url: str, duration_minutes: int, folder_name: str):
    """Record a meeting session and upload to Google Drive"""
    try:
        logger.info(f"Starting recording for meeting: {meeting_url}")
        
        # Get credentials from environment variables
        mail_address = os.getenv('GMAIL_ADDRESS')
        password = os.getenv('GMAIL_PASSWORD')
        
        if not mail_address or not password:
            raise Exception("Gmail credentials not found in environment variables")
        
        opt = config.get_chrome_options()
        
        try:
            opt.binary_location = "/usr/bin/chromium"
            service = Service("/usr/bin/chromedriver")
            driver = webdriver.Chrome(service=service, options=opt)
        except Exception as e:
            logger.warning(f"Failed to use chromium-browser, trying default: {e}")
            # Fallback to default Chrome
            driver = webdriver.Chrome(options=opt)

        try:
            # Login to Google
            logger.info("Logging in to Google account")
            if not google_login(driver, mail_address, password):
                raise Exception("Failed to login to Google account")
            
            # Navigate to meeting
            logger.info("Joining meeting")
            driver.get(meeting_url)
            
            # Wait for and click join button
            join_btn = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH,
                    "//span[contains(text(),'Join now') or contains(text(),'Ask to join')]/ancestor::button"
                ))
            )
            join_btn.click()
            
            # Start recording
            logger.info("Starting recording")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            meeting_id = meeting_url.split("/")[-1]

            output_file = f"{meeting_id}_{timestamp}.mp3"
            duration_seconds = duration_minutes * 60

            recording_success = await start_recording_async(output_file, duration_seconds)

            if recording_success:
                logger.info("Recording completed, uploading to Google Drive")
                
                upload_result = upload_to_drive(output_file, folder_name)
                
                if upload_result:
                    logger.info("Upload completed successfully")
                    return {
                        "success": True,
                        "recording_file": output_file,
                        "drive_link": upload_result.get('webViewLink'),
                        "message": "Recording completed and uploaded to Google Drive"
                    }
                else:
                    return {
                        "success": False,
                        "recording_file": output_file,
                        "drive_link": None,
                        "message": "Recording completed but failed to upload to Google Drive"
                    }
            else:
                return {
                    "success": False,
                    "recording_file": None,
                    "drive_link": None,
                    "message": "Recording failed"
                }
                
        finally:
            driver.quit()
            
    except Exception as e:
        logger.error(f"Recording failed: {str(e)}")
        return {
            "success": False,
            "recording_file": None,
            "drive_link": None,
            "message": f"Recording failed: {str(e)}"
        }
