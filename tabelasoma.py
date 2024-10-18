
import sqlite3
import streamlit as st
import pandas as pd

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('produtos.db')
c = conn.cursor()

# Criação da tabela, caso não exista
c.execute('''
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    valor_unitario REAL NOT NULL,
    quantidade INTEGER NOT NULL,
    valor_total REAL NOT NULL
)
''')
conn.commit()

# Função para adicionar produto ao banco de dados
def adicionar_produto(nome, valor_unitario, quantidade):
    valor_total = valor_unitario * quantidade
    c.execute('INSERT INTO produtos (nome, valor_unitario, quantidade, valor_total) VALUES (?, ?, ?, ?)',
              (nome, valor_unitario, quantidade, valor_total))
    conn.commit()

# Função para excluir produto do banco de dados
def excluir_produto(produto_id):
    c.execute('DELETE FROM produtos WHERE id = ?', (produto_id,))
    conn.commit()

# Função para obter produtos do banco de dados
def obter_produtos():
    return pd.read_sql('SELECT * FROM produtos', conn)

# Título do aplicativo
st.title('Controle de Produtos')

# Inputs para o usuário
nome = st.text_input('Nome do Produto')
valor_unitario = st.number_input('Valor Unitário', min_value=0.0, step=0.01)
quantidade = st.number_input('Quantidade', min_value=1, step=1)

# Botão para adicionar produto
if st.button('Adicionar Produto'):
    if nome and valor_unitario and quantidade:
        adicionar_produto(nome, valor_unitario, quantidade)
        st.success('Produto adicionado com sucesso!')
    else:
        st.error('Por favor, preencha todos os campos.')

# Mostrar tabela de produtos
st.subheader('Lista de Produtos')
produtos_df = obter_produtos()
st.write(produtos_df)

# Opção de excluir produto
st.subheader('Excluir Produto')
produto_id = st.number_input('ID do Produto a ser excluído', min_value=1, step=1)

if st.button('Excluir Produto'):
    if produto_id:
        excluir_produto(produto_id)
        st.success('Produto excluído com sucesso!')
    else:
        st.error('Por favor, insira um ID válido.')

# Fechar a conexão com o banco de dados ao final
conn.close()