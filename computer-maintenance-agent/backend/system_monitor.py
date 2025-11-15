"""
Monitor de Sistema - Coleta dados de performance do computador
"""

import psutil
import platform
from datetime import datetime


class SystemMonitor:
    """Classe responsável pelo monitoramento do sistema"""

    def __init__(self):
        self.threshold_cpu = 80
        self.threshold_memory = 85
        self.threshold_disk = 90

    def get_quick_diagnostics(self):
        """Diagnóstico rápido - apenas métricas críticas"""
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu': {
                'percent': psutil.cpu_percent(interval=1),
                'status': self._get_cpu_status()
            },
            'memory': {
                'percent': psutil.virtual_memory().percent,
                'status': self._get_memory_status()
            },
            'disk': {
                'percent': self._get_disk_usage_percent(),
                'status': self._get_disk_status()
            }
        }

    def get_full_diagnostics(self):
        """Diagnóstico completo do sistema"""
        cpu_data = self._get_cpu_diagnostics()
        memory_data = self._get_memory_diagnostics()
        disk_data = self._get_disk_diagnostics()
        network_data = self._get_network_diagnostics()
        process_data = self._get_processes_diagnostics()

        return {
            'timestamp': datetime.now().isoformat(),
            'system_info': {
                'hostname': platform.node(),
                'system': platform.system(),
                'release': platform.release()
            },
            'cpu': cpu_data,
            'memory': memory_data,
            'disk': disk_data,
            'network': network_data,
            'processes': process_data,
            'health_score': self._calculate_health_score(
                cpu_data, memory_data, disk_data
            )
        }

    def _get_cpu_diagnostics(self):
        """Coleta dados detalhados de CPU"""
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_freq = psutil.cpu_freq()

        return {
            'percent': cpu_percent,
            'count': psutil.cpu_count(),
            'frequency': {
                'current': cpu_freq.current if cpu_freq else None,
                'min': cpu_freq.min if cpu_freq else None,
                'max': cpu_freq.max if cpu_freq else None
            },
            'status': self._get_cpu_status(),
            'cores': psutil.cpu_count(logical=False)
        }

    def _get_memory_diagnostics(self):
        """Coleta dados detalhados de memória"""
        virtual = psutil.virtual_memory()
        swap = psutil.swap_memory()

        return {
            'virtual': {
                'total': virtual.total,
                'used': virtual.used,
                'available': virtual.available,
                'percent': virtual.percent,
                'free': virtual.free
            },
            'swap': {
                'total': swap.total,
                'used': swap.used,
                'free': swap.free,
                'percent': swap.percent
            },
            'status': self._get_memory_status()
        }

    def _get_disk_diagnostics(self):
        """Coleta dados detalhados de disco"""
        partitions_data = []
        total_usage = 0
        total_size = 0

        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                partitions_data.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent
                })
                total_usage += usage.used
                total_size += usage.total
            except PermissionError:
                continue

        return {
            'partitions': partitions_data,
            'total_percent': (total_usage / total_size * 100) if total_size > 0 else 0,
            'status': self._get_disk_status()
        }

    def _get_network_diagnostics(self):
        """Coleta dados detalhados de rede"""
        net_io = psutil.net_io_counters()

        return {
            'bytes_sent': net_io.bytes_sent,
            'bytes_received': net_io.bytes_recv,
            'packets_sent': net_io.packets_sent,
            'packets_received': net_io.packets_recv,
            'errors_in': net_io.errin,
            'errors_out': net_io.errout
        }

    def _get_processes_diagnostics(self):
        """Coleta dados sobre processos"""
        processes = []
        total_processes = len(psutil.pids())

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

        # Top 10 processos por CPU
        top_cpu = sorted(
            processes, key=lambda x: x['cpu_percent'], reverse=True)[:10]
        # Top 10 processos por memória
        top_memory = sorted(
            processes, key=lambda x: x['memory_percent'], reverse=True)[:10]

        return {
            'total': total_processes,
            'top_by_cpu': top_cpu,
            'top_by_memory': top_memory
        }

    def _get_cpu_status(self):
        """Retorna status da CPU"""
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent >= self.threshold_cpu:
            return 'crítico'
        elif cpu_percent >= 60:
            return 'aviso'
        else:
            return 'normal'

    def _get_memory_status(self):
        """Retorna status da memória"""
        memory_percent = psutil.virtual_memory().percent
        if memory_percent >= self.threshold_memory:
            return 'crítico'
        elif memory_percent >= 70:
            return 'aviso'
        else:
            return 'normal'

    def _get_disk_status(self):
        """Retorna status do disco"""
        disk_percent = self._get_disk_usage_percent()
        if disk_percent >= self.threshold_disk:
            return 'crítico'
        elif disk_percent >= 75:
            return 'aviso'
        else:
            return 'normal'

    def _get_disk_usage_percent(self):
        """Calcula percentual de uso total de disco"""
        total_usage = 0
        total_size = 0

        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                total_usage += usage.used
                total_size += usage.total
            except PermissionError:
                continue

        return (total_usage / total_size * 100) if total_size > 0 else 0

    def _calculate_health_score(self, cpu_data, memory_data, disk_data):
        """Calcula pontuação de saúde geral do sistema (0-100)"""
        cpu_score = max(0, 100 - cpu_data['percent'])
        memory_score = max(0, 100 - memory_data['virtual']['percent'])
        disk_score = max(0, 100 - disk_data['total_percent'])

        # Ponderação: CPU 30%, Memória 40%, Disco 30%
        health = (cpu_score * 0.3 + memory_score * 0.4 + disk_score * 0.3)

        return round(health, 2)
