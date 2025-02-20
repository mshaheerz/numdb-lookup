#!/bin/bash

# Function to display usage
usage() {
    echo "Usage: $0 [option]"
    echo "Options:"
    echo "  normal       Run the normal phone number lookup script"
    echo "  truecaller   Run the Truecaller phone number lookup script"
    echo "  numverify    Run the Numverify phone number lookup script"
    echo "  help         Display this help message"
}

# Function to run normal phone number lookup
run_normal() {
    python3 normal_lookup.py
}

# Function to run Truecaller phone number lookup
run_truecaller() {
    read -p "Enter your Truecaller API key: " truecaller_api_key
    python3 truecaller_lookup.py --api_key "$truecaller_api_key"
}

# Function to run Numverify phone number lookup
run_numverify() {
    read -p "Enter your Numverify API key: " numverify_api_key
    python3 numverify_lookup.py --api_key "$numverify_api_key"
}

# Check if an option is provided
if [ $# -eq 0 ]; then
    usage
    exit 1
fi

# Parse the option
case $1 in
    normal)
        run_normal
        ;;
    truecaller)
        run_truecaller
        ;;
    numverify)
        run_numverify
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