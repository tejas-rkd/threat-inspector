import argparse
import sys
import os

class ArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Fetch and display vulnerability information for a CVE ID in context of your code"
        )
        self.parser.add_argument("cve_id", help="The CVE identifier (e.g., CVE-2021-44228)")
        self.parser.add_argument(
            "--path",
            default=".",
            help="Path to the code directory (default: current directory)"
        )

    def parse_arguments(self):
        args = self.parser.parse_args()
        self.validate_arguments(args)
        return args

    def validate_arguments(self, args):
        cve_id = args.cve_id.upper()
        if not cve_id.startswith("CVE-"):
            print("Warning: CVE ID should be in the format 'CVE-YYYY-NNNNN'")
            sys.exit(1)

        path = args.path
        if not os.path.exists(path) or not os.path.isdir(path):
            print(f"Error: The specified path '{path}' does not exist or is not a directory.")
            sys.exit(1)