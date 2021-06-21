#!/usr/bin/env python3

import os,sys
import csv
import argparse
import json
import uploadSC2Data as UD

if __name__ == '__main__':
    #setup argparser to display help if no arguments
    class MyParser(argparse.ArgumentParser):
        def error(self, message):
            sys.stderr.write('error: %s\n' % message)
            self.print_help()
            sys.exit(2)

    parser = MyParser(description=f"Transfer sequence data to dynamoDB")
    parser.add_argument("data_path",help="Path to sequencing results")
    parser.add_argument("--aws",default=False,action="store_true",help="Use AWS resource")
    args = parser.parse_args()

    run_data_path = None
    for root,dirs,files in os.walk(args.data_path):
        for file in files:
            if "results.csv" in file:
                run_data_path = os.path.join(root,file)

    if run_data_path:
        #from csv to object
        run_data = {}
        with open(run_data_path,'r') as csvfile:
            run = csv.DictReader(csvfile)
            for sample in run:
                sample['run_name'] = os.path.basename(run_data_path).split('_')[0]
                sample['KeyID'] = sample['sample_id'] + "_" + sample['run_name']
                run_data[sample['KeyID']] = sample
    else:
        print("Could not find summary.csv file.")
        sys.exit(1)

    UD.upload_seqrun(run_data,args.aws)
