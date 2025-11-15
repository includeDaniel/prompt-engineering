"""
Analisador de Manutenção - Propõe ações e recomendações
"""

import platform
import psutil
from datetime import datetime
import os
from gemini_client import get_gemini_client


class MaintenanceAnalyzer:
    """Classe responsável pela análise e recomendações de manutenção"""

    def __init__(self):
        self.priority_levels = {
            'crítico': 1,
            'aviso': 2,
            'normal': 3
        }

    def analyze_and_recommend(self, diagnostics):
        """Análise completa e gera recomendações"""
        recommendations = []

        # Análise de CPU
        recommendations.extend(self._analyze_cpu(diagnostics))

        # Análise de Memória
        recommendations.extend(self._analyze_memory(diagnostics))

        # Análise de Disco
        recommendations.extend(self._analyze_disk(diagnostics))

        # Análise de Processos
        recommendations.extend(self._analyze_processes(diagnostics))

        # Análise de Rede
        recommendations.extend(self._analyze_network(diagnostics))

        # Ordenar por prioridade
        recommendations.sort(key=lambda x: self.priority_levels[x['priority']])

        return {
            'timestamp': datetime.now().isoformat(),
            'total_recommendations': len(recommendations),
            'recommendations': recommendations,
            'health_score': diagnostics.get('health_score', 0)
        }

    def _analyze_cpu(self, diagnostics):
        """Analisa CPU e gera recomendações"""
        recommendations = []
        cpu_data = diagnostics.get('cpu', {})
        cpu_percent = cpu_data.get('percent', 0)

        if cpu_data.get('status') == 'crítico':
            recommendations.append({
                'category': 'CPU',
                'priority': 'crítico',
                'issue': 'Uso crítico de CPU detectado',
                'description': f'CPU está em {cpu_percent}% de uso',
                'actions': [
                    'Fechar aplicações desnecessárias',
                    'Verificar processos com alto uso de CPU',
                    'Considerar atualização de hardware se o problema for recorrente',
                    'Verificar se há malware usando CPU'
                ]
            })
        elif cpu_data.get('status') == 'aviso':
            recommendations.append({
                'category': 'CPU',
                'priority': 'aviso',
                'issue': 'CPU com uso elevado',
                'description': f'CPU está em {cpu_percent}% de uso',
                'actions': [
                    'Monitorar uso de CPU',
                    'Fechar aplicações não essenciais',
                    'Considerar limpeza de malware'
                ]
            })
        else:
            recommendations.append({
                'category': 'CPU',
                'priority': 'normal',
                'issue': 'CPU em condições normais',
                'description': f'CPU está em {cpu_percent}% de uso',
                'actions': [
                    'Continuar monitorando',
                    'Realizar limpeza de startup periodicamente'
                ]
            })

        return recommendations

    def _analyze_memory(self, diagnostics):
        """Analisa memória e gera recomendações"""
        recommendations = []
        memory_data = diagnostics.get('memory', {})
        memory_percent = memory_data.get('virtual', {}).get('percent', 0)

        if memory_data.get('status') == 'crítico':
            recommendations.append({
                'category': 'Memória',
                'priority': 'crítico',
                'issue': 'Memória crítica detectada',
                'description': f'Memória está em {memory_percent}% de uso',
                'actions': [
                    'Fechar aplicações para liberar memória',
                    'Reiniciar o computador',
                    'Desinstalar aplicações desnecessárias',
                    'Adicionar mais RAM ao sistema'
                ]
            })
        elif memory_data.get('status') == 'aviso':
            recommendations.append({
                'category': 'Memória',
                'priority': 'aviso',
                'issue': 'Memória com uso elevado',
                'description': f'Memória está em {memory_percent}% de uso',
                'actions': [
                    'Fechar abas do navegador',
                    'Desabilitar extensões de navegador',
                    'Realizar limpeza temporária'
                ]
            })
        else:
            recommendations.append({
                'category': 'Memória',
                'priority': 'normal',
                'issue': 'Memória em condições normais',
                'description': f'Memória está em {memory_percent}% de uso',
                'actions': [
                    'Continuar monitorando',
                    'Manter aplicações desnecessárias fechadas'
                ]
            })

        return recommendations

    def _analyze_disk(self, diagnostics):
        """Analisa disco e gera recomendações"""
        recommendations = []
        disk_data = diagnostics.get('disk', {})
        disk_percent = disk_data.get('total_percent', 0)

        if disk_data.get('status') == 'crítico':
            recommendations.append({
                'category': 'Disco',
                'priority': 'crítico',
                'issue': 'Espaço em disco crítico',
                'description': f'Disco está em {disk_percent}% de uso',
                'actions': [
                    'Limpar arquivos temporários',
                    'Desinstalar programas não utilizados',
                    'Executar limpeza de disco',
                    'Mover arquivos para armazenamento externo',
                    'Aumentar espaço em disco'
                ]
            })
        elif disk_data.get('status') == 'aviso':
            recommendations.append({
                'category': 'Disco',
                'priority': 'aviso',
                'issue': 'Disco com espaço limitado',
                'description': f'Disco está em {disk_percent}% de uso',
                'actions': [
                    'Limpar pasta de Downloads',
                    'Deletar arquivos antigos',
                    'Executar ferramenta de limpeza'
                ]
            })
        else:
            recommendations.append({
                'category': 'Disco',
                'priority': 'normal',
                'issue': 'Espaço em disco adequado',
                'description': f'Disco está em {disk_percent}% de uso',
                'actions': [
                    'Manter limpeza regular',
                    'Backup periódico de dados importantes'
                ]
            })

        return recommendations

    def _analyze_processes(self, diagnostics):
        """Analisa processos e gera recomendações"""
        recommendations = []
        processes_data = diagnostics.get('processes', {})
        top_cpu = processes_data.get('top_by_cpu', [])
        top_memory = processes_data.get('top_by_memory', [])

        if top_cpu and top_cpu[0]['cpu_percent'] > 50:
            high_cpu_process = top_cpu[0]
            recommendations.append({
                'category': 'Processos',
                'priority': 'aviso',
                'issue': f'Processo usando muita CPU: {high_cpu_process["name"]}',
                'description': f'{high_cpu_process["name"]} está usando {high_cpu_process["cpu_percent"]}% de CPU',
                'actions': [
                    'Investigar se o processo é necessário',
                    'Fechar ou encerrar o processo se não for essencial',
                    'Verificar atualização do software'
                ]
            })

        if top_memory and top_memory[0]['memory_percent'] > 15:
            high_memory_process = top_memory[0]
            recommendations.append({
                'category': 'Processos',
                'priority': 'aviso',
                'issue': f'Processo usando muita memória: {high_memory_process["name"]}',
                'description': f'{high_memory_process["name"]} está usando {high_memory_process["memory_percent"]}% de memória',
                'actions': [
                    'Considerar fechar a aplicação',
                    'Verificar se existe vazamento de memória',
                    'Reiniciar a aplicação'
                ]
            })

        if not recommendations:
            recommendations.append({
                'category': 'Processos',
                'priority': 'normal',
                'issue': 'Processos em condições normais',
                'description': 'Nenhum processo com consumo excessivo detectado',
                'actions': [
                    'Continuar monitorando processos',
                    'Desabilitar inicialização de aplicações desnecessárias'
                ]
            })

        return recommendations

    def _analyze_network(self, diagnostics):
        """Analisa rede e gera recomendações"""
        recommendations = []
        network_data = diagnostics.get('network', {})
        errors = network_data.get('errors_in', 0) + \
            network_data.get('errors_out', 0)

        if errors > 100:
            recommendations.append({
                'category': 'Rede',
                'priority': 'aviso',
                'issue': 'Erros de rede detectados',
                'description': f'{errors} erros de rede detectados',
                'actions': [
                    'Reiniciar adaptador de rede',
                    'Verificar conexão com o roteador',
                    'Atualizar drivers de rede',
                    'Contatar provedor de internet se problema persistir'
                ]
            })
        else:
            recommendations.append({
                'category': 'Rede',
                'priority': 'normal',
                'issue': 'Rede em condições normais',
                'description': 'Conexão de rede estável',
                'actions': [
                    'Continuar monitorando',
                    'Manter drivers de rede atualizados'
                ]
            })

        return recommendations

    def check_services_status(self):
        """Verifica status de serviços críticos (varia por SO)"""
        services_status = {
            'timestamp': datetime.now().isoformat(),
            'system': platform.system(),
            'services': []
        }

        if platform.system() == 'Windows':
            # Serviços Windows críticos
            critical_services = [
                'Windefend',  # Windows Defender
                'WinRM',
                'Themes',
                'AudioEndpointBuilder'
            ]
        else:
            # Serviços Linux/Mac
            critical_services = [
                'sshd',
                'cron'
            ]

        return services_status

    def process_support_message(self, message):
        """Processa mensagens de suporte do usuário com respostas inteligentes"""
        message_lower = message.lower()

        # Se o cliente Gemini estiver configurado, tente gerar resposta usando o modelo remoto
        try:
            gemini = get_gemini_client()
            if gemini.enabled:
                prompt = f"Usuário: {message}\n\nResponda de forma clara, em português, com instruções passo a passo apropriadas para um técnico de informática."
                gen = gemini.generate(prompt)
                if gen:
                    return gen
        except Exception:
            # Não interromper fluxo se Gemini falhar; cair para fallback local
            pass

        # Categorizar dúvida e retornar resposta detalhada
        responses = {
            'cpu': {
                'keywords': ['cpu', 'processador', 'uso de cpu', 'processor'],
                'response': """🖥️ **CPU - Processador Central**

A CPU é o "cérebro" do computador. Seu uso alto causa lentidão.

⚠️ **Problema**: CPU acima de 80%
✓ **Solução**:
  1. Abra Gerenciador de Tarefas (Ctrl+Shift+Esc)
  2. Veja qual processo usa mais CPU
  3. Feche ou desinstale se desnecessário
  4. Escaneie malware
  5. Atualize drivers de placa mãe

💡 **Dica**: Desabilite programas de inicialização"""
            },
            'memoria': {
                'keywords': ['memória', 'ram', 'memo', 'heap'],
                'response': """🧠 **Memória RAM - Armazenamento Temporário**

RAM é essencial para multitarefa. Cheia = sistema lento.

⚠️ **Problema**: Memória acima de 85%
✓ **Solução**:
  1. Feche abas do navegador (Chrome consome muito)
  2. Desinstale extensões não usadas
  3. Desinstale programas desnecessários
  4. Reinicie o computador
  5. Se persistir, adicione mais RAM (upgrade)

💡 **Dica**: Use ferramentas de limpeza de memória periodicamente"""
            },
            'disco': {
                'keywords': ['disco', 'ssd', 'hdd', 'espaço', 'armazenamento'],
                'response': """💾 **Disco Rígido - Armazenamento Permanente**

Disco cheio afeta velocidade do sistema. Limpe regularmente.

⚠️ **Problema**: Disco acima de 90%
✓ **Solução**:
  1. Abra "Limpeza de Disco" (procure no Windows)
  2. Delete Downloads antigos
  3. Desinstale programas não usados
  4. Mova fotos/vídeos para externo
  5. Considere aumentar capacidade

💡 **Dica**: Faça backup antes de deletar qualquer coisa!"""
            },
            'lento': {
                'keywords': ['lento', 'lag', 'travado', 'congela', 'lentidão'],
                'response': """⚡ **Sistema Lento - Diagnosis e Soluções**

Vários fatores podem causar lentidão.

✓ **Checklist de Otimização**:
  1. Verifique CPU (acima de 80%?)
  2. Verifique RAM (acima de 85%?)
  3. Verifique Disco (acima de 90%?)
  4. Escaneie malware/vírus
  5. Desabilite programas de inicialização
  6. Atualize drivers
  7. Limpe arquivos temporários
  8. Desfragmente disco (HDDs apenas)
  9. Reinicie o computador
  10. Considere SSD upgrade

💡 **Dica**: Use o Diagnóstico Completo desta ferramenta!"""
            },
            'temperatura': {
                'keywords': ['quente', 'temperatura', 'temp', 'aquecimento', 'overheat'],
                'response': """🌡️ **Temperatura - Resfriamento do Sistema**

Temperatura alta reduz vida útil e performance.

⚠️ **Temperatura Normal**:
  • CPU: 30-80°C (em repouso: 30-50°C)
  • GPU: 30-85°C

✓ **Se muito quente**:
  1. Limpe ventiladores (poeira)
  2. Verifique fluxo de ar
  3. Use suporte de resfriamento
  4. Considere repaste térmico
  5. Verifique processador em uso
  6. Mude local do computador (melhor ventilação)

⚠️ **Risco**: Acima de 100°C = dano ao hardware!

💡 **Dica**: Monitore temperatura com ferramentas específicas"""
            },
            'ventilador': {
                'keywords': ['ventilador', 'barulho', 'barulhenta', 'ruído', 'som'],
                'response': """🌪️ **Ventilador Barulhento - Diagnóstico**

Som alto geralmente indica problema de resfriamento.

✓ **Causas Comuns**:
  1. Ventilador com poeira
  2. Temperatura alta (ventilador em turbo)
  3. Ventilador danificado
  4. Dissipador de calor entupido
  5. Pasta térmica vencida

✓ **Soluções**:
  1. Abra gabinete e limpe poeira
  2. Use ar comprimido
  3. Verifique temperatura
  4. Se continuar: troque ventilador
  5. Considere repasse térmico

💡 **Dica**: Barulho = seu PC pedindo ajuda!"""
            },
            'atualizacao': {
                'keywords': ['atualização', 'update', 'updater', 'patches'],
                'response': """📦 **Atualizações - Manutenção Crítica**

Atualizações trazem segurança e performance.

✓ **O que Atualizar**:
  1. Windows Update (mensal)
  2. Drivers GPU (NVIDIA/AMD)
  3. Drivers de chipset
  4. Antivírus/Windows Defender
  5. Programas frequentemente usados

✓ **Como Atualizar**:
  1. Windows: Configurações > Atualização
  2. Drivers: Gerenciador de Dispositivos
  3. Programas: Verificar dentro deles

⚠️ **Importante**: Backup antes de atualizar!

💡 **Dica**: Atualize mensalmente, não ignore!"""
            },
            'virus': {
                'keywords': ['vírus', 'malware', 'spyware', 'ransomware', 'trojan'],
                'response': """🔒 **Segurança - Proteção Contra Malware**

Malware compromete performance e privacidade.

✓ **Se Suspeita de Infecção**:
  1. Escaneie com Windows Defender
  2. Ou use: Malwarebytes (gratuito)
  3. Escaneie em Modo Seguro
  4. Isolada arquivos suspeitos

✓ **Prevenção**:
  1. Mantenha Windows atualizado
  2. Use antivírus (Defender é bom)
  3. Não baixe de sites desconhecidos
  4. Cuidado com emails/links suspeitos
  5. Use navegador seguro (Chrome/Firefox)

⚠️ **Sinais de Infecção**:
  • Lentidão anormal
  • Pop-ups constantes
  • Programas desconhecidos
  • Disco sempre em 100%

💡 **Dica**: Prevenção é melhor que cura!"""
            },
            'backup': {
                'keywords': ['backup', 'backup', 'cópia', 'recuperação', 'dados'],
                'response': """💿 **Backup - Proteção de Dados**

Backup é ESSENCIAL! Disco falha, você perde tudo.

✓ **Como Fazer Backup**:
  1. **Windows Backup Nativo**:
     - Configurações > Sistema > Backup
  2. **Externo (Recomendado)**:
     - Compre HD externo
     - Copie arquivos importantes
     - Guarde em local seguro
  3. **Nuvem (Google Drive, OneDrive)**:
     - Arquivos importantes
     - Acesso remoto

✓ **Frequência**:
  • Dados críticos: Diário
  • Fotos/documentos: Semanal
  • Sistema completo: Mensal

⚠️ **Risco**: Sem backup = perda permanente!

💡 **Dica**: "Quem não faz backup, já está perdendo!"
"""
            }
        }

        # Procurar por keywords
        for category, data in responses.items():
            for keyword in data['keywords']:
                if keyword in message_lower:
                    return data['response']

        # Fallback com dicas
        return """🤖 **Assistente de Manutenção**

Não entendi sua pergunta. Posso ajudar com:

📌 **Tópicos Disponíveis**:
• CPU / Processador
• Memória / RAM
• Disco / Armazenamento
• Lentidão / Performance
• Temperatura / Resfriamento
• Ventilador / Barulho
• Atualização / Updates
• Vírus / Malware / Segurança
• Backup / Recuperação

💡 **Dica**: Faça uma pergunta clara sobre estes tópicos!

Exemplo: "Como baixar o uso de CPU?" ou "Meu disco está cheio"
"""
