import os
import argparse
import requests
import time
from clint.textui import progress

DEFAULT_5G_TEST_URL = "http://speedtest-sgp1.digitalocean.com/5gb.test"
DEFAULT_512MB_TEST_URL = "http://ipv4.download.thinkbroadband.com/512MB.zip"
DEFAULT_50MB_TEST_URL = "http://ipv4.download.thinkbroadband.com/50MB.zip"

TEST_URLS = {
	"S" : DEFAULT_50MB_TEST_URL,
	"M" : DEFAULT_512MB_TEST_URL, 
	"L" : DEFAULT_5G_TEST_URL
}


parser = argparse.ArgumentParser(prog="SpeedTest", description="Download a random file to check download speeds")
parser.add_argument("-s", "--size", choices=["S", "M", "L"], required=True)
args = parser.parse_args()

selected_url = TEST_URLS[args.size]
dir_path = os.path.dirname(os.path.realpath(__file__))
r = requests.get(selected_url, stream=True)
download_file_path = f"{dir_path}/speedtest"

start_time = time.time()
with open(download_file_path, "wb") as f:
	download_size_kb = (int(r.headers.get("content-length")))/1024
	for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=download_size_kb + 1):
		if chunk:
			f.write(chunk)
			f.flush()
end_time = time.time()

os.remove(download_file_path)

time_taken_seconds = end_time - start_time
download_size_mb = download_size_kb / 1024
download_speed_mb_s = round((download_size_mb / time_taken_seconds), 2)

print("Took %s seconds" % time_taken_seconds)
print("Download speed: %s MB/s" % download_speed_mb_s)


