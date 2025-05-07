import google.generativeai as genai
from PIL import Image
import requests
from bs4 import BeautifulSoup
import os
import json
from typing import List, Dict, Any
import pdfkit
from app.core.config import settings
from transformers import CLIPProcessor, CLIPModel
import torch

class NotesGenerator:
    def __init__(self):
        # Initialize Gemini
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
        
        # Initialize CLIP for image validation
        self.clip_model = CLIPModel.from_pretrained(settings.CLIP_MODEL)
        self.clip_processor = CLIPProcessor.from_pretrained(settings.CLIP_MODEL)
        
    async def generate(
        self,
        topic: str,
        depth: str = "intermediate",
        include_diagrams: bool = True,
        include_tables: bool = True,
        style: str = "academic"
    ) -> Dict[str, Any]:
        # Generate text content using Gemini
        text_content = await self._generate_text(topic, depth, style)
        
        # Extract image placeholders and fetch relevant images
        image_placeholders = self._extract_image_placeholders(text_content)
        images = await self._fetch_and_validate_images(topic, image_placeholders)
        
        # Generate tables if requested
        tables = []
        if include_tables:
            tables = await self._generate_tables(topic, text_content)
        
        # Create PDF
        pdf_path = await self._create_pdf(text_content, images, tables)
        
        return {
            "pdf_url": f"/static/{os.path.basename(pdf_path)}",
            "text_content": text_content,
            "images": [img["url"] for img in images],
            "tables": tables
        }
    
    async def _generate_text(self, topic: str, depth: str, style: str) -> str:
        prompt = f"""
        Generate comprehensive study notes on the topic: {topic}
        Depth level: {depth}
        Style: {style}
        
        Include:
        1. Introduction and key concepts
        2. Detailed explanations
        3. Examples and applications
        4. [IMAGE] placeholders for relevant diagrams
        5. Important formulas and equations
        6. Summary and key takeaways
        
        Format the content in markdown.
        """
        
        response = await self.model.generate_content(prompt)
        return response.text
    
    def _extract_image_placeholders(self, text: str) -> List[str]:
        # Extract [IMAGE: description] placeholders
        import re
        return re.findall(r'\[IMAGE: (.*?)\]', text)
    
    async def _fetch_and_validate_images(self, topic: str, descriptions: List[str]) -> List[Dict[str, str]]:
        images = []
        for desc in descriptions:
            # Search for images using SerpAPI
            image_url = await self._search_image(f"{topic} {desc}")
            if image_url:
                # Validate image relevance using CLIP
                if await self._validate_image_relevance(image_url, desc):
                    images.append({
                        "url": image_url,
                        "description": desc
                    })
        return images
    
    async def _search_image(self, query: str) -> str:
        # Implement image search using SerpAPI
        # This is a placeholder - implement actual API call
        return ""
    
    async def _validate_image_relevance(self, image_url: str, description: str) -> bool:
        try:
            # Download and process image
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            
            # Process image and text with CLIP
            inputs = self.clip_processor(
                images=image,
                text=description,
                return_tensors="pt",
                padding=True
            )
            
            # Get similarity score
            outputs = self.clip_model(**inputs)
            similarity = outputs.logits_per_image.item()
            
            return similarity > 0.5  # Threshold for relevance
        except Exception:
            return False
    
    async def _generate_tables(self, topic: str, text_content: str) -> List[Dict[str, Any]]:
        # Generate tables using Gemini
        prompt = f"""
        Based on the following content about {topic}, generate relevant tables in JSON format:
        {text_content}
        
        Format each table as:
        {{
            "title": "Table Title",
            "headers": ["Header1", "Header2", ...],
            "rows": [["Data1", "Data2", ...], ...]
        }}
        """
        
        response = await self.model.generate_content(prompt)
        return json.loads(response.text)
    
    async def _create_pdf(self, text_content: str, images: List[Dict[str, str]], tables: List[Dict[str, Any]]) -> str:
        # Convert markdown to HTML
        html_content = self._markdown_to_html(text_content, images, tables)
        
        # Generate PDF
        pdf_path = os.path.join(settings.UPLOAD_DIR, f"notes_{int(time.time())}.pdf")
        pdfkit.from_string(html_content, pdf_path)
        
        return pdf_path
    
    def _markdown_to_html(self, text: str, images: List[Dict[str, str]], tables: List[Dict[str, Any]]) -> str:
        # Convert markdown to HTML with images and tables
        # This is a placeholder - implement actual conversion
        return text
    
    async def customize(self, pdf_file: UploadFile, modifications: str) -> Dict[str, Any]:
        # Implement PDF customization logic
        # This is a placeholder - implement actual customization
        return {"message": "Customization not implemented yet"} 