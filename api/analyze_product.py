import os
import json
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_product(product_data: dict):
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    prompt = f"""
    Analise o seguinte produto e retorne um JSON com:
    - recomendacao: COMPRAR | ANALISAR | EVITAR
    - score: número de 0 a 100
    - riscos: array de strings
    - oportunidades: array de strings
    - suggestedShippingMode: PAC | SEDEX | RETIRADA | MOTOBOY | N/A (baseado no peso, volume e tipo do produto)
    
    Produto: {json.dumps(product_data, ensure_ascii=False)}
    """
    
    response = model.generate_content(prompt)
    
    try:
        result = json.loads(response.text)
        return result
    except:
        return {
            "recomendacao": "ANALISAR",
            "score": 50,
            "riscos": ["Erro na análise"],
            "oportunidades": [],
            "suggestedShippingMode": "N/A"
        }
