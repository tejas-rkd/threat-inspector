import json
import sys
import urllib.request
import urllib.error
from utils.constants import OSV_API_URL

class CVEService:
    def __init__(self, api_url=OSV_API_URL):
        self.api_url = api_url

    def fetch_cve_info(self, cve_id):
        print(f"Fetching information for {cve_id}...")
        url = self.api_url.format(cve_id)
        try:
            with urllib.request.urlopen(url) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"Error: CVE {cve_id} not found")
            else:
                print(f"Error: HTTP {e.code} - {e.reason}")
            sys.exit(1)
        except urllib.error.URLError as e:
            print(f"Error: Could not connect to the API - {e.reason}")
            sys.exit(1)
        except json.JSONDecodeError:
            print("Error: Invalid response received from the API")
            sys.exit(1)