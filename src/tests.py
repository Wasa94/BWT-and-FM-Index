import fm
#import initial as fm

def main():
    assert fm.suffix_array('') == []
    assert fm.suffix_array('$') == [0]
    assert fm.suffix_array('ABAABA') == [5, 2, 3, 0, 4, 1]
    assert fm.suffix_array('BANANA') == [5, 3, 1, 0, 4, 2]

    assert fm.bwt('') == ''
    assert fm.bwt('$') == '$'
    assert fm.bwt('ABAABA$') == 'ABBA$AA'
    assert fm.bwt('BANANA$') == 'ANNB$AA'

    fmInd = fm.FmIndex('ABAABA')

    assert fmInd.has_substring('') == True
    assert fmInd.has_substring('A') == True
    assert fmInd.has_substring('B') == True
    assert fmInd.has_substring('ABAABA') == True
    assert fmInd.has_substring('BB') == False

    assert fmInd.has_suffix('') == True
    assert fmInd.has_suffix('A') == True
    assert fmInd.has_suffix('ABAABA') == True
    assert fmInd.has_suffix('B') == False
    assert fmInd.has_suffix('BB') == False

    assert sorted(fmInd.search('')) == [i for i in range(0, 7)]
    assert sorted(fmInd.search('A')) == [0, 2, 3, 5]
    assert sorted(fmInd.search('ABA')) == [0, 3]
    assert sorted(fmInd.search('ABAABA')) == [0]
    assert sorted(fmInd.search('BB')) == []

if __name__ == '__main__':
    main()