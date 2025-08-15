#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - MCP Supadata Manager CORRIGIDO
Cliente para pesquisa REAL em redes sociais
"""

import os
import requests
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class MCPSupadataManager:
    """Cliente CORRIGIDO para pesquisa em redes sociais"""
    
    def __init__(self):
        """Inicializa o cliente Supadata CORRIGIDO"""
        # URLs corretas para Supadata
        self.base_url = os.getenv("SUPADATA_API_URL", "https://api.supadata.ai/v1")
        self.api_key = os.getenv("SUPADATA_API_KEY")
        
        # Headers CORRETOS
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}" if self.api_key else "",
            "User-Agent": "ARQV30-Enhanced/2.0",
            "Accept": "application/json"
        }
        
        # Configuração de disponibilidade REAL
        self.is_available = bool(self.api_key)
        
        if self.is_available:
            logger.info("✅ MCP Supadata Manager ATIVO - pesquisas em redes sociais habilitadas")
            
        # Ativa modo de produção
        self.production_mode = True
    
    def search_youtube(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """Busca REAL no YouTube"""
        
        try:
            endpoint = f"{self.base_url}/youtube/search"
            payload = {
                "q": f"{query} Brasil",
                "maxResults": max_results,
                "regionCode": "BR",
                "relevanceLanguage": "pt",
                "type": "video",
                "order": "relevance"
            }
            
            response = requests.post(
                endpoint,
                json=payload,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                processed_results = []
                for item in data.get("items", []):
                    snippet = item.get("snippet", {})
                    processed_results.append({
                        "title": snippet.get("title", ""),
                        "description": snippet.get("description", ""),
                        "channel": snippet.get("channelTitle", ""),
                        "published_at": snippet.get("publishedAt", ""),
                        "view_count": item.get("statistics", {}).get("viewCount", "0"),
                        "url": f"https://youtube.com/watch?v={item.get('id', {}).get('videoId', '')}",
                        "platform": "youtube",
                        "query_used": query
                    })
                
                return {
                    "success": True,
                    "platform": "youtube",
                    "results": processed_results,
                    "total_found": len(processed_results),
                    "query": query
                }
            else:
                logger.error(f"YouTube API error: {response.status_code}")
                raise ValueError("Erro na API do YouTube. Dados simulados não permitidos.")
                
        except Exception as e:
            logger.error(f"Erro YouTube: {e}")
            raise ValueError("Erro ao buscar dados do YouTube. Dados simulados não permitidos.")
    
    def search_twitter(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """Busca REAL no Twitter/X"""
        
        try:
            endpoint = f"{self.base_url}/twitter/search"
            payload = {
                "query": f"{query} lang:pt",
                "max_results": max_results,
                "expansions": "author_id,geo.place_id",
                "tweet.fields": "created_at,public_metrics,lang"
            }
            
            response = requests.post(
                endpoint,
                json=payload,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                processed_results = []
                for item in data.get("data", []):
                    metrics = item.get("public_metrics", {})
                    processed_results.append({
                        "text": item.get("text", ""),
                        "author_id": item.get("author_id", ""),
                        "created_at": item.get("created_at", ""),
                        "retweet_count": metrics.get("retweet_count", 0),
                        "like_count": metrics.get("like_count", 0),
                        "reply_count": metrics.get("reply_count", 0),
                        "quote_count": metrics.get("quote_count", 0),
                        "url": f"https://twitter.com/i/status/{item.get("id", "")}",
                        "platform": "twitter",
                        "query_used": query
                    })
                
                return {
                    "success": True,
                    "platform": "twitter",
                    "results": processed_results,
                    "total_found": len(processed_results),
                    "query": query
                }
            else:
                logger.error(f"Twitter API error: {response.status_code}")
                raise ValueError("Erro na API do Twitter. Dados simulados não permitidos.")
                
        except Exception as e:
            logger.error(f"Erro Twitter: {e}")
            raise ValueError("Erro ao buscar dados do Twitter. Dados simulados não permitidos.")
    
    def search_linkedin(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """Busca REAL no LinkedIn"""
        
        try:
            endpoint = f"{self.base_url}/linkedin/search"
            payload = {
                "keywords": query,
                "count": max_results,
                "facets": "geoUrn:br"
            }
            
            response = requests.post(
                endpoint,
                json=payload,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                processed_results = []
                for item in data.get("elements", []):
                    processed_results.append({
                        "title": item.get("title", ""),
                        "content": item.get("content", ""),
                        "author": item.get("author", {}).get("name", ""),
                        "company": item.get("author", {}).get("company", ""),
                        "published_date": item.get("publishedDate", ""),
                        "likes": item.get("socialCounts", {}).get("numLikes", 0),
                        "comments": item.get("socialCounts", {}).get("numComments", 0),
                        "shares": item.get("socialCounts", {}).get("numShares", 0),
                        "url": item.get("url", ""),
                        "platform": "linkedin",
                        "query_used": query
                    })
                
                return {
                    "success": True,
                    "platform": "linkedin",
                    "results": processed_results,
                    "total_found": len(processed_results),
                    "query": query
                }
            else:
                logger.error(f"LinkedIn API error: {response.status_code}")
                raise ValueError("Erro na API do LinkedIn. Dados simulados não permitidos.")
                
        except Exception as e:
            logger.error(f"Erro LinkedIn: {e}")
            raise ValueError("Erro ao buscar dados do LinkedIn. Dados simulados não permitidos.")
    
    def search_instagram(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """Busca REAL no Instagram"""
        
        try:
            endpoint = f"{self.base_url}/instagram/search"
            payload = {
                "q": query,
                "count": max_results,
                "type": "media"
            }
            
            response = requests.post(
                endpoint,
                json=payload,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                processed_results = []
                for item in data.get("data", []):
                    processed_results.append({
                        "caption": item.get("caption", {}).get("text", ""),
                        "media_type": item.get("media_type", ""),
                        "like_count": item.get("like_count", 0),
                        "comment_count": item.get("comments_count", 0),
                        "timestamp": item.get("timestamp", ""),
                        "url": item.get("permalink", ""),
                        "username": item.get("username", ""),
                        "platform": "instagram",
                        "query_used": query
                    })
                
                return {
                    "success": True,
                    "platform": "instagram",
                    "results": processed_results,
                    "total_found": len(processed_results),
                    "query": query
                }
            else:
                logger.error(f"Instagram API error: {response.status_code}")
                raise ValueError("Erro na API do Instagram. Dados simulados não permitidos.")
                
        except Exception as e:
            logger.error(f"Erro Instagram: {e}")
            raise ValueError("Erro ao buscar dados do Instagram. Dados simulados não permitidos.")
    
    def search_all_platforms(self, query: str, max_results_per_platform: int = 5) -> Dict[str, Any]:
        """Busca UNIFICADA em todas as plataformas"""
        
        logger.info(f"🔍 Iniciando busca UNIFICADA para: {query}")
        
        results = {
            "query": query,
            "platforms": [],
            "total_results": 0,
            "youtube": {},
            "twitter": {},
            "linkedin": {},
            "instagram": {}
        }
        
        # YouTube
        try:
            youtube_results = self.search_youtube(query, max_results_per_platform)
            if youtube_results.get("success"):
                results["youtube"] = youtube_results
                results["platforms"].append("youtube")
                results["total_results"] += len(youtube_results.get("results", []))
                logger.info(f"✅ YouTube: {len(youtube_results.get("results", []))} posts")
        except Exception as e:
            logger.warning(f"YouTube search failed: {e}")
        
        # Twitter
        try:
            twitter_results = self.search_twitter(query, max_results_per_platform)
            if twitter_results.get("success"):
                results["twitter"] = twitter_results
                results["platforms"].append("twitter")
                results["total_results"] += len(twitter_results.get("results", []))
                logger.info(f"✅ Twitter: {len(twitter_results.get("results", []))} posts")
        except Exception as e:
            logger.warning(f"Twitter search failed: {e}")
        
        # LinkedIn
        try:
            linkedin_results = self.search_linkedin(query, max_results_per_platform)
            if linkedin_results.get("success"):
                results["linkedin"] = linkedin_results
                results["platforms"].append("linkedin")
                results["total_results"] += len(linkedin_results.get("results", []))
                logger.info(f"✅ LinkedIn: {len(linkedin_results.get("results", []))} posts")
        except Exception as e:
            logger.warning(f"LinkedIn search failed: {e}")
        
        # Instagram
        try:
            instagram_results = self.search_instagram(query, max_results_per_platform)
            if instagram_results.get("success"):
                results["instagram"] = instagram_results
                results["platforms"].append("instagram")
                results["total_results"] += len(instagram_results.get("results", []))
                logger.info(f"✅ Instagram: {len(instagram_results.get("results", []))} posts")
        except Exception as e:
            logger.warning(f"Instagram search failed: {e}")
        
        results["success"] = len(results["platforms"]) > 0
        
        logger.info(f"🎯 Busca UNIFICADA concluída: {results["total_results"]} posts de {len(results["platforms"])} plataformas")
        
        return results
    
    def analyze_sentiment(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Análise de sentimento APRIMORADA"""
        
        if not posts:
            return {"sentiment": "neutral", "score": 0.0, "analysis_quality": "no_data"}
        
        # Análise aprimorada de sentimento
        positive_words = [
            "bom", "ótimo", "excelente", "recomendo", "perfeito", "incrível", 
            "fantástico", "maravilhoso", "adorei", "amei", "top", "show",
            "sucesso", "qualidade", "satisfeito", "feliz", "positivo"
        ]
        
        negative_words = [
            "ruim", "péssimo", "terrível", "não recomendo", "horrível", 
            "decepcionante", "problema", "erro", "falha", "insatisfeito",
            "frustrado", "negativo", "pior", "odiei", "detestei"
        ]
        
        neutral_words = [
            "ok", "normal", "regular", "médio", "comum", "básico"
        ]
        
        total_posts = len(posts)
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        for post in posts:
            # Extrai texto do post
            text = ""
            if "text" in post:
                text = post["text"].lower()
            elif "caption" in post:
                text = post["caption"].lower()
            elif "content" in post:
                text = post["content"].lower()
            elif "title" in post:
                text = post["title"].lower()
            elif "description" in post:
                text = post["description"].lower()
            
            # Análise de sentimento
            positive_score = sum(1 for word in positive_words if word in text)
            negative_score = sum(1 for word in negative_words if word in text)
            neutral_score = sum(1 for word in neutral_words if word in text)
            
            if positive_score > negative_score and positive_score > neutral_score:
                positive_count += 1
            elif negative_score > positive_score and negative_score > neutral_score:
                negative_count += 1
            else:
                neutral_count += 1
        
        # Calcula sentimento geral
        if positive_count > negative_count and positive_count > neutral_count:
            sentiment = "positive"
            score = (positive_count / total_posts) * 100
        elif negative_count > positive_count and negative_count > neutral_count:
            sentiment = "negative"
            score = (negative_count / total_posts) * -100
        else:
            sentiment = "neutral"
            score = 0.0
        
        return {
            "sentiment": sentiment,
            "score": round(score, 2),
            "positive_posts": positive_count,
            "negative_posts": negative_count,
            "neutral_posts": neutral_count,
            "total_posts": total_posts,
            "confidence": min(abs(score) / 50, 1.0),  # Confiança baseada na polarização
            "analysis_quality": "real_analysis"
        }

# Instância global CORRIGIDA
mcp_supadata_manager = MCPSupadataManager()

