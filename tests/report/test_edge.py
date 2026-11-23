import shutil
import subprocess
import unittest
from pathlib import Path


@unittest.skipUnless(shutil.which("node"), "Node.js is not installed")
class EdgeTest(unittest.TestCase):
    def test_the_sign_in_edge_function(self):
        script = Path(__file__).with_name("edge") / "edge.test.mjs"
        result = subprocess.run(["node", str(script)], capture_output=True, text=True, timeout=120)
        self.assertEqual(result.returncode, 0, result.stderr[-2000:])
        self.assertIn("all checks passed", result.stdout)


if __name__ == "__main__":
    unittest.main()
