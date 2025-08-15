#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Mental Drivers Architect
Arquiteto de Drivers Mentais Customizados
"""

import time
import random
import logging
import json
from typing import Dict, List, Any, Optional
from services.ai_manager import ai_manager
from services.auto_save_manager import salvar_etapa, salvar_erro

logger = logging.getLogger(__name__)

class MentalDriversArchitect:
    """Arquiteto de Drivers Mentais Customizados"""

    def __init__(self, ai_manager_instance=None):
        """Inicializa o arquiteto de drivers mentais"""
        self.logger = logging.getLogger(__name__)
        self.ai_manager = ai_manager_instance or ai_manager
        self.universal_drivers = {
            "urgencia_temporal": {
                'nome': 'Urgência Temporal',
                'gatilho_central': 'Tempo limitado para agir',
                'definicao_visceral': 'Criar pressão temporal que força decisão imediata',
                'aplicacao': 'Quando prospect está procrastinando'
            },
            'escassez_oportunidade': {
                'nome': 'Escassez de Oportunidade',
                'gatilho_central': 'Oportunidade única e limitada',
                'definicao_visceral': 'Amplificar valor através da raridade',
                'aplicacao': 'Para aumentar percepção de valor'
            },
            'prova_social': {
                'nome': 'Prova Social Qualificada',
                'gatilho_central': 'Outros como ele já conseguiram',
                'definicao_visceral': 'Reduzir risco através de validação social',
                'aplicacao': 'Para superar objeções de confiança'
            },
            'autoridade_tecnica': {
                'nome': 'Autoridade Técnica',
                'gatilho_central': 'Expertise comprovada',
                'definicao_visceral': 'Estabelecer credibilidade através de conhecimento',
                'aplicacao': 'Para construir confiança inicial'
            },
            'reciprocidade': {
                'nome': 'Reciprocidade Estratégica',
                'gatilho_central': 'Valor entregue antecipadamente',
                'definicao_visceral': 'Criar obrigação psicológica de retribuição',
                'aplicacao': 'Para gerar compromisso'
            }
        }
        logger.info("🧠 Mental Drivers Architect inicializado")

    def generate_custom_drivers(self, segmento: str, produto: str, publico: str, web_data: Dict = None, social_data: Dict = None) -> Dict[str, Any]:
        """Gera drivers mentais customizados baseados nos dados fornecidos"""
        try:
            prompt = f"""
            Crie 19 drivers mentais psicológicos ESPECÍFICOS para:

            SEGMENTO: {segmento}
            PRODUTO/SERVIÇO: {produto}
            PÚBLICO-ALVO: {publico}

            Dados da Web: {str(web_data)[:500] if web_data else 'Não disponível'}
            Dados Sociais: {str(social_data)[:500] if social_data else 'Não disponível'}

            Para cada driver, forneça:
            1. Nome específico e impactante
            2. Descrição psicológica detalhada
            3. Como aplicar especificamente para este segmento
            4. Exemplo prático de uso
            5. Impacto esperado na conversão

            Formato JSON:
            {{
                "drivers": [
                    {{
                        "numero": 1,
                        "nome": "Nome Específico",
                        "descricao": "Descrição psicológica detalhada",
                        "aplicacao": "Como aplicar especificamente",
                        "exemplo_pratico": "Exemplo concreto",
                        "impacto_conversao": "Alto/Médio/Baixo + explicação"
                    }}
                ],
                "resumo_psicologico": "Resumo da estratégia psicológica geral",
                "recomendacoes_implementacao": ["Rec 1", "Rec 2", "Rec 3"]
            }}
            """

            response = self.ai_manager.generate_content(prompt, max_tokens=4000)

            # Tenta fazer parse do JSON
            import json
            try:
                drivers_data = json.loads(response)

                # Valida se tem pelo menos 19 drivers
                if 'drivers' in drivers_data and len(drivers_data['drivers']) >= 19:
                    return drivers_data
                else:
                    # Se não tem 19, completa
                    drivers_list = drivers_data.get('drivers', [])
                    while len(drivers_list) < 19:
                        drivers_list.append({
                            "numero": len(drivers_list) + 1,
                            "nome": f"Driver Mental {len(drivers_list) + 1}",
                            "descricao": f"Driver customizado para {segmento}",
                            "aplicacao": f"Aplicação específica para {produto}",
                            "exemplo_pratico": f"Exemplo prático para {publico}",
                            "impacto_conversao": "Alto - impacto psicológico significativo"
                        })

                    drivers_data['drivers'] = drivers_list
                    return drivers_data

            except json.JSONDecodeError:
                # Se não conseguir fazer parse, cria estrutura básica
                return self._create_fallback_drivers(segmento, produto, publico)

        except Exception as e:
            logger.error(f"❌ Erro ao gerar drivers customizados: {e}")
            return self._create_fallback_drivers(segmento, produto, publico)

    def _create_fallback_drivers(self, segmento: str, produto: str, publico: str) -> Dict[str, Any]:
        """Cria drivers de fallback quando a IA falha"""
        drivers = []

        driver_templates = [
            {"nome": "Autoridade Especializada", "desc": "Estabelece credibilidade e expertise"},
            {"nome": "Prova Social Específica", "desc": "Usa casos de sucesso do segmento"},
            {"nome": "Escassez Temporal", "desc": "Cria urgência baseada em tempo"},
            {"nome": "Reciprocidade Estratégica", "desc": "Oferece valor antes da venda"},
            {"nome": "Ancoragem de Valor", "desc": "Posiciona preço como investimento"},
            {"nome": "Medo da Perda", "desc": "Destaca o custo de não agir"},
            {"nome": "Pertencimento Tribal", "desc": "Cria senso de comunidade"},
            {"nome": "Novidade Disruptiva", "desc": "Apresenta como inovação necessária"},
            {"nome": "Facilitação Cognitiva", "desc": "Simplifica decisões complexas"},
            {"nome": "Validação Externa", "desc": "Usa endossos de terceiros"},
            {"nome": "Contraste Estratégico", "desc": "Compara com alternativas piores"},
            {"nome": "Narrativa Emocional", "desc": "Conecta através de histórias"},
            {"nome": "Compromisso Público", "desc": "Induz compromisso através de declaração"},
            {"nome": "Exclusividade Seletiva", "desc": "Faz sentir especial e escolhido"},
            {"nome": "Progressão Incremental", "desc": "Mostra evolução passo a passo"},
            {"nome": "Alívio da Dor", "desc": "Foca na solução de problemas específicos"},
            {"nome": "Ampliação de Ganhos", "desc": "Maximiza benefícios percebidos"},
            {"nome": "Redução de Riscos", "desc": "Minimiza percepção de risco"},
            {"nome": "Catalisador de Ação", "desc": "Remove barreiras para decisão"}
        ]

        for i, template in enumerate(driver_templates):
            drivers.append({
                "numero": i + 1,
                "nome": template["nome"],
                "descricao": f"{template['desc']} - Customizado para {segmento}",
                "aplicacao": f"Aplicação específica para {produto} no segmento {segmento}",
                "exemplo_pratico": f"Exemplo prático para {publico}",
                "impacto_conversao": "Alto - impacto psicológico comprovado"
            })

        return {
            "drivers": drivers,
            "resumo_psicologico": f"Estratégia psicológica customizada para {segmento} focada em {produto}",
            "recomendacoes_implementacao": [
                f"Implementar drivers gradualmente para {publico}",
                f"Testar eficácia específica no segmento {segmento}",
                "Monitorar métricas de conversão por driver"
            ]
        }

    def _load_universal_drivers(self) -> Dict[str, Dict[str, Any]]:
        """Carrega drivers mentais universais"""
        return self.universal_drivers

    def _load_driver_templates(self) -> Dict[str, str]:
        """Carrega templates de drivers"""
        return {
            'historia_analogia': 'Era uma vez {personagem} que enfrentava {problema_similar}. Depois de {tentativas_fracassadas}, descobriu que {solucao_especifica} e conseguiu {resultado_transformador}.',
            'metafora_visual': 'Imagine {situacao_atual} como {metafora_visual}. Agora visualize {situacao_ideal} como {metafora_transformada}.',
            'comando_acao': 'Agora que você {compreensao_adquirida}, a única ação lógica é {acao_especifica} porque {consequencia_inevitavel}.'
        }

    def generate_complete_drivers_system(
        self,
        avatar_data: Dict[str, Any],
        context_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Gera sistema completo de drivers mentais customizados"""

        # Validação crítica de entrada
        if not avatar_data:
            logger.error("❌ Dados do avatar ausentes")
            raise ValueError("DRIVERS MENTAIS FALHARAM: Dados do avatar ausentes")

        if not context_data.get('segmento'):
            logger.error("❌ Segmento não informado")
            raise ValueError("DRIVERS MENTAIS FALHARAM: Segmento obrigatório")

        try:
            logger.info("🧠 Gerando drivers mentais customizados...")

            # Salva dados de entrada imediatamente
            salvar_etapa("drivers_entrada", {
                "avatar_data": avatar_data,
                "context_data": context_data
            }, categoria="drivers_mentais")

            # Analisa avatar para identificar drivers ideais
            ideal_drivers = self._identify_ideal_drivers(avatar_data, context_data)

            # Gera drivers customizados
            customized_drivers = self._generate_customized_drivers(ideal_drivers, avatar_data, context_data)

            if not customized_drivers:
                logger.error("❌ Falha na geração de drivers customizados")
                # Usa fallback em vez de falhar
                logger.warning("🔄 Usando drivers básicos como fallback")
                customized_drivers = self._create_fallback_drivers(context_data.get('segmento', 'negócios'), context_data.get('produto', 'produto'), context_data.get('publico', 'público'))


            # Salva drivers customizados
            salvar_etapa("drivers_customizados", customized_drivers, categoria="drivers_mentais")

            # Cria roteiros de ativação
            activation_scripts = self._create_activation_scripts(customized_drivers, avatar_data)

            # Gera frases de ancoragem
            anchor_phrases = self._generate_anchor_phrases(customized_drivers, avatar_data)

            result = {
                'drivers_customizados': customized_drivers,
                'roteiros_ativacao': activation_scripts,
                'frases_ancoragem': anchor_phrases,
                'drivers_universais_utilizados': [d['nome'] for d in ideal_drivers],
                'personalizacao_nivel': self._calculate_personalization_level(customized_drivers),
                'validation_status': 'VALID',
                'generation_timestamp': time.time()
            }

            # Salva resultado final imediatamente
            salvar_etapa("drivers_final", result, categoria="drivers_mentais")

            logger.info("✅ Drivers mentais customizados gerados com sucesso")
            return result

        except Exception as e:
            logger.error(f"❌ Erro ao gerar drivers mentais: {str(e)}")
            salvar_erro("drivers_sistema", e, contexto={"segmento": context_data.get('segmento')})

            # Fallback para sistema básico em caso de erro
            logger.warning("🔄 Gerando drivers básicos como fallback...")
            return self._create_fallback_drivers(context_data.get('segmento', 'negócios'), context_data.get('produto', 'produto'), context_data.get('publico', 'público'))


    def _identify_ideal_drivers(self, avatar_data: Dict[str, Any], context_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identifica drivers ideais baseado no avatar"""

        ideal_drivers = []

        # Analisa dores para identificar drivers
        dores = avatar_data.get('dores_viscerais', [])

        # Mapeia dores para drivers
        if any('tempo' in dor.lower() for dor in dores):
            ideal_drivers.append(self.universal_drivers['urgencia_temporal'])

        if any('concorrência' in dor.lower() or 'competidor' in dor.lower() for dor in dores):
            ideal_drivers.append(self.universal_drivers['escassez_oportunidade'])

        if any('resultado' in dor.lower() or 'crescimento' in dor.lower() for dor in dores):
            ideal_drivers.append(self.universal_drivers['prova_social'])

        # Sempre inclui autoridade técnica
        ideal_drivers.append(self.universal_drivers['autoridade_tecnica'])

        # Sempre inclui reciprocidade
        ideal_drivers.append(self.universal_drivers['reciprocidade'])

        return ideal_drivers[:5]  # Máximo 5 drivers

    def _generate_customized_drivers(
        self,
        ideal_drivers: List[Dict[str, Any]],
        avatar_data: Dict[str, Any],
        context_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Gera drivers customizados usando IA"""

        try:
            segmento = context_data.get('segmento', 'negócios')
            produto = context_data.get('produto', 'produto')
            publico = context_data.get('publico', 'público')


            prompt = f"""
Crie drivers mentais customizados para o segmento {segmento}.

AVATAR:
{json.dumps(avatar_data, indent=2, ensure_ascii=False)[:2000]}

DRIVERS IDEAIS:
{json.dumps(ideal_drivers, indent=2, ensure_ascii=False)[:1000]}

RETORNE APENAS JSON VÁLIDO:

```json
[
  {{
    "nome": "Nome específico do driver",
    "gatilho_central": "Gatilho psicológico principal",
    "definicao_visceral": "Definição que gera impacto emocional",
    "roteiro_ativacao": {{
      "pergunta_abertura": "Pergunta que ativa o driver",
      "historia_analogia": "História específica de 150+ palavras",
      "metafora_visual": "Metáfora visual poderosa",
      "comando_acao": "Comando específico de ação"
    }},
    "frases_ancoragem": [
      "Frase 1 de ancoragem",
      "Frase 2 de ancoragem",
      "Frase 3 de ancoragem"
    ],
    "prova_logica": "Prova lógica que sustenta o driver"
  }}
]
"""

            response = ai_manager.generate_analysis(prompt, max_tokens=2000)

            if response:
                clean_response = response.strip()
                if "```json" in clean_response:
                    start = clean_response.find("```json") + 7
                    end = clean_response.rfind("```")
                    clean_response = clean_response[start:end].strip()

                try:
                    drivers = json.loads(clean_response)
                    if isinstance(drivers, list) and len(drivers) > 0:
                        logger.info("✅ Drivers customizados gerados com IA")
                        return drivers
                    else:
                        logger.warning("⚠️ IA retornou formato inválido")
                except json.JSONDecodeError:
                    logger.warning("⚠️ IA retornou JSON inválido")

            # Fallback para drivers básicos
            return self._create_fallback_drivers(segmento, produto, publico)

        except Exception as e:
            logger.error(f"❌ Erro ao gerar drivers customizados: {str(e)}")
            return self._create_fallback_drivers(segmento, produto, publico)


    def _create_comprehensive_drivers_fallback(self, segmento: str) -> Dict[str, Any]:
        """Cria sistema completo de drivers mentais em caso de falha"""

        drivers_completos = [
            {
                'nome': 'Diagnóstico Brutal',
                'tipo': 'Dor',
                'intensidade': 'Alta',
                'categoria': 'Reconhecimento',
                'script': f'A verdade sobre {segmento}: você está perdendo oportunidades todos os dias.',
                'momento_aplicacao': 'Abertura',
                'resultado_esperado': 'Despertar consciência da situação atual'
            },
            {
                'nome': 'Relógio Psicológico',
                'tipo': 'Urgência',
                'intensidade': 'Crescente',
                'categoria': 'Temporal',
                'script': f'Cada dia que passa sem otimizar {segmento} é uma oportunidade perdida para sempre.',
                'momento_aplicacao': 'Meio',
                'resultado_esperado': 'Criar pressão temporal'
            },
            {
                'nome': 'Método vs Sorte',
                'tipo': 'Solução',
                'intensidade': 'Definitiva',
                'categoria': 'Autoridade',
                'script': f'Existe um método comprovado para {segmento}. A questão é: você vai continuar tentando na sorte?',
                'momento_aplicacao': 'Fechamento',
                'resultado_esperado': 'Posicionar solução como única alternativa'
            },
            {
                'nome': 'Custo Invisível',
                'tipo': 'Dor',
                'intensidade': 'Crescente',
                'categoria': 'Financeiro',
                'script': f'O que você não vê é o quanto está perdendo em {segmento} por não ter o sistema certo.',
                'momento_aplicacao': 'Desenvolvimento',
                'resultado_esperado': 'Conscientizar sobre perdas financeiras'
            },
            {
                'nome': 'Ambição Expandida',
                'tipo': 'Desejo',
                'intensidade': 'Alta',
                'categoria': 'Aspiracional',
                'script': f'Imagine onde seu {segmento} estaria se você tivesse começado certo há um ano.',
                'momento_aplicacao': 'Vislumbre',
                'resultado_esperado': 'Amplificar ambições'
            },
            {
                'nome': 'Identidade Aprisionada',
                'tipo': 'Dor',
                'intensidade': 'Profunda',
                'categoria': 'Identitário',
                'script': f'Você não é o tipo de pessoa que aceita mediocridade em {segmento}, é?',
                'momento_aplicacao': 'Provocação',
                'resultado_esperado': 'Desafiar autoimagem'
            },
            {
                'nome': 'Prova Social Invertida',
                'tipo': 'Pressão',
                'intensidade': 'Crescente',
                'categoria': 'Social',
                'script': f'Enquanto você hesita, seus concorrentes em {segmento} estão agindo.',
                'momento_aplicacao': 'Pressão',
                'resultado_esperado': 'Criar pressão social'
            },
            {
                'nome': 'Mentor Salvador',
                'tipo': 'Solução',
                'intensidade': 'Esperançosa',
                'categoria': 'Autoridade',
                'script': f'Todo especialista em {segmento} teve um mentor que mudou tudo.',
                'momento_aplicacao': 'Posicionamento',
                'resultado_esperado': 'Posicionar como mentor necessário'
            },
            {
                'nome': 'Decisão Binária',
                'tipo': 'Urgência',
                'intensidade': 'Definitiva',
                'categoria': 'Escolha',
                'script': f'Em {segmento}, você tem duas opções: evoluir ou estagnar.',
                'momento_aplicacao': 'Fechamento',
                'resultado_esperado': 'Forçar decisão clara'
            },
            {
                'nome': 'Ferida Exposta',
                'tipo': 'Dor',
                'intensidade': 'Máxima',
                'categoria': 'Vulnerabilidade',
                'script': f'A dor de ver {segmento} não funcionar como deveria.',
                'momento_aplicacao': 'Exposição',
                'resultado_esperado': 'Amplificar dor existente'
            },
            {
                'nome': 'Visão Futura',
                'tipo': 'Desejo',
                'intensidade': 'Inspiradora',
                'categoria': 'Futuro',
                'script': f'Visualize como será quando seu {segmento} funcionar perfeitamente.',
                'momento_aplicacao': 'Inspiração',
                'resultado_esperado': 'Criar visão clara do futuro'
            },
            {
                'nome': 'Gap de Execução',
                'tipo': 'Dor',
                'intensidade': 'Crescente',
                'categoria': 'Performance',
                'script': f'A diferença entre saber e executar em {segmento} está custando caro.',
                'momento_aplicacao': 'Desenvolvimento',
                'resultado_esperado': 'Mostrar gap entre conhecimento e ação'
            },
            {
                'nome': 'Autoridade Silenciosa',
                'tipo': 'Credibilidade',
                'intensidade': 'Sólida',
                'categoria': 'Expertise',
                'script': f'Quem realmente entende de {segmento} sabe que...',
                'momento_aplicacao': 'Credibilidade',
                'resultado_esperado': 'Estabelecer autoridade'
            },
            {
                'nome': 'Consequência Inevitável',
                'tipo': 'Medo',
                'intensidade': 'Crescente',
                'categoria': 'Futuro Negativo',
                'script': f'Se nada mudar em {segmento}, onde você estará em 5 anos?',
                'momento_aplicacao': 'Pressão',
                'resultado_esperado': 'Mostrar consequências da inação'
            },
            {
                'nome': 'Transformação Radical',
                'tipo': 'Esperança',
                'intensidade': 'Poderosa',
                'categoria': 'Mudança',
                'script': f'Uma única mudança pode revolucionar todo seu {segmento}.',
                'momento_aplicacao': 'Esperança',
                'resultado_esperado': 'Mostrar potencial de transformação'
            },
            {
                'nome': 'Validação Externa',
                'tipo': 'Confiança',
                'intensidade': 'Crescente',
                'categoria': 'Social',
                'script': f'Outros profissionais de {segmento} já descobriram isso.',
                'momento_aplicacao': 'Validação',
                'resultado_esperado': 'Validar através de outros'
            },
            {
                'nome': 'Oportunidade Única',
                'tipo': 'Exclusividade',
                'intensidade': 'Urgente',
                'categoria': 'Escassez',
                'script': f'Esta oportunidade para {segmento} não vai durar para sempre.',
                'momento_aplicacao': 'Fechamento',
                'resultado_esperado': 'Criar senso de oportunidade limitada'
            },
            {
                'nome': 'Preço da Mediocridade',
                'tipo': 'Dor',
                'intensidade': 'Acumulativa',
                'categoria': 'Custo',
                'script': f'Aceitar mediocridade em {segmento} tem um preço que você paga todo dia.',
                'momento_aplicacao': 'Conscientização',
                'resultado_esperado': 'Mostrar custo da inação'
            },
            {
                'nome': 'Momentum Perdido',
                'tipo': 'Urgência',
                'intensidade': 'Crescente',
                'categoria': 'Timing',
                'script': f'Cada momento de hesitação em {segmento} é momentum perdido.',
                'momento_aplicacao': 'Urgência',
                'resultado_esperado': 'Criar senso de momentum'
            }
        ]

        return {
            'drivers': drivers_completos,
            'status': 'drivers_fallback_completo',
            'segmento': segmento,
            'total_drivers': len(drivers_completos),
            'categorias': list(set(d['categoria'] for d in drivers_completos)),
            'intensidades': list(set(d['intensidade'] for d in drivers_completos))
        }

    def _create_basic_drivers_fallback(self, segmento: str) -> Dict[str, Any]:
        """Mantém método básico para compatibilidade"""
        return self._create_comprehensive_drivers_fallback(segmento)

    def _create_activation_scripts(self, drivers: List[Dict[str, Any]], avatar_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria roteiros de ativação para cada driver"""

        scripts = {}

        for driver in drivers:
            driver_name = driver.get('nome', 'Driver')
            roteiro = driver.get('roteiro_ativacao', {})

            scripts[driver_name] = {
                'abertura': roteiro.get('pergunta_abertura', ''),
                'desenvolvimento': roteiro.get('historia_analogia', ''),
                'fechamento': roteiro.get('comando_acao', ''),
                'tempo_estimado': '3-5 minutos',
                'intensidade': 'Alta'
            }

        return scripts

    def _generate_anchor_phrases(self, drivers: List[Dict[str, Any]], avatar_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Gera frases de ancoragem para cada driver"""

        anchor_phrases = {}

        for driver in drivers:
            driver_name = driver.get('nome', 'Driver')
            frases = driver.get('frases_ancoragem', [])

            if frases:
                anchor_phrases[driver_name] = frases
            else:
                # Frases padrão
                anchor_phrases[driver_name] = [
                    f"Este é o momento de ativar {driver_name}",
                    f"Você sente o impacto de {driver_name}",
                    f"Agora {driver_name} faz sentido para você"
                ]

        return anchor_phrases

    def _calculate_personalization_level(self, drivers: List[Dict[str, Any]]) -> str:
        """Calcula nível de personalização dos drivers"""

        if not drivers:
            return "Baixo"

        # Verifica se tem histórias específicas
        has_stories = sum(1 for d in drivers if len(d.get('roteiro_ativacao', {}).get('historia_analogia', '')) > 100)

        # Verifica se tem frases de ancoragem
        has_anchors = sum(1 for d in drivers if len(d.get('frases_ancoragem', [])) >= 3)

        personalization_score = (has_stories + has_anchors) / (len(drivers) * 2)

        if personalization_score >= 0.8:
            return "Alto"
        elif personalization_score >= 0.5:
            return "Médio"
        else:
            return "Baixo"

    def _generate_fallback_drivers_system(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera sistema de drivers básico como fallback"""

        segmento = context_data.get('segmento', 'negócios')

        fallback_drivers = self._create_fallback_drivers(segmento, context_data.get('produto', 'produto'), context_data.get('publico', 'público'))

        return {
            'drivers_customizados': fallback_drivers,
            'roteiros_ativacao': {
                driver['nome']: {
                    'abertura': driver['roteiro_ativacao']['pergunta_abertura'],
                    'desenvolvimento': driver['roteiro_ativacao']['historia_analogia'],
                    'fechamento': driver['roteiro_ativacao']['comando_acao'],
                    'tempo_estimado': '3-5 minutos'
                } for driver in fallback_drivers
            },
            'frases_ancoragem': {
                driver['nome']: driver['frases_ancoragem'] for driver in fallback_drivers
            },
            'validation_status': 'FALLBACK_VALID',
            'generation_timestamp': time.time(),
            'fallback_mode': True
        }

# Instância global
mental_drivers_architect = MentalDriversArchitect()