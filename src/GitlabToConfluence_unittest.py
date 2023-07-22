import os
import unittest
from unittest.mock import patch
from atlassian_python_api_code import process_line, convert_gitlab_to_confluence

class TestAtlassianPythonApiCode(unittest.TestCase):

    def test_process_line(self):
        input_line = "This is *bold* text."
        expected_output = "<p>This is <em>bold</em> text.</p>"
        self.assertEqual(process_line(input_line), expected_output)

    def test_convert_gitlab_to_confluence(self):
        input_file = "input_file.md"
        output_file = "output_file.txt"

        # Create a mock GitLab file content
        gitlab_text = "This is a GitLab markdown content."
        with open(input_file, 'w') as file:
            file.write(gitlab_text)

        # Mock the 'process_line' function
        with patch('atlassian_python_api_code.process_line') as mock_process_line:
            mock_process_line.return_value = "Processed line"
            convert_gitlab_to_confluence(input_file, output_file)

        # Check that the output file contains the processed line
        with open(output_file, 'r') as file:
            output_content = file.read()
            self.assertIn("Processed line", output_content)

        # Clean up the temporary files
        os.remove(input_file)
        os.remove(output_file)

if __name__ == '__main__':
    unittest.main()

