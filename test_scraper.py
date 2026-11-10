import unittest
from scraper import parse_jobs

class TestScraper(unittest.TestCase):
    def setUp(self):
        with open("fixture.html", "r", encoding="utf-8") as f:
            self.html = f.read()

    def test_parse_jobs_extracts_all_fields(self):
        # The fixture has 3 jobs. We check the first one for completeness.
        jobs = parse_jobs(self.html)
        self.assertEqual(len(jobs), 3)

        first_job = jobs[0]
        self.assertEqual(first_job["Title"], "Python Developer")
        self.assertEqual(first_job["Company"], "Tech Corp")
        self.assertEqual(first_job["Location"], "Remote")
        self.assertEqual(first_job["URL"], "https://example.com/apply/1")

    def test_parse_jobs_handles_missing_location(self):
        # The 3rd job in fixture.html has no location.
        jobs = parse_jobs(self.html)
        third_job = jobs[2]
        self.assertEqual(third_job["Location"], "N/A")

if __name__ == "__main__":
    unittest.main()
