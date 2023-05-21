import csv
import re
import sys
from typing import List

group_pattern = re.compile("^[0-9]+\.$")
txt_file_path = sys.argv[1]
header = ["Company", "Industry", "Location", "Description", "Size"]

if txt_file_path is None:
    print("Please provide file path")


def remove_empty_lines(input_lines):
    result_lines = []
    for line in input_lines:
        line = line.strip()
        if not line or line.endswith("Logo"):
            continue
        result_lines.append(line.strip())
    return result_lines


def group_data(input_lines: List[str]):
    result_data = []
    group = []
    for line in input_lines:
        if bool(group_pattern.match(line)):
            if group:
                group = group[1:]
                result_data.append(group)
                group = []
        group.append(line)
    return result_data


def write_to_csv(input_groups: List[List[str]]):
    with open(f"{txt_file_path}.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(input_groups)


with open(txt_file_path, "r") as f:
    lines = f.readlines()
    lines = remove_empty_lines(lines)
    grouped_data = group_data(lines)
    write_to_csv(grouped_data)
