"""
Agente de Apoio à Manutenção de Computadores
Backend Flask para diagnóstico e análise de sistemas
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import psutil
import platform
import json
from datetime import datetime
from maintenance_analyzer import MaintenanceAnalyzer
from system_monitor import SystemMonitor
from report_generator import ReportGenerator
from google import genai

app = Flask(__name__)
CORS(app)

# Inicializar analisadores
maintenance_analyzer = MaintenanceAnalyzer()
system_monitor = SystemMonitor()
report_generator = ReportGenerator()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Verifica se o servidor está funcionando"""
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/system/info', methods=['GET'])
def get_system_info():
    """Retorna informações gerais do sistema"""
    try:
        info = {
            'hostname': platform.node(),
            'system': platform.system(),
            'release': platform.release(),
            'processor': platform.processor(),
            'python_version': platform.python_version(),
            'machine': platform.machine()
        }
        return jsonify(info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/diagnostics/quick', methods=['GET'])
def quick_diagnostics():
    """Realiza diagnóstico rápido do sistema"""
    try:
        diagnostics = system_monitor.get_quick_diagnostics()
        return jsonify(diagnostics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/diagnostics/full', methods=['GET'])
def full_diagnostics():
    """Realiza diagnóstico completo do sistema"""
    try:
        diagnostics = system_monitor.get_full_diagnostics()
        return jsonify(diagnostics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/maintenance/recommendations', methods=['GET'])
def get_recommendations():
    """Obtém recomendações de manutenção"""
    try:
        diagnostics = system_monitor.get_full_diagnostics()
        recommendations = maintenance_analyzer.analyze_and_recommend(
            diagnostics)
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/performance/cpu', methods=['GET'])
def get_cpu_performance():
    """Retorna informações de performance da CPU"""
    try:
        data = {
            'percent': psutil.cpu_percent(interval=1),
            'count': psutil.cpu_count(),
            'freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
            'times': psutil.cpu_times()._asdict()
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/performance/memory', methods=['GET'])
def get_memory_performance():
    """Retorna informações de performance da memória"""
    try:
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        data = {
            'virtual': {
                'total': memory.total,
                'available': memory.available,
                'percent': memory.percent,
                'used': memory.used,
                'free': memory.free
            },
            'swap': {
                'total': swap.total,
                'used': swap.used,
                'free': swap.free,
                'percent': swap.percent
            }
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/performance/disk', methods=['GET'])
def get_disk_performance():
    """Retorna informações de performance do disco"""
    try:
        partitions = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                partitions.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent
                })
            except PermissionError:
                continue

        io_counters = psutil.disk_io_counters()
        data = {
            'partitions': partitions,
            'io': {
                'read_count': io_counters.read_count,
                'write_count': io_counters.write_count,
                'read_bytes': io_counters.read_bytes,
                'write_bytes': io_counters.write_bytes
            } if io_counters else None
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/performance/network', methods=['GET'])
def get_network_performance():
    """Retorna informações de performance da rede"""
    try:
        net_io = psutil.net_io_counters()
        net_if_stats = psutil.net_if_stats()

        interfaces = {}
        for interface, stats in net_if_stats.items():
            interfaces[interface] = {
                'isup': stats.isup,
                'speed': stats.speed,
                'mtu': stats.mtu
            }

        data = {
            'io': {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv,
                'errin': net_io.errin,
                'errout': net_io.errout,
                'dropin': net_io.dropin,
                'dropout': net_io.dropout
            },
            'interfaces': interfaces
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/processes', methods=['GET'])
def get_processes():
    """Retorna lista de processos em execução"""
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'cpu_percent': proc.info['cpu_percent'],
                    'memory_percent': proc.info['memory_percent']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # Ordenar por uso de CPU
        processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        return jsonify(processes[:20])  # Top 20 processos
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/services/status', methods=['GET'])
def get_services_status():
    """Retorna status dos serviços do sistema"""
    try:
        status = maintenance_analyzer.check_services_status()
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/support/chat', methods=['POST'])
def support_chat():
    """Interface de chat para suporte"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')

        # Extrair apenas o texto digitado pelo usuário e normalizar
        user_text = str(user_message).strip()

        print("User message:", user_text)

        client = genai.Client(
            api_key="AIzaSyCLzGBLxB5NQcd2HE1t6vVNVXLVlpDiDn4")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_text,
        )

        gemini_text = response.candidates[0].content.parts[0].text

        print("Gemini response:", gemini_text)

        return jsonify({'response': gemini_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reports/text', methods=['GET'])
def export_text_report():
    """Exporta relatório em texto"""
    try:
        diagnostics = system_monitor.get_full_diagnostics()
        recommendations = maintenance_analyzer.analyze_and_recommend(
            diagnostics)
        report = report_generator.generate_text_report(
            diagnostics, recommendations)

        return app.response_class(
            response=report,
            mimetype='text/plain',
            headers={'Content-Disposition': 'attachment;filename=relatorio.txt'}
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reports/json', methods=['GET'])
def export_json_report():
    """Exporta relatório em JSON"""
    try:
        diagnostics = system_monitor.get_full_diagnostics()
        recommendations = maintenance_analyzer.analyze_and_recommend(
            diagnostics)
        report = report_generator.generate_json_report(
            diagnostics, recommendations)

        return app.response_class(
            response=report,
            mimetype='application/json',
            headers={'Content-Disposition': 'attachment;filename=relatorio.json'}
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reports/html', methods=['GET'])
def export_html_report():
    """Exporta relatório em HTML"""
    try:
        diagnostics = system_monitor.get_full_diagnostics()
        recommendations = maintenance_analyzer.analyze_and_recommend(
            diagnostics)
        report = report_generator.generate_html_report(
            diagnostics, recommendations)

        return app.response_class(
            response=report,
            mimetype='text/html',
            headers={'Content-Disposition': 'attachment;filename=relatorio.html'}
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
