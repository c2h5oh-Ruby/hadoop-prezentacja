Przykłady
=============

Map reduce
----------

* Pythonowe skrypty map-reduce do odpalenia na hadoopie poprzez skrypt 
test.sh

* Działanie skryptów można zaobserwować bez użycia hadoopa pisząc

```sh
cat testData.txt | ./map.py | reduce.py
```

* Dane testowe są malutkie, rekomendujemy ściągnięcie ich np. ze stron 
podanych w readme instalacji.

* Skrypt test.sh robi właściwie wszystko za nas, nie musimy martwić się 
kopiowaniem danych testowych do HDFS i późniejszym szukaniem wyniku.

* Przykładowy wordcount w javie: 
[klik](http://wiki.apache.org/hadoop/WordCount)
