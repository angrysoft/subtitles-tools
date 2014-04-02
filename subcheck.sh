#!/bin/sh

while getopts ":f:" opt
do
    case $opt in 
        f)FPS=$OPTARG;shift 2;;
        \?)echo "Invalid option: -$OPTARG" >&2
           exit 1
           ;;
        :)echo "Option -$OPTARG requires an argument." >&2
          exit 1
          ;;
    esac
done

IFS=":"
for x in $(echo $@ | sed 's/\.txt /\.txt:/g')
do
    case "$x" in
        *.txt)grep -H "^\[" "$x" >/dev/null || continue
              echo "Convertig subtitle $x"
              if [ "$FPS" == "" ];then
                  subconverter.py "$x"
              else
                  subconverter.py -f $FPS "$x"
              fi
              mv "${x%.txt}.sub" "$x"
              ;;
    esac
done


