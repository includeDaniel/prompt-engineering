"""
Gemini API client wrapper for the maintenance agent.
"""

import os
from google import genai


def get_gemini_client():
    """
    Initialize and return a Gemini API client.

    The API key should be set via environment variable GEMINI_API_KEY
    or in a .env file.

    Returns:
        genai.Client: Configured Gemini client, or None if not configured.
    """
    api_key = os.getenv('GEMINI_API_KEY')

    if not api_key:
        return None

    try:
        client = genai.Client(api_key=api_key)
        return client
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")
        return None


def generate_gemini_response(prompt: str, client=None) -> str:
    """
    Generate a response using Gemini API.

    Args:
        prompt: The prompt to send to Gemini
        client: Optional pre-configured Gemini client

    Returns:
        str: The generated response, or error message if generation fails
    """
    if client is None:
        client = get_gemini_client()

    if client is None:
        return "Gemini API não está configurado. Configure a chave GEMINI_API_KEY."

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        # Extrair o texto da resposta
        if response and response.candidates and len(response.candidates) > 0:
            candidate = response.candidates[0]
            if candidate.content and candidate.content.parts and len(candidate.content.parts) > 0:
                return candidate.content.parts[0].text
        return "Desculpe, não consegui gerar uma resposta. Tente novamente."
    except Exception as e:
        return f"Erro ao gerar resposta do Gemini: {str(e)}"
