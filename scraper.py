import csv
import time
import requests
from bs4 import BeautifulSoup

# Configuration
TARGET_URL = "https://realpython.github.io/fake-jobs/"
OUTPUT_FILE = "jobs.csv"
HEADERS = {
    "User-Agent": "JobScraperBot/1.0 (+https://github.com/yourprofile/job-listings-scraper)"
}

def fetch_html(url):
    """Fetches HTML content from the target URL."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_jobs(html):
    """Parses job listings from HTML content."""
    soup = BeautifulSoup(html, "html.parser")
    jobs = []

    # Based on target site structure: listings are usually in a specific container
    # Using a generic selector that fits the common roadmap.sh demo site pattern
    job_elements = soup.find_all("div", class_="card-content")

    for element in job_elements:
        # Extract with fallbacks to prevent crashes on missing data
        # Use class_ only (no tag prefix) to remain resilient to whether
        # the site marks up fields with <div>, <h2>, etc.
        title_elem = element.find(class_="title")
        company_elem = element.find(class_="company")
        location_elem = element.find(class_="location")
        link_elem = element.find("a")

        jobs.append({
            "Title": title_elem.text.strip() if title_elem else "N/A",
            "Company": company_elem.text.strip() if company_elem else "N/A",
            "Location": location_elem.text.strip() if location_elem else "N/A",
            "URL": link_elem["href"] if link_elem and link_elem.has_attr("href") else "N/A"
        })

    return jobs

def save_to_csv(jobs, filename):
    """Saves the list of jobs to a CSV file, overwriting existing."""
    if not jobs:
        print("No jobs found to save.")
        return

    keys = jobs[0].keys()
    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(jobs)
        print(f"Successfully saved {len(jobs)} jobs to {filename}")
    except IOError as e:
        print(f"Error saving to CSV: {e}")

def main():
    print(f"Fetching jobs from {TARGET_URL}...")
    html = fetch_html(TARGET_URL)

    if html:
        print("Parsing jobs...")
        jobs = parse_jobs(html)

        if jobs:
            save_to_csv(jobs, OUTPUT_FILE)
        else:
            print("No jobs were parsed from the page.")
    else:
        print("Failed to retrieve HTML content.")

if __name__ == "__main__":
    main()
