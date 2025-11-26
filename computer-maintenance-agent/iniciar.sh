#!/bin/bash
# Agente de Manutenção de Computadores - Script de Inicialização (Linux/Mac)

echo ""
echo "====================================="
echo "Agente de Manutenção de Computadores"
echo "====================================="
echo ""

# Verificar se estamos no diretório correto
if [ ! -f "backend/app.py" ]; then
    echo "Erro: Arquivo backend/app.py não encontrado!"
    echo "Execute este script do diretório raiz do projeto."
    exit 1
fi

echo "Iniciando aplicação..."
echo ""

# Iniciar backend em background
echo "Iniciando servidor backend na porta 5000..."
cd backend
python app.py &
BACKEND_PID=$!
cd ..

# Aguardar um pouco para o backend iniciar
sleep 3

# Abrir frontend no navegador
echo "Abrindo interface web no navegador..."
if command -v xdg-open &> /dev/null; then
    xdg-open "frontend/index.html"
elif command -v open &> /dev/null; then
    open "frontend/index.html"
else
    echo "Por favor, abra frontend/index.html no seu navegador"
fi

echo ""
echo "====================================="
echo "Aplicação iniciada!"
echo ""
echo "Backend: http://localhost:5000"
echo "Frontend: frontend/index.html"
echo ""
echo "Para parar o servidor, pressione Ctrl+C"
echo "====================================="
echo ""

# Aguardar até que o usuário pare o script
wait $BACKEND_PID
