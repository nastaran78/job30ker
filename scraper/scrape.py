import asyncio
import time
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from config.config import LINKEDIN_EMAIL, LINKEDIN_PASSWORD

# Constants
LOGIN_URL = 'https://www.linkedin.com/login'
BASE_SEARCH_URL = 'https://www.linkedin.com/jobs/search/'
MAX_PAGES = 4
SCROLL_STEP = 500
SLEEP_TIME = 2
RATE_LIMIT_WAIT = 300

class JobDetails:
    def __init__(self, job_id, title, company_name, link, job_desc):
        self.id = job_id
        self.title = title
        self.company_name = company_name
        self.link = link
        self.job_desc = job_desc

    def __str__(self):
        return f"Job ID: {self.id}, Title: {self.title}, Company: {self.company_name}, Job Link: {self.link}, Description: {self.job_desc}"

def setup_driver():
    """Set up the Selenium WebDriver with options."""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    return webdriver.Chrome(options=options)

def login_to_linkedin(driver):
    """Log in to LinkedIn using the provided credentials."""
    driver.get(LOGIN_URL)
    driver.find_element(By.ID, 'username').send_keys(LINKEDIN_EMAIL)
    driver.find_element(By.ID, 'password').send_keys(LINKEDIN_PASSWORD)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(SLEEP_TIME)

def build_search_url(page):
    """Build the LinkedIn job search URL for a specific page."""
    return (f"{BASE_SEARCH_URL}?keywords=software%20engineer"
            f"&f_E=1%2C2"
            f"&f_TPR=r604800"
            f"&location=Germany"
            f"&f_AL=true"
            f"&start={page * 25}")

def scrape_job_details(driver, llm_client, job, notifier, loop):
    """Scrape job details and send them to the notifier."""
    try:
        title_div = job.find_element(By.CLASS_NAME, 'artdeco-entity-lockup__title')
        title = job.find_element(By.TAG_NAME, 'a').get_attribute('aria-label')
        company_name = job.find_element(By.TAG_NAME, 'span').text
        link = title_div.find_element(By.TAG_NAME, 'a').get_attribute('href')
        job.find_element(By.TAG_NAME, 'a').click()
        driver.execute_script("arguments[0].scrollIntoView();", job)
        job_desc = driver.find_element(By.CLASS_NAME, 'jobs-description').text
        current_job_id = parse_qs(urlparse(driver.current_url).query).get('currentJobId', [0])[0]

        job_details = JobDetails(
            job_id=current_job_id,
            title=title,
            company_name=company_name,
            link=link,
            job_desc=job_desc,
        )
        loop.run_until_complete(llm_client.get_job_details(str(job_details), notifier))
    except NoSuchElementException as e:
        print("Error scraping job:", e)

def search_jobs(llm_client, notifier):
    """Search for jobs on LinkedIn and process the results."""
    loop = asyncio.get_event_loop()
    driver = setup_driver()
    try:
        login_to_linkedin(driver)
        for page in range(MAX_PAGES):
            search_url = build_search_url(page)
            try:
                driver.get(search_url)
            except NoSuchElementException:
                print("Rate limit exceeded. Waiting...")
                time.sleep(RATE_LIMIT_WAIT)
                driver.get(search_url)
            time.sleep(SLEEP_TIME)

            container = driver.find_element(By.TAG_NAME, 'ul')
            jobs = driver.find_elements(By.CLASS_NAME, 'job-card-container--clickable')
            for i in range(0, len(jobs), 5):  # Process jobs in batches of 5
                for job in jobs[i:i + 5]:
                    scrape_job_details(driver, llm_client, job, notifier, loop)
                driver.execute_script(f"arguments[0].scrollTop = {i * SCROLL_STEP}", container)
                time.sleep(SLEEP_TIME)
    finally:
        driver.quit()