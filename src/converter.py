import sys, os, utils
from os.path import isfile

def main():
    if not len(sys.argv) in [3]:
        print('Usage: %s INPUT_FILE(*.fa.gz) OUTPUT_FILE' % sys.argv[0])
        os.abort()
    else:
        if not isfile(sys.argv[1]):
            print("Input file doesn't exist")
            os.abort()
        
        # Read fasta file
        print("Reading %s" % sys.argv[1])
        sequence = utils.read_fasta_gzip(sys.argv[1])
        sequence += "$"
        print("Finished reading...")
       
        # Save only sequence to file
        print("Writing %s" % sys.argv[2])
        with open(sys.argv[2], "w") as file:
            file.write(sequence)
        print("Finished writing...")

if __name__ == '__main__':
    main()