@echo off
REM Agente de Manutenção de Computadores - Script de Inicialização
REM Este script inicia tanto o backend quanto o frontend

echo.
echo =====================================
echo Agente de Manutenção de Computadores
echo =====================================
echo.

REM Verificar se estamos no diretório correto
if not exist "backend\app.py" (
    echo Erro: Arquivo backend\app.py não encontrado!
    echo Execute este script do diretório raiz do projeto.
    pause
    exit /b 1
)

echo Iniciando aplicação...
echo.

REM Iniciar backend em uma nova janela
echo Abrindo servidor backend na porta 5000...
start cmd /k "cd backend && python app.py"

REM Aguardar um pouco para o backend iniciar
timeout /t 3

REM Abrir frontend no navegador
echo Abrindo interface web no navegador...
start "" "frontend/index.html"

echo.
echo =====================================
echo Aplicação iniciada!
echo.
echo Backend: http://localhost:5000
echo Frontend: Abra frontend/index.html no navegador
echo.
echo Para parar o servidor, feche a janela do terminal ou pressione Ctrl+C
echo =====================================
echo.
pause
