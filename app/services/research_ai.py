from openai import OpenAI
from typing import List, Dict, Any
from app.core.config import settings
import json

class ResearchAI:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.OPENROUTER_API_KEY
        )
        self.headers = {
            "HTTP-Referer": settings.SITE_URL,
            "X-Title": settings.SITE_NAME
        }
    
    async def search_research(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search for research papers and generate summaries using DeepSeek R1.
        """
        prompt = f"""
        Search for research papers about: {query}
        
        For each paper, provide:
        1. Title
        2. Authors
        3. Abstract
        4. Key findings
        5. Citation
        
        Format the response as a JSON array with the following structure:
        [
            {{
                "title": "Paper Title",
                "authors": ["Author 1", "Author 2"],
                "abstract": "Abstract text",
                "key_findings": ["Finding 1", "Finding 2"],
                "citation": "Citation in APA format"
            }}
        ]
        
        Limit to {max_results} most relevant papers.
        """
        
        try:
            completion = self.client.chat.completions.create(
                extra_headers=self.headers,
                model=settings.DEEPSEEK_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a research assistant specialized in academic paper analysis and summarization."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Parse the response
            response_text = completion.choices[0].message.content
            papers = json.loads(response_text)
            
            return papers
            
        except Exception as e:
            raise Exception(f"Error in research search: {str(e)}")
    
    async def analyze_paper(self, paper_content: str) -> Dict[str, Any]:
        """
        Analyze a specific research paper and provide detailed insights.
        """
        prompt = f"""
        Analyze the following research paper and provide:
        1. Main research question
        2. Methodology
        3. Key findings
        4. Limitations
        5. Future research directions
        6. Practical applications
        
        Paper content:
        {paper_content}
        
        Format the response as a JSON object.
        """
        
        try:
            completion = self.client.chat.completions.create(
                extra_headers=self.headers,
                model=settings.DEEPSEEK_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a research analyst specialized in academic paper analysis."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Parse the response
            response_text = completion.choices[0].message.content
            analysis = json.loads(response_text)
            
            return analysis
            
        except Exception as e:
            raise Exception(f"Error in paper analysis: {str(e)}")
    
    async def generate_literature_review(self, topic: str, papers: List[Dict[str, Any]]) -> str:
        """
        Generate a comprehensive literature review based on multiple papers.
        """
        papers_text = json.dumps(papers, indent=2)
        prompt = f"""
        Generate a comprehensive literature review on the topic: {topic}
        
        Based on the following papers:
        {papers_text}
        
        Include:
        1. Introduction to the topic
        2. Synthesis of key findings
        3. Comparison of methodologies
        4. Identification of research gaps
        5. Future research directions
        6. Conclusion
        
        Format the response in markdown.
        """
        
        try:
            completion = self.client.chat.completions.create(
                extra_headers=self.headers,
                model=settings.DEEPSEEK_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a research synthesis expert specialized in literature reviews."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Error in literature review generation: {str(e)}") 