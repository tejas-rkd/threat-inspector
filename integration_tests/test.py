import os
import sys
import subprocess
import unittest
from pathlib import Path

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class ThreatInspectorIntegrationTest(unittest.TestCase):
    """Integration tests for the threat inspector application."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = Path(__file__).parent
        self.data_dir = self.test_dir / "data"
        self.main_script = self.test_dir.parent / "src" / "main.py"
        
        # Ensure the main script exists
        self.assertTrue(self.main_script.exists(), f"Main script not found at {self.main_script}")
        
        # Get all test data files
        self.test_files = list(self.data_dir.glob("*.py"))
        self.assertTrue(len(self.test_files) > 0, "No test data files found")
    
    def extract_cve_id_from_filename(self, filename):
        """Extract CVE ID from filename like '2017_18342.py' -> 'CVE-2017-18342'."""
        stem = Path(filename).stem  # Remove .py extension
        parts = stem.split('_')
        if len(parts) >= 2:
            year = parts[0]
            number = parts[1]
            return f"CVE-{year}-{number}"
        return None
    
    def run_main_script(self, cve_id, file_path):
        """Run the main script with given CVE ID and file path."""
        cmd = [sys.executable, str(self.main_script), cve_id, "--path", str(file_path)]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,  # 60 second timeout
                cwd=str(self.test_dir.parent)  # Run from project root
            )
            return result
        except subprocess.TimeoutExpired:
            self.fail(f"Script timed out for CVE {cve_id}")
        except Exception as e:
            self.fail(f"Failed to run script for CVE {cve_id}: {str(e)}")
    
    def test_cve_2017_18342(self):
        """Test analysis of CVE-2017-18342 (YAML deserialization vulnerability)."""
        file_path = self.data_dir / "2017_18342.py"
        cve_id = "CVE-2017-18342"
        
        result = self.run_main_script(cve_id, file_path)
        
        # Check that the script ran successfully
        self.assertEqual(result.returncode, 0, 
                        f"Script failed for {cve_id}. stderr: {result.stderr}")
        
        # Check that there's some output
        self.assertTrue(len(result.stdout) > 0, 
                       f"No output generated for {cve_id}")
        
        # Check for relevant keywords in output (YAML vulnerability related)
        output_lower = result.stdout.lower()
        self.assertTrue(any(keyword in output_lower for keyword in 
                           ['yaml', 'deserialization', 'vulnerability', 'cve-2017-18342']),
                       f"Output doesn't contain expected vulnerability information for {cve_id}")
    
    def test_cve_2023_43364(self):
        """Test analysis of CVE-2023-43364."""
        file_path = self.data_dir / "2023_43364.py"
        cve_id = "CVE-2023-43364"
        
        result = self.run_main_script(cve_id, file_path)
        
        # Check that the script ran successfully
        self.assertEqual(result.returncode, 0, 
                        f"Script failed for {cve_id}. stderr: {result.stderr}")
        
        # Check that there's some output
        self.assertTrue(len(result.stdout) > 0, 
                       f"No output generated for {cve_id}")
        
        # Check for CVE ID in output
        self.assertIn("2023-43364", result.stdout,
                     f"CVE ID not found in output for {cve_id}")
    
    def test_cve_2024_45848(self):
        """Test analysis of CVE-2024-45848."""
        file_path = self.data_dir / "2024‑45848.py"  # Note: using en-dash character
        cve_id = "CVE-2024-45848"
        
        result = self.run_main_script(cve_id, file_path)
        
        # Check that the script ran successfully
        self.assertEqual(result.returncode, 0, 
                        f"Script failed for {cve_id}. stderr: {result.stderr}")
        
        # Check that there's some output
        self.assertTrue(len(result.stdout) > 0, 
                       f"No output generated for {cve_id}")
        
        # Check for CVE ID in output
        self.assertIn("2024", result.stdout,
                     f"Year not found in output for {cve_id}")
    
    def test_all_data_files_automatically(self):
        """Automatically test all files in the data directory."""
        for test_file in self.test_files:
            with self.subTest(file=test_file.name):
                cve_id = self.extract_cve_id_from_filename(test_file.name)
                
                if cve_id is None:
                    self.skipTest(f"Could not extract CVE ID from filename: {test_file.name}")
                
                result = self.run_main_script(cve_id, test_file)
                
                # Basic checks for all files
                self.assertEqual(result.returncode, 0, 
                               f"Script failed for {cve_id} with file {test_file.name}. "
                               f"stderr: {result.stderr}")
                
                self.assertTrue(len(result.stdout) > 0, 
                               f"No output generated for {cve_id} with file {test_file.name}")
                
                # Print output for debugging (optional)
                if result.stdout:
                    print(f"\n--- Output for {cve_id} ({test_file.name}) ---")
                    print(result.stdout)
                    print(f"--- End output for {cve_id} ---\n")
    
    def test_invalid_cve_id(self):
        """Test that the script handles invalid CVE IDs appropriately."""
        file_path = self.data_dir / "2017_18342.py"
        invalid_cve_id = "INVALID-CVE-ID"
        
        result = self.run_main_script(invalid_cve_id, file_path)
        
        # Script should exit with error for invalid CVE ID
        self.assertNotEqual(result.returncode, 0, 
                           "Script should fail with invalid CVE ID")
    
    def test_nonexistent_file_path(self):
        """Test that the script handles nonexistent file paths appropriately."""
        nonexistent_path = self.data_dir / "nonexistent_file.py"
        cve_id = "CVE-2017-18342"
        
        result = self.run_main_script(cve_id, nonexistent_path)
        
        # Script should exit with error for nonexistent file
        self.assertNotEqual(result.returncode, 0, 
                           "Script should fail with nonexistent file path")

if __name__ == "__main__":
    # Configure test runner
    unittest.main(verbosity=2, buffer=True)