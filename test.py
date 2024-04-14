import unittest
import tkinter as tk
from main import SteganographyApp


class TestSteganographyApp(unittest.TestCase):
    """Test case for SteganographyApp class."""

    def setUp(self):
        """Set up the test environment."""
        self.app = SteganographyApp(tk.Tk())

    def test_encrypt_text(self):
        """Test encryption and decryption of text."""
        text = "Sample text to encrypt and decrypt."
        encrypted_text = self.app.encrypt_text(text)
        decrypted_text = self.app.decrypt_text(encrypted_text)
        self.assertEqual(text, decrypted_text)


if __name__ == "__main__":
    unittest.main()