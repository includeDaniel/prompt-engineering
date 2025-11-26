# 🖥️ INSTRUÇÕES DE EXECUÇÃO

## ✅ Pré-requisitos Verificados
- ✓ Python 3.11.9 configurado
- ✓ Ambiente virtual criado
- ✓ Todas as dependências instaladas:
  - Flask 2.3.3
  - Flask-CORS 4.0.0
  - psutil 5.9.5
  - requests 2.31.0
  - Werkzeug 2.3.7

## 🚀 Como Executar

### Opção 1: Inicializar Tudo com Um Clique (Windows)
```
Duplo clique em: iniciar.bat
```
- O servidor backend iniciará automaticamente na porta 5000
- A interface web abrirá no navegador padrão

### Opção 2: Inicialização Manual (Windows)

#### Terminal 1 - Backend:
```powershell
cd backend
python app.py
```
Saída esperada:
```
* Serving Flask app 'app'
* Running on http://127.0.0.1:5000
```

#### Terminal 2 - Frontend:
```powershell
# Opção A: Abrir arquivo diretamente
start frontend/index.html

# Opção B: Usar servidor local (opcional)
cd frontend
python -m http.server 8000
# Acessar: http://localhost:8000
```

### Opção 3: Linux/Mac

```bash
# Tornar script executável
chmod +x iniciar.sh

# Executar
./iniciar.sh
```

## 📍 Acessar a Aplicação

- **Frontend (Interface)**: `frontend/index.html` ou `http://localhost:8000`
- **API Backend**: `http://localhost:5000`
- **Health Check**: `http://localhost:5000/api/health`

## 🔌 Endpoints Principais da API

```
GET  /api/health                      - Status do servidor
GET  /api/system/info                 - Informações do sistema
GET  /api/diagnostics/quick           - Diagnóstico rápido
GET  /api/diagnostics/full            - Diagnóstico completo
GET  /api/performance/cpu             - Performance da CPU
GET  /api/performance/memory          - Performance da memória
GET  /api/performance/disk            - Performance do disco
GET  /api/performance/network         - Performance da rede
GET  /api/processes                   - Processos em execução
GET  /api/services/status             - Status de serviços
GET  /api/maintenance/recommendations - Recomendações
POST /api/support/chat                - Chat de suporte
```

## 🎯 Funcionalidades Disponíveis

✓ Dashboard em tempo real com saúde do sistema
✓ Monitoramento de CPU, Memória e Disco
✓ Diagnóstico Rápido e Completo
✓ Performance Detalhada (CPU, RAM, Disco, Rede, Processos)
✓ Recomendações Inteligentes de Manutenção
✓ Assistente de Suporte com IA
✓ Interface responsiva e intuitiva
✓ Atualização automática do dashboard a cada 5 segundos

## 📊 Dashboard

Ao abrir a interface, você verá:
- Score de saúde do sistema (0-100)
- Percentual de uso de CPU
- Percentual de uso de memória
- Percentual de uso de disco
- Informações do computador
- Status de cada componente (normal/aviso/crítico)

## 🔍 Diagnósticos

Clique em "Diagnósticos" para:
- Executar diagnóstico rápido (< 1 segundo)
- Executar diagnóstico completo (< 5 segundos)
- Ver detalhes de todos os componentes

## ⚡ Performance

Navegue pelas abas para ver:
- **CPU**: Uso, frequência, núcleos
- **Memória**: RAM e Swap detalhado
- **Disco**: Partições e I/O
- **Rede**: Tráfego e erros
- **Processos**: Top 20 por uso

## 💡 Recomendações

Clique em "Gerar Recomendações" para:
- Análise automática de problemas
- Priorização por criticidade
- Ações específicas para resolver

## 💬 Suporte

Faça perguntas sobre:
- CPU, Memória, Disco
- Lentidão do sistema
- Temperatura e ventiladores
- Segurança e malware
- Backup de dados

## 🛑 Parar a Aplicação

Pressione `Ctrl+C` no terminal onde o backend está rodando

## ⚙️ Configurações (Opcional)

Para alterar a porta do servidor:

**Arquivo: backend/app.py**
Linha final, altere:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Alterar porta aqui
```

## 🐛 Solução de Problemas

### Erro: Porta 5000 em uso
- Altere a porta no arquivo app.py
- Ou feche outro aplicativo usando porta 5000

### Erro: Flask não encontrado
```powershell
pip install -r requirements.txt
```

### Frontend não carrega
- Verifique se backend está rodando (http://localhost:5000/api/health)
- Abra DevTools (F12) e verifique console
- Atualize página (F5)

### Dados não aparecem
- Verifique conexão de internet
- Execute diagnóstico novamente
- Reinicie backend

## 📁 Estrutura do Projeto

```
computer-maintenance-agent/
├── backend/
│   ├── app.py                    # API Flask
│   ├── system_monitor.py         # Monitor do sistema
│   └── maintenance_analyzer.py   # Analisador
├── frontend/
│   ├── index.html               # Interface web
│   ├── styles.css               # Estilos
│   └── script.js                # Lógica
├── iniciar.bat                   # Iniciar (Windows)
├── iniciar.sh                    # Iniciar (Linux/Mac)
├── requirements.txt              # Dependências
├── README.md                     # Documentação
└── GUIA_RAPIDO.md               # Guia de uso
```

## 📱 Navegadores Suportados

✓ Chrome 90+
✓ Firefox 88+
✓ Safari 14+
✓ Edge 90+

## 💡 Dicas

1. Deixe o dashboard aberto para monitoramento contínuo
2. Execute diagnóstico completo uma vez por mês
3. Analise recomendações regularmente
4. Use o assistente para dúvidas
5. Faça backup dos dados importantes

## 📞 Suporte

Para dúvidas sobre o software, consulte:
- GUIA_RAPIDO.md - Guia de uso
- README.md - Documentação completa
- Assistente de Suporte (aba Suporte na aplicação)

---

**Versão**: 1.0.0
**Requisitos**: Python 3.7+
**Status**: ✅ Pronto para usar
**Última atualização**: Novembro de 2025

🎉 Aproveite o agente de manutenção de computadores!
