# BWT and FM index
Implementirati na programskom jeziku Python algoritam za indeksirano pretraživanje stringova u zatadom tekstu koristeći Burrows-Wheeler transformaciju i FM index.

Inicijalna verzija algoritma treba da bude realizovana na tradicionalan način opisan na predavanju, bez optimizicije memorije i vremena izvršavanja (10 poena).

Za svaku od funkcija u kodu, kao i za sam finalni algoritam napisati testove (5 poena).

Izvršiti optimizaciju koda iz aspekta zauzeća memorije i vremena izvršavanja. Pokrenuti prethodno definisane testove i proveriti da li i dalje svi prolaze (regresiono testiranje). Izmeriti unapređenje zauzeća memorije i vremena izvršavanja koristeći kao test podatke 3 seta (10 poena):
  1. Tekst: Coffea arabica, Chromosome 1c i paterni: ATGCATG, TCTCTCTA, TTCACTACTCTCA
  2. Tekst: Mus pahari chromosome X, i paterni: ATGATG, CTCTCTA, TCACTACTCTCA
  3. Genom po slobodnom izboru iz NIH baze i proizvoljna 3 paterna različite dužine.
  
Pripremiti prezentaciju (Google slides ili power point) inicijalnog i optimizovanog algoritma, kao i samih rezultata (5 poena).
Pripremiti video prezentaciju projekta (3 - 5 minuta trajanja) koja će biti dostupna na YouTube ili drugom on-line video servisu (10 poena).

## Kako pokrenuti

### Konvertor fasta gzip fajla za sais C:
    python3 converter.py INPUT_FILE(*.fa.gz) OUTPUT_FILE

  INPUT_FILE(\*.fa.gz) - ulazni fajl u fasta formatu kompresovan gzip algoritmom (*Napomena:* U fajlu će se posmatrati samo prva sekvenca, ostale, ukoliko ih je više, će se ignorisati).
  
  OUTPUT_FILE - Izlazni fajl koji se koristi u sais C-u.
  
  Primeri:
  
    python3 converter.py "Coffea arabica, chromosome 1c.fa.gz" "Coffea arabica.seq"
    
### Kreiranje sufiksnog niza
    suffix_array_sais.exe INPUT_FILE [OUTPUT_FILE]
    
  INPUT_FILE - ulazni fajl (izlazni fajl converter.py)
  
  OUTPUT_FILE (opcioni argument) - izlazni fajl koji sadrži sufiksni niz (opcioni ulaz fm_build.py)
  
  Primeri:
  
    suffix_array_sais.exe "Coffea arabica.seq" "Coffea arabica.sa"

### Pravljenje FM Indexa:
    python3 fm_build.py SEQUENCE_INPUT_FILE(*.fa.gz) [-sa SA_INPUT_FILE] [-cps CPS_SAMPLE] [-ssa SSA_SAMPLE] OUTPUT_FILE

  SEQUENCE_INPUT_FILE(\*.fa.gz) - ulazni fajl u fasta formatu kompresovan gzip algoritmom (*Napomena:* U fajlu će se posmatrati samo prva sekvenca, ostale, ukoliko ih je više, će se ignorisati).
  
  -sa SA_INPUT_FILE (opcioni argument) - Ulazni fajl koji sadrži sufiksni niz (izlaz sais C algoritma). Ukoliko nije naveden kreira se unapređenom verzijom Python algoritma.
  
  -cps CPS_SAMPLE (opcioni argument) - Ceo broj kojim će se sample-ovati checkpoint niz. Podrazumevana vrednost je 128
  
  -ssa SSA_SAMPLE (opcioni argument) - Ceo broj kojim će se sample-ovati sufiksni niz. Podrazumevana vrednost je 32
  
  OUTPUT_FILE - Izlazni fajl u koji će se sačuvati FM Index za dalju upotrebu.
  
  Primeri:
  
    python3 fm_build.py "Coffea arabica, chromosome 1c.fa.gz" -sa "Coffea arabica.sa" -cps 64 -ssa 64 "Coffea arabica.fm"
  
    python3 fm_build.py "Coffea arabica, chromosome 1c.fa.gz" -cps 64 "Coffea arabica.fm"
  
    python3 fm_build.py "Coffea arabica, chromosome 1c.fa.gz" "Coffea arabica.fm"
  
### Pretraga FM Indexa:
    python3 fm_search.py FM_INPUT_FILE PATTERN [-p]

  FM_INPUT_FILE - ulazni fajl koji sadrži FM Index strukturu (izlazni fajl fm_build.py).
  
  PATTERN - patern koji će se tražiti u ulaznoj sekvenci.
  
  -p (opcioni argument) - Ukoliko je naveden ispisaće se i sve lokacije na kojima je pronađen patern.
  
  Primeri:
  
    python3 fm_search.py "Podarcis muralis.fm" ACGTACGT -p

    python3 fm_search.py "Podarcis muralis.fm" ACGTACGT
    
### Pokretanje unit testova:
    python3 tests.py

## FM Index fajlovi

https://tinyurl.com/fm-index-files

## Video prezentacija

https://www.youtube.com/watch?v=bepB7Xqz96Q&feature=youtu.be
