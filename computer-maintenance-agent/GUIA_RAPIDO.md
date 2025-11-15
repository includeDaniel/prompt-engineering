# 📖 Guia de Uso Rápido - Agente de Manutenção

## 🚀 Começar Rapidamente

### Opção 1: Windows (Recomendado)
1. Clique duas vezes em `iniciar.bat`
2. O backend iniciará automaticamente
3. A interface web abrirá no navegador

### Opção 2: Linux/Mac
```bash
chmod +x iniciar.sh
./iniciar.sh
```

### Opção 3: Manual
```bash
# Terminal 1: Iniciar backend
cd backend
python app.py

# Terminal 2: Abrir frontend
# Abra o arquivo "frontend/index.html" no seu navegador
```

## 🎯 Como Usar

### 📊 Dashboard
- Visualiza a saúde geral do seu sistema (0-100)
- Monitora CPU, Memória e Disco em tempo real
- Atualiza automaticamente a cada 5 segundos

### 🔍 Diagnósticos
- **Diagnóstico Rápido**: Verifica apenas métricas essenciais (< 1s)
- **Diagnóstico Completo**: Análise profunda de todos os componentes (< 5s)

### ⚡ Performance
Navegue pelas abas para ver detalhes:
- **CPU**: Frequência, núcleos, uso
- **Memória**: RAM e Swap
- **Disco**: Partições e I/O
- **Rede**: Tráfego e erros
- **Processos**: Top 20 por uso

### 💡 Recomendações
1. Clique em "Gerar Recomendações"
2. Veja problemas identificados com prioridades
3. Leia as ações sugeridas para resolver

### 💬 Suporte
Faça perguntas ao assistente sobre:
- Como resolver problemas comuns
- Otimização do sistema
- Segurança e malware
- Backup e recuperação
- Temperatura e resfriamento

## 🎨 Entendendo as Cores

- 🟢 **Verde (Normal)**: Uso 0-59%
- 🟡 **Amarelo (Aviso)**: Uso 60-79%
- 🔴 **Vermelho (Crítico)**: Uso 80%+

## 📊 Interpretando os Resultados

### Score de Saúde
- **90-100**: Excelente - nenhuma ação necessária
- **70-89**: Bom - monitorar regularmente
- **50-69**: Aceitável - considerar otimização
- **0-49**: Crítico - ação imediata recomendada

### Status da CPU
- **Normal**: Deixa aplicações rodarem bem
- **Aviso**: Algumas aplicações podem ficar lentas
- **Crítico**: Sistema pode ficar instável

### Status da Memória
- **Normal**: Multitarefa sem problemas
- **Aviso**: Feche algumas aplicações
- **Crítico**: Sistema muito lento, reinicie

### Status do Disco
- **Normal**: Espaço suficiente
- **Aviso**: Libere espaço em breve
- **Crítico**: Limpe arquivos urgentemente

## 🔧 Ações Recomendadas

### Se CPU está alta (80%+)
1. Abra a aba "Processos" em Performance
2. Identifique qual aplicação está usando muita CPU
3. Feche ou desinstale se não for necessária
4. Escaneie com antivírus se processador estiver sempre quente

### Se Memória está alta (85%+)
1. Feche abas do navegador
2. Desinstale extensões de navegador não usadas
3. Desinstale programas que você não usa
4. Reinicie o computador se problema persistir

### Se Disco está cheio (90%+)
1. Execute Limpeza de Disco do Windows
2. Exclua Downloads antigos
3. Desinstale programas não usados
4. Mova arquivos para armazenamento externo

## 💾 Dados Coletados

A aplicação coleta (somente local):
- ✓ CPU e temperatura
- ✓ Memória RAM
- ✓ Espaço em disco
- ✓ Tráfego de rede
- ✓ Processos em execução
- ✗ Arquivos e documentos (privados)
- ✗ Senhas (nunca)
- ✗ Navegação de internet

## ⏱️ Frequência de Verificação

- **Dashboard**: A cada 5 segundos
- **Diagnóstico Rápido**: Sob demanda
- **Diagnóstico Completo**: Sob demanda
- **Performance Detalhada**: Ao clicar na aba

## 🆘 Solução de Problemas

### Porta 5000 já está em uso
```bash
# Mude a porta no arquivo backend/app.py
# Linha: app.run(debug=True, host='0.0.0.0', port=5000)
# Altere 5000 para outra porta (ex: 5001)
```

### CORS Error no navegador
- Verifique se o backend está rodando
- Confirme que está em: http://localhost:5000

### Dados não atualizam
- Atualize a página (F5)
- Reinicie o backend
- Verifique se há erros no console (F12)

## 📱 Dispositivos Suportados

- Windows 10/11 (recomendado)
- Linux (qualquer distribuição)
- macOS (10.14+)
- Navegadores: Chrome, Firefox, Safari, Edge

## 🎓 Dicas de Manutenção

1. **Semanal**: Verifique o dashboard
2. **Mensal**: Execute diagnóstico completo
3. **Trimestral**: Faça limpeza de disco
4. **Anual**: Considere atualizar drivers

## 📞 Precisa de Ajuda?

Use o assistente de suporte (aba Suporte) para dúvidas comuns sobre:
- CPU, Memória, Disco
- Lentidão do sistema
- Temperatura e ventiladores
- Segurança e malware
- Backup de dados

---

**Versão**: 1.0.0
**Última atualização**: Novembro de 2025
