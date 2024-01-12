import os
import json
import tkinter as tk
from tkinter import simpledialog, messagebox
from azure.storage.blob import BlobServiceClient

import authInfo

class FileUploader:
    def __init__(self):
        # check data count
        self.count_path = "data_count.json"
        # if json file not exist, create it
        if not os.path.exists(self.count_path):
            with open(self.count_path, "w") as file:
                json.dump({"user_id": 0, "image_count": 1, "video_count": 1}, file)
        # read from the json data
        self.read_user_info()

        # Azure blob storage connection
        self.azure_connection_string = authInfo.azure_connection_string
        self.azure_container_name = authInfo.azure_container_name

        # initialize user id
        self.change_user_id()

        # Run the Tkinter main loop
        self.root.mainloop()
    
    def read_user_info(self):
        # Read information from json file
        with open(self.count_path, "r") as file:
            data = json.load(file)

        # Extract values and store in local
        self.user_id = data["user_id"]
        self.image_count = data["image_count"]
        self.video_count = data["video_count"]

    def update_user_info(self, new_user_id, new_image_count, new_video_count):
        with open(self.count_path, "w") as file:
            json.dump({"user_id": new_user_id, "image_count": new_image_count, "video_count": new_video_count}, file)

    def get_user_id(self):
        # Prompt for user id
        try:
            user_id = simpledialog.askstring("Enter ID", "Enter Your ID:")
            while not user_id.isdigit() or int(user_id) == 0:
                user_id = simpledialog.askstring("Enter ID", "Enter Your ID:")
            return int(user_id)
        except:
            exit()

    def change_user_id(self):
        try:
            self.root.destroy()
        except:
            pass

        # initialize local static values
        self.user_id = self.get_user_id()

        # Azure blob storage connection
        self.azure_connection_string = authInfo.azure_connection_string
        self.azure_container_name = authInfo.azure_container_name

        # Create Tkinter window
        self.root = tk.Tk()
        self.root.title("File Uploader")

        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the position for the window to be centered
        x_position = int((screen_width - self.root.winfo_reqwidth()) / 2)
        y_position = int((screen_height - self.root.winfo_reqheight()) / 2)

        # Set the window's position
        self.root.geometry(f"250x100+{x_position}+{y_position}")

        # Create Tkinter GUI
        self.id_label = tk.Label(self.root, text = f"Your ID: {self.user_id}")
        self.change_id_button = tk.Button(self.root, text = "Change ID", command=self.change_user_id)
        self.upload_button = tk.Button(self.root, text = "Upload Files", command=self.upload_files)

        # Pack GUI elements
        self.id_label.pack(pady=10)
        self.change_id_button.pack(side=tk.LEFT, padx=20)
        self.upload_button.pack(side=tk.RIGHT, padx=20)

    def upload_files(self):
        # Upload all the data into the "new" folder first
        azure_folder_name = 'new'

        # Get all files in the current directory
        files = [f for f in os.listdir() if os.path.isfile(f)]

        # Create blob service client
        blob_service_client = BlobServiceClient.from_connection_string(self.azure_connection_string)
        # Get a reference to the container
        container_client = blob_service_client.get_container_client(self.azure_container_name)

        # Manipulate files
        for file in files:
            # Determine the type of the file
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                file_type = "img"
                file_count = self.image_count
                self.image_count += 1
            elif file.lower().endswith((".mp4", ".mov")):
                file_type = "vid"
                file_count = self.video_count
                self.video_count += 1
            else:
                continue

            # Rename the file in format
            new_file_name = f"{azure_folder_name}/{self.user_id}-{file_type}-{file_count}"

            # Upload file to Azure blob storage
            blob_client = container_client.get_blob_client(new_file_name)
            for attempt in range(3):
                try:
                    with open(file, "rb") as data:
                        blob_client.upload_blob(data, max_concurrency=1, timeout=60)
                    print(f"File '{file}' has been uploaded as '{new_file_name}'")
                    self.update_user_info(self.user_id, self.image_count, self.video_count)
                    break
                except Exception as e:
                    print("Error: ", e)
                    if attempt < 2:
                        print(f"Retrying... Attempt {attempt + 1}")
                        continue
                    else:
                        print("Max retries reached. Upload failed.")
                        break
        
        print("Upload data Complete")

        # Show a completion message box
        messagebox.showinfo("Upload Complete", "The upload is complete.")


if __name__ == "__main__":
    FileUploader()