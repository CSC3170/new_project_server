# syntax=docker/dockerfile:1


FROM greyltc/archlinux-aur:latest AS base

RUN echo 'Server = https://opentuna.cn/archlinux/$repo/os/$arch' > /etc/pacman.d/mirrorlist
RUN pacman -Syu --noconfirm


FROM base AS dev-frontend

RUN pacman -S --noconfirm nodejs yarn
RUN yarn config set registry https://registry.npmmirror.com

WORKDIR /new_project_server/frontend
ENTRYPOINT yarn && \
    yarn install && \
    yarn watch


FROM base AS dev-backend

RUN pacman -S --noconfirm python python-poetry
RUN poetry config virtualenvs.in-project true

WORKDIR /new_project_server/backend
ENTRYPOINT poetry lock && \
    poetry install && \
    poetry run watch


FROM base AS prod-frontend

RUN pacman -S --noconfirm nodejs yarn
RUN yarn config set registry https://registry.npmmirror.com

WORKDIR /new_project_server/frontend
ENTRYPOINT yarn && \
    yarn install && \
    yarn build


FROM base AS prod-backend

RUN pacman -S --noconfirm python python-poetry
RUN poetry config virtualenvs.in-project true

WORKDIR /new_project_server/backend
ENTRYPOINT poetry lock && \
    poetry install && \
    poetry run watch


FROM base AS vscode

RUN pacman -S --noconfirm git python python-poetry nodejs yarn
RUN poetry config virtualenvs.in-project true
RUN yarn config set registry https://registry.npmmirror.com
RUN aur-install code-server
      
ENTRYPOINT aur-install code-server && \
    code-server --host 0.0.0.0 --auth none
