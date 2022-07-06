import sys
import hashlib
import os
import requests
import time


# file, apikey
def main():
    if len(sys.argv) != 3:
        print("Error: Invalid number of arguments. Please only provide one file. \nUsage: python scan.py file_name APIKEY", file=sys.stderr)
        return
    f = None
    try:
        f = open(os.path.abspath(sys.argv[1]), "r")
    except IOError:
        print("File does not exist.", file=sys.stderr)
    else:
        dat = f.read()

        #check hash
        hsh = hashlib.md5(dat.encode()) 
        url = "https://api.metadefender.com/v4/hash/" + str(hsh)
        headers = {'apikey': sys.argv[2]}
        result = requests.request("GET", url, headers=headers)

        # hash was found
        if "error" in result.json():

            # upload file to scan and get data id
            headers["Content-Type"] = "application/octet-stream"
            res_id = requests.post("https://api.metadefender.com/v4/file", headers=headers,data=dat)
            did = res_id.json()["data_id"]

            # get result data from data id
            headers = {'apikey': sys.argv[2], 'x-file-metadata': "{x-file-metadata}"}
            result = requests.request("GET", "https://api.metadefender.com/v4/file/" + did , headers=headers)
            time.sleep(5) # time.sleep added to not spam the api

            while result.json()["scan_results"]["progress_percentage"] != 100:
                time.sleep(5)
                result = requests.request("GET", "https://api.metadefender.com/v4/file/" + did, headers=headers)

        result = result.json()["scan_results"]
        details = result["scan_details"]

        print("\nfilename: " + sys.argv[1])
        print("overall status: " + result["scan_all_result_a"])
        for engine in details:
            print("engine: " + engine)

            if details[engine]["threat_found"]:
                print("threat_found: " + details[engine]["threat_found"])
            else:
                print("threat_found: Clean")

            print("scan_result: " + str(details[engine]["scan_result_i"]))
            print("def_time: " + details[engine]["def_time"])



if __name__ == "__main__":
    main()