#!/bin/bash

# Define the necessary variables
PYTHON_SCRIPT="script.py"
OUTPUT_CSV="crypto.csv"
S3_BUCKET_NAME="news--bucket"


# Run the Python script and save the output to a timestamped CSV file
echo "Starting the scraper script..."
python3 $PYTHON_SCRIPT > $OUTPUT_CSV || { echo "Error: Python script execution failed"; exit 1; }


if [ -f $OUTPUT_CSV ]; then

    # Generate a timestamp for the new file name
    TIMESTAMP=$(date +'%Y-%m-%d %H-%M-%S')
    NEW_FILE="crypto-${TIMESTAMP}.csv"

    # Rename the file with the timestamp
     mv "$OUTPUT_CSV" "$NEW_FILE"


    # Upload the CSV file to Amazon S3 
    echo "Uploading data to S3..."
   
    aws s3 cp "$NEW_FILE" "s3://$S3_BUCKET_NAME/$NEW_FILE" || { echo "Error: Failed to upload data to S3"; exit 1; }
    
    # Remove the local CSV file
    rm "$NEW_FILE" || { echo "Error: Failed to delete local CSV file"; exit 1; }

    echo "Script execution and data upload completed successfully."
else
   echo "CSV file not found. Check your scraping script."
fi