#!/usr/bin/env python3
'''
Given a "MOSS linkage" JSON (e.g. generated by moss_connectivity.py), output a zip file of the reports
Niema Moshiri 2019
'''
from json import load
from urllib.request import urlopen
from zipfile import ZipFile,ZIP_DEFLATED

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=str, default='stdin', help="MOSS Linkage File (JSON)")
    parser.add_argument('-o', '--output', required=True, type=str, help="Output File (zip)")
    args = parser.parse_args()
    if args.input == 'stdin':
        from sys import stdin as infile
    else:
        infile = open(args.input)
    if not args.output.lower().endswith('.zip'):
        raise ValueError("Output file must be zip")

    # download MOSS match reports
    links = load(infile)
    emails = sorted(links.keys())
    outzip = ZipFile(args.output, mode='w', compression=ZIP_DEFLATED)
    num_pairs = int(len(emails)*(len(emails)-1)/2)
    for i in range(len(emails)-1):
        for j in range(i+1, len(emails)):
            if emails[j] in links[emails[i]]:
                folder = "%s,%s" % (emails[i], emails[j])
                for url in links[emails[i]][emails[j]]:
                    outzip.writestr("%s/%s" % (folder, url.split('/')[-2]), urlopen(url).read().decode())
            print("Successfully downloaded student pair %d of %d" % (len(emails)*i+j+1, num_pairs), end='\r')
