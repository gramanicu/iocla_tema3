# IOCLA Tema 3

## Exercitiul 1

O posibila vulnerabilitate este legata de buffer overflow. La adresa 0x8048663 din cod , unde se afla un "entry point" in functia "print_flag" (care are mai multe entry point-uri), se aloca spatiu pe stiva pentru a citi un string de la tastatura. Spatiul alocat pe stiva este mult mai mic decat cel ce poate fi citit de la tastatura. Putem folosi astfel un string mai mare pentru a genera un buffer overflow si sa alteram control flow-ul programului, deoarece, dupa citirea sirului de caractere, de pe stiva se incarca in $eax o adresa, unde va sari executia programului (call eax)

Provocand un buffer overflow, putem incarca o alta valoare in $eax, de pe stiva, si astfel, sa sarim cu executia programului la o adresa aleasa de noi.

Adresa entry point-ului : 0x8048663 (unde incep problemele)

## Exercitiul 2

In urma analizarii executabilului (cu ajutorul gdb si afl-fuzz) am determinat lungimea minima a unui string/payload ca fiind de 1118 caractere (1117 caractere se incadreaza in limite). Urmatoarele 4 caractere din payload sunt incarcate in registrul eax (ca pointer), si apoi se executia programului sare la acel pointer.

EIP - 0x804867e
START - 0xffffceb2
END - 0xffffcfb2