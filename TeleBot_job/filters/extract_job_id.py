import re
from typing import Iterable

def is_job_already_sent(sent_links: Iterable[str], new_link: str) -> bool:
    """
    משווה Job ID מתוך לינק חדש מול Job IDs של לינקים קיימים
    """
    match = re.search(r'/jobs/view/.*-(\d+)', new_link)
    if not match:
        return False  # אם אין ID בלינק – נחשב כחדש

    new_job_id = match.group(1)

    for link in sent_links:
        if not isinstance(link, str):
            continue

        old_match = re.search(r'/jobs/view/.*-(\d+)', link)
        if old_match and old_match.group(1) == new_job_id:
            return True

    return False
