import os
import json
import google.generativeai as genai
from pdf2image import convert_from_path
from PIL import Image
import io
import base64

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_products_from_pdf(pdf_path: str):
    images = convert_from_path(pdf_path, dpi=200)
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    all_products = []
    
    for page_num, image in enumerate(images):
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        prompt = f"""
        Extraia todos os produtos desta página do PDF.
        Retorne um array JSON com os seguintes campos para cada produto:
        - name: nome do produto
        - price: preço (número)
        - category: categoria
        - image_url: imagem do produto em base64 (formato data:image/jpeg;base64,...) ou screenshot da seção do produto. Se não conseguir extrair a imagem completa, forneça um screenshot da seção do produto no PDF.
        
        Página {page_num + 1}:
        """
        
        response = model.generate_content([
            prompt,
            {"mime_type": "image/png", "data": img_base64}
        ])
        
        try:
            products = json.loads(response.text)
            all_products.extend(products)
        except:
            continue
    
    return all_products
