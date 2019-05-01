import sys, os, utils, datetime, time, fm
from os.path import isfile

def main():
    if not len(sys.argv) in [3, 5, 7, 9]:
        print('Usage: %s SEQUENCE_INPUT_FILE(*.fa.gz) [-sa SA_INPUT_FILE] [-cps CPS_SAMPLE] [-ssa SSA_SAMPLE] OUTPUT_FILE' % sys.argv[0])
        os.abort()
    else:
        if not isfile(sys.argv[1]):
            print("Sequence input file doesn't exist")
            os.abort()

        # Checkpoints fraction argument
        try:
            cpsInd = sys.argv.index('-cps') + 1
            cps = int(sys.argv[cpsInd])
        except ValueError:
            cps = 128

        # Suffix array fraction argument
        try:
            ssaInd = sys.argv.index('-ssa') + 1
            ssa = int(sys.argv[ssaInd])
        except ValueError:
            ssa = 32

        # Suffix array file
        try:
            saInd = sys.argv.index('-sa') + 1
            print("Reading suffix array from %s" % sys.argv[1])
            sa = utils.read_C_suffix_array(sys.argv[saInd])
            print("Finished reading...")
        except ValueError:
            sa = None
        
        # Read sequence from fasta file   
        print("Reading sequence from %s" % sys.argv[1]) 
        sequence = utils.read_fasta_gzip(sys.argv[1])
        sequence += "$"
        print("Finished reading...")

        # Create FM Index
        print('Creating FM index: ' + str(datetime.datetime.now()))
        start_time = time.time()
        fmInd = fm.FmIndex(sequence, False, sa, cps, ssa)
        end_time = time.time()
        print("FM index created: " + str(datetime.datetime.now()))
        print("Creation time: %.2f seconds" % (end_time-start_time))
        
        # Check Memory
        mem = utils.check_mem()
        print("Used memory: %d MB" % mem)

        # Save FM Index to File
        print("Saving %s" % sys.argv[len(sys.argv) - 1])
        fmInd.save(sys.argv[len(sys.argv) - 1])
        print("Finished saving...")

if __name__ == '__main__':
    main()