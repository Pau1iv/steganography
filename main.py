import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from cryptography.fernet import Fernet,InvalidToken
import os

class SteganographyApp:
    """Class representing an application for hiding text in images."""

    def __init__(self, master):
        """Initialize the application.

        Args:
            master: The main user interface element.
        """
        self.master = master
        self.master.title("Steganography App")

        self.text_entry = tk.Text(master, height=4, width=50)
        self.text_entry.pack()

        self.confirm_text_button = tk.Button(master, text="Confirm Text", command=self.confirm_text)
        self.confirm_text_button.pack()

        self.select_image_button = tk.Button(master, text="Select Image", command=self.select_image)
        self.select_image_button.pack()

        self.read_text_entry = tk.Text(master, height=4, width=50)
        self.read_text_entry.pack()

        self.image_label = tk.Label(master)
        self.image_label.pack()

        self.hide_text_button = tk.Button(master, text="Hide Text", command=self.hide_text)
        self.hide_text_button.pack()

        self.read_text_button = tk.Button(master, text="Read Text", command=self.read_text)
        self.read_text_button.pack()

        self.image = None
        self.text_to_hide = ""
        self.encryption_key = self.load_encryption_key()

    def confirm_text(self):
        """Confirm the entered text."""
        self.text_to_hide = self.text_entry.get("1.0", "end-1c")

    def select_image(self):
        """Select an image for processing."""
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            self.image.thumbnail((300, 300))
            self.photo = ImageTk.PhotoImage(self.image)
            self.image_label.config(image=self.photo)

    def hide_text(self):
        """Hide the entered text in the image and save it to a file."""
        if self.image and self.text_to_hide:
            encrypted_text = self.encrypt_text(self.text_to_hide)
            text_length = len(encrypted_text)
            binary_text_length = bin(text_length)[2:].zfill(32)

            binary_text = ''.join(format(byte, '08b') for byte in encrypted_text)

            # Add text length to the beginning of the image
            image_with_text_length = binary_text_length + binary_text
            image_with_text_length += "0" * ((-len(image_with_text_length)) % 8)  # Pad with zeros

            image_pixels = list(self.image.getdata())
            pixel_index = 0

            for bit in image_with_text_length:
                pixel = list(image_pixels[pixel_index])
                pixel[-1] = (pixel[-1] & 254) | int(bit)
                image_pixels[pixel_index] = tuple(pixel)
                pixel_index += 1

            self.image.putdata(image_pixels)

            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                self.image.save(file_path)

    def read_text(self):
        """Read the hidden text from the image."""
        if self.image:
            image_pixels = list(self.image.getdata())
            binary_text_length = ''

            for i in range(32):
                binary_text_length += str(image_pixels[i][-1] & 1)

            text_length = int(binary_text_length, 2)

            if text_length == 0:
                self.read_text_entry.delete("1.0", "end")
                self.read_text_entry.insert("1.0", "No hidden text found in the image.")
                return

            binary_text = ''
            pixel_index = 32

            for _ in range(text_length * 8):
                if pixel_index < len(image_pixels):
                    binary_text += str(image_pixels[pixel_index][-1] & 1)
                    pixel_index += 1
                else:
                    break

            encrypted_text = bytes(int(binary_text[i:i + 8], 2) for i in range(0, len(binary_text), 8))
            decrypted_text = self.decrypt_text(encrypted_text)

            self.read_text_entry.delete("1.0", "end")
            self.read_text_entry.insert("1.0", decrypted_text)

    def encrypt_text(self, text):
        """Encrypt the text."""
        if not self.encryption_key:
            self.encryption_key = self.generate_encryption_key()
            self.save_encryption_key(self.encryption_key)

        cipher_suite = Fernet(self.encryption_key)
        encrypted_text = cipher_suite.encrypt(text.encode())

        return encrypted_text

    def decrypt_text(self, encrypted_text):
        """Decrypt the text."""
        if not self.encryption_key:
            return "No encryption key found. Cannot decrypt text."

        try:
            cipher_suite = Fernet(self.encryption_key)
            decrypted_text = cipher_suite.decrypt(encrypted_text).decode()
            return decrypted_text
        except InvalidToken:
            return "Invalid or expired token. Cannot decrypt text."
        except Exception as e:
            return f"An error occurred during decryption: {e}"

    def generate_encryption_key(self):
        """Generate a new encryption key."""
        return Fernet.generate_key()

    def save_encryption_key(self, key):
        """Save the encryption key to a file."""
        with open("encryption_key.txt", "wb") as key_file:
            key_file.write(key)

    def load_encryption_key(self):
        """Load the encryption key from a file."""
        key_file_path = "encryption_key.txt"
        if os.path.exists(key_file_path):
            with open(key_file_path, "rb") as key_file:
                return key_file.read()
        else:
            return None

def main():
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
