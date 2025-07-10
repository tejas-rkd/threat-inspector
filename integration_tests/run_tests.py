#!/usr/bin/env python3
"""
Test runner for threat inspector integration tests.
Run this script to execute all integration tests.
"""

import os
import sys
import unittest
from pathlib import Path

def main():
    """Run all integration tests."""
    # Change to the integration tests directory
    test_dir = Path(__file__).parent
    os.chdir(test_dir)
    
    # Add src directory to path
    src_dir = test_dir.parent / "src"
    sys.path.insert(0, str(src_dir))
    
    # Discover and run tests
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern='test*.py')
    
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)

if __name__ == "__main__":
    main()
