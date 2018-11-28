import argparse
import csv

parser = argparse.ArgumentParser(description='Run the B2 problem.')
parser.add_argument('infile',
                    help='The input file (compounds.tsv).')
args = parser.parse_args()

# test cases:
# chartaceone
# daunorubicin
# secobarbital
def legalize_name(name):
    result = ''
    from re import compile, sub
    r = compile(r'[\w\d]')
    pos_charge = compile(r'\(([\d]*)\+\)')
    neg_charge = compile(r'\(([\d]*)-\)')
    pm_charge = compile(r'\(\+-\)')
    name = sub(pos_charge,r'@\1x@',name)
    name = sub(neg_charge,r'@\1n@',name)
    name = sub(pm_charge,r'@xn@',name)
    for c in name:
        if r.match(c) is not None:
            result += c
        elif c == '+':
            result += 'x'
        elif c == "'":
            result += 'p'
        elif c == ' ' or c == '-' or c == '@':
            result += '@'
        else:
            result += '_'
    result = '_'.join(result.split('@@@@'))
    result = '_'.join(result.split('@@@'))
    result = '_'.join(result.split('@@'))
    result = '_'.join(filter(lambda x: x != '', result.split('@')))
    result = result.replace('@','_')
    return result

dash_cutoff = 10
length_cutoff = 20

with open(args.infile,'r') as f:
    compounds = csv.reader(f, delimiter='\t')
    # skip first row
    for row in compounds:
        break

    for row in compounds:
        id = row[0]
        status = row[1]
        curated = status == 'C'
        parent_id = int(row[4]) if row[4] != 'null' else None
        name = row[5] if row[5] != 'null' else None
        stars = int(row[9])
        if curated and parent_id is None and name is not None and stars >= 3 and len(name) < length_cutoff and name.count('-') < dash_cutoff:
            legalized_name = legalize_name(name)
            print(id,name,legalized_name)
