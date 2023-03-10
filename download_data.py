from data_cleaning import main
import requests
import zipfile
import os
import pandas as pd
import glob
import datetime


# URL for the .zip file to be downloaded
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00501/PRSA2017_Data_20130301-20170228.zip"

# Path for the directory where the files will be stored
data_dir = "./Data"

# Name of the .zip file
zip_file = "Airqualitydata.zip"

# Full path to the .zip file
zip_file_path = f"{data_dir}/{zip_file}"

# Create the directory if it doesn't exist
if not os.path.isdir(data_dir):
    os.mkdir(data_dir)

# Download the file if it doesn't exist
if not os.path.isfile(zip_file_path):
    print("---------------------Downloading data ---------------------")
    r = requests.get(url, allow_redirects=True)
    open(zip_file_path, "wb").write(r.content)
    print(f"File downloaded and saved to {zip_file_path}")
else:
    print("Data already downloaded")

# Extract the contents of the zip file to the directory
with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
    zip_ref.extractall(data_dir)

# Merge the CSV files and save the resulting DataFrame to a new CSV file
merged_data_file = f"{data_dir}/merged_data.csv"
if not os.path.isfile(merged_data_file):
    print("---------------------Merging data ---------------------")
    csv_files = glob.glob(f"{data_dir}/PRSA_Data_20130301-20170228/*")
    merged_data = pd.concat((pd.read_csv(f) for f in csv_files), ignore_index=True)
    merged_data["date"] = merged_data.apply(
        lambda x: datetime.datetime(x["year"], x["month"], x["day"], x["hour"]), axis=1
    )
    merged_data = merged_data.sort_values(["date"], ascending=True)
    merged_data.set_index("date", inplace=True)
    merged_data.to_csv(merged_data_file)
    print(f"Data merged and saved to {merged_data_file}")

    # Preprocess the merged data and split into train and test sets
    print("---------------------Preprocessing data---------------------")
    train, test = main(merged_data)
    train_file = f"{data_dir}/train.csv"
    test_file = f"{data_dir}/test.csv"
    train.to_csv(train_file)
    test.to_csv(test_file)
    print(f"Train and test sets saved to {train_file} and {test_file}")
    print("---------------------Done---------------------")

else:
    print("Merged data already exists")
