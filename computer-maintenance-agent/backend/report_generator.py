"""
Gerador de Relatórios - Exporta diagnósticos e recomendações
"""

import json
from datetime import datetime
from typing import Dict, List, Any


class ReportGenerator:
    """Classe para gerar relatórios de manutenção"""

    def __init__(self):
        self.timestamp = datetime.now()

    def generate_text_report(self, diagnostics: Dict[str, Any],
                             recommendations: Dict[str, Any]) -> str:
        """Gera relatório em formato texto"""

        report = f"""
╔════════════════════════════════════════════════════════════════════════════════╗
║                    RELATÓRIO DE MANUTENÇÃO DO COMPUTADOR                      ║
╚════════════════════════════════════════════════════════════════════════════════╝

📅 DATA E HORA: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}

═══════════════════════════════════════════════════════════════════════════════

📊 INFORMAÇÕES DO SISTEMA:

Computador: {diagnostics.get('system_info', {}).get('hostname', 'N/A')}
Sistema Operacional: {diagnostics.get('system_info', {}).get('system', 'N/A')} {diagnostics.get('system_info', {}).get('release', '')}
Arquitetura: {diagnostics.get('system_info', {}).get('machine', 'N/A')}

═══════════════════════════════════════════════════════════════════════════════

💾 RESUMO DE PERFORMANCE:

⚡ CPU (Processador):
   Uso: {diagnostics.get('cpu', {}).get('percent', 0):.1f}%
   Status: {diagnostics.get('cpu', {}).get('status', 'N/A').upper()}
   Núcleos: {diagnostics.get('cpu', {}).get('cores', 'N/A')}
   
🧠 MEMÓRIA (RAM):
   Uso: {diagnostics.get('memory', {}).get('virtual', {}).get('percent', 0):.1f}%
   Status: {diagnostics.get('memory', {}).get('status', 'N/A').upper()}
   Total: {self._format_bytes(diagnostics.get('memory', {}).get('virtual', {}).get('total', 0))}
   Usada: {self._format_bytes(diagnostics.get('memory', {}).get('virtual', {}).get('used', 0))}
   
💾 DISCO (Armazenamento):
   Uso: {diagnostics.get('disk', {}).get('total_percent', 0):.1f}%
   Status: {diagnostics.get('disk', {}).get('status', 'N/A').upper()}

═══════════════════════════════════════════════════════════════════════════════

📈 SAÚDE DO SISTEMA:

Score de Saúde: {diagnostics.get('health_score', 0):.1f}/100

"""

        # Adicionar detalhes das partições
        if diagnostics.get('disk', {}).get('partitions'):
            report += "🗂️  PARTIÇÕES DE DISCO:\n\n"
            for partition in diagnostics['disk']['partitions']:
                report += f"""   {partition['device']}:
      Tipo: {partition['fstype']}
      Ponto: {partition['mountpoint']}
      Total: {self._format_bytes(partition['total'])}
      Usada: {self._format_bytes(partition['used'])} ({partition['percent']:.1f}%)
      Livre: {self._format_bytes(partition['free'])}

"""

        # Adicionar processos principais
        if diagnostics.get('processes'):
            report += "⚙️  PRINCIPAIS PROCESSOS:\n\n"
            report += "   TOP 5 por CPU:\n"
            for i, proc in enumerate(diagnostics['processes'].get('top_by_cpu', [])[:5], 1):
                report += f"   {i}. {proc['name']} - CPU: {proc['cpu_percent']:.1f}%, Memória: {proc['memory_percent']:.2f}%\n"

            report += "\n   TOP 5 por Memória:\n"
            for i, proc in enumerate(diagnostics['processes'].get('top_by_memory', [])[:5], 1):
                report += f"   {i}. {proc['name']} - Memória: {proc['memory_percent']:.2f}%, CPU: {proc['cpu_percent']:.1f}%\n"

        report += "\n" + "═" * 80 + "\n"

        # Adicionar recomendações
        if recommendations.get('recommendations'):
            report += "\n💡 RECOMENDAÇÕES DE MANUTENÇÃO:\n\n"

            for i, rec in enumerate(recommendations['recommendations'], 1):
                priority_symbol = {
                    'crítico': '🔴',
                    'aviso': '🟡',
                    'normal': '🟢'
                }

                report += f"""{priority_symbol.get(rec['priority'], '•')} [{rec['priority'].upper()}] {rec['issue']}
   Categoria: {rec['category']}
   Descrição: {rec['description']}
   
   Ações recomendadas:
"""
                for action in rec['actions']:
                    report += f"   • {action}\n"
                report += "\n"

        report += "═" * 80 + "\n"
        report += "\n✅ Fim do Relatório\n"
        report += f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}\n"

        return report

    def generate_json_report(self, diagnostics: Dict[str, Any],
                             recommendations: Dict[str, Any]) -> str:
        """Gera relatório em formato JSON"""

        report_data = {
            'timestamp': datetime.now().isoformat(),
            'diagnostics': diagnostics,
            'recommendations': recommendations,
            'report_type': 'maintenance_report',
            'version': '1.0'
        }

        return json.dumps(report_data, indent=2, ensure_ascii=False, default=str)

    def generate_html_report(self, diagnostics: Dict[str, Any],
                             recommendations: Dict[str, Any]) -> str:
        """Gera relatório em formato HTML"""

        health_color = self._get_health_color(
            diagnostics.get('health_score', 0))

        html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Manutenção</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            text-align: center;
            color: #2563eb;
            margin-bottom: 10px;
        }}
        
        .timestamp {{
            text-align: center;
            color: #999;
            font-size: 0.9em;
            margin-bottom: 30px;
        }}
        
        .health-section {{
            text-align: center;
            margin-bottom: 40px;
        }}
        
        .health-score {{
            display: inline-block;
            width: 150px;
            height: 150px;
            border-radius: 50%;
            background: linear-gradient(135deg, {health_color}, rgba(0,0,0,0.1));
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 3em;
            font-weight: bold;
            color: white;
        }}
        
        .metric {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .metric-card {{
            padding: 20px;
            background: #f9f9f9;
            border-radius: 8px;
            border-left: 4px solid #2563eb;
        }}
        
        .metric-label {{
            font-size: 0.9em;
            color: #999;
            margin-bottom: 5px;
        }}
        
        .metric-value {{
            font-size: 1.8em;
            font-weight: bold;
            color: #333;
        }}
        
        .metric-status {{
            font-size: 0.85em;
            margin-top: 5px;
        }}
        
        .status-normal {{ color: #10b981; }}
        .status-aviso {{ color: #f59e0b; }}
        .status-critico {{ color: #ef4444; }}
        
        h2 {{
            color: #2563eb;
            margin-top: 40px;
            margin-bottom: 20px;
            border-bottom: 2px solid #2563eb;
            padding-bottom: 10px;
        }}
        
        .recommendation {{
            padding: 15px;
            margin-bottom: 15px;
            border-left: 4px solid #2563eb;
            background: #f9f9f9;
            border-radius: 4px;
        }}
        
        .recommendation.critico {{
            border-left-color: #ef4444;
        }}
        
        .recommendation.aviso {{
            border-left-color: #f59e0b;
        }}
        
        .recommendation.normal {{
            border-left-color: #10b981;
        }}
        
        .rec-title {{
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .rec-priority {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 0.8em;
            margin-right: 10px;
        }}
        
        .rec-actions {{
            margin-top: 10px;
            padding-left: 20px;
        }}
        
        .rec-actions li {{
            margin-bottom: 5px;
            color: #666;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #999;
            font-size: 0.9em;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            .container {{
                box-shadow: none;
                padding: 0;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🖥️ Relatório de Manutenção do Computador</h1>
        <div class="timestamp">
            Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}
        </div>
        
        <div class="health-section">
            <div class="health-score">
                {diagnostics.get('health_score', 0):.0f}
            </div>
            <p style="margin-top: 10px; color: #666;">Score de Saúde do Sistema</p>
        </div>
        
        <div class="metric">
            <div class="metric-card">
                <div class="metric-label">CPU</div>
                <div class="metric-value">{diagnostics.get('cpu', {}).get('percent', 0):.1f}%</div>
                <div class="metric-status status-{diagnostics.get('cpu', {}).get('status', 'normal')}">
                    {diagnostics.get('cpu', {}).get('status', 'N/A').upper()}
                </div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Memória</div>
                <div class="metric-value">{diagnostics.get('memory', {}).get('virtual', {}).get('percent', 0):.1f}%</div>
                <div class="metric-status status-{diagnostics.get('memory', {}).get('status', 'normal')}">
                    {diagnostics.get('memory', {}).get('status', 'N/A').upper()}
                </div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Disco</div>
                <div class="metric-value">{diagnostics.get('disk', {}).get('total_percent', 0):.1f}%</div>
                <div class="metric-status status-{diagnostics.get('disk', {}).get('status', 'normal')}">
                    {diagnostics.get('disk', {}).get('status', 'N/A').upper()}
                </div>
            </div>
        </div>
        
        <h2>📊 Informações do Sistema</h2>
        <p><strong>Computador:</strong> {diagnostics.get('system_info', {}).get('hostname', 'N/A')}</p>
        <p><strong>Sistema:</strong> {diagnostics.get('system_info', {}).get('system', 'N/A')} {diagnostics.get('system_info', {}).get('release', '')}</p>
        <p><strong>Arquitetura:</strong> {diagnostics.get('system_info', {}).get('machine', 'N/A')}</p>
        
        <h2>💡 Recomendações de Manutenção</h2>
"""

        if recommendations.get('recommendations'):
            for rec in recommendations['recommendations']:
                priority = rec.get('priority', 'normal')
                html += f"""        <div class="recommendation {priority}">
            <div class="rec-title">
                <span class="rec-priority" style="background: 
                {'#ef4444' if priority == 'crítico' else '#f59e0b' if priority == 'aviso' else '#10b981'};
                color: white;">
                    {priority.upper()}
                </span>
                {rec.get('issue', 'N/A')}
            </div>
            <p style="margin-top: 5px; color: #666;">{rec.get('description', '')}</p>
            <ul class="rec-actions">
"""
                for action in rec.get('actions', []):
                    html += f"                <li>{action}</li>\n"
                html += """            </ul>
        </div>
"""

        html += f"""        <div class="footer">
            Relatório gerado automaticamente pelo Agente de Manutenção de Computadores<br>
            {datetime.now().strftime('%d de %B de %Y às %H:%M:%S')}
        </div>
    </div>
</body>
</html>
"""

        return html

    @staticmethod
    def _format_bytes(bytes_value):
        """Formata bytes em formato legível"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024
        return f"{bytes_value:.2f} PB"

    @staticmethod
    def _get_health_color(health_score):
        """Retorna cor baseada no score de saúde"""
        if health_score >= 80:
            return '#10b981'  # Verde
        elif health_score >= 60:
            return '#f59e0b'  # Amarelo
        else:
            return '#ef4444'  # Vermelho
