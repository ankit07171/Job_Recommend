from apify_client import ApifyClient
import os
from dotenv import load_dotenv

load_dotenv()
apify_client = ApifyClient(os.getenv("APIFY_API_KEY"))

def fetch_linkedin_jobs(search_query, location="india", rows=60):
    run_input = {
        "title": search_query,
        "location": location,
        "rows": rows,
        "proxy": {"useApifyProxy": True, "apifyProxyGroups": ["RESIDENTIAL"]},
    }
    run = apify_client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)
    return list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
 