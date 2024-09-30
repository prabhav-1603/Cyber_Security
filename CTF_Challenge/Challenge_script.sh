#!/bin/bash

# Dependencies check
command -v unzip >/dev/null 2>&1 || { echo >&2 "unzip command not found. Please install unzip."; exit 1; }
command -v 7z >/dev/null 2>&1 || { echo >&2 "7z command not found. Please install p7zip."; exit 1; }
command -v base64 >/dev/null 2>&1 || { echo >&2 "base64 command not found. Please install coreutils."; exit 1; }
command -v base32 >/dev/null 2>&1 || { echo >&2 "base32 command not found. Please install coreutils."; exit 1; }
command -v xxd >/dev/null 2>&1 || { echo >&2 "xxd command not found. Please install xxd."; exit 1; }

# Initial zip file
zip_file="chall1.7z"
output_dir="extracted"

# Function to try different password encodings
try_password_encodings() {
    local zip_file="$1"
    local password="$2"
    local output_dir="$3"

    for encoding in "plain" "base64" "base32" "hex"; do
        case $encoding in
            plain)
                encoded_password="$password"
                ;;
            base64)
                encoded_password=$(echo -n "$password" | base64)
                ;;
            base32)
                encoded_password=$(echo -n "$password" | base32)
                ;;
            hex)
                encoded_password=$(echo -n "$password" | xxd -p)
                ;;
        esac

        # Attempt to unzip with the encoded password
        if [[ "$zip_file" == *.zip ]]; then
            unzip -o -P "$encoded_password" "$zip_file" -d "$output_dir" >/dev/null 2>&1
        elif [[ "$zip_file" == *.7z ]]; then
            7z x -p"$encoded_password" -o"$output_dir" "$zip_file" >/dev/null 2>&1
        fi

        if [ $? -eq 0 ]; then
            return 0  # Success
        fi
    done

    return 1  # Failure
}

# Extraction loop
for i in {1..690}; do
    # Create output directory if it does not exist
    mkdir -p "$output_dir"
    
    # Extract the password file
    if [ $i -eq 1 ]; then
        curr_zip_file=$(find "." -type f -name '*.zip' -o -name '*.7z')
        if [[ "$curr_zip_file" == *.zip ]]; then
            unzip -o "$curr_zip_file" -d "$output_dir" >/dev/null 2>&1
        elif [[ "$curr_zip_file" == *.7z ]]; then
            7z x "$curr_zip_file" -o"$output_dir" >/dev/null 2>&1
        fi
        continue
    fi
    echo "Reached $i"

    # Determine the next zip file name (assuming it has the same base name)
    curr_zip_file=$(find "$output_dir" -type f -name '*.zip' -o -name '*.7z')
    echo $curr_zip_file
    if [ -z "$curr_zip_file" ]; then
        echo "Next zip file not found at step $i. Extraction complete."
        break
    fi
    filename=$(basename "$curr_zip_file")
    # Read the password
    password_file=$(find "$output_dir" -type f ! -name "$filename")
    echo $password_file
    if [ ! -f "$password_file" ]; then
        echo "Password file not found at step $i."
        exit 1
    fi
    password=$(cat "$password_file")

    # Try to extract using the password in different encodings
    if ! try_password_encodings "$curr_zip_file" "$password" "$output_dir"; then
        echo "Extraction failed for $next_zip_file with all encodings at step $i."
        exit 1
    fi
    # Clean up and prepare for the next iteration
    rm -f "$password_file"
    rm -f "$curr_zip_file"
done

echo "Extraction complete. The flag should be in the final directory."