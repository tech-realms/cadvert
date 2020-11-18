#!/usr/bin/python3

import csv
import sys
import re

### generate_template_conversion_map creates a list of numbers to be used internally by convert_csv.
### The index corresponds to a column in the destination, and the value corresponds to a column in the source.
# src_template = the format to be converted from
# dst_template = the format to convert to
def generate_template_conversion_map(src_template, dst_template):
    src_list = list(map(lambda s : s.strip(), src_template.split(',')))
    dst_list = list(map(lambda s : s.strip(), dst_template.split(',')))
    def find_column_from_source(col_str):
        for index, c in enumerate(src_list):
            if col_str == c:
                return index
    return list(map(find_column_from_source, dst_list))

### convert_csv converts a csv file according to a source and destination template and a post conversion function.
# csv_file     = path of csv file
# src_template = the format that the csv file is currently in
# dst_template = the format that the csv file will be converted to
# post_fn      = the function that is called for each row after it has been converted by the template
def convert_csv(csv_filename, new_filename, src_template, dst_template, post_fn = (lambda x : x)):
    template_map = generate_template_conversion_map(src_template, dst_template)
    with open(csv_filename, mode='r') as csv_file:
        csv_file.readline()
        csv_file.readline()
        with open(new_filename, mode='w', newline="\n") as new_file:
            src_reader = csv.reader(csv_file, delimiter=',')
            dst_writer = csv.writer(new_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, dialect='excel')
            for row in src_reader:
                dst_writer.writerow(post_fn(list(map(lambda c : row[c], template_map))))

CURRENT_911_ROW = 1
SERVICE_CLASS_ABBR = { "0" : "ERR",
                       "1" : "RESD",
                       "2" : "BUSN",
                       "3" : "PBXR",
                       "4" : "PBXB",
                       "5" : "CNTX",
                       "6" : "PAY$",
                       "7" : "COIN",
                       "8" : "MOBL",
                       "9" : "RESX",
                       "W" : "WRLS",
                       "G" : "WPH1",
                       "H" : "WPH2",
                       "V" : "VOIP",
                       "T" : "TLMA" }

LISTED_OR_UNLISTED = { "0" : "FALSE",
                       "3" : "TRUE" }

def convert_911_row(row):
    global CURRENT_911_ROW
    new_row = [ CURRENT_911_ROW, 
                *row[1:3], 
                SERVICE_CLASS_ABBR[row[3]], 
                re.sub(r"\s{2,}", " ", (" ".join(row[4:10])).strip()), 
                row[10], 
                LISTED_OR_UNLISTED[row[11]] ]
    CURRENT_911_ROW += 1
    return new_row

SOURCE_TEMPLATE = "Number,CompID1,F,House #,House Sfx,Pre Dir,Street Name,Street Sfx,Post Dir,Community Name,County,State,Customer,ESN,Location,Exchange,Class,Type,Main No,Zip,Zip4,CompID2,TAR,Alt. No,Extract,Entry Date,Last_Update"
DEST_TEMPLATE   = "ESN, Customer, Number, Class, House #, House Sfx, Pre Dir, Street Name, Street Sfx, Post Dir, Community Name, Type"

def main():
    convert_csv(sys.argv[1], "./converted.csv", SOURCE_TEMPLATE, DEST_TEMPLATE, convert_911_row)
    print("DONE!")

if __name__ == "__main__":
    main()

