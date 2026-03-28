# Splice Sample Organizer
Splice Sample Organizer is a Python-based automation tool designed for music producers to instantly declutter their Splice download folders. It intelligently categorizes audio files into a structured library based on instrument types, techniques, and sonic characteristics.

## 🚀 Overview
-As a music producer, managing thousands of samples from Splice can be overwhelming. This script automates the tedious process of manual sorting. By parsing filenames and matching them against a comprehensive keyword database, it moves your .wav and .aif files into a clean, hierarchical folder structure.

## ✨ Key Features
-Deep Categorization: Supports 10+ main categories (Drums, Vocals, Synth, etc.) and over 60 specific sub-categories (Kicks, Leads, Risers, etc.).
-Intelligent Keyword Matching: Uses a robust dictionary-based mapping system to identify instruments even with abbreviated filenames (e.g., "BD" for Kick, "HH" for Hats).
-Automatic Report Generation: Every run generates a classification_report.txt that tracks successfully sorted files and flags "Unclassified" samples for manual review.
-Safe File Handling: Utilizes Python's shutil module for reliable file moving and os for cross-platform directory management.

🛠️ Technical Implementation
The core logic of this tool relies on Dictionary Mapping and Pattern Recognition.

1. The Mapping Engine
The script uses a nested dictionary structure called SAMPLE_MAP. Each key represents a musical category, and each value contains a list of associated keywords found in Splice's naming conventions.

Python
# Example of the logic
SAMPLE_MAP = {
    "Drums": {
        "Kicks": ["kick", "bd"],
        "Snares": ["snare", "sd"],
        "Hats": ["hat", "hh", "hihat"]
    }
}
2. Decision Logic
The get_category function iterates through the dictionary. If a filename contains a keyword (e.g., "Snare"), the script assigns it to the corresponding path (Drums/Snares).

3. Error Handling & Logging
To ensure no files are lost, the script includes try-except blocks. If a file cannot be moved (due to being open in a DAW like Ableton or FL Studio), it logs the error in the report instead of crashing the program.

📁 Project Structure
Plaintext
.
├── splice_organizer.py       # Main Python source code
├── splice_organizer.exe      # Compiled standalone executable
├── README.md                 # Project documentation
├── .gitignore                # Prevents large audio files from uploading to GitHub
└── LICENSE                   # MIT License

⚙️ How to Use
Clone the Repository:
git clone https://github.com/your-username/splice-sample-organizer.git

Configure Paths: Open splice_organizer.py and update the SOURCE_DIR and EXPORT_DIR to match your local folders.

Run the Script:

Via Python: python splice_organizer.py

Via Executable: Double-click splice_organizer.exe in the dist/ folder.

Review the Report: Check classification_report.txt to see the results.
