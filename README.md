# 🏡 Real Estate Web Scraping & Analysis

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4.9+-green.svg)
![Pandas](https://img.shields.io/badge/pandas-Latest-red.svg)
![Scikit-learn](https://img.shields.io/badge/scikit--learn-Latest-orange.svg)

## 📋 Sobre o Projeto

Sistema de webscraping desenvolvido para coleta e análise automatizada de dados do mercado imobiliário. Implementa técnicas de extração, limpeza e visualização de dados, demonstrando aplicação prática de Python para análise de Real Estate.

## 💡 Objetivo de Negócio

Esta ferramenta foi projetada para identificar **oportunidades de arbitragem** no mercado imobiliário. Ao coletar dados massivos e aplicar modelos de Machine Learning, o sistema permite:

1.  **Identificar ativos subvalorizados**: Imóveis com preço abaixo da média prevista para suas características (área, quartos, localização).
2.  **Monitorar tendências**: Acompanhar a evolução de preços por m² em diferentes bairros.
3.  **Suporte à decisão**: Fornecer dados quantitativos para teses de investimento imobiliário (Kinea/Funds).

## 🎯 Funcionalidades

- ✅ **Webscraping Robusto**: Coleta automatizada com tratamento de erros
- ✅ **Armazenamento SQL**: Persistência de dados em banco SQLite
- ✅ **Machine Learning**: Modelo de Regressão Linear para previsão de preços
- ✅ **Análise Estatística**: Métricas descritivas e agrupamentos
- ✅ **Visualizações**: 4 gráficos profissionais com Matplotlib/Seaborn

## 🚀 Tecnologias

- **Python 3.8+**
- **BeautifulSoup4** - Parsing HTML
- **Requests** - HTTP requests
- **Pandas** - Manipulação de dados
- **SQLite3** - Banco de dados SQL
- **Scikit-learn** - Machine Learning (Regressão Linear)
- **Matplotlib/Seaborn** - Visualizações

## 💻 Como Executar

```bash
# Clone o repositório
git clone https://github.com/ricardopaivamelo/webscraping-real-estate

# Instale as dependências
pip install -r requirements.txt

# 1. Execute o scraper (Coleta + SQL)
python webscraping_imoveis.py

# 2. Execute o modelo de ML
python ml_previsao.py
```

## 📊 Análises Geradas

O script gera automaticamente:

1.  **Estatísticas Descritivas**: Média, mediana, min, max de preços
2.  **Análise por Quartos**: Agrupamento por número de quartos
3.  **Preço por M²**: Cálculo e ranking de localizações
4.  **Visualizações**: 4 gráficos profissionais

## 📁 Estrutura

```
webscraping-real-estate/
├── webscraping_imoveis.py    # Script principal (Scraper + SQL)
├── ml_previsao.py            # Script de Machine Learning
├── requirements.txt          # Dependências
├── README.md                 # Documentação
├── imoveis.db                # Banco de dados SQLite
└── analise_imoveis.png       # Gráficos gerados
```

## ⚠️ Nota Ética

Este projeto é para fins **educacionais e demonstrativos**. Sempre respeite os Termos de Serviço dos sites e implemente rate limiting adequado.

## 👤 Autor

**Ricardo Paiva**

- GitHub: [@ricardopaivamelo](https://github.com/ricardopaivamelo)
- LinkedIn: [Ricardo Paiva](https://linkedin.com/in/ricardo-paiva-a95012340)

## 📝 Licença

MIT License
