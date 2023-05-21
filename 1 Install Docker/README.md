# Установка Docker

## 1) Добавляем репозиторий докера (чтобы получить последнюю его версию)
```
sudo apt-get update
```

```sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release -y
```
    
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

```
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```


## 2) Устанавливаем docker
```
sudo apt-get update
```

```
sudo apt-get install docker-ce docker-ce-cli containerd.io -y
```


## 3) Устанавливаем docker-compose

```
sudo curl -L "https://github.com/docker/compose/releases/download/v2.6.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

```
sudo chmod +x /usr/local/bin/docker-compose
```

## 4) Проверяем, что всё установилось
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

## 5) Запуск докера не из-под суперпользователя

```
sudo groupadd docker
```

```
sudo usermod -aG docker $USER
```

Проверим, что все работает.

```
id -nG
```

```
docker ps
```

```
docker images
```