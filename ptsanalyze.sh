#!/bin/bash
if [ "$1" = "" ]; then echo "$0 file.pts [startframe]"; exit; fi
if [ "$2" = "" ]; then stf=0; else stf=$2; fi

echo "creating tstamps.csv"
(
read -r line
read -r line
o=$((`echo $line | sed "s/\.//g"`))
echo ",$o"
while read -r line
do
  u=$((`echo $line | sed "s/\.//g"`))
  echo $(($u - $o)),$u
  o=$u
done
) <$1 >tstamps.csv

us=`cut -f1 -d, tstamps.csv | sort -n | uniq -c | sort -n | tail -1 | cut -b9-`
l=$((`wc --lines tstamps.csv | cut -f1 -d\ ` - $stf))
fps=$((1000000 / $us)) 
echo -e "$l frames were captured\nmajority framerate ${fps}fps" 
stf=$(($stf + 1 + 3))

echo "  frame delta time[us] distribution"
tail -n +$stf tstamps.csv | cut -f1 -d, | sort -n | uniq -c

D=`echo "0123456789" | sed "s/\`echo $((1000000/$fps)) | cut -b1\`//"`

echo "> after skip frame indices (middle column)"
tail -n +$stf tstamps.csv | grep "^[$D]" | sed "s/^/> /"

skips=`tail tstamps.csv -n +$stf | grep "^[$D]" | wc --lines | cut -f1 -d\ `
stamps=`tail tstamps.csv -n +$stf | wc --lines | cut -f1 -d\ `
per=`expr \( 100 \* $skips \) / \( $skips + $stamps \)`
echo "$skips frame skips ($per%)"

fst=`head -1 tstamps.csv | cut -f2 -d,`
lst=`tail -1 tstamps.csv | cut -f2 -d,`
dif=`expr $lst - $fst`
dif2=`expr $dif / 2`
avg=`expr \( 1000000 \* \( $l - 1 \) + $dif2 \) / $dif`
echo "average framerate ${avg}fps"