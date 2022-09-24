import subprocess
import time
import os
import csv

CODECS = "copy gzip lzma zstd lz4 lzo1b density zpaq".split()
VERBOSE = False
DATASET_DIR = "datasets"

files = os.listdir(DATASET_DIR)

if VERBOSE:
    print(f"{len(files)} files found in {DATASET_DIR}.")
    for file in files:
        print("\t"+file)

def compress(filename: str, codec: str):
    outputfile = f"./tmp/{filename}.{codec}"
    squash_process = subprocess.run(["squash", "-fkc", codec, DATASET_DIR+"/"+filename, outputfile])
    if squash_process.returncode:
        print("There was an error with Squash.")
        quit(1)
    return outputfile
        
def decompress(filename: str, codec: str):
    # WARNING: deletes input files.
    squash_process = subprocess.run(["squash", "-fdc", codec, filename, "/dev/null"])
    if squash_process.returncode:
        print("There was an error with Squash.")
        quit(1)

csv_header = "filename codec original_size compressed_size compression_time decompression_time".split()
with open('results.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(csv_header)
    for codec in CODECS: 
        for file in files:
            start_time = time.perf_counter_ns()
            output = compress(file, codec)
            compression_time = time.perf_counter_ns() - start_time
            original_size = os.path.getsize(f"{DATASET_DIR}/{file}")
            size = os.path.getsize(output)
            if VERBOSE:
                print(f"[{codec}] Compressing to {size} bytes in {compression_time}ns")
                
            start_time = time.perf_counter_ns()
            decompress(output, codec)
            decompression_time = time.perf_counter_ns() - start_time
            if VERBOSE:
                print(f"\t Compression percentage is {(size/original_size * 100)}%")
                print(f"\t Decompression time is {decompression_time}ns")
            writer.writerow([file,codec,original_size,size,compression_time,decompression_time])