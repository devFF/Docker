name=$1
len=${#name}
first_letter=${name::1}
rest_letters=${name:1:len}
if [ -z "$name" ]; then
    echo "Нужно ввести аргумент"
    exit 1
else
  echo "Hello, ${first_letter^}${rest_letters,,} :)"
fi
