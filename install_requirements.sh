#!/bin/bash

# Function to display usage
usage() {
    echo "Usage: $0 [option]"
    echo "Options:"
    echo "  all           Install all dependencies and run normal lookup"
    echo "  python        Install Python dependencies"
    echo "  bash          Make the Bash script executable"
    echo "  normal        Run normal phone number lookup"
    echo "  truecaller    Run Truecaller phone number lookup"
    echo "  numverify     Run Numverify phone number lookup"
    echo "  help          Display this help message"
}

# Function to install Python dependencies
install_python_deps() {
    echo "Installing Python dependencies..."
    pip install phonenumbers requests
    echo "Python dependencies installed successfully."
}

# Function to make the Bash script executable
make_bash_executable() {
    echo "Making the Bash script executable..."
    chmod +x phone_lookup.sh
    echo "Bash script is now executable."
}

# Function to run normal phone number lookup
run_normal_lookup() {
    read -p "Enter the phone number: " phone_number
    python3 normal_lookup.py "$phone_number"
}

# Function to run Truecaller phone number lookup
run_truecaller_lookup() {
    read -p "Enter the phone number: " phone_number
    read -p "Enter your Truecaller API key: " truecaller_api_key
    python3 truecaller_lookup.py --api_key "$truecaller_api_key" "$phone_number"
}

# Function to run Numverify phone number lookup
run_numverify_lookup() {
    read -p "Enter the phone number: " phone_number
    read -p "Enter your Numverify API key: " numverify_api_key
    python3 numverify_lookup.py --api_key "$numverify_api_key" "$phone_number"
}

# Check if an option is provided
if [ $# -eq 0 ]; then
    usage
    exit 1
fi

# Parse the option
case $1 in
    all)
        install_python_deps
        make_bash_executable
        run_normal_lookup
        ;;
    python)
        install_python_deps
        ;;
    bash)
        make_bash_executable
        ;;
    normal)
        run_normal_lookup
        ;;
    truecaller)
        run_truecaller_lookup
        ;;
    numverify)
        run_numverify_lookup
        ;;
    help)
        usage
        ;;
    *)
        echo "Invalid option: $1"
        usage
        exit 1
        ;;
esac