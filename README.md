# P7M to PDF Converter

A Python-based desktop application that helps users convert multiple P7M (signed email) files to PDF format in batch. The application provides a simple graphical user interface and handles OpenSSL installation automatically if needed.

## Features

- 🔄 Batch conversion of P7M files to PDF
- 📂 Simple folder selection interface
- 📊 Real-time conversion progress tracking
- 📝 Detailed conversion logs
- 🔧 Automatic OpenSSL installation
- 📋 File listing with scrollable view
- 💫 User-friendly GUI with status updates

## Prerequisites

- Windows 64-bit operating system
- Python 3.x
- Internet connection (for first-time OpenSSL installation)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/saikrishnamallam/P7MConverterApp.git
cd P7MConverterApp
```

2. Install required packages using pip:
```bash
pip install -r requirements.txt
```

Alternatively, if you want to install packages in a virtual environment (recommended):
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

Note: The application will automatically download and install OpenSSL if it's not already present on your system.

## Usage

1. Run the application:
```bash
python app.py
```

2. The application will check for OpenSSL installation and install it if necessary.

3. Click the "Select Folder" button to choose a directory containing P7M files.

4. The application will display all P7M files found in the selected directory.

5. Click "Convert" to start the batch conversion process.

6. Monitor the progress through the progress bar and status updates.

7. Converted PDF files will be saved in the same directory as the source P7M files.

## Application Structure

- `P7MConverterApp`: Main application class handling the GUI and conversion workflow
- `OpenSSLInstaller`: Helper class managing OpenSSL installation
- Logging system storing operation logs in the AppData directory
- Threading implementation for non-blocking UI during conversion
- Progress tracking for batch operations

## Configuration

The application uses the following default paths:
- OpenSSL Installation: `C:\Program Files\OpenSSL-Win64\bin\openssl.exe`
- Log Directory: `%APPDATA%\P7MConverterLogs`
- OpenSSL Installer: Downloaded to `%APPDATA%\Win64OpenSSL-3_3_2.exe`

## Logging

The application maintains detailed logs of all operations in:
```
%APPDATA%\P7MConverterLogs\app.log
```

## Error Handling

- The application includes comprehensive error handling for:
  - OpenSSL installation failures
  - File conversion errors
  - Directory access issues
  - Invalid file formats

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Uses OpenSSL for P7M file processing
- Built with Python's tkinter for the GUI
- Developed for Windows 64-bit systems

## Troubleshooting

### Common Issues

1. **OpenSSL Installation Fails**
   - Ensure you have administrative privileges
   - Check your internet connection
   - Verify Windows Defender or antivirus isn't blocking the installation

2. **Conversion Errors**
   - Verify the P7M files are valid and not corrupted
   - Check if the files are properly signed
   - Ensure you have write permissions in the target directory

3. **Application Won't Start**
   - Verify Python 3.x is installed correctly
   - Check if tkinter is installed properly
   - Ensure all required permissions are granted
   - Make sure all dependencies are installed correctly using `pip install -r requirements.txt`

4. **Package Installation Issues**
   - If you get permission errors during installation, try running:
     ```bash
     pip install --user -r requirements.txt
     ```
   - If you're behind a proxy, configure pip accordingly:
     ```bash
     pip install --proxy http://user:password@proxyserver:port -r requirements.txt
     ```

### Getting Help

If you encounter any issues:
1. Check the application logs in the AppData directory
2. Open an issue in the GitHub repository with:
   - Detailed description of the problem
   - Steps to reproduce
   - Log file contents
   - Operating system details

## Future Enhancements

- [ ] Add support for other operating systems
- [ ] Implement drag-and-drop functionality
- [ ] Add option to specify output directory
- [ ] Include file validation before conversion
- [ ] Add support for other file formats