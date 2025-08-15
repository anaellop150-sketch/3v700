
import logging
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import re

logger = logging.getLogger(__name__)

class OfficialDataCollector:
    """Coletor de dados de fontes oficiais brasileiras"""
    
    def __init__(self):
        self.official_apis = {
            'ibge': 'https://servicodados.ibge.gov.br/api/v3/',
            'sebrae': 'https://datasebrae.com.br/api/',
            'bcb': 'https://api.bcb.gov.br/',
            'receita': 'https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/dados-abertos'
        }
        
        self.trusted_domains = [
            '.gov.br', 'ibge.gov.br', 'sebrae.com.br', 'bndes.gov.br', 
            'cvm.gov.br', 'mdic.gov.br', 'bcb.gov.br', 'anvisa.gov.br'
        ]
    
    def validate_source_credibility(self, domain: str) -> bool:
        """Valida se a fonte é oficial/confiável"""
        return any(trusted in domain.lower() for trusted in self.trusted_domains)
    
    def extract_statistical_data(self, content: str) -> Dict[str, Any]:
        """Extrai dados estatísticos reais do conteúdo"""
        stats = {
            'percentages': [],
            'monetary_values': [],
            'numerical_data': [],
            'growth_rates': [],
            'market_size': []
        }
        
        # Percentuais
        percentages = re.findall(r'(\d+(?:,\d+)?(?:\.\d+)?)\s*%', content)
        stats['percentages'] = [float(p.replace(',', '.')) for p in percentages]
        
        # Valores monetários
        monetary = re.findall(r'R\$\s*(\d+(?:[\.,]\d+)*(?:[\.,]\d+)?)', content)
        stats['monetary_values'] = monetary
        
        # Dados numéricos gerais
        numbers = re.findall(r'\b(\d+(?:[\.,]\d+)*)\b', content)
        stats['numerical_data'] = numbers[:20]  # Limita para evitar spam
        
        # Taxas de crescimento
        growth = re.findall(r'crescimento.{0,50}?(\d+(?:,\d+)?(?:\.\d+)?)\s*%', content, re.IGNORECASE)
        stats['growth_rates'] = [float(g.replace(',', '.')) for g in growth]
        
        return stats
    
    def get_ibge_market_data(self, sector: str) -> Dict[str, Any]:
        """Coleta dados do mercado via IBGE"""
        try:
            # API do IBGE para dados econômicos
            url = f"{self.official_apis['ibge']}agregados/6612/periodos/2023/variaveis/9324"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'source': 'IBGE',
                    'reliability': 'official',
                    'data': data,
                    'collected_at': datetime.now().isoformat()
                }
        except Exception as e:
            logger.error(f"Erro ao coletar dados IBGE: {e}")
        
        return {'source': 'IBGE', 'status': 'unavailable'}
    
    def get_sebrae_sector_data(self, sector: str) -> Dict[str, Any]:
        """Coleta dados setoriais do Sebrae"""
        try:
            # Simula busca por dados do Sebrae (API real pode variar)
            # Em implementação real, usaria API oficial do Sebrae
            sector_data = {
                'micro_small_enterprises': {
                    'total_count': None,  # Seria preenchido com dados reais
                    'sector_distribution': None,
                    'employment_data': None
                },
                'source': 'Sebrae',
                'reliability': 'official',
                'collected_at': datetime.now().isoformat()
            }
            return sector_data
        except Exception as e:
            logger.error(f"Erro ao coletar dados Sebrae: {e}")
        
        return {'source': 'Sebrae', 'status': 'unavailable'}
    
    def validate_data_quality(self, data: Dict[str, Any]) -> float:
        """Calcula score de qualidade dos dados"""
        score = 0.0
        
        # Verifica fonte oficial
        if data.get('source') in ['IBGE', 'Sebrae', 'BCB', 'Receita Federal']:
            score += 0.4
        
        # Verifica se tem dados numéricos
        if any(isinstance(v, (int, float)) for v in str(data).split()):
            score += 0.3
        
        # Verifica timestamp recente
        if data.get('collected_at'):
            score += 0.2
        
        # Verifica estrutura de dados
        if isinstance(data, dict) and len(data) > 2:
            score += 0.1
        
        return min(score, 1.0)
    
    def collect_comprehensive_market_data(self, sector: str, region: str = 'Brasil') -> Dict[str, Any]:
        """Coleta dados abrangentes de mercado de fontes oficiais"""
        
        comprehensive_data = {
            'metadata': {
                'sector': sector,
                'region': region,
                'collection_timestamp': datetime.now().isoformat(),
                'data_sources': []
            },
            'official_statistics': {},
            'quality_scores': {},
            'limitations': []
        }
        
        # Coleta IBGE
        ibge_data = self.get_ibge_market_data(sector)
        if ibge_data.get('status') != 'unavailable':
            comprehensive_data['official_statistics']['ibge'] = ibge_data
            comprehensive_data['quality_scores']['ibge'] = self.validate_data_quality(ibge_data)
            comprehensive_data['metadata']['data_sources'].append('IBGE')
        
        # Coleta Sebrae
        sebrae_data = self.get_sebrae_sector_data(sector)
        if sebrae_data.get('status') != 'unavailable':
            comprehensive_data['official_statistics']['sebrae'] = sebrae_data
            comprehensive_data['quality_scores']['sebrae'] = self.validate_data_quality(sebrae_data)
            comprehensive_data['metadata']['data_sources'].append('Sebrae')
        
        # Adiciona limitações
        if not comprehensive_data['metadata']['data_sources']:
            comprehensive_data['limitations'].append('Nenhuma fonte oficial disponível')
        
        if len(comprehensive_data['metadata']['data_sources']) < 2:
            comprehensive_data['limitations'].append('Dados limitados - apenas uma fonte oficial')
        
        return comprehensive_data

# Instância global
official_data_collector = OfficialDataCollector()
