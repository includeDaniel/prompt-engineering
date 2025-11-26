#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para testar o endpoint /api/health do servidor Flask.
"""
import sys
import requests
import json


def test_health_endpoint():
    try:
        url = "http://127.0.0.1:5000/api/health"
        print(f"[*] Testando endpoint: {url}")

        response = requests.get(url, timeout=5)

        print(f"[✓] Status code: {response.status_code}")
        print(f"[✓] Resposta:")

        try:
            data = response.json()
            print(json.dumps(data, indent=2, ensure_ascii=False))
            return True
        except json.JSONDecodeError:
            print(f"    {response.text}")
            return False

    except requests.exceptions.ConnectionError as e:
        print(f"[✗] ERRO: Não consegui conectar ao servidor.")
        print(f"    {e}")
        return False
    except requests.exceptions.Timeout as e:
        print(f"[✗] ERRO: Timeout na requisição.")
        print(f"    {e}")
        return False
    except Exception as e:
        print(f"[✗] ERRO inesperado: {type(e).__name__}")
        print(f"    {e}")
        return False


if __name__ == "__main__":
    success = test_health_endpoint()
    sys.exit(0 if success else 1)
