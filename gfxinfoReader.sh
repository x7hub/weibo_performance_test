#! /bin/sh

#if [ ! -s ~/bin/python ]
#then
#    mkdir ~/bin
#    ln -s /usr/bin/python2 ~/bin/python
#    ln -s /usr/bin/python2-config ~/bin/python-config
#fi
#export PATH=~/bin:$PATH

adb shell dumpsys gfxinfo com.sina.weibo | sed -n '/Draw\tProcess\tExecute/,/View hierarchy:/p'| tee gfxinfo.cvs | grep [0-9] | awk '{printf("%02d %s\n", NR, $0)}' > gfxinfoSum.cvs

#if [ ! -s gfxinfoSum.cvs ]
#then
#    echo "empty file"
#    exit
#fi

cat << EOF | gnuplot
set title "gfxinfo"
set terminal png truecolor
set output "gfxinfo.png"
set term pngcairo size 1600,1200
set grid
set auto x
unset xtics
set xtics nomirror rotate by -45 scale 0 font ",8"
set style data histogram
set style histogram rowstacked
set style fill solid border -1
plot "gfxinfoSum.cvs" using 2:xtic(1) title 'Draw', '' using 3 title 'Process', '' using 4 title 'Execute'
EOF

ristretto gfxinfo.png
