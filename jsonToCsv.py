from argparse import ArgumentParser
from os import path
import sys
import csv
import json
from datetime import datetime

# utc_offset, location, followers_count, verified, lang from user
column_names = ['created_at', 'text', 'reply_count', 'retweet_count', 'favorite_count', 'utc_offset', 'location', 'followers_count', 'verified', 'lang', 'geo', 'coordinates', 'place', 'epoch']
user_colums = ['utc_offset', 'location', 'followers_count', 'verified']

def filesToCsv(files, outputDir='./'):
    for filename in files:
        outputName = path.join(path.abspath(outputDir), path.basename('%s.csv' % filename))
        with open(filename, 'r') as inp:
            with open(outputName, 'w') as outp:
                writer = csv.DictWriter(outp, fieldnames=column_names)
                writer.writeheader()
                for line in inp:
                    j = json.loads(line)
                    data = dict()
                    try:
                        userData = j['user']
                    except:
                        pass
                    for col in column_names:
                        if col == 'epoch':
                            try:
                                pattern = r"%a %b %d %H:%M:%S %z %Y"
                                t = datetime.strptime(j['created_at'], pattern).timestamp()

                                data['epoch'] = t
                                if 'utc_offset' in userData:
                                    data['epoch'] += int(userData['utc_offset']) * 60;
                            except:
                                pass
                        elif col in user_colums:
                            try:
                                data[col] = userData[col]
                            except:
                                pass
                        else:
                            try:
                                data[col] = j[col]
                            except:
                                pass
                    writer.writerow(data)

def main():
    parser = ArgumentParser(usage='%(prog)s [<sourceOne> sourceTwo [...]] [options...]', description='Json to CSV converter.')
    parser.add_argument('sourceFiles', nargs= '+', help='Files to parse.')
    parser.add_argument('-d', default='./', help='Where to dump output files')
    parsed = parser.parse_args(sys.argv[1:])
    if not path.exists(parsed.d):
        exit('Error! %s is not a valid dir.' % parsed.d)
    filesToCsv(parsed.sourceFiles, outputDir=parsed.d)

if __name__ == '__main__':
    main()
