import os
import subprocess
import threading
import urllib.request
from tkinter import filedialog, Tk, Button, Label, StringVar, Toplevel, messagebox, Listbox, Scrollbar
from tkinter.ttk import Progressbar
from pathlib import Path
import logging
import queue

# URL for OpenSSL installer (silent installation)
OPENSSL_INSTALLER_URL = "https://slproweb.com/download/Win64OpenSSL-3_3_2.exe"
APPDATA_PATH = os.getenv('APPDATA')
APP_LOG_DIR = os.path.join(APPDATA_PATH, "P7MConverterLogs")
OPENSSL_PATH = r"C:\Program Files\OpenSSL-Win64\bin\openssl.exe"
OPENSSL_INSTALLER_PATH = os.path.join(APPDATA_PATH, "Win64OpenSSL-3_3_2.exe")

# Ensure log directory exists
os.makedirs(APP_LOG_DIR, exist_ok=True)

# Configure logging
log_file = os.path.join(APP_LOG_DIR, 'app.log')
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')
logging.info("Application started.")


class OpenSSLInstaller:
    def __init__(self, update_queue):
        print("OpenSSLInstaller initialized.")  # Debugging line
        self.installation_window = None
        self.update_queue = update_queue

    def start_installation(self):
        """Starts the installation of OpenSSL in a new window."""
        print("Starting OpenSSL installation...")  # Debugging line
        self.installation_window = Toplevel()
        self.installation_window.title("Installing OpenSSL")
        self.installation_window.geometry("300x150")

        self.status_label = Label(self.installation_window, text="Installing OpenSSL... Please wait.")
        self.status_label.pack(pady=10)

        self.progress = Progressbar(self.installation_window, orient="horizontal", length=250, mode="indeterminate")
        self.progress.pack(pady=10)
        self.progress.start()

        threading.Thread(target=self.install_openssl).start()

    def install_openssl(self):
        """Downloads and installs OpenSSL silently if not present."""
        try:
            # Download OpenSSL installer if it's not already downloaded
            if not os.path.exists(OPENSSL_INSTALLER_PATH):
                logging.info("Downloading OpenSSL installer...")
                urllib.request.urlretrieve(OPENSSL_INSTALLER_URL, OPENSSL_INSTALLER_PATH)
                logging.info(f"Downloaded OpenSSL installer to {OPENSSL_INSTALLER_PATH}")

            # Install OpenSSL silently
            logging.info("Running OpenSSL installer...")
            install_command = f'"{OPENSSL_INSTALLER_PATH}" /verysilent /norestart'
            result = subprocess.run(install_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if result.returncode != 0:
                logging.error(f"OpenSSL installation failed: {result.stderr.decode()}")
                self.update_queue.put("OpenSSL installation failed.")
            else:
                logging.info("OpenSSL installed successfully.")
                self.update_queue.put("OpenSSL installation complete.")
        except Exception as e:
            logging.error(f"Error during OpenSSL installation: {str(e)}")
            self.update_queue.put(f"Error installing OpenSSL: {str(e)}")
        finally:
            self.progress.stop()
            self.installation_window.destroy()
            self.update_queue.put("Launch Main App")


class P7MConverterApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("P7M to PDF Converter")
        self.folder_path = ""
        self.files_to_convert = []
        self.update_queue = queue.Queue()

        # Label for file count
        self.file_count_label = Label(self.root, text="No folder selected")
        self.file_count_label.pack(pady=10)

        # Listbox to display file names
        self.file_listbox = Listbox(self.root, height=10, width=50)
        self.file_listbox.pack(pady=10)

        # Scrollbar for file listbox
        self.scrollbar = Scrollbar(self.root, orient="vertical", command=self.file_listbox.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.file_listbox.config(yscrollcommand=self.scrollbar.set)

        # Progress bar
        self.progress = Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

        # Status label for updates
        self.status_label = StringVar()
        self.status_label.set("Waiting for folder selection...")
        self.status = Label(self.root, textvariable=self.status_label)
        self.status.pack(pady=10)

        # Select folder button
        self.select_button = Button(self.root, text="Select Folder", command=self.select_folder)
        self.select_button.pack(pady=10)

        # Convert button
        self.convert_button = Button(self.root, text="Convert", command=self.start_conversion)
        self.convert_button.pack(pady=10)
        self.convert_button.config(state="disabled")  # Disabled until a folder is selected

        # Quit button
        quit_button = Button(self.root, text="Quit", command=self.root.quit)
        quit_button.pack(pady=10)

        # Listbox for converted files
        self.converted_files_listbox = Listbox(self.root, height=10, width=50)
        self.converted_files_listbox.pack(pady=10)
        self.converted_files_scrollbar = Scrollbar(self.root, orient="vertical",
                                                   command=self.converted_files_listbox.yview)
        self.converted_files_scrollbar.pack(side="right", fill="y")
        self.converted_files_listbox.config(yscrollcommand=self.converted_files_scrollbar.set)

    def run(self):
        self.check_openssl()
        self.root.after(100, self.process_queue)  # Start processing the update queue
        self.root.mainloop()

    def check_openssl(self):
        """Checks if OpenSSL is present; if not, starts the installation."""
        if not os.path.exists(OPENSSL_PATH):
            installer = OpenSSLInstaller(self.update_queue)
            installer.start_installation()
        else:
            logging.info("OpenSSL is already installed.")

    def select_folder(self):
        """Allows the user to select a folder and displays the number of .p7m files in it."""
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.file_listbox.delete(0, 'end')
            self.converted_files_listbox.delete(0, 'end')

            self.files_to_convert = [f for f in os.listdir(self.folder_path) if f.lower().endswith('.p7m')]
            file_count = len(self.files_to_convert)

            if file_count > 0:
                for idx, file in enumerate(self.files_to_convert):
                    self.file_listbox.insert('end', f"{idx + 1}. {file}")

                self.file_count_label.config(text=f"Found {file_count} .p7m files in the selected folder.")
                self.convert_button.config(state="normal")
                self.status_label.set("")
                logging.info(f"Selected folder contains {file_count} .p7m files.")
            else:
                self.file_count_label.config(text="No .p7m files found in the selected folder.")
                self.convert_button.config(state="disabled")
                logging.info("No .p7m files found in the selected folder.")

    def start_conversion(self):
        """Starts the conversion process in a separate thread."""
        if not self.files_to_convert:
            return

        self.convert_button.config(state="disabled")
        self.status_label.set("Converting files...")
        logging.info("Starting file conversion...")
        threading.Thread(target=self.convert_p7m_to_pdf).start()

    def convert_p7m_to_pdf(self):
        """Converts all .p7m files to PDF and updates progress."""
        total_files = len(self.files_to_convert)
        self.progress['maximum'] = total_files

        for idx, filename in enumerate(self.files_to_convert):
            p7m_file_path = os.path.join(self.folder_path, filename)
            output_file = os.path.join(self.folder_path, filename.replace('.p7m', '.pdf'))
            self.extract_p7m_content(p7m_file_path, output_file)

            self.progress['value'] = idx + 1
            self.root.update_idletasks()

            self.converted_files_listbox.insert('end', f"{idx + 1}. {filename.replace('.p7m', '.pdf')}")
            files_left = total_files - (idx + 1)
            self.status_label.set(f"Converted {idx + 1}/{total_files} files. {files_left} files remaining.")
            logging.info(f"Converted {filename} to PDF.")

        self.status_label.set(f"Conversion completed! {total_files} files converted.")
        self.convert_button.config(state="normal")
        logging.info("File conversion completed.")

    def extract_p7m_content(self, p7m_file_path, output_file):
        """Extracts content from a .p7m file using OpenSSL."""
        command = f'"{OPENSSL_PATH}" smime -verify -noverify -binary -inform DER -in "{p7m_file_path}" -out "{output_file}" -outform PEM'
        try:
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                logging.error(f"Error converting {p7m_file_path}: {result.stderr.decode()}")
                messagebox.showerror("Error", f"Error converting {p7m_file_path}: {result.stderr.decode()}")
        except Exception as e:
            logging.error(f"Exception while converting {p7m_file_path}: {str(e)}")
            messagebox.showerror("Error", f"Exception while converting {p7m_file_path}: {str(e)}")

    def process_queue(self):
        """Processes messages from the update queue."""
        try:
            while True:
                message = self.update_queue.get_nowait()
                if message == "Launch Main App":
                    self.show_main_app()
                else:
                    self.status_label.set(message)
                    logging.info(message)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.process_queue)  # Check again after 100ms

    def show_main_app(self):
        """Show the main application interface."""
        self.status_label.set("OpenSSL installed. Select Folder to start converting files.")
        self.convert_button.config(state="normal")


if __name__ == "__main__":
    app = P7MConverterApp()
    app.run()
