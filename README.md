Hadoop
===============

* Apache hadoop jest frameworkiem do odpalania aplikacji na klastrach. Zapewnia on niezawodność i przenośność danych. Działanie hadoopa oparte jest na 
paradygmacie map-reduce, gdzie obliczenia są podzielone na części, z których każda może być obliczona na oddzielnym węźle w klastrze. Dodatkowo posiada on 
własny rozproszony system plików (HDFS). Zapewnia on doskonałą komunikację i wymianę danych w klastrze. Co więcej, błędy i problemy z węzłami są 
rozwiązywane przez framework.

Instalacja Hadoop'a
===================

single-instance
--------------
* wymagania wstępne: do dzialania hadoop wymaga dzialajacej Javy co najmniej w wersji 1.5.x, zaleca sie używanie Javy w wersji 1.6.x.
Żeby hadoop działał, musimy także mieć skonfigurowane SSH do łączenia się z klastrem:
* Generowanie kluczy

```sh
ssh-keygen -t rsa -P ""
```

```/sh
cat $HOME/.ssh/id_rsa.pub >> $HOME/.ssh/authorized_keys.
```

Udane połączenie wygląda np. tak:

```sh
hduser@ubuntu:~$ ssh localhost
The authenticity of host 'localhost (::1)' can't be established.
RSA key fingerprint is d7:87:25:47:ae:02:00:eb:1d:75:4f:bb:44:f9:36:26.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'localhost' (RSA) to the list of known hosts.
Linux ubuntu 2.6.32-22-generic #33-Ubuntu SMP Wed Apr 28 13:27:30 UTC 2010 i686 GNU/Linux
Ubuntu 10.04 LTS
[...snipp...]
hduser@ubuntu:~$
```
* uwaga! wszystkie przykłady pokazane są dla użytkownika hduser!

* z tego powodu musimy kontrolować nazwy folderów i inne ścieżki, da się to wyłapać obserwując błędy

* ściągamy hadoop ze [strony](http://hadoop.apache.org/common/releases.html) fundacji apache (w momencie pisania tego tekstu stabilne wydanie to 1.0.0)

* rozpakowujemy archiwum z hadoop'em

* update pliku $HOME/.bashrc

```sh
# Set Hadoop-related environment variables
export HADOOP_HOME=/usr/local/hadoop

# Set JAVA_HOME (we will also configure JAVA_HOME directly for Hadoop later on)
export JAVA_HOME=/usr/lib/jvm/java-6-sun

# Some convenient aliases and functions for running Hadoop-related commands
unalias fs &> /dev/null
alias fs="hadoop fs"
unalias hls &> /dev/null
alias hls="fs -ls"

# If you have LZO compression enabled in your Hadoop cluster and
# compress job outputs with LZOP (not covered in this tutorial):
# Conveniently inspect an LZOP compressed file from the command
# line; run via:
#
# $ lzohead /hdfs/path/to/lzop/compressed/file.lzo
#
# Requires installed 'lzop' command.
#
lzohead () {
    hadoop fs -cat $1 | lzop -dc | head -1000 | less
}

# Add Hadoop bin/ directory to PATH
export PATH=$PATH:$HADOOP_HOME/bin
```

* wchodzimy do katalogu głównego hadoopa. W pliku /conf/hadoop-env.sh w miejscu

```sh
# The java implementation to use.  Required.
# export JAVA_HOME=/usr/lib/j2sdk1.5-sun
```
odkomentowujemy drugą linijkę i zmieniamy ścieżkę do swojej instalacji javy, np na sigmie:

```sh
export JAVA_HOME=/usr/lib/jvm/java
```

* w folderze /conf/ znajdują się pliki konfiguracyjne. Na potrzeby konfiguracji tworzymy foldery:

```sh
$ sudo mkdir -p /app/hadoop/tmp
$ sudo chown hduser:hadoop /app/hadoop/tmp
# ...and if you want to tighten up security, chmod from 755 to 750...
$ sudo chmod 750 /app/hadoop/tmp
```

* w pliku conf/core-site.xml:

```sh
<!-- In: conf/core-site.xml -->
<property>
  <name>hadoop.tmp.dir</name>
  <value>/app/hadoop/tmp</value>
  <description>A base for other temporary directories.</description>
</property>

<property>
  <name>fs.default.name</name>
  <value>hdfs://localhost:54310</value>
  <description>The name of the default file system.  A URI whose
  scheme and authority determine the FileSystem implementation.  The
  uri's scheme determines the config property (fs.SCHEME.impl) naming
  the FileSystem implementation class.  The uri's authority is used to
  determine the host, port, etc. for a filesystem.</description>
</property>
```

* w pliku conf/mapred-site.xml:

```sh
<!-- In: conf/mapred-site.xml -->
<property>
  <name>mapred.job.tracker</name>
  <value>localhost:54311</value>
  <description>The host and port that the MapReduce job tracker runs
  at.  If "local", then jobs are run in-process as a single map
  and reduce task.
  </description>
</property>
```

* w pliku  conf/hdfs-site.xml:

```sh
<!-- In: conf/hdfs-site.xml -->
<property>
  <name>dfs.replication</name>
  <value>1</value>
  <description>Default block replication.
  The actual number of replications can be specified when the file is created.
  The default is used if replication is not specified in create time.
  </description>
</property>
```

* porty ustawiamy na jakieś wolne!

* formatujemy system plików (jesteśmy w folderze hadoopa):

```sh
/bin/hadoop namenode -format
```

* przykładowy output:

```sh
hduser@ubuntu:/usr/local/hadoop$ bin/hadoop namenode -format
10/05/08 16:59:56 INFO namenode.NameNode: STARTUP_MSG:
/************************************************************
STARTUP_MSG: Starting NameNode
STARTUP_MSG:   host = ubuntu/127.0.1.1
STARTUP_MSG:   args = [-format]
STARTUP_MSG:   version = 0.20.2
STARTUP_MSG:   build = https://svn.apache.org/repos/asf/hadoop/common/branches/branch-0.20 -r 911707; compiled by 'chrisdo' on Fri Feb 19 08:07:34 UTC 2010
************************************************************/
10/05/08 16:59:56 INFO namenode.FSNamesystem: fsOwner=hduser,hadoop
10/05/08 16:59:56 INFO namenode.FSNamesystem: supergroup=supergroup
10/05/08 16:59:56 INFO namenode.FSNamesystem: isPermissionEnabled=true
10/05/08 16:59:56 INFO common.Storage: Image file of size 96 saved in 0 seconds.
10/05/08 16:59:57 INFO common.Storage: Storage directory .../hadoop-hduser/dfs/name has been successfully formatted.
10/05/08 16:59:57 INFO namenode.NameNode: SHUTDOWN_MSG:
/************************************************************
SHUTDOWN_MSG: Shutting down NameNode at ubuntu/127.0.1.1
************************************************************/
hduser@ubuntu:/usr/local/hadoop$
```

* teraz możemy odpalić hadoopa

```sh
/bin/start-all.sh
```

* Żeby zobaczyć co działa, możemy wpisać 

```sh
hduser@ubuntu:/usr/local/hadoop$ jps
2287 TaskTracker
2149 JobTracker
1938 DataNode
2085 SecondaryNameNode
2349 Jps
1788 NameNode
```

* Nie zrażamy się, jeżeli coś jest nie tak. W katalogu logs możemy podejrzeć logi i błędy w uruchomieniu. Ich rozwiązania łatwo znaleść w internecie.

* Żeby zatrzymać klaster:

```sh
/bin/stop-all.sh
```

* Przykładowy output:

```sh
hduser@ubuntu:/usr/local/hadoop$ bin/stop-all.sh
stopping jobtracker
localhost: stopping tasktracker
stopping namenode
localhost: stopping datanode
localhost: stopping secondarynamenode
hduser@ubuntu:/usr/local/hadoop$
```


testowanie
--------------

* ściągamy jakiegoś ebooka, na przykład z tych stron:
[1](http://www.gutenberg.org/etext/20417)
[2](http://www.gutenberg.org/etext/5000)
[3](http://www.gutenberg.org/etext/4300)
na przykład do folderu /tmp/gutenberg. Pamiętamy, aby była to wersja tekstowa UTF-8.

```sh
hduser@ubuntu:~$ ls -l /tmp/gutenberg/
total 3604
-rw-r--r-- 1 hduser hadoop  674566 Feb  3 10:17 pg20417.txt
-rw-r--r-- 1 hduser hadoop 1573112 Feb  3 10:18 pg4300.txt
-rw-r--r-- 1 hduser hadoop 1423801 Feb  3 10:18 pg5000.txt
hduser@ubuntu:~$
```

* Żeby móc skorzystać z tych plików, musimy je skopiować do Hadoopowego HDFS:

```sh
hduser@ubuntu:/usr/local/hadoop$ bin/hadoop dfs -copyFromLocal /tmp/gutenberg /user/hduser/gutenberg
hduser@ubuntu:/usr/local/hadoop$ bin/hadoop dfs -ls /user/hduser
Found 1 items
drwxr-xr-x   - hduser supergroup          0 2010-05-08 17:40 /user/hduser/gutenberg
hduser@ubuntu:/usr/local/hadoop$ bin/hadoop dfs -ls /user/hduser/gutenberg
Found 3 items
-rw-r--r--   3 hduser supergroup     674566 2011-03-10 11:38 /user/hduser/gutenberg/pg20417.txt
-rw-r--r--   3 hduser supergroup    1573112 2011-03-10 11:38 /user/hduser/gutenberg/pg4300.txt
-rw-r--r--   3 hduser supergroup    1423801 2011-03-10 11:38 /user/hduser/gutenberg/pg5000.txt
hduser@ubuntu:/usr/local/hadoop$
```

* Teraz odpalamy przykład map-reduce, który liczy ile razy dane słowo wystepuje w tekstach.

```sh
hduser@ubuntu:/usr/local/hadoop$ bin/hadoop jar hadoop*examples*.jar wordcount /user/hduser/
```

* Komenda ta czyta wszystkie pliki z katalogu np.  /user/hduser/gutenberg, przetwarza je i wynik składuje w katalogu HDFS np. /user/hduser/gutenberg-output.

* Przykładowe działanie map-reduce na konsoli:

```sh
hduser@ubuntu:/usr/local/hadoop$ bin/hadoop jar hadoop*examples*.jar wordcount /user/hduser/gutenberg /user/hduser/gutenberg-output
10/05/08 17:43:00 INFO input.FileInputFormat: Total input paths to process : 3
10/05/08 17:43:01 INFO mapred.JobClient: Running job: job_201005081732_0001
10/05/08 17:43:02 INFO mapred.JobClient:  map 0% reduce 0%
10/05/08 17:43:14 INFO mapred.JobClient:  map 66% reduce 0%
10/05/08 17:43:17 INFO mapred.JobClient:  map 100% reduce 0%
10/05/08 17:43:26 INFO mapred.JobClient:  map 100% reduce 100%
10/05/08 17:43:28 INFO mapred.JobClient: Job complete: job_201005081732_0001
10/05/08 17:43:28 INFO mapred.JobClient: Counters: 17
10/05/08 17:43:28 INFO mapred.JobClient:   Job Counters
10/05/08 17:43:28 INFO mapred.JobClient:     Launched reduce tasks=1
10/05/08 17:43:28 INFO mapred.JobClient:     Launched map tasks=3
10/05/08 17:43:28 INFO mapred.JobClient:     Data-local map tasks=3
10/05/08 17:43:28 INFO mapred.JobClient:   FileSystemCounters
10/05/08 17:43:28 INFO mapred.JobClient:     FILE_BYTES_READ=2214026
10/05/08 17:43:28 INFO mapred.JobClient:     HDFS_BYTES_READ=3639512
10/05/08 17:43:28 INFO mapred.JobClient:     FILE_BYTES_WRITTEN=3687918
10/05/08 17:43:28 INFO mapred.JobClient:     HDFS_BYTES_WRITTEN=880330
10/05/08 17:43:28 INFO mapred.JobClient:   Map-Reduce Framework
10/05/08 17:43:28 INFO mapred.JobClient:     Reduce input groups=82290
10/05/08 17:43:28 INFO mapred.JobClient:     Combine output records=102286
10/05/08 17:43:28 INFO mapred.JobClient:     Map input records=77934
10/05/08 17:43:28 INFO mapred.JobClient:     Reduce shuffle bytes=1473796
10/05/08 17:43:28 INFO mapred.JobClient:     Reduce output records=82290
10/05/08 17:43:28 INFO mapred.JobClient:     Spilled Records=255874
10/05/08 17:43:28 INFO mapred.JobClient:     Map output bytes=6076267
10/05/08 17:43:28 INFO mapred.JobClient:     Combine input records=629187
10/05/08 17:43:28 INFO mapred.JobClient:     Map output records=629187
10/05/08 17:43:28 INFO mapred.JobClient:     Reduce input records=102286
```

* Przeglądamy katalog outputu, np. /user/hduser/gutenberg-output, aby znaleść wyniki.

* Aby odczytać wyniki:

```sh
hduser@ubuntu:/usr/local/hadoop$ bin/hadoop dfs -cat /user/hduser/gutenberg-output/part-r-00000
```

przydatne interfejsy:
---------------

* http://localhost:50030/ – webowy UI dla job trackera

* http://localhost:50060/ – webowy UI dla task tracera

* http://localhost:50070/ – webowy UI dla HDFS name node

* Dzięki tym interfejsom możemy przyjrzeć się działaniu klastra, jak i stwierdzić, czy w ogóle się odpalił

* Na podstawie 
[strony](http://www.michael-noll.com/tutorials/running-hadoop-on-ubuntu-linux-single-node-cluster/)

* Instalacja kilku klastrów na 
[stronie](http://www.michael-noll.com/tutorials/running-hadoop-on-ubuntu-linux-multi-node-cluster/)

## Użyteczne linki

* [Hadoop deep dive: How it enables big data processing](http://h30458.www3.hp.com/us/us/ent/1191327.html)
* [Kto używa hadoop'a?](http://wiki.apache.org/hadoop/PoweredBy)
* [Strona projektu hadoop](http://hadoop.apache.org/)
