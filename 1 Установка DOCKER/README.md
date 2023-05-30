# 1 Установка Docker - Ubuntu

## 1.1 Добавляем репозиторий докера (чтобы получить последнюю его версию)
```
sudo apt-get update
```

```
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release -y
```

```
sudo mkdir -p /etc/apt/keyrings
```

```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

```
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```


## 1.2 Устанавливаем docker
```
sudo apt-get update
```

```
sudo apt-get install docker-ce docker-ce-cli containerd.io -y
```


## 1.3 Устанавливаем docker-compose

```
sudo curl -L "https://github.com/docker/compose/releases/download/v2.6.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

```
sudo chmod +x /usr/local/bin/docker-compose
```

## 1.4 Проверяем, что всё установилось
```
sudo docker -v
```

```
sudo docker ps
```

```
sudo docker images
```

```
docker-compose -v
```

## 1.5 Запуск докера не из-под суперпользователя

```
sudo groupadd docker
```

```
sudo usermod -aG docker $USER
```

Выйти из сессии. Проверим, что все работает.

```
id -nG
```

```
docker ps
```

```
docker images
```

# 2 Установка Docker - Windows
Установим docker и docker-compose на Windows 10 через WSL2 и Docker Desktop.

## 2.1 Установка WSL
Запустить cmd от имени администратора. Установим платформу виртауальной машины и Ubuntu. После чего перезагрузим ПК.
```
wsl --install
```
После перезагрузки продолжится установка Ubuntu. Если нет, то открыть командную строку в режиме администратора. И ввести:

## 2.2 Установка Ubuntu
```
wsl --install -d Ubuntu
```
и создать пользователя. Теперь увидим Ubuntu:
```
wsl -l -v
```

Чтобы перейти из cmd в Ubuntu, нужно ввести ```wsl```.

## 2.3 Установка Docker Desktop
Перейдите на сайт докера, где предлагают установить его на винду ([Ссылка](https://docs.docker.com/desktop/install/windows-install/)). 

Ознакомьтесь с ним и скачайте установщик Docker Desktop for Windows (файл .exe).

Когда он скачается, нажмите на этот установщик. Обратите внимание, что у вас должна стоять галочка на Use WSL 2 instead of Hyper-V. 

После установки введем команду 

```
wsl -l -v
```

И увидим docker.

Таким образом, теперь мы можем работать с докером через CLI!

Попробуйте в CMD ввести ```wsl``` (вы должны провалиться в убунту), после чего выполнить команды ```docker -v``` и ```docker-compose -v```.

## 2.4. Полезная фишка

В курсе нам нужно будет прокидывать файлы в докер-контейнеры, а также использовать файлы для докер компоуза.

Чтобы попасть в нужную папку, можно в вашей убунте выполнить команду ```explorer.exe .``` ([ссылка](https://superuser.com/questions/1110974/how-to-access-linux-ubuntu-files-from-windows-10-wsl)).

Например, перейдем в Ubuntu ```wsl``` и создадим каталог DOCKERTEST, а затем откроем его в windows:
```
wsl
```

```
mkdir DOCKERTEST
```

```
explorer.exe .
```

## Возможные ошибки в Windows и их устранение
Иногда могут возникнуть ошибки при выполнении ```wsl --install```, с 99% вероятностью они будут устранены после следующих действий:
1. Перейти в **Дополнительные компоненты** (Параметры - Приложения - Дополнительные компоненты - Другие компоненты (в самом низу))
2. Установить: Hyper-V, контейнеры, платформа виртуальной машины, подсистема Windows для Linux
3. Включить виртуализацию в BIOS
4. В антивирусе включить (Управление приложениями и бразуером - Параметры защиты от эксплойтов - Параметры программы - Добавить программу - Выбрать точный путь). Указать путь **C:\Windows\System32\vmcompute.exe**. Для этой  программы  в защите управления потока (CFG) поставить галочку **Переопределить системные параметры** и переключить на **ВКЛ**.
5. Перезапустить ПК
6. Удалить Ubuntu в списке приложений, можно также (```wsl --unregister Ubuntu```)
7. Выполнить установку с самого начала.



