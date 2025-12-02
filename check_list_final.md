# **1. Název práce**

**Analýza sítě 100 nejvýdělečnějších herců a jejich žánrů**

---

# **2. Motivace / Cíl práce**

Cílem práce je analyzovat vztahy mezi 100 nejvýdělečnějšími dosud žijícími herci na základě jejich filmové tvorby, vzájemných spoluprací a preferovaných žánrů. Práce se zaměřuje na určení vzdáleností mezi herci pomocí algoritmů nejkratších cest, identifikaci herců, kteří výrazně propojují ostatní, a zjištění, kteří herci mají v síti největší vliv či nejčastěji spolupracují.

Dále je cílem zjistit, jak se jednotlivé filmové žánry prolínají, které žánry tvoří přirozené mosty mezi ostatními a které mají roli centrálních nebo univerzálních žánrů. Zároveň bude zkoumáno, jak se preference žánrů vyvíjejí v čase a zda existují rozdíly mezi žánry typickými pro mladší a starší herce. Práce využije reálná data z IMDB, což umožní analyzovat skutečné filmové vazby a dlouhodobé trendy.

---

# **3. Popis sítě nebo problému**

Analyzována bude **sociální síť herců**, doplněná o **sémantickou síť žánrů**. Primárním datovým modelem bude **tripartitní graf**, jehož uzly budou představovat:

* dosud žijící nejvýdělečnější herce,
* filmy, ve kterých hráli,
* žánry, do kterých jsou filmy zařazeny.

Hrany budou reprezentovat vztahy:

* *herec–film* (herec hrál ve filmu),
* *film–žánr* (film patří do určitých žánrů).

Z tripartitního grafu budou vytvořeny projekce na:

* **síť herců** (vážené hrany dle počtu sdílených filmů),
* **síť žánrů** (vážené hrany dle počtu filmů kombinujících dané žánry).
* **síť herců a žánrů** (vážené hrany dle počtu filmů majících daný žánr v nichž hraje daný herec)

---

# **4. Zdroje dat**

Data pocházejí z veřejných datasetů IMDB (zejména *name.basics*, *title.basics*, *title.principals*).

Seznam nejvýdělečnějších herců je převzat z žebříčku serveru *The Numbers*:
[https://www.the-numbers.com/box-office-star-records/domestic/lifetime-acting/top-grossing-leading-stars](https://www.the-numbers.com/box-office-star-records/domestic/lifetime-acting/top-grossing-leading-stars).

---

# **5. Plánované metody / přístupy**

* Vytvoření vážené projekce na síť herců podle počtu sdílených filmů.
* Výpočet délek nejkratších cest mezi herci.
* Výpočet stupňové centrality pro identifikaci nejaktivnějších spolupracovníků.
* Výpočet betweenness centrality pro určení herců, kteří propojují ostatní.
* Výpočet closeness centrality pro identifikaci centrálních osobností v síti.
* Vytvoření vážené projekce na síť žánrů podle vzájemných kombinací.
* Rozdělení sítě podle časových období (např. dekády) a jejich porovnání.
* Vytvoření vážené projekce na síť herců a žánrů podle vzájemných kombinací.
* Vizualizace grafů pomocí NetworkX.

Tento seznam kroků není ani kompletní ani nejde nutně za sebou – jednotlivé kroky budou voleny podle potřeby v rámci analýzy.

---

# **6. Očekávaný výsledek / výstup**

Výsledkem budou vizualizace a interpretace klíčových charakteristik sítě:

* zobrazení centrálních a spojovacích herců,
* graf délek nejkratších cest mezi herci,
* vývoj preferovaných žánrů podle věku nebo délky hraní,
* identifikace nejpopulárnějších žánrů v čase,
* určení univerzálních žánrů kombinovatelných s mnoha dalšími,
* vizualizace a interpretace sítě žánrů a jejich vazeb.

---

# **7. Technické prostředky / software**

Python, Jupyter Notebook, NetworkX, Polars (případně pandas), matplotlib, další doplňkové knihovny.

---

# **8. Rozsah (stručně)**

Bude zpracován tripartitní graf obsahující přibližně:

* **100 herců**,
* **3503 filmů**,
* **22 žánrů**,
* celkem **3625 uzlů** a **13242 hran**.

Rozsah byl zvolen tak, aby byl dostatečně komplexní, ale zároveň výpočetně zvládnutelný.

**Kroky:**

* Sběr a filtrace dat – dokončeno, případně dopracováno při chybějících údajích.
* Načtení dat do grafových struktur.
* Analýza těchto struktur a vytváření projekcí.
* Vizualizace a tvorba výstupů (grafy, tabulky, shrnutí).
* Interpretace výsledků a zhodnocení pozorovaných jevů.

---
