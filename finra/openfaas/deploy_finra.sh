funcs=("marketdata" "lastpx" "side" "trddate" "volume" "margin-balance" "yfinance")
for ((i=0;i<7;i++))
do
    faashwh-cli build -f ${funcs[$i]}.yml
done

for ((i=0;i<7;i++))
do
    faashwh-cli deploy -f ${funcs[$i]}.yml
done
