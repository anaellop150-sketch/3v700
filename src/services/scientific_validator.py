
import logging
from typing import Dict, List, Any, Tuple
import statistics
from datetime import datetime

logger = logging.getLogger(__name__)

class ScientificValidator:
    """Validador científico para análises de mercado"""
    
    def __init__(self):
        self.min_sample_size = 30
        self.min_source_credibility = 0.7
        self.required_statistical_fields = ['sample_size', 'confidence_interval', 'methodology']
    
    def validate_phase_output(self, phase_name: str, data: Dict[str, Any]) -> Tuple[bool, float, List[str]]:
        """Valida output de uma fase com critérios científicos"""
        
        issues = []
        scores = {}
        
        # 1. Verificar fontes reais
        source_score = self._check_sources(data)
        scores['sources'] = source_score
        if source_score < self.min_source_credibility:
            issues.append(f"Fontes insuficientemente credíveis: {source_score:.2f}")
        
        # 2. Validar dados estatísticos
        stats_score = self._validate_stats(data)
        scores['statistics'] = stats_score
        if stats_score < 0.6:
            issues.append("Dados estatísticos insuficientes ou inválidos")
        
        # 3. Verificar tamanho da amostra
        sample_score = self._check_sample_size(data)
        scores['sample_size'] = sample_score
        if sample_score < 0.5:
            issues.append("Tamanho de amostra muito pequeno")
        
        # 4. Verificar metodologia
        method_score = self._check_methodology(data)
        scores['methodology'] = method_score
        if method_score < 0.5:
            issues.append("Metodologia não documentada adequadamente")
        
        # Score final
        quality_score = sum(scores.values()) / len(scores)
        is_valid = quality_score >= 0.7 and len(issues) <= 2
        
        logger.info(f"Validação {phase_name}: Score={quality_score:.2f}, Válido={is_valid}")
        
        return is_valid, quality_score, issues
    
    def _check_sources(self, data: Dict[str, Any]) -> float:
        """Verifica credibilidade das fontes"""
        score = 0.0
        
        # Procura por fontes oficiais
        data_str = str(data).lower()
        official_sources = ['ibge', 'sebrae', 'gov.br', 'bcb', 'bndes', 'receita federal']
        
        found_sources = sum(1 for source in official_sources if source in data_str)
        
        if found_sources > 0:
            score = min(found_sources / 3, 1.0)  # Máximo 1.0 com 3+ fontes
        
        # Verifica se tem URLs ou referências
        if 'http' in data_str or 'fonte:' in data_str:
            score += 0.2
        
        return min(score, 1.0)
    
    def _validate_stats(self, data: Dict[str, Any]) -> float:
        """Valida presença de dados estatísticos"""
        score = 0.0
        
        # Procura por dados numéricos
        data_str = str(data)
        import re
        
        # Percentuais
        percentages = re.findall(r'\d+(?:\.\d+)?%', data_str)
        if percentages:
            score += 0.3
        
        # Valores monetários
        monetary = re.findall(r'R\$\s*\d+', data_str)
        if monetary:
            score += 0.3
        
        # Números gerais
        numbers = re.findall(r'\b\d+(?:\.\d+)?\b', data_str)
        if len(numbers) >= 5:
            score += 0.4
        
        return min(score, 1.0)
    
    def _check_sample_size(self, data: Dict[str, Any]) -> float:
        """Verifica adequação do tamanho da amostra"""
        
        # Procura por indicações de tamanho de amostra
        data_str = str(data).lower()
        
        sample_indicators = [
            'empresas pesquisadas', 'respondentes', 'amostra', 'entrevistados',
            'participantes', 'casos analisados'
        ]
        
        if any(indicator in data_str for indicator in sample_indicators):
            return 0.8  # Indica que há consciência sobre amostra
        
        # Se tem dados estatísticos, assume amostra adequada
        if self._validate_stats(data) > 0.5:
            return 0.6
        
        return 0.3  # Score baixo se não há indicação de amostra
    
    def _check_methodology(self, data: Dict[str, Any]) -> float:
        """Verifica documentação da metodologia"""
        score = 0.0
        
        data_str = str(data).lower()
        
        # Palavras-chave metodológicas
        method_keywords = [
            'metodologia', 'método', 'pesquisa', 'coleta', 'análise',
            'critério', 'amostragem', 'período', 'fonte', 'base de dados'
        ]
        
        found_keywords = sum(1 for keyword in method_keywords if keyword in data_str)
        score = min(found_keywords / 5, 0.8)  # Máximo 0.8 com 5+ palavras
        
        # Verificações específicas
        if 'fonte:' in data_str or 'baseado em' in data_str:
            score += 0.2
        
        return min(score, 1.0)
    
    def generate_quality_report(self, phase_name: str, validation_result: Tuple[bool, float, List[str]]) -> Dict[str, Any]:
        """Gera relatório de qualidade"""
        
        is_valid, score, issues = validation_result
        
        return {
            'phase': phase_name,
            'validation_timestamp': datetime.now().isoformat(),
            'is_scientifically_valid': is_valid,
            'quality_score': round(score, 3),
            'issues_found': issues,
            'recommendation': self._get_recommendation(score),
            'next_steps': self._get_next_steps(issues)
        }
    
    def _get_recommendation(self, score: float) -> str:
        """Gera recomendação baseada no score"""
        if score >= 0.9:
            return "Excelente qualidade científica"
        elif score >= 0.7:
            return "Qualidade científica adequada"
        elif score >= 0.5:
            return "Qualidade científica limitada - melhorias necessárias"
        else:
            return "Qualidade científica insuficiente - revisão obrigatória"
    
    def _get_next_steps(self, issues: List[str]) -> List[str]:
        """Sugere próximos passos baseado nos problemas"""
        if not issues:
            return ["Manter padrão de qualidade"]
        
        steps = []
        for issue in issues:
            if "fonte" in issue.lower():
                steps.append("Adicionar mais fontes oficiais (IBGE, Sebrae, gov.br)")
            elif "estatístic" in issue.lower():
                steps.append("Incluir mais dados numéricos e estatísticas")
            elif "amostra" in issue.lower():
                steps.append("Documentar tamanho e método de amostragem")
            elif "metodologia" in issue.lower():
                steps.append("Detalhar metodologia de coleta e análise")
        
        return steps

# Instância global
scientific_validator = ScientificValidator()
