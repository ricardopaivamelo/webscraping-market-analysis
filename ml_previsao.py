# ml_previsao.py
"""
Machine Learning Module - Previsão de Preços de Imóveis
Desenvolvido por: Ricardo Paiva
Objetivo: Prever preços de imóveis usando Regressão Linear (Scikit-learn)
"""

import pandas as pd
import sqlite3
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def carregar_dados(db_path='imoveis.db'):
    """
    Carrega dados do banco SQLite
    """
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT * FROM imoveis", conn)
        conn.close()
        logging.info(f"Dados carregados: {len(df)} registros")
        return df
    except Exception as e:
        logging.error(f"Erro ao carregar dados: {e}")
        return None

def treinar_modelo(df):
    """
    Treina modelo de Regressão Linear
    """
    # Preparação dos dados
    X = df[['area', 'quartos']]
    y = df['preco']
    
    # Split treino/teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Treinamento
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Avaliação
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    
    print("\n🤖 RESULTADOS DO MODELO (Regressão Linear)")
    print("=" * 50)
    print(f"R² Score: {r2:.4f}")
    print(f"MAE (Erro Médio Absoluto): R$ {mae:,.2f}")
    
    # Exemplo de previsão
    exemplo = pd.DataFrame({'area': [100], 'quartos': [3]})
    previsao = model.predict(exemplo)[0]
    print("\n🔮 PREVISÃO EXEMPLO")
    print(f"Imóvel 100m², 3 quartos: R$ {previsao:,.2f}")
    
    return model

if __name__ == "__main__":
    # Tenta carregar do banco, se falhar usa dados fictícios para demonstração
    df = carregar_dados()
    
    if df is None or len(df) < 5:
        logging.warning("Usando dados fictícios para demonstração...")
        dados_exemplo = [
            {'preco': 450000, 'area': 80, 'quartos': 2},
            {'preco': 680000, 'area': 120, 'quartos': 3},
            {'preco': 320000, 'area': 55, 'quartos': 1},
            {'preco': 890000, 'area': 150, 'quartos': 3},
            {'preco': 520000, 'area': 90, 'quartos': 2},
            {'preco': 1200000, 'area': 200, 'quartos': 4},
            {'preco': 350000, 'area': 60, 'quartos': 1},
        ]
        df = pd.DataFrame(dados_exemplo)
    
    treinar_modelo(df)
