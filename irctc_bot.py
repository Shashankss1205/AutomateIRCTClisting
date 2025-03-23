from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os
import random
import time

# Load environment variables
load_dotenv()

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Edg/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.88 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) CriOS/122.0.0.0 Mobile/15E148 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/121.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.99 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.134 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
]


USERNAME = os.getenv("IRCTC_USERNAME", "")
PASSWORD = os.getenv("IRCTC_PASSWORD", "")

def random_delay(min_t=1, max_t=3):
    """Introduce a random delay to mimic human behavior."""
    time.sleep(random.uniform(min_t, max_t))

def automate_irctc(train_from, train_to, journey_date):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"])
        random_user_agent = random.choice(user_agents)
        context = browser.new_context(
            viewport={"width": 1366, "height": 768},
            user_agent=random_user_agent,
        )
        page = context.new_page()

        # Step 1: Open IRCTC Website
        page.goto("https://www.irctc.co.in/nget/train-search")
        random_delay(2, 5)

        # Step 2: Close popup if it appears
        try:
            page.click("text=OK", timeout=3000)
        except:
            pass  # Ignore if no popup appears
        random_delay()

        # # Step 3: Click Login
        page.click("text=LOGIN")
        random_delay()

        # Step 4: Enter Credentials
        page.fill("input[formcontrolname='userid']", USERNAME)
        random_delay()
        page.fill("input[formcontrolname='password']", PASSWORD)
        random_delay()

        # Step 5: Manual Captcha Entry
        input("Enter the Captcha manually and press Enter to continue...")

        # Step 6: Click Sign In
        page.locator("button:has-text('SIGN IN')").click()
        page.wait_for_load_state("networkidle")
        random_delay()

        # Step 7: Enter Train Details
        page.fill("input[aria-controls='pr_id_1_list']", train_from)
        random_delay()
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")

        page.fill("input[aria-controls='pr_id_2_list']", train_to)
        random_delay()
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")

        # page.fill("input[class='ng-tns-c58-11']", journey_date)
        page.fill("p-calendar[formcontrolname='journeyDate'] input", "24/03/2025")

        random_delay()
        page.evaluate("window.scrollBy(0, 200)")
        # Step 8: Search Trains
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")
        random_delay(3, 6)

        # Step 9: Select First Available Train
        page.click("xpath=(//button[contains(text(),'Check availability & fare')])[1]")
        page.wait_for_load_state("networkidle")
        random_delay(3, 6)

        # Step 10: Proceed with Booking (Optional)
        proceed = input("Do you want to proceed with booking? (yes/no): ").strip().lower()
        if proceed == "yes":
            page.click("xpath=(//button[contains(text(),'Book Now')])[1]")
            random_delay(3, 6)

            # Enter Passenger Details
            page.fill("input[formcontrolname='passengerName']", "John Doe")
            random_delay()
            page.fill("input[formcontrolname='passengerAge']", "25")
            random_delay()
            page.select_option("select[formcontrolname='passengerGender']", "M")

            # Click on Continue Booking
            page.click("button[type='submit']")
            page.wait_for_timeout(3000)

            # Payment Handling (Manual Step)
            input("Complete the payment manually and press Enter...")

        print("Process completed successfully.")
        browser.close()

# Run the function
automate_irctc("NEW DELHI - NDLS", "MUMBAI CENTRAL - MMCT", "24-03-2025")
