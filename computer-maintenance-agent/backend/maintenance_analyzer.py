"""
Minimal MaintenanceAnalyzer that uses Gemini exclusively for support chat responses.

This module intentionally keeps other methods minimal/stubbed so the Flask
routes in `app.py` continue to work without the previous local NLP/fallback
logic. The `process_support_message` method will attempt to generate a reply
via the Gemini client and return informative messages when Gemini is not
configured or an error occurs.
"""

from datetime import datetime
import platform
from typing import Any, Dict
from gemini_client import get_gemini_client


class MaintenanceAnalyzer:
    """Lightweight analyzer: Gemini-only chat, minimal stubs for other APIs."""

    def __init__(self) -> None:
        pass

    def analyze_and_recommend(self, diagnostics: Dict[str, Any]) -> Dict[str, Any]:
        """Return a minimal recommendations response (no local analysis).

        Kept to avoid breaking callers. If you want Gemini to produce
        recommendations, we can delegate here as well — ask me to enable it.
        """
        return {
            'timestamp': datetime.now().isoformat(),
            'total_recommendations': 0,
            'recommendations': [],
            'health_score': diagnostics.get('health_score', 0) if isinstance(diagnostics, dict) else 0
        }

    def check_services_status(self) -> Dict[str, Any]:
        """Return a minimal services status structure."""
        return {
            'timestamp': datetime.now().isoformat(),
            'system': platform.system(),
            'services': []
        }

    def process_support_message(self, message: str) -> str:
        """Generate a support response using the configured Gemini client.

        Returns a human-readable string. If Gemini is not configured, returns
        instructions for the user to enable it. Exceptions are caught and
        returned as error messages (so the API keeps responding).
        """
        try:
            from gemini_client import generate_gemini_response

            gemini = get_gemini_client()
            if gemini is None:
                return (
                    "O serviço Gemini não está configurado. Para habilitar o assistente baseado em "
                    "Gemini, defina a variável de ambiente `GEMINI_API_KEY`."
                )

            prompt = (
                f"Usuário: {message}\n\n"
                "Responda de forma clara, em português, com instruções passo a passo apropriadas para um técnico de informática."
            )

            response = generate_gemini_response(prompt, gemini)
            if response:
                # Garantir que retornamos string
                return str(response)

            return "Desculpe, o serviço Gemini não retornou uma resposta. Tente novamente mais tarde."
        except Exception as exc:
            return f"Erro ao contactar Gemini: {str(exc)}"
