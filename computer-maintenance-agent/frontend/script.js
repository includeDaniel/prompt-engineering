// Configuração da API
const API_BASE_URL = 'http://localhost:5000/api';

// Estado da aplicação
let currentSection = 'dashboard';
let updateInterval = null;

// Inicializar ao carregar página
document.addEventListener('DOMContentLoaded', () => {
    loadDashboard();
    startAutoUpdate();
});

// ==================== NAVEGAÇÃO ====================
function showSection(sectionId) {
    // Ocultar todas as seções
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });

    // Remover classe active de todos os botões
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Mostrar seção selecionada
    document.getElementById(sectionId).classList.add('active');

    // Marcar botão como ativo
    event.target.classList.add('active');

    currentSection = sectionId;

    // Carregar dados específicos
    if (sectionId === 'performance') {
        loadPerformanceDetails();
    }
}

function showTab(tabId) {
    // Ocultar todos os tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // Remover classe active de todos os botões
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Mostrar tab selecionado
    document.getElementById(tabId).classList.add('active');

    // Marcar botão como ativo
    event.target.classList.add('active');
}

// ==================== DASHBOARD ====================
async function loadDashboard() {
    try {
        // Carregar informações do sistema
        const systemInfo = await fetch(`${API_BASE_URL}/system/info`).then(r => r.json());
        displaySystemInfo(systemInfo);

        // Carregar diagnóstico rápido
        const diagnostics = await fetch(`${API_BASE_URL}/diagnostics/quick`).then(r => r.json());
        displayDashboardMetrics(diagnostics);

        // Carregar diagnóstico completo para saúde
        const fullDiag = await fetch(`${API_BASE_URL}/diagnostics/full`).then(r => r.json());
        displayHealthScore(fullDiag.health_score);
    } catch (error) {
        console.error('Erro ao carregar dashboard:', error);
    }
}

function displaySystemInfo(info) {
    const infoDiv = document.getElementById('system-info');
    infoDiv.innerHTML = `
        <table class="info-table">
            <tr><td>Computador:</td><td>${info.hostname}</td></tr>
            <tr><td>Sistema:</td><td>${info.system} ${info.release}</td></tr>
            <tr><td>Processador:</td><td>${info.processor}</td></tr>
            <tr><td>Arquitetura:</td><td>${info.machine}</td></tr>
            <tr><td>Python:</td><td>${info.python_version}</td></tr>
        </table>
    `;
}

function displayDashboardMetrics(diagnostics) {
    // CPU
    const cpuPercent = diagnostics.cpu.percent;
    updateProgressBar('cpu-bar', cpuPercent);
    document.getElementById('cpu-percent').textContent = `${cpuPercent.toFixed(1)} %`;
    const cpuStatus = diagnostics.cpu.status;
    const cpuStatusElem = document.getElementById('cpu-status');
    cpuStatusElem.textContent = `Status: ${cpuStatus.toUpperCase()}`;
    cpuStatusElem.className = `status ${cpuStatus}`;

    // Memória
    const memoryPercent = diagnostics.memory.percent;
    updateProgressBar('memory-bar', memoryPercent);
    document.getElementById('memory-percent').textContent = `${memoryPercent.toFixed(1)} %`;
    const memoryStatus = diagnostics.memory.status;
    const memoryStatusElem = document.getElementById('memory-status');
    memoryStatusElem.textContent = `Status: ${memoryStatus.toUpperCase()}`;
    memoryStatusElem.className = `status ${memoryStatus}`;

    // Disco
    const diskPercent = diagnostics.disk.percent;
    updateProgressBar('disk-bar', diskPercent);
    document.getElementById('disk-percent').textContent = `${diskPercent.toFixed(1)} %`;
    const diskStatus = diagnostics.disk.status;
    const diskStatusElem = document.getElementById('disk-status');
    diskStatusElem.textContent = `Status: ${diskStatus.toUpperCase()}`;
    diskStatusElem.className = `status ${diskStatus}`;
}

function displayHealthScore(score) {
    document.getElementById('score-circle').textContent = score.toFixed(0);
    const scoreElem = document.getElementById('score-circle');

    if (score >= 80) {
        scoreElem.style.background = 'linear-gradient(135deg, #10b981, #059669)';
        document.getElementById('health-status').textContent = '✓ Sistema em ótimo estado';
    } else if (score >= 60) {
        scoreElem.style.background = 'linear-gradient(135deg, #f59e0b, #d97706)';
        document.getElementById('health-status').textContent = '⚠ Sistema com alguns problemas';
    } else {
        scoreElem.style.background = 'linear-gradient(135deg, #ef4444, #dc2626)';
        document.getElementById('health-status').textContent = '✕ Sistema em condições críticas';
    }
}

function updateProgressBar(elementId, percentage) {
    const bar = document.getElementById(elementId);
    bar.style.width = percentage + '%';

    // Alterar cor conforme porcentagem
    if (percentage >= 80) {
        bar.style.background = 'linear-gradient(90deg, #ef4444, #dc2626)';
    } else if (percentage >= 60) {
        bar.style.background = 'linear-gradient(90deg, #f59e0b, #d97706)';
    } else {
        bar.style.background = 'linear-gradient(90deg, #10b981, #059669)';
    }
}

// Diagnostics UI removed: functions quickDiagnostics, fullDiagnostics and displayDiagnosticsResults were removed

// ==================== PERFORMANCE ====================
async function loadPerformanceDetails() {
    try {
        const cpuData = await fetch(`${API_BASE_URL}/performance/cpu`).then(r => r.json());
        const memoryData = await fetch(`${API_BASE_URL}/performance/memory`).then(r => r.json());
        const diskData = await fetch(`${API_BASE_URL}/performance/disk`).then(r => r.json());
        const networkData = await fetch(`${API_BASE_URL}/performance/network`).then(r => r.json());
        const processesData = await fetch(`${API_BASE_URL}/processes`).then(r => r.json());

        displayCPUDetails(cpuData);
        displayMemoryDetails(memoryData);
        displayDiskDetails(diskData);
        displayNetworkDetails(networkData);
        displayProcessesDetails(processesData);
    } catch (error) {
        console.error('Erro ao carregar performance:', error);
    }
}

function displayCPUDetails(data) {
    const html = `
        <table class="info-table">
            <tr><td>Uso Atual:</td><td>${data.percent.toFixed(1)}%</td></tr>
            <tr><td>Núcleos Lógicos:</td><td>${data.count}</td></tr>
            <tr><td>Frequência Atual:</td><td>${data.freq ? (data.freq.current / 1000).toFixed(1) + ' GHz' : 'N/A'}</td></tr>
            <tr><td>Frequência Mínima:</td><td>${data.freq ? (data.freq.min / 1000).toFixed(1) + ' GHz' : 'N/A'}</td></tr>
            <tr><td>Frequência Máxima:</td><td>${data.freq ? (data.freq.max / 1000).toFixed(1) + ' GHz' : 'N/A'}</td></tr>
        </table>
    `;
    document.getElementById('cpu-detail').innerHTML = html;
}

function displayMemoryDetails(data) {
    const virtualMem = data.virtual;
    const html = `
        <h4>Memória Virtual</h4>
        <table class="info-table">
            <tr><td>Total:</td><td>${formatBytes(virtualMem.total)}</td></tr>
            <tr><td>Usada:</td><td>${formatBytes(virtualMem.used)} (${virtualMem.percent.toFixed(1)}%)</td></tr>
            <tr><td>Disponível:</td><td>${formatBytes(virtualMem.available)}</td></tr>
            <tr><td>Livre:</td><td>${formatBytes(virtualMem.free)}</td></tr>
        </table>
        <h4 style="margin-top: 20px;">Swap</h4>
        <table class="info-table">
            <tr><td>Total:</td><td>${formatBytes(data.swap.total)}</td></tr>
            <tr><td>Usada:</td><td>${formatBytes(data.swap.used)} (${data.swap.percent.toFixed(1)}%)</td></tr>
            <tr><td>Livre:</td><td>${formatBytes(data.swap.free)}</td></tr>
        </table>
    `;
    document.getElementById('memory-detail').innerHTML = html;
}

function displayDiskDetails(data) {
    let html = '<h4>Partições de Disco</h4>';

    data.partitions.forEach(partition => {
        html += `
            <div class="result-item">
                <strong>${partition.device}</strong> (${partition.fstype})<br>
                Ponto de montagem: ${partition.mountpoint}<br>
                Total: ${formatBytes(partition.total)} | Usada: ${formatBytes(partition.used)} | Livre: ${formatBytes(partition.free)} (${partition.percent.toFixed(1)}%)
            </div>
        `;
    });

    if (data.io) {
        html += `
            <h4 style="margin-top: 20px;">I/O do Disco</h4>
            <table class="info-table">
                <tr><td>Leitura:</td><td>${formatBytes(data.io.read_bytes)}</td></tr>
                <tr><td>Escrita:</td><td>${formatBytes(data.io.write_bytes)}</td></tr>
                <tr><td>Operações Leitura:</td><td>${data.io.read_count}</td></tr>
                <tr><td>Operações Escrita:</td><td>${data.io.write_count}</td></tr>
            </table>
        `;
    }

    document.getElementById('disk-detail').innerHTML = html;
}

function displayNetworkDetails(data) {
    const html = `
        <table class="info-table">
            <tr><td>Bytes Enviados:</td><td>${formatBytes(data.io.bytes_sent)}</td></tr>
            <tr><td>Bytes Recebidos:</td><td>${formatBytes(data.io.bytes_recv)}</td></tr>
            <tr><td>Pacotes Enviados:</td><td>${data.io.packets_sent}</td></tr>
            <tr><td>Pacotes Recebidos:</td><td>${data.io.packets_recv}</td></tr>
            <tr><td>Erros Entrada:</td><td>${data.io.errin}</td></tr>
            <tr><td>Erros Saída:</td><td>${data.io.errout}</td></tr>
            <tr><td>Perdas Entrada:</td><td>${data.io.dropin}</td></tr>
            <tr><td>Perdas Saída:</td><td>${data.io.dropout}</td></tr>
        </table>
    `;
    document.getElementById('network-detail').innerHTML = html;
}

function displayProcessesDetails(processes) {
    let html = '<h4>Top 20 Processos por Uso de CPU</h4>';

    processes.forEach((proc, index) => {
        html += `
            <div class="result-item">
                ${index + 1}. <strong>${proc.name}</strong> (PID: ${proc.pid})<br>
                CPU: ${(proc.cpu_percent || 0).toFixed(1)}% | Memória: ${(proc.memory_percent || 0).toFixed(2)}%
            </div>
        `;
    });

    document.getElementById('processes-detail').innerHTML = html;
}

// ==================== RECOMENDAÇÕES ====================
async function getRecommendations() {
    const listDiv = document.getElementById('recommendations-list');
    listDiv.innerHTML = '<div class="loading"><div class="spinner"></div>Gerando recomendações...</div>';

    try {
        const data = await fetch(`${API_BASE_URL}/maintenance/recommendations`).then(r => r.json());
        displayRecommendations(data);
    } catch (error) {
        listDiv.innerHTML = `<div class="result-item">Erro ao gerar recomendações: ${error.message}</div>`;
    }
}

function displayRecommendations(data) {
    const listDiv = document.getElementById('recommendations-list');
    let html = `<h3>Recomendações - Saúde: ${data.health_score.toFixed(0)}/100</h3>`;

    data.recommendations.forEach(rec => {
        html += `
            <div class="recommendation-card ${rec.priority}">
                <h4>📋 ${rec.issue}</h4>
                <p>${rec.description}</p>
                <h5>Ações Recomendadas:</h5>
                <ul>
                    ${rec.actions.map(action => `<li>${action}</li>`).join('')}
                </ul>
                <small>Prioridade: ${rec.priority.toUpperCase()} | Categoria: ${rec.category}</small>
            </div>
        `;
    });

    listDiv.innerHTML = html;
}

// ==================== SUPORTE ====================
function handleChatKeypress(event) {
    if (event.key === 'Enter') {
        sendChatMessage();
    }
}

async function sendChatMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();

    if (!message) return;

    // Mostrar mensagem do usuário
    addChatMessage(message, 'user');
    input.value = '';

    // Mostrar indicador de digitação do bot enquanto aguarda a resposta
    showTypingIndicator();

    try {
        const response = await fetch(`${API_BASE_URL}/support/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        }).then(r => r.json());

        console.log(response);

        // Remover indicador de digitação antes de adicionar a resposta real
        removeTypingIndicator();

        // Formatar/sanitizar a resposta antes de mostrar ao usuário
        const formatted = formatBotResponse(response);
        addChatMessage(formatted, 'bot');
    } catch (error) {
        removeTypingIndicator();
        addChatMessage('Desculpe, ocorreu um erro ao processar sua mensagem.', 'bot');
    }
}

// Adiciona um indicador de digitação temporário (aparece como mensagem do bot)
function showTypingIndicator() {
    const messagesDiv = document.getElementById('chat-messages');
    // Se já existir, não duplicar
    if (document.getElementById('typing-indicator')) return;

    const typingDiv = document.createElement('div');
    typingDiv.id = 'typing-indicator';
    typingDiv.className = 'message bot-message typing';
    typingDiv.innerHTML = `<p><span class="dot"></span><span class="dot"></span><span class="dot"></span></p>`;
    messagesDiv.appendChild(typingDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function removeTypingIndicator() {
    const typing = document.getElementById('typing-indicator');
    if (typing) typing.parentNode.removeChild(typing);
}

// Escapa caracteres HTML para evitar XSS ao usar innerHTML
function escapeHtml(unsafe) {
    if (unsafe === null || unsafe === undefined) return '';
    return String(unsafe)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

// Formata a resposta recebida da API para exibir no chat.
// Aceita objetos no formato bruto da SDK ou o formato simplificado { response: 'texto' }.
function formatBotResponse(apiResponse) {
    if (!apiResponse) return '--- Sem resposta ---';

    // Caso comum: backend já retornou { response: 'texto' }
    if (typeof apiResponse === 'object' && apiResponse.response) {
        const raw = apiResponse.response;
        // Substitui quebras de linha por <br> e escapa HTML
        return escapeHtml(raw).replace(/\n/g, '<br>');
    }

    // Se a API retornou uma string direta
    if (typeof apiResponse === 'string') {
        return escapeHtml(apiResponse).replace(/\n/g, '<br>');
    }

    // Tentar extrair texto de um possível objeto da SDK (candidates...parts...text)
    try {
        if (apiResponse.candidates && apiResponse.candidates.length > 0) {
            const candidate = apiResponse.candidates[0];
            if (candidate.content && candidate.content.parts && candidate.content.parts.length > 0) {
                const text = candidate.content.parts[0].text;
                return escapeHtml(text).replace(/\n/g, '<br>');
            }
        }

        // Outras formas: apiResponse.text or apiResponse.output_text
        if (apiResponse.text) return escapeHtml(apiResponse.text).replace(/\n/g, '<br>');
        if (apiResponse.output_text) return escapeHtml(apiResponse.output_text).replace(/\n/g, '<br>');
    } catch (e) {
        // cairá para fallback abaixo
    }

    // Fallback: mostrar representação JSON curta
    try {
        const short = JSON.stringify(apiResponse);
        return escapeHtml(short).replace(/\n/g, '<br>');
    } catch (e) {
        return '--- Resposta inválida ---';
    }
}

function addChatMessage(text, sender) {
    const messagesDiv = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.innerHTML = `<p>${text}</p>`;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// ==================== UTILIDADES ====================
function formatBytes(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return (bytes / Math.pow(k, i)).toFixed(2) + ' ' + sizes[i];
}

function startAutoUpdate() {
    // Atualizar dashboard a cada 5 segundos
    updateInterval = setInterval(() => {
        if (currentSection === 'dashboard') {
            loadDashboard();
        }
    }, 5000);
}

// Parar atualização ao descarregar página
window.addEventListener('beforeunload', () => {
    clearInterval(updateInterval);
});

// ==================== EXPORTAÇÃO DE RELATÓRIOS ====================
async function exportReportText() {
    try {
        const response = await fetch(`${API_BASE_URL}/reports/text`);
        const blob = await response.blob();
        downloadFile(blob, 'relatorio_manutencao.txt', 'text/plain');
    } catch (error) {
        alert('Erro ao exportar relatório: ' + error.message);
    }
}

async function exportReportJSON() {
    try {
        const response = await fetch(`${API_BASE_URL}/reports/json`);
        const blob = await response.blob();
        downloadFile(blob, 'relatorio_manutencao.json', 'application/json');
    } catch (error) {
        alert('Erro ao exportar relatório: ' + error.message);
    }
}

async function exportReportHTML() {
    try {
        const response = await fetch(`${API_BASE_URL}/reports/html`);
        const blob = await response.blob();
        downloadFile(blob, 'relatorio_manutencao.html', 'text/html');
    } catch (error) {
        alert('Erro ao exportar relatório: ' + error.message);
    }
}

function downloadFile(blob, filename, mimeType) {
    const url = window.URL.createObjectURL(new Blob([blob], { type: mimeType }));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    link.parentNode.removeChild(link);
    window.URL.revokeObjectURL(url);
}
