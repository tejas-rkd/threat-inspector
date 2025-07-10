import unittest
from src.services.cve_service import CVEService

class TestCVEService(unittest.TestCase):

    def setUp(self):
        self.cve_service = CVEService()

    def test_fetch_cve_info_valid(self):
        cve_id = "CVE-2021-44228"
        response = self.cve_service.fetch_cve_info(cve_id)
        self.assertIn("cve", response)
        self.assertEqual(response["cve"]["id"], cve_id)

    def test_fetch_cve_info_not_found(self):
        cve_id = "CVE-0000-0000"
        with self.assertRaises(SystemExit):
            self.cve_service.fetch_cve_info(cve_id)

    def test_fetch_cve_info_connection_error(self):
        # Simulate a connection error by providing an invalid CVE ID
        cve_id = "INVALID-CVE-ID"
        with self.assertRaises(SystemExit):
            self.cve_service.fetch_cve_info(cve_id)

if __name__ == "__main__":
    unittest.main()