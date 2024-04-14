import unittest
from PIL import Image
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

    def test_hide_and_read_text(self):
        """Test hiding and reading text from an image."""
        # Test with image containing text
        with open('img_with_text.png', 'rb') as file:
            self.app.image = Image.open(file)
        text_to_hide = "Secret message hidden in the image."
        self.app.text_to_hide = text_to_hide
        self.app.hide_text()
        self.app.read_text()
        self.assertEqual(text_to_hide, self.app.read_text_entry.get("1.0", "end-1c"))

        # Test with image without text
        with open('img_without_text.png', 'rb') as file:
            self.app.image = Image.open(file)
        self.app.read_text()
        self.assertEqual("", self.app.read_text_entry.get("1.0", "end-1c"))


if __name__ == "__main__":
    unittest.main()
