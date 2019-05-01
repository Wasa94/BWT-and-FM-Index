import sys, os, time, datetime, utils, fm
from os.path import isfile

def main():
    if not len(sys.argv) in [3, 4]:
        print('Usage: %s FM_INPUT_FILE PATTERN [-p]' % sys.argv[0])
        os.abort()
    else:
        if not isfile(sys.argv[1]):
            print("Input file doesn't exist")
            os.abort()

        # Print all pattern offsets
        try:
            sys.argv.index('-p')
            printAll = True
        except ValueError:
            printAll = False


        # Loading FM Index
        print('Creating FM index: ' + str(datetime.datetime.now()))
        start_time = time.time()
        fmInd = fm.FmIndex(sys.argv[1], True)
        end_time = time.time()
        print("FM index created: " + str(datetime.datetime.now()))
        print("Creation time: %.2f seconds" % (end_time-start_time))
       
        # Check Memory
        mem = utils.check_mem()
        print("Used memory: %d MB" % mem)
        print()

        # Search for pattern in sequence
        print('Search started: ' + str(datetime.datetime.now()))
        start_time = time.time()
        result = fmInd.search(sys.argv[2])
        end_time = time.time()
        print("Search finished: " + str(datetime.datetime.now()))
        print("Search time: %.2f seconds" % (end_time-start_time))
      
        # Check Memory
        mem = utils.check_mem()
        print("Used memory: %d MB" % mem)
        print()

        print("Entered pattern occurred %d times in sequence" % len(result))
        if printAll:
            print("Locations:")
            print(sorted(result))
        
if __name__ == '__main__':
    main()