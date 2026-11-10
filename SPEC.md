# Specification: Job Listings Scraper

## Problem Statement
The user needs a way to automatically collect job listings from the "Fake Python Jobs" demo site. Manually copying job titles, companies, locations, and application links is tedious and error-prone.

## Solution
A Python-based command-line utility that scrapes the target website and exports the extracted job data into a structured CSV file.

## User Stories
1. As a job seeker, I want to run a single command to collect all current job listings, so that I don't have to browse the site manually.
2. As a data analyst, I want the job data to be saved in a CSV format, so that I can easily open it in Excel or Google Sheets.
3. As a user, I want the scraper to capture the **Job Title**, so I know what the role is.
4. As a user, I want the scraper to capture the **Company Name**, so I know who is hiring.
5. As a user, I want the scraper to capture the **Location**, so I know if the job is remote or in a city I can move to.
6. As a user, I want the scraper to capture the **Application URL**, so I can apply directly from the CSV.
7. As a developer, I want the script to handle missing data fields (e.g., a missing location) without crashing, so that the rest of the listings are still collected.
8. As a server administrator, I want the scraper to use a proper `User-Agent` header, so that the request is not immediately blocked as a bot.
9. As a server administrator, I want the scraper to implement basic rate limiting (delays), so that it does not overwhelm the demo server.
10. As a user, I want the CSV to be overwritten on each run, so that I always have the most up-to-date list without duplicate entries from previous runs.

## Implementation Decisions
- **Language**: Python 3.x.
- **Networking**: Use the `requests` library for HTTP GET requests.
- **Parsing**: Use `BeautifulSoup4` (bs4) to traverse the DOM and extract data based on CSS selectors.
- **Persistence**: Use the built-in `csv` module to write data.
- **Architecture**: 
    - A `fetch_html` function to handle network requests and error handling.
    - A `parse_jobs` function that takes HTML content and returns a list of job dictionaries.
    - A `save_to_csv` function to handle the file output.
- **Resilience**: Use `.find()` and `.get_text()` with fallback values (e.g., "N/A") to prevent `AttributeError` when tags are missing.

## Testing Decisions
- **Behavioral Testing**: A "good" test verifies that given a specific piece of HTML, the scraper produces the expected list of job dictionaries.
- **Testing Seam**: The `parse_jobs` function will be the primary test target.
- **Method**: Use a local HTML fixture file to simulate the website response, ensuring tests are deterministic and do not depend on network stability or site changes.

## Out of Scope
- **Dynamic Content**: Handling JavaScript-rendered content (e.g., via Playwright/Selenium) is out of scope as the target site is static.
- **Pagination**: Scraping multiple pages of results is out of scope unless the demo site requires it.
- **Database Integration**: Saving data to SQL/NoSQL databases; CSV is the only required output.
- **Authentication**: Logging into the site to access private listings.

## Further Notes
- The script will be a specialized scraper for the "Fake Python Jobs" site to maintain the smallest possible codebase (Ponytail mode).
- Implementation will follow the "smallest complete change" philosophy: a single script file.
