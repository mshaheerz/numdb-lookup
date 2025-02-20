# numdb-lookup
Finding number details all possible ways
# Phone Number Lookup Script

This script allows you to perform phone number lookups using different services such as normal lookup, Truecaller, and Numverify.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/phone_lookup.git
   cd phone_lookup
Make the installation script executable:
bash
Copy
chmod +x install_requirements.sh
Run the installation script:
bash
Copy
./install_requirements.sh all
Install all dependencies: ./install_requirements.sh all
Install only Python dependencies: ./install_requirements.sh python
Make the Bash script executable: ./install_requirements.sh bash
Display help message: ./install_requirements.sh help
Usage
Normal Lookup
bash
Copy
./phone_lookup.sh normal
Truecaller Lookup
bash
Copy
./phone_lookup.sh truecaller
You will be prompted to enter your Truecaller API key.
Numverify Lookup
bash
Copy
./phone_lookup.sh numverify
You will be prompted to enter your Numverify API key.
Help
bash
Copy
./phone_lookup.sh help
Dependencies
Python 3
phonenumbers library for normal lookup
requests library for API calls
Contributing
Feel free to contribute to this project by submitting pull requests or opening issues.
License
This project is licensed under the MIT License - see the LICENSE file for details.
Copy

### Downloadable `README.md`

To make the `README.md` file downloadable, you can simply create a GitHub repository and push your project files, including the `README.md`, to the repository. Users can then clone the repository or download the files directly from GitHub.

Here are the steps to create a GitHub repository and push your project:

1. **Create a GitHub Repository:**
   - Go to [GitHub](https://github.com/) and sign in to your account.
   - Click on the "+" icon in the upper right corner and select "New repository."
   - Fill in the repository name (e.g., `phone_lookup`), description, and choose whether it should be public or private.
   - Click "Create repository."

2. **Push Your Project to GitHub:**
   - Open a terminal and navigate to your project directory.
   - Initialize a new Git repository (if not already done):
     ```bash
     git init
     ```
   - Add your files to the repository:
     ```bash
     git add .
     ```
   - Commit your changes:
     ```bash
     git commit -m "Initial commit"
     ```
   - Link your local repository to the remote GitHub repository:
     ```bash
     git remote add origin https://github.com/yourusername/phone_lookup.git
     ```
   - Push your changes to GitHub:
     ```bash
     git push -u origin main
     ```

3. **Download the Project:**
   - Users can clone the repository using:
     ```bash
     git clone https://github.com/yourusername/phone_lookup.git
     ```
   - Alternatively, they can download the repository as a ZIP file by clicking on the "Code" button on the repository page and selecting "Download ZIP."

By following these steps, you will have a downloadable `README.md` file as part of your project on GitHub.