#! /usr/bin/env python
import screed
import argparse
import csv

P=0.05

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('genes_file')
    parser.add_argument('transcript_file')
    parser.add_argument('output')

    args = parser.parse_args()

    print 'Loading transcript matrix from:', args.transcript_file
    annots = {}
    for record in screed.open(args.transcript_file):
        tr = record.name.split('.')[2]
        assert tr.startswith('tr')

        # find the location of the x_of_y string; before that is the
        # annotation.
        annot_loc = record.description.find('_of_')
        assert annot_loc > 0
        while annot_loc > 0 and record.description[annot_loc] != ' ':
            annot_loc -= 1
        assert annot_loc >= 0, annot_loc

        # if we got anything, record it.
        if annot_loc > 0:
            annot = record.description[:annot_loc].strip()

            # eliminate 'transcript family' annotations since the
            # original annotations will be gathered.
            if annot.startswith('transcript family'):
                continue

            x = annots.get(tr, [])
            x.append(annot)
            annots[tr] = x

    print 'Annotating matrix from:', args.genes_file\

    fp = open(args.genes_file, 'rb')
    r = csv.DictReader(fp, delimiter='\t',
        fieldnames=['tr','one','two','three','four','five','six'])
    outfp = open(args.output+'.csv', 'w')
    w = csv.writer(outfp)
    fp.readline()
    w.writerow(["tr", "1.fq.genes.results", "2.fq.genes.results",
    "3.fq.genes.results", "4.fq.genes.results", "7.fq.genes.results",
    "8.fq.genes.results", "annotation"])
    for row in r:
        tr = row['tr']
        w.writerow([tr, row['one'], row['two'], row['three'], row['four'],
        row['five'], row['six'], annots.get(tr, '')])
    outfp.close()
    fp.close()


if __name__ == '__main__':
    main()
