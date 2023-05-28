if [ ! -e names.txt ]; then
    echo "Не могу найти файл 'names.txt'"
    exit 1
fi
cat names.txt | awk '{print "Hello, "$1}'