import gzip, psutil, os
from Bio import SeqIO

def read_fasta_gzip(filePath):
    sequence = ''
    with gzip.open(filePath, "rt") as file:
        for record in SeqIO.parse(file, "fasta"):
            sequence = str(record.seq)
            break
    return sequence

def check_mem():
    process = psutil.Process(os.getpid()) 
    mem = process.memory_info().rss / 1024 / 1024
    return mem 

def read_C_suffix_array(filePath):
    sa = []
    with open(filePath) as file:
        tmp = file.read()
        lst = tmp.split(' ')
        sa = [int(x) for x in lst]
    return sa