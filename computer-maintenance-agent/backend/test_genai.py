import os
from google import genai

key = os.environ.get('GEMINI_API_KEY')
model = os.environ.get('GEMINI_MODEL', 'gemini-2.5-flash')
print('GEMINI_API_KEY set:', bool(key))
print('Using model:', model)

client = genai.Client(api_key=key)
try:
    response = client.models.generate_content(
        model=model, contents='Explique em português, passo a passo, como reduzir o uso de CPU em Windows. Resuma em até 200 tokens')
    text = getattr(response, 'text', None)
    if text is None:
        print('Response object:', response)
    else:
        print('Response text (truncated 1000 chars):')
        print(text[:1000])
except Exception as e:
    print('ERROR:', type(e), e)
