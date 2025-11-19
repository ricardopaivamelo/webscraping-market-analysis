# webscraping_imoveis.py
"""
Real Estate Web Scraping - Análise de Mercado Imobiliário
Desenvolvido por: Ricardo Paiva
Objetivo: Demonstrar habilidades em webscraping para vaga Kinea
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import time
import logging
import sqlite3

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class RealEstateScraper:
    """
    Classe para scraping de dados de imóveis
    """
    
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.dados = []
        
    def fazer_request(self, url, max_retries=3):
        """
        Faz requisição HTTP com retry
        """
        for tentativa in range(max_retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                logging.info(f"✓ Request bem-sucedido: {url}")
                return response
            except requests.RequestException as e:
                logging.warning(f"Tentativa {tentativa + 1} falhou: {e}")
                time.sleep(2)
        return None
    
    def extrair_dados_imovel(self, elemento):
        """
        Extrai dados de um elemento HTML de imóvel
        """
        try:
            # Exemplo de extração (adapte conforme o site)
            preco = elemento.find('span', class_='preco').text.strip()
            area = elemento.find('span', class_='area').text.strip()
            quartos = elemento.find('span', class_='quartos').text.strip()
            localizacao = elemento.find('span', class_='localizacao').text.strip()
            
            return {
                'preco': self.limpar_preco(preco),
                'area': self.limpar_area(area),
                'quartos': int(quartos),
                'localizacao': localizacao,
                'data_coleta': datetime.now().strftime('%Y-%m-%d')
            }
        except AttributeError as e:
            logging.error(f"Erro ao extrair dados: {e}")
            return None
    
    def limpar_preco(self, preco_str):
        """
        Remove caracteres não numéricos do preço
        """
        import re
        numeros = re.findall(r'\d+', preco_str.replace('.', '').replace(',', '.'))
        return float(''.join(numeros)) if numeros else None
    
    def limpar_area(self, area_str):
        """
        Extrai valor numérico da área
        """
        import re
        numeros = re.findall(r'\d+', area_str)
        return int(numeros[0]) if numeros else None
    
    def scrape_pagina(self, url):
        """
        Faz scraping de uma página
        """
        response = self.fazer_request(url)
        if not response:
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        imoveis = soup.find_all('div', class_='imovel-card')  # Ajuste conforme o site
        
        dados_pagina = []
        for imovel in imoveis:
            dado = self.extrair_dados_imovel(imovel)
            if dado:
                dados_pagina.append(dado)
        
        logging.info(f"✓ {len(dados_pagina)} imóveis extraídos desta página")
        return dados_pagina
    
    def scrape_multiplas_paginas(self, num_paginas=5):
        """
        Faz scraping de múltiplas páginas
        """
        logging.info(f"Iniciando scraping de {num_paginas} páginas...")
        
        for pagina in range(1, num_paginas + 1):
            url = f"{self.base_url}?pagina={pagina}"
            dados_pagina = self.scrape_pagina(url)
            self.dados.extend(dados_pagina)
            time.sleep(1)  # Respeito ao servidor
        
        logging.info(f"✓ Scraping concluído: {len(self.dados)} imóveis coletados")
        return self.dados
    
    def salvar_csv(self, filename='imoveis_scraped.csv'):
        """
        Salva dados em CSV
        """
        if not self.dados:
            logging.warning("Nenhum dado para salvar")
            return
        
        df = pd.DataFrame(self.dados)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        logging.info(f"✓ Dados salvos em {filename}")
        return df

    def salvar_sql(self, db_name='imoveis.db'):
        """
        Salva dados em banco SQLite
        """
        if not self.dados:
            logging.warning("Nenhum dado para salvar no SQL")
            return

        df = pd.DataFrame(self.dados)
        try:
            conn = sqlite3.connect(db_name)
            df.to_sql('imoveis', conn, if_exists='replace', index=False)
            conn.close()
            logging.info(f"✓ Dados salvos no banco de dados '{db_name}' (tabela 'imoveis')")
        except Exception as e:
            logging.error(f"Erro ao salvar no SQL: {e}")


class AnalisadorImoveis:
    """
    Classe para análise de dados de imóveis
    """
    
    def __init__(self, df):
        self.df = df
    
    def estatisticas_descritivas(self):
        """
        Calcula estatísticas descritivas
        """
        print("\n📊 ESTATÍSTICAS DESCRITIVAS")
        print("=" * 60)
        print(self.df.describe())
        
        print("\n💰 ANÁLISE DE PREÇOS")
        print(f"Preço Médio: R$ {self.df['preco'].mean():,.2f}")
        print(f"Preço Mediano: R$ {self.df['preco'].median():,.2f}")
        print(f"Preço Mínimo: R$ {self.df['preco'].min():,.2f}")
        print(f"Preço Máximo: R$ {self.df['preco'].max():,.2f}")
    
    def analise_por_quartos(self):
        """
        Análise agrupada por número de quartos
        """
        print("\n🏠 ANÁLISE POR NÚMERO DE QUARTOS")
        print("=" * 60)
        agrupado = self.df.groupby('quartos')['preco'].agg(['mean', 'median', 'count'])
        agrupado.columns = ['Preço Médio', 'Preço Mediano', 'Quantidade']
        print(agrupado)
    
    def visualizacoes(self):
        """
        Cria visualizações dos dados
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Análise de Mercado Imobiliário', fontsize=16, fontweight='bold')
        
        # 1. Distribuição de Preços
        sns.histplot(data=self.df, x='preco', bins=30, kde=True, ax=axes[0, 0])
        axes[0, 0].set_title('Distribuição de Preços')
        axes[0, 0].set_xlabel('Preço (R$)')
        
        # 2. Boxplot por Quartos
        sns.boxplot(data=self.df, x='quartos', y='preco', ax=axes[0, 1])
        axes[0, 1].set_title('Preço por Número de Quartos')
        axes[0, 1].set_ylabel('Preço (R$)')
        
        # 3. Scatter: Preço vs Área
        sns.scatterplot(data=self.df, x='area', y='preco', hue='quartos', 
                       palette='viridis', ax=axes[1, 0])
        axes[1, 0].set_title('Relação Preço x Área')
        axes[1, 0].set_xlabel('Área (m²)')
        axes[1, 0].set_ylabel('Preço (R$)')
        
        # 4. Top Localizações
        top_locais = self.df['localizacao'].value_counts().head(10)
        top_locais.plot(kind='barh', ax=axes[1, 1])
        axes[1, 1].set_title('Top 10 Localizações')
        axes[1, 1].set_xlabel('Quantidade de Imóveis')
        
        plt.tight_layout()
        plt.savefig('analise_imoveis.png', dpi=300, bbox_inches='tight')
        logging.info("✓ Visualizações salvas em 'analise_imoveis.png'")
        plt.show()
    
    def calcular_preco_m2(self):
        """
        Calcula preço por m²
        """
        self.df['preco_m2'] = self.df['preco'] / self.df['area']
        
        print("\n📐 ANÁLISE DE PREÇO POR M²")
        print("=" * 60)
        print(f"Preço/m² Médio: R$ {self.df['preco_m2'].mean():,.2f}")
        print(f"Preço/m² Mediano: R$ {self.df['preco_m2'].median():,.2f}")
        
        # Top 5 localizações mais caras por m²
        print("\n🏆 TOP 5 LOCALIZAÇÕES MAIS CARAS (R$/m²)")
        top_preco_m2 = self.df.groupby('localizacao')['preco_m2'].mean().sort_values(ascending=False).head(5)
        print(top_preco_m2)


# EXEMPLO DE USO
def main():
    """
    Função principal de execução
    """
    print("🏡 Real Estate Web Scraping - Ricardo Paiva")
    print("=" * 60)
    
    # NOTA: Este é um exemplo demonstrativo
    # Para uso real, substitua pela URL do site alvo
    
    # Simulação com dados fictícios (para demonstração)
    dados_exemplo = [
        {'preco': 450000, 'area': 80, 'quartos': 2, 'localizacao': 'Vila Mariana', 'data_coleta': '2025-01-15'},
        {'preco': 680000, 'area': 120, 'quartos': 3, 'localizacao': 'Pinheiros', 'data_coleta': '2025-01-15'},
        {'preco': 320000, 'area': 55, 'quartos': 1, 'localizacao': 'Mooca', 'data_coleta': '2025-01-15'},
        {'preco': 890000, 'area': 150, 'quartos': 3, 'localizacao': 'Jardins', 'data_coleta': '2025-01-15'},
        {'preco': 520000, 'area': 90, 'quartos': 2, 'localizacao': 'Perdizes', 'data_coleta': '2025-01-15'},
    ]
    
    df = pd.DataFrame(dados_exemplo)
    
    # Salvar no SQL (Simulando dados coletados)
    # Em um cenário real, isso seria chamado após o scraping
    print("\n💾 Salvando dados no SQL...")
    try:
        conn = sqlite3.connect('imoveis.db')
        df.to_sql('imoveis', conn, if_exists='replace', index=False)
        conn.close()
        print("✓ Dados salvos em 'imoveis.db'")
    except Exception as e:
        print(f"Erro ao salvar SQL: {e}")

    # Análise
    analisador = AnalisadorImoveis(df)
    analisador.estatisticas_descritivas()
    analisador.analise_por_quartos()
    analisador.calcular_preco_m2()
    analisador.visualizacoes()
    
    print("\n✅ Análise concluída com sucesso!")
    print("📊 Gráficos salvos em 'analise_imoveis.png'")
    
    # Para scraping real, descomente:
    # scraper = RealEstateScraper('https://site-exemplo.com.br/imoveis')
    # dados = scraper.scrape_multiplas_paginas(num_paginas=5)
    # df = scraper.salvar_csv()
    # scraper.salvar_sql() # Novo método
    # analisador = AnalisadorImoveis(df)
    # analisador.visualizacoes()


if __name__ == "__main__":
    main()
