#!/usr/bin/env bash

export HADOOP_HOME=/home/szolek/hadoop
export HERE=`pwd`

if [ $# = "1" ] && [ $1 = "-c" ]
then
echo Clean
$HADOOP_HOME/bin/hadoop dfs -rmr testData
$HADOOP_HOME/bin/hadoop dfs -rmr testData-output
else
echo Test
$HADOOP_HOME/bin/hadoop dfs -copyFromLocal $HERE/testData.txt testData
$HADOOP_HOME/bin/hadoop jar 
$HADOOP_HOME/contrib/streaming/hadoop-streaming-1.0.0.jar -file 
$HERE/map.py -mapper $HERE/map.py -file $HERE/reduce.py -reducer 
$HERE/reduce.py -input testData -output testData-output
$HADOOP_HOME/bin/hadoop dfs -cat testData-output/part-00000
fi

