#!/bin/bash

if [ ! -d "venv" ]; then
  echo "Criando ambiente virtual..."
  python3 -m venv venv
fi

source venv/bin/activate

echo "Instalando dependências..."
pip install -r requirements.txt

echo "Iniciando aplicação em segundo plano..."

nohup python3 app.py &

echo "A aplicação está rodando em segundo plano."
