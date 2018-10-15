#!/bin/bash
rm -rf ips
rm -rf mail
rm -rf domain
rm -rf *.txt
#echo "pls input domain name,like:sina.com"
#read domain
domain=$1

mkdir report/$domain

cd ./subDomainsBrute
#不使用&&，保证路径正确
python subDomainsBrute.py $domain -o ../report/$domain/1$domain.txt

cd ../Sublist3r
python sublist3r.py -d $domain -o ../report/$domain/2$domain.txt

cd ../teemo
python teemo.py -d $domain -o ../../report/$domain/3$domain.txt

cd ../GSDF
python GSDFT.py -d $domain -s ../report/$domain/4$domain.txt -e show

cd ../DiscoverSubdomain
python DiscoverSubdomain.py -d $domain -o ../report/$domain/5$domain.txt
#已经进去一层了
#cp $domain*.txt ../5$domain.txt

cd ../hellfarm
python hellfarm.py -d $domain -o ../report/$domain/6$domain.txt
#python search_engine_spider.py -d $domain -o ../../6$domain.txt

#这样是根目录，得换下
#cd ..

#切换到子域名目录
cd ../report/$domain/

cat 3*.txt 5*.txt 6*.txt|grep @ >> mail
#cat 6*.txt |grep -v @| grep -v / >>a.txt
cat 1*.txt |awk '{print($1)}'>> a.txt
cat 1*.txt |sed 's/,//g'|awk '{print($2)}'>> b.txt
cat 4*.txt | grep -v "\[" | sed 's/\*\.//g'>> a.txt
cat 2*.txt >> a.txt

cat b.txt|while read ip
do
#need install ipcalc
ipcalc -n $ip/28 |grep Network |awk '{print ($2)}'>> ips.txt
done

cat 6*.txt | grep "[0-9]\{1,3\}[.][0-9]\{1,3\}[.][0-9]\{1,3\}[.][0-9]\{1,3\}" >> ips.txt
cat 6*.txt | grep / >> ips.txt
cat 3*.txt |grep / >> ips.txt

cat ips.txt|sort|uniq >> ips

cat 6*.txt |grep -v @|grep -v / >> a.txt
cat 3*.txt |grep -v @|grep -v / |awk '{print($1)}' |grep -v ^[0-9]>>a.txt
cat 5*.txt >>a.txt

#make sure domain write won't be a repeat result, and result will be the same as the past
cat a.txt|sort|uniq|grep $domain  >> $domain.txt
cp $domain.txt domain

rm -rf *.txt
echo "IP段计算完毕，请查看ips文件"
echo "邮箱计算完毕，请查看mail文件"
echo "域名计算完毕，请查看domain文件"

cp domain ../../domain
cp ips ../../ips
cp mail ../../mail

cd ../../

