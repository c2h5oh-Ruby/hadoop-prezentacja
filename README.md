Instalacja Hadoop'a
===================

single-instance
--------------
* wymagania wstępne: do dzialania hadoop wymaga dzialajacej Javy co najmniej w wersji 1.5.x, zaleca sie używanie Javy w wersji 1.6.x.
Żeby hadoop działał, musimy także mieć skonfigurowane SSH.
> cat $HOME/.ssh/id_rsa.pub >> $HOME/.ssh/authorized_keys.
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

* ściągamy hadoop ze [strony](http://hadoop.apache.org/common/releases.html) fundacji apache (w momencie pisania tego tekstu stabilne wydanie to 0.21.0)
