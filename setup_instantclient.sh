#!/bin/bash
# Criar pasta para o Instant Client
mkdir -p instantclient

# Baixar o pacote oficial da Oracle (Linux x86-64, versão 19.22)
curl -o instantclient.zip https://download.oracle.com/otn_software/linux/instantclient/instantclient-basic-linux.x64-19.22.zip

# Extrair o conteúdo
unzip -o instantclient.zip -d instantclient

# Remover o arquivo zip para economizar espaço
rm instantclient.zip

