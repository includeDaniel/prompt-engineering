# 🖥️ Agente de Apoio à Manutenção de Computadores

Uma aplicação web inteligente para diagnóstico, monitoramento e suporte à manutenção de computadores em tempo real.

## 📋 Características

### 🎯 Dashboard
- **Saúde do Sistema**: Score visual (0-100) da saúde geral
- **Monitoramento em Tempo Real**: CPU, Memória e Disco
- **Informações do Sistema**: Detalhes de hardware e SO

### 🔍 Diagnósticos
- **Diagnóstico Rápido**: Métricas essenciais
- **Diagnóstico Completo**: Análise detalhada de todos os componentes

### ⚡ Performance
- Análise detalhada de CPU (frequência, núcleos)
- Memória virtual e swap
- Partições de disco e I/O
- Interface de rede
- Processos em execução (Top 20)

### 💡 Recomendações Inteligentes
- Análise automática de problemas
- Ações recomendadas por prioridade (crítico, aviso, normal)
- Sugestões baseadas em padrões de uso

### 💬 Assistente de Suporte
- Chat com IA para dúvidas de manutenção
- Respostas inteligentes sobre:
  - CPU e processamento
  - Memória e RAM
  - Disco rígido
  - Performance
  - Temperatura e resfriamento
  - Segurança e malware
  - Backup e recuperação

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.7+
- pip (gerenciador de pacotes Python)

### Passo 1: Instalar Dependências
```bash
pip install -r requirements.txt
```

### Passo 2: Iniciar o Servidor Backend
```bash
cd backend
python app.py
```

O servidor iniciará em: `http://localhost:5000`

### Passo 3: Abrir a Interface Web
```bash
cd frontend
# Abrir index.html em um navegador
# Ou usar um servidor local:
python -m http.server 8000
```

Acesse: `http://localhost:8000`

## 📁 Estrutura do Projeto

```
computer-maintenance-agent/
├── backend/
│   ├── app.py                    # Aplicação Flask principal
│   ├── system_monitor.py         # Monitor de sistema
│   └── maintenance_analyzer.py   # Analisador de manutenção
├── frontend/
│   ├── index.html               # Interface web
│   ├── styles.css               # Estilos
│   └── script.js                # Lógica JavaScript
├── data/                         # Diretório para dados
├── requirements.txt              # Dependências Python
└── README.md                     # Este arquivo
```

## 🔧 Endpoints da API

### Informações do Sistema
- `GET /api/system/info` - Informações gerais do computador
- `GET /api/health` - Status do servidor

### Diagnósticos
- `GET /api/diagnostics/quick` - Diagnóstico rápido
- `GET /api/diagnostics/full` - Diagnóstico completo

### Performance
- `GET /api/performance/cpu` - Dados de CPU
- `GET /api/performance/memory` - Dados de memória
- `GET /api/performance/disk` - Dados de disco
- `GET /api/performance/network` - Dados de rede

### Processos
- `GET /api/processes` - Top 20 processos por CPU
- `GET /api/services/status` - Status de serviços

### Manutenção
- `GET /api/maintenance/recommendations` - Recomendações de manutenção
- `POST /api/support/chat` - Chat de suporte

## 📊 Indicadores de Saúde

### Score de Saúde (0-100)
- **80-100**: ✓ Sistema em ótimo estado
- **60-79**: ⚠ Sistema com alguns problemas
- **0-59**: ✕ Sistema em condições críticas

### Status por Componente
- **Normal**: CPU < 80%, Memória < 85%, Disco < 90%
- **Aviso**: CPU 60-80%, Memória 70-85%, Disco 75-90%
- **Crítico**: CPU ≥ 80%, Memória ≥ 85%, Disco ≥ 90%

## 💻 Requisitos de Sistema

### Mínimo
- RAM: 2GB
- Espaço em disco: 500MB
- Python 3.7+

### Recomendado
- RAM: 4GB+
- Espaço em disco: 1GB+
- Python 3.9+

## 🔐 Segurança

- Interface disponível localmente (localhost)
- CORS habilitado para desenvolvimento
- Sem armazenamento de senhas ou dados sensíveis
- Informações de sistema apenas para diagnóstico

## 📝 Recomendações de Manutenção

A aplicação gera recomendações automáticas para:

### CPU
- Fechar aplicações desnecessárias
- Verificar malware
- Limpeza de startup

### Memória
- Fechar abas do navegador
- Desinstalar aplicações
- Adicionar RAM se necessário

### Disco
- Limpar arquivos temporários
- Desinstalar programas
- Executar limpeza de disco

### Processos
- Investigar uso anormal
- Verificar atualizações
- Detectar vazamentos de memória

### Rede
- Reiniciar adaptador
- Atualizar drivers
- Contatar ISP se necessário

## 🚀 Funcionalidades Futuras

- [ ] Histórico de diagnósticos
- [ ] Alertas automáticos
- [ ] Agendamento de manutenção
- [ ] Exportação de relatórios
- [ ] Suporte multi-usuário
- [ ] Integração com serviços de limpeza
- [ ] Análise de malware avançada
- [ ] Previsões de falhas

## 📞 Suporte

Para dúvidas sobre manutenção, use o assistente de suporte integrado:
- Dúvidas frequentes: CPU, Memória, Disco, Lentidão, Temperatura, Segurança, Backup

## 📄 Licença

Este projeto é fornecido como está, sem garantias.

## 👨‍💻 Desenvolvido por

Agente de Manutenção Inteligente v1.0

---

**Última atualização:** Novembro de 2025
