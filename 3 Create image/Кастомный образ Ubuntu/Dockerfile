FROM ubuntu:20.04

RUN apt-get update && apt-get install -y nano wget curl git

WORKDIR /home/igor

COPY random_file.txt random_file.txt

# Изменим интерфейс терминала в контейнере
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.5/zsh-in-docker.sh)" -- \
    -t robbyrussell \
    -p https://github.com/zsh-users/zsh-autosuggestions

ENV ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE="fg=#dedede,bg=#9c9c9c,bold,underline"

# Запустим оболочку
#CMD [ "zsh" ]
ENTRYPOINT [ "zsh" ]




