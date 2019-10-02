# tk 
from enum import Enum
from datetime import datetime,timedelta
from dateutil import parser
import os
import csv
import numpy as np
from sklearn.preprocessing import normalize

# Domain Data (for our example)
from color import Color

# Fake data section
def fake_data(storage_dir) : 

    def generate_fake_data(minutes, mu, sigma) :
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=minutes)
        # Generate a random amount of data
        amount_of_fake_data = minutes * int(mu + sigma * np.random.randn())
        # Generate at least 1 element
        amount_of_fake_data = 1 if amount_of_fake_data < 1 else amount_of_fake_data
        arrival_times = np.arange(start_time, end_time, timedelta(minutes = minutes / amount_of_fake_data)).astype(datetime)
        color_votes = list(Color.randn_color().name for _ in range(amount_of_fake_data))
        time_and_vote = zip(arrival_times, color_votes)
        return time_and_vote

    input_data_file = 'unprocessed_data.csv'
    input_path = os.path.join(storage_dir, input_data_file)
    # If first time, generate a bit more data 
    minutes_back = 1 if os.path.exists(input_path) else 10 
    data = generate_fake_data(minutes_back, 100, 50)
    with open(input_path, mode='w+') as f : 
        writer = csv.writer(f)
        writer.writerows(data)

# Example of ML task code (data preprocessing)
def read_raw_data(storage_dir) : 
    input_data_file = 'unprocessed_data.csv'
    input_path = os.path.join(storage_dir, input_data_file)
    if os.path.exists(input_path) : 
        with open(input_path, mode='r') as f : 
            reader = csv.reader(f)
            return list(reader)
    else :
        # If file doesn't exist, return empty list 
        return []

# Please note: this is just a silly example of converting and normalizing, e.g., "preprocessing stuff"     
def process_raw_data(raw_data) : 
    def convert(d) :
        for datum in d : 
            dt = parser.parse(datum[0])
            ts = int(dt.timestamp())
            c = Color[datum[1]].value
            yield (ts, c)
    processed_data = list(convert(raw_data))
    normalized_data = normalize(processed_data, axis = 0)
    return normalized_data

def write_processed_data(storage_dir, processed_data) : 
    output_data_file = 'processed_data.csv'
    output_path = os.path.join(storage_dir, output_data_file)

    # Note: Clobbers existing processed data -- fine in this example
    with open(output_path, mode='w') as f : 
        writer = csv.writer(f)
        writer.writerows(processed_data)

def main() : 
    storage_dir = '.'
    # Write some fake data to 'unprocessed_data.csv' -- normally data would be written via some external process
    fake_data(storage_dir)
    print("Beginning periodic data processing...")
    raw_data = read_raw_data(storage_dir)
    processed_data = process_raw_data(raw_data)
    write_processed_data(storage_dir, processed_data)
    print(f"Wrote {len(processed_data)} records")
    print("...Periodic data processing ended.")

if __name__== "__main__":
    main()