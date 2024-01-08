import os
import tkinter as tk
from tkinter import simpledialog
from azure.storage.blob import BlobServiceClient

import authInfo

class FileUploader:
    def __init__(self):
        # initialize local static values
        self.user_id = self.get_user_id()
        print(self.user_id)
        print(type(self.user_id))
        # self.image_count = self.get_image_count()
        # self.video_count = self.get_video_count()

        # # Azure blob storage connection
        # self.azure_connection_string = authInfo.azure_connection_string
        # self.azure_container_name = authInfo.azure_container_name

        # Create Tkinter window
        self.root = tk.Tk()
        self.root.title("File Uploader")

        # Create Tkinter GUI
        self.label = tk.Label(self.root, text = f"Enter Your ID: {self.user_id}")
        # self.upload_button = tk.Button(self.root, text = "Upload Files", command=self.upload_files)

        # Pack GUI elements
        self.label.pack(pady=10)
        # self.upload_button.pack(pady=10)

        # Run the Tkinter main loop
        self.root.mainloop()

    def get_user_id(self):
        # Prompt for user id
        try:
            user_id = simpledialog.askstring("Input", "Enter Your ID:")
            while not user_id.isdigit():
                user_id = simpledialog.askstring("Input", "Enter Your ID:")
            return int(user_id)
        except:
            exit()

if __name__ == "__main__":
    FileUploader()