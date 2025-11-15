# 🧪 GUIA DE TESTE - Agente de Manutenção

## ✅ Verificação de Funcionalidades

### 1️⃣ Verificar se Backend está Funcionando

```
URL: http://localhost:5000/api/health
Método: GET
Resposta Esperada:
{
  "status": "online",
  "timestamp": "2025-11-11T10:30:00.000000"
}
```

### 2️⃣ Testar Informações do Sistema

```
URL: http://localhost:5000/api/system/info
Método: GET
Resposta Esperada:
{
  "hostname": "seu-computador",
  "system": "Windows",
  "release": "10",
  "processor": "Intel Core i7...",
  "python_version": "3.11.9",
  "machine": "AMD64"
}
```

### 3️⃣ Testar Diagnóstico Rápido

```
URL: http://localhost:5000/api/diagnostics/quick
Método: GET
Resposta Esperada:
{
  "timestamp": "2025-11-11T10:30:00.000000",
  "cpu": {
    "percent": 25.5,
    "status": "normal"
  },
  "memory": {
    "percent": 45.2,
    "status": "normal"
  },
  "disk": {
    "percent": 60.8,
    "status": "normal"
  }
}
```

### 4️⃣ Testar Performance da CPU

```
URL: http://localhost:5000/api/performance/cpu
Método: GET
Resposta Esperada:
{
  "percent": 25.5,
  "count": 8,
  "freq": {
    "current": 2400.0,
    "min": 800.0,
    "max": 3600.0
  },
  "times": {...}
}
```

### 5️⃣ Testar Performance da Memória

```
URL: http://localhost:5000/api/performance/memory
Método: GET
Resposta Esperada:
{
  "virtual": {
    "total": 16000000000,
    "available": 8000000000,
    "percent": 50.0,
    "used": 8000000000,
    "free": 8000000000
  },
  "swap": {...}
}
```

### 6️⃣ Testar Performance do Disco

```
URL: http://localhost:5000/api/performance/disk
Método: GET
Resposta Esperada:
{
  "partitions": [
    {
      "device": "C:",
      "mountpoint": "C:\\",
      "fstype": "NTFS",
      "total": 256000000000,
      "used": 150000000000,
      "free": 106000000000,
      "percent": 58.6
    }
  ],
  "io": {...}
}
```

### 7️⃣ Testar Processos

```
URL: http://localhost:5000/api/processes
Método: GET
Resposta Esperada:
[
  {
    "pid": 1234,
    "name": "chrome.exe",
    "cpu_percent": 5.2,
    "memory_percent": 2.3
  },
  ...
]
```

### 8️⃣ Testar Recomendações

```
URL: http://localhost:5000/api/maintenance/recommendations
Método: GET
Resposta Esperada:
{
  "timestamp": "2025-11-11T10:30:00.000000",
  "total_recommendations": 4,
  "health_score": 82.5,
  "recommendations": [
    {
      "category": "CPU",
      "priority": "normal",
      "issue": "CPU em condições normais",
      "description": "CPU está em 25.5% de uso",
      "actions": [...]
    },
    ...
  ]
}
```

### 9️⃣ Testar Chat de Suporte

```
URL: http://localhost:5000/api/support/chat
Método: POST
Body:
{
  "message": "Como baixar o uso de CPU?"
}

Resposta Esperada:
{
  "user_message": "Como baixar o uso de CPU?",
  "agent_response": "CPU: Responsável pelo processamento...",
  "timestamp": "2025-11-11T10:30:00.000000"
}
```

## 🖥️ Testar Interface Web

### Dashboard
- [ ] Score de saúde aparece (0-100)
- [ ] CPU mostra percentual correto
- [ ] Memória mostra percentual correto
- [ ] Disco mostra percentual correto
- [ ] Informações do sistema aparecem
- [ ] Dashboard atualiza a cada 5 segundos

### Diagnósticos
- [ ] Botão "Diagnóstico Rápido" funciona
- [ ] Botão "Diagnóstico Completo" funciona
- [ ] Resultados aparecem com timestamp
- [ ] Status (normal/aviso/crítico) corretos

### Performance
- [ ] Aba CPU mostra frequência e núcleos
- [ ] Aba Memória mostra RAM e Swap
- [ ] Aba Disco mostra partições
- [ ] Aba Rede mostra tráfego
- [ ] Aba Processos mostra Top 20

### Recomendações
- [ ] Botão "Gerar Recomendações" funciona
- [ ] Recomendações aparecem com prioridade
- [ ] Score de saúde mostra
- [ ] Ações são listadas

### Suporte
- [ ] Chat carrega sem erros
- [ ] Mensagens do usuário aparecem
- [ ] Respostas do bot aparecem
- [ ] Enter envia mensagem
- [ ] Chat rola para última mensagem


## 🔄 Testar Responsividade

### Desktop (1920x1080)
- [ ] Todos elementos visíveis
- [ ] Layout organizado
- [ ] Sem scroll horizontal
- [ ] Cores corretas

### Tablet (768x1024)
- [ ] Sidebar adaptado
- [ ] Cards em duas colunas
- [ ] Tudo legível

### Mobile (375x667)
- [ ] Menu funciona
- [ ] Cards em uma coluna
- [ ] Chat usável
- [ ] Tudo acessível


## 🎨 Verificar Cores

### Estados
- [ ] Verde para status "normal" (< 60%)
- [ ] Amarelo para status "aviso" (60-79%)
- [ ] Vermelho para status "crítico" (80%+)

### Score de Saúde
- [ ] Verde escuro para score alto (80-100)
- [ ] Amarelo para score médio (60-79)
- [ ] Vermelho para score baixo (0-59)


## ⚡ Teste de Performance

### Backend
- [ ] Diagnóstico rápido: < 1 segundo
- [ ] Diagnóstico completo: < 5 segundos
- [ ] Dashboard atualiza: suave
- [ ] Sem travamentos

### Frontend
- [ ] Página carrega: < 2 segundos
- [ ] Mudança de abas: instantâneo
- [ ] Chat responde: < 1 segundo
- [ ] Sem erros no console (F12)


## 🔐 Teste de Segurança

- [ ] Sem coleta de dados pessoais
- [ ] Sem armazenamento de senhas
- [ ] APIs retornam dados locais apenas
- [ ] CORS está ativo
- [ ] Sem vulnerabilidades óbvias


## 📱 Teste de Navegadores

### Chrome
- [ ] Todos features funcionam
- [ ] Sem erros
- [ ] Performance boa

### Firefox
- [ ] Todos features funcionam
- [ ] Sem erros
- [ ] Performance boa

### Safari
- [ ] Todos features funcionam
- [ ] Sem erros
- [ ] Performance boa

### Edge
- [ ] Todos features funcionam
- [ ] Sem erros
- [ ] Performance boa


## 🧩 Casos de Teste Específicos

### Teste 1: Sistema Normal
Pré-condição: CPU < 60%, RAM < 70%, Disco < 75%
Esperado:
- [ ] Score > 80
- [ ] Todos status "normal"
- [ ] Recomendações positivas

### Teste 2: Sistema com Aviso
Pré-condição: CPU 60-80% ou RAM 70-85% ou Disco 75-90%
Esperado:
- [ ] Score 60-80
- [ ] Alguns status "aviso"
- [ ] Recomendações de ação

### Teste 3: Sistema Crítico
Pré-condição: CPU > 80% ou RAM > 85% ou Disco > 90%
Esperado:
- [ ] Score < 60
- [ ] Alguns status "crítico"
- [ ] Recomendações urgentes

### Teste 4: Chat com Tópicos Diferentes
- [ ] "cpu" → Retorna info sobre CPU
- [ ] "memória" → Retorna info sobre RAM
- [ ] "disco" → Retorna info sobre Disco
- [ ] "lento" → Dá sugestões
- [ ] "vírus" → Alertas de segurança
- [ ] "backup" → Info de backup


## 📊 Relatório de Testes

Após completar todos os testes:

```
Total de testes: XX
Aprovados: XX
Falhados: 0
Taxa de sucesso: 100%

Funcionalidades OK:
✓ Backend API
✓ Frontend UI
✓ Diagnósticos
✓ Recomendações
✓ Chat
✓ Performance
✓ Responsividade
✓ Compatibilidade
```


## 🐛 Troubleshooting

Se algo não funcionar:

1. Verifique erro no console (F12)
2. Verifique se backend está rodando
3. Tente atualizar a página (F5)
4. Reinicie o backend
5. Limpe cache do navegador

---

Todos os testes passando? ✅ Aplicação pronta para produção!
