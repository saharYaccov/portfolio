import asyncio
import csv
import os
import tempfile
import unittest
from datetime import datetime, timedelta
from unittest import mock

# Modules under test
from filters.job_filter import is_relevant
from filters.extract_job_id import is_job_already_sent
from scraper.linkedin_jobs import fetch_jobs
from bot.telegram_bot import TelegramNotifier
from bot.message_cleaner import TelegramCleaner


class TestJobFilter(unittest.TestCase):
    def test_is_relevant_excludes_senior_like_titles(self):
        job = {"title": "Senior Data Scientist"}
        self.assertFalse(is_relevant(job))

    def test_is_relevant_matches_keywords_case_insensitive(self):
        job = {"title": "Junior MACHINE Learning Engineer"}
        self.assertTrue(is_relevant(job))

    def test_is_relevant_non_matching_title(self):
        job = {"title": "Frontend Developer"}
        self.assertFalse(is_relevant(job))


class TestExtractJobId(unittest.TestCase):
    def test_detects_duplicate_by_id(self):
        sent = [
            "https://www.linkedin.com/jobs/view/some-role-1234567890",
            "https://www.linkedin.com/jobs/view/another-999",
        ]
        new = "https://www.linkedin.com/jobs/view/interesting-role-1234567890"
        self.assertTrue(is_job_already_sent(sent, new))

    def test_handles_invalid_and_non_string_inputs(self):
        sent = [None, 42, "https://www.linkedin.com/jobs/view/title-111"]
        new = "https://www.linkedin.com/jobs/view/title-222"
        self.assertFalse(is_job_already_sent(sent, new))

    def test_new_link_without_id_considered_new(self):
        sent = ["https://www.linkedin.com/jobs/view/title-111"]
        new = "https://www.linkedin.com/jobs/view/title"
        self.assertFalse(is_job_already_sent(sent, new))


class TestScraperLinkedIn(unittest.TestCase):
    @mock.patch("scraper.linkedin_jobs.requests.get")
    def test_fetch_jobs_parses_cards_and_limits(self, mock_get):
        html = """
        <html><body>
          <div class="base-card">
            <h3>Data Analyst</h3>
            <h4>Acme Inc</h4>
            <a href="https://www.linkedin.com/jobs/view/role-111">Link</a>
          </div>
          <div class="base-card">
            <h3>ML Engineer</h3>
            <h4>Beta LLC</h4>
            <a href="https://www.linkedin.com/jobs/view/role-222">Link</a>
          </div>
          <div class="base-card">
            <h3>Ignored Beyond Limit</h3>
            <h4>Zeta</h4>
            <a href="https://www.linkedin.com/jobs/view/role-333">Link</a>
          </div>
        </body></html>
        """
        mock_get.return_value = mock.Mock(text=html)

        jobs = fetch_jobs(keywords="data", location="Israel", limit=2)
        self.assertEqual(len(jobs), 2)
        self.assertEqual(jobs[0]["title"], "Data Analyst")
        self.assertEqual(jobs[0]["company"], "Acme Inc")
        self.assertEqual(jobs[0]["link"], "https://www.linkedin.com/jobs/view/role-111")

    @mock.patch("scraper.linkedin_jobs.requests.get")
    def test_fetch_jobs_skips_broken_cards(self, mock_get):
        html = """
        <html><body>
          <div class=\"base-card\">
            <!-- Missing elements should be skipped gracefully -->
            <h3>Title Only</h3>
          </div>
          <div class=\"base-card\">
            <h3>Data Scientist</h3>
            <h4>Gamma</h4>
            <a href=\"https://www.linkedin.com/jobs/view/role-444\">Link</a>
          </div>
        </body></html>
        """
        mock_get.return_value = mock.Mock(text=html)

        jobs = fetch_jobs(limit=10)
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]["title"], "Data Scientist")
        self.assertEqual(jobs[0]["company"], "Gamma")


class TestTelegramNotifier(unittest.TestCase):
    def setUp(self):
        # Create a temporary CSV log file
        self.temp_dir = tempfile.TemporaryDirectory()
        self.log_path = os.path.join(self.temp_dir.name, "sent_jobs.csv")

        # Instantiate notifier with mocked Bot and pyshorteners
        self.token = "TEST_TOKEN"
        self.chat_id = "TEST_CHAT"

    def tearDown(self):
        self.temp_dir.cleanup()

    @mock.patch("bot.telegram_bot.pyshorteners.Shortener")
    @mock.patch("bot.telegram_bot.Bot")
    def test_send_job_appends_to_csv_and_sends_message(self, MockBot, MockShort):
        mock_bot = MockBot.return_value
        # Fake send_message return with message_id
        mock_bot.send_message = mock.AsyncMock(return_value=mock.Mock(message_id=123))

        # Shortener returns a tinyurl.short that returns the same link for determinism
        shortener_instance = MockShort.return_value
        shortener_instance.tinyurl.short.return_value = "https://t.ly/abc"

        notifier = TelegramNotifier(self.token, self.chat_id, log_file=self.log_path)

        job = {
            "title": "Data Analyst",
            "company": "Acme",
            "link": "https://www.linkedin.com/jobs/view/role-111"
        }
        message = "I’m interested in this position."

        asyncio.run(notifier.send_job(job, message))

        # Verify Telegram message sent
        mock_bot.send_message.assert_awaited()

        # Verify CSV written
        with open(self.log_path, "r", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["message_id"], "123")
            self.assertEqual(rows[0]["job_title"], "Data Analyst")
            self.assertEqual(rows[0]["link"], job["link"])

    @mock.patch("bot.telegram_bot.pyshorteners.Shortener")
    @mock.patch("bot.telegram_bot.Bot")
    def test_notifier_initializes_log_file_and_links_cache(self, MockBot, MockShort):
        # When file does not exist, it should be created with header and links set empty
        notifier = TelegramNotifier(self.token, self.chat_id, log_file=self.log_path)
        self.assertTrue(os.path.exists(self.log_path))
        self.assertEqual(notifier.links, set())

        # Append a row and re-initialize to see links cache populated
        with open(self.log_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["1", "Some Job", "01/01/2025 12:00:00", "https://example.com/job-1"])

        notifier2 = TelegramNotifier(self.token, self.chat_id, log_file=self.log_path)
        self.assertIn("https://example.com/job-1", notifier2.links)


class TestTelegramCleaner(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.log_path = os.path.join(self.temp_dir.name, "sent_jobs.csv")

        # Seed CSV with today and old entries
        fieldnames = ["message_id", "job_title", "date", "link"]
        today = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y %H:%M:%S")
        with open(self.log_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({"message_id": "10", "job_title": "Today Job", "date": today, "link": "L1"})
            writer.writerow({"message_id": "20", "job_title": "Old Job", "date": yesterday, "link": "L2"})

    def tearDown(self):
        self.temp_dir.cleanup()

    @mock.patch("bot.message_cleaner.Bot")
    def test_delete_old_messages_keeps_today_and_deletes_older(self, MockBot):
        mock_bot = MockBot.return_value
        cleaner = TelegramCleaner(token="T", chat_id="C", log_file=self.log_path)

        cleaner.delete_old_messages()

        # Should delete one old message
        mock_bot.delete_message.assert_called_once_with(chat_id="C", message_id=20)

        # CSV should now contain only today's row
        with open(self.log_path, "r", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["message_id"], "10")


if __name__ == "__main__":
    unittest.main()
