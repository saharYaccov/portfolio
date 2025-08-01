
# NVIDIA Job Listings Web Scraper

This script scrapes job listings from NVIDIA's career site, translates job titles to Hebrew, filters for relevant experience, and stores the results in a CSV file without duplications. It also logs timing and status to the console using colored output.

## Main Features

- Automatically installs and launches ChromeDriver in headless mode.
- Searches for multiple job keywords (e.g., "intern", "data", "python").
- Parses job listings and filters useful job details.
- Translates job titles into Hebrew using GoogleTranslator.
- Stores jobs in a CSV file, avoiding duplicates.
- Highlights new entries and elapsed time per job search.
- Automatically opens the final CSV file after execution.

## Key Functions

- `scrape_nvidia_jobs_selenium(url)`: Uses Selenium to fetch job listings HTML and extracts job info.
- `save_jobs_to_csv_no_duplicates(...)`: Appends new job listings to CSV only if they're not already stored.
- `filter_li_by_experience(...)`: (Currently unused) Filters job descriptions by relevant experience keywords.
- `get_data_dicts(...)`: Maps search keywords to terminal colors for better visual feedback.

## Dependencies

- selenium
- beautifulsoup4
- webdriver-manager
- colorama
- pandas
- deep-translator
- requests

## Usage

1. Configure the `main_job_title` list to search for relevant positions.
2. The script handles timing, translation, and CSV output automatically.
3. Optional: Set `DEL_FILE = True` to delete the previous CSV before starting.

## Notes

- Requires Google Chrome to be installed.
- Assumes internet access and no CAPTCHA on the job site.
- Optimized for the structure of NVIDIA's Workday job board.

## Author

Sahar

## Example

```python
location_code = '970bf8c909a701c749f87bdcd4008607'
main_job_title = [
    'student', 'intern', 'data', 'ai', 'deep', 'machine', 'junior', 'python', 'analyst', 'machine', 'algorithm'
]

# Run the script
t1 = datetime.datetime.now()
print('🚀 Starting NVIDIA job scraping...')
for i in range(len(main_job_title)):
    item = main_job_title[i]
    student_question = f'https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite?q={main_job_title[i]}&locations={location_code}'
    print('-' * N)
    color = key_color_map.get(item, Fore.WHITE)
    print(color + f'🔎 Searching for "{item}" jobs in Nvidia...')
    jobs = scrape_nvidia_jobs_selenium(student_question)
    save_jobs_to_csv_no_duplicates(jobs, title_job=item)
    t_now = datetime.datetime.now()
    print(f'⏱️ Elapsed time for {item} job: {t_now - t1}')
    if i > 0:
        print(f'⏳ Elapsed diff time: {t_now - t_prev}')
    t_prev = t_now
print('✅ Program finished.')
t2 = datetime.datetime.now()
print(f'🕒 Total elapsed time: {t2 - t1}')

# Open the CSV file
import subprocess
import platform
system_name = platform.system()
subprocess.call(('open', file_name))
