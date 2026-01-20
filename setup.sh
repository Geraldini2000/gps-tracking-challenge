#!/bin/bash

echo "🚀 Iniciando setup do GPS Tracking System"

# Instalar dependências
echo "📦 Instalando dependências..."
pip install -r requirements.txt

# Iniciar PostgreSQL via Docker
echo "🐳 Iniciando PostgreSQL..."
docker-compose up -d postgres

# Aguardar PostgreSQL iniciar
echo "⏳ Aguardando PostgreSQL iniciar..."
sleep 5

# Executar migrações
echo "🔄 Executando migrações do banco de dados..."
cd api
python manage.py makemigrations
python manage.py migrate

# Criar superusuário (opcional)
echo "👤 Deseja criar um superusuário? (s/n)"
read -r response
if [[ "$response" == "s" ]]; then
    python manage.py createsuperuser
fi

echo "✅ Setup concluído!"
echo ""
echo "Para iniciar os serviços:"
echo "  Terminal 1: python -m tcp_gateway.server"
echo "  Terminal 2: cd api && python manage.py runserver"
echo ""
echo "Ou use Docker:"
echo "  docker-compose up --build"
