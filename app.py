import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 Dashboard de Estatísticas - Cursos Udemy")

df = pd.read_csv("udemy_courses.csv")

# 1. Top 10 cursos com mais inscritos
top_cursos = df.sort_values(by="num_subscribers", ascending=False).head(10)
fig1 = px.bar(top_cursos, x="course_title", y="num_subscribers", title="Top 10 Cursos com Mais Inscritos")

# 2. Preço médio por categoria
preco_medio = df[df['is_paid'] == True].groupby("subject")["price"].mean().reset_index()
fig2 = px.bar(preco_medio, x="subject", y="price", title="Preço Médio por Categoria (Cursos Pagos)")

# 3. Preço vs Inscritos
fig3 = px.scatter(df[df['is_paid'] == True], x="price", y="num_subscribers", 
                  size="num_reviews", color="subject", 
                  title="Preço vs Inscritos (Cursos Pagos)")

# 4. Distribuição por nível
fig4 = px.pie(df, names="level", title="Distribuição de Cursos por Nível")

# 5. Duração do curso vs inscritos
fig5 = px.scatter(df, x="content_duration", y="num_subscribers", 
                  color="subject", 
                  title="Duração do Curso vs Número de Inscritos")

# 6. Cursos pagos vs gratuitos
pagos_vs_gratis = df['is_paid'].value_counts().reset_index()
pagos_vs_gratis.columns = ['Tipo', 'Quantidade']
pagos_vs_gratis['Tipo'] = pagos_vs_gratis['Tipo'].replace({True: 'Pago', False: 'Gratuito'})
fig6 = px.pie(pagos_vs_gratis, names='Tipo', values='Quantidade', title='Cursos Pagos vs Gratuitos')

# === LAYOUT EM COLUNAS ===

col1, col2 = st.columns(2)
col1.plotly_chart(fig1, use_container_width=True)
col2.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)
col3.plotly_chart(fig3, use_container_width=True)
col4.plotly_chart(fig4, use_container_width=True)

col5, col6 = st.columns(2)
col5.plotly_chart(fig5, use_container_width=True)
col6.plotly_chart(fig6, use_container_width=True)
