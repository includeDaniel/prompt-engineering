"""
Cliente simples para integrar com um endpoint de geração (Gemini/Generative API).

Comportamento:
- Se `GEMINI_ENDPOINT` não estiver definido, o cliente será considerado desabilitado.
- Envia POST JSON com payload {'prompt': message} por padrão. O formato do payload pode ser adaptado
  pelo usuário apontando `GEMINI_ENDPOINT` para o endpoint adequado (por exemplo, Generative API ou um proxy).
- Usa `GEMINI_API_KEY` em header Authorization Bearer se disponível, ou envia como parâmetro `key`.

Observação: Não incluo chamadas a bibliotecas proprietárias. O usuário deve configurar `GEMINI_ENDPOINT`
e `GEMINI_API_KEY` em variáveis de ambiente. Em ausência dessas variáveis, o sistema cairá para o comportamento
de resposta local (fallback já existente).
"""
from __future__ import annotations

import os
import requests
from typing import Optional


class GeminiClient:
    """Cliente HTTP genérico para um endpoint de geração de texto (Gemini).

    Expected env vars:
    - GEMINI_ENDPOINT: URL completa para chamada POST (ex: https://.../generate)
    - GEMINI_API_KEY: (opcional) chave para enviar como Bearer token
    - GEMINI_MODEL: (opcional) nome do modelo a incluir no payload
    """

    def __init__(self):
        # Espera variáveis de ambiente padronizadas
        self.endpoint = os.environ.get('GEMINI_ENDPOINT')
        self.api_key = os.environ.get('GEMINI_API_KEY')
        self.model = os.environ.get('GEMINI_MODEL')

    @property
    def enabled(self) -> bool:
        return bool(self.endpoint)

    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.2) -> Optional[str]:
        """Envia o prompt para o endpoint configurado e retorna o texto gerado.

        Retorna None em caso de falha ou se o cliente não estiver configurado.
        """
        if not self.enabled:
            return None

        headers = {'Content-Type': 'application/json'}
        if self.api_key:
            # Preferir Authorization Bearer
            headers['Authorization'] = f'Bearer {self.api_key}'

        # Estrutura genérica do payload; alguns endpoints podem esperar outro formato.
        payload = {
            'prompt': prompt,
            'max_tokens': max_tokens,
            'temperature': temperature
        }
        if self.model:
            payload['model'] = self.model

        try:
            # If google genai client is available and API key is provided, prefer it
            try:
                from google import genai  # type: ignore
            except Exception:
                genai = None

            if genai is not None and self.api_key:
                try:
                    client = genai.Client(api_key=self.api_key)
                    # The library expects model and contents
                    resp = client.models.generate_content(
                        model=self.model or payload.get('model'), contents=prompt)
                    # The response object used in examples exposes .text
                    if hasattr(resp, 'text'):
                        return getattr(resp, 'text')
                    # Fallback: try to coerce to string
                    return str(resp)
                except Exception:
                    # If genai call fails, fall back to HTTP variant below
                    pass

            # Special-case: Google Gemini / Generative API via HTTP expects API key as query param
            # and a different payload shape. Detect common hostname and adapt.
            params = None
            endpoint = self.endpoint
            if self.api_key and endpoint and ('gemini.googleapis.com' in endpoint or 'generativelanguage' in endpoint):
                params = {'key': self.api_key}
                # Google expects prompt in a field like 'prompt' or 'input'; include model
                # if available. We'll prefer the shape {model, prompt:{text:...}}
                payload = {
                    'model': self.model or payload.get('model'),
                    'prompt': {'text': prompt}
                }

            # Tenta enviar como POST JSON.
            resp = requests.post(endpoint, json=payload,
                                 headers=headers, params=params, timeout=30)
            resp.raise_for_status()

            # Tentar extrair texto de forma robusta.
            data = resp.json()
            # Possíveis locais onde texto pode estar, dependendo da API:
            # - data['output'] ou data['outputs'][0]['text']
            # - data['candidates'][0]['output']
            # - data['content']
            # Vamos checar várias opções.
            if isinstance(data, dict):
                # common shapes
                for key in ('output', 'text', 'content'):
                    if key in data and isinstance(data[key], str):
                        return data[key]

                if 'outputs' in data and isinstance(data['outputs'], list) and data['outputs']:
                    first = data['outputs'][0]
                    if isinstance(first, dict):
                        for k in ('text', 'output', 'content'):
                            if k in first and isinstance(first[k], str):
                                return first[k]

                if 'candidates' in data and isinstance(data['candidates'], list) and data['candidates']:
                    cand = data['candidates'][0]
                    if isinstance(cand, dict) and 'output' in cand:
                        return cand['output']

                # fallback: try to join strings from any leaf values
                def find_first_str(obj):
                    if isinstance(obj, str):
                        return obj
                    if isinstance(obj, dict):
                        for v in obj.values():
                            r = find_first_str(v)
                            if r:
                                return r
                    if isinstance(obj, list):
                        for v in obj:
                            r = find_first_str(v)
                            if r:
                                return r
                    return None

                return find_first_str(data)

            # If not JSON, return raw text
            return resp.text
        except Exception:
            # Não lançar exceção; caller fará fallback
            return None


_default_client: Optional[GeminiClient] = None


def get_gemini_client() -> GeminiClient:
    global _default_client
    if _default_client is None:
        _default_client = GeminiClient()
    return _default_client
