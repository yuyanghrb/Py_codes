import csv

def list2csv(listname, csvname):    
    with open(csvname,  "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(listname)
    return 1