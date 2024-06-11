import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import plotly.graph_objects as go



st.set_page_config(layout = "wide",
                   page_title = "SIS Dashboard",
                   page_icon = ":bar_chart:")
st.header(":bar_chart: SIS Cursos")
st.markdown("""---""")


con = sqlite3.connect("db.sqlite3")

df = pd.read_sql_query("SELECT * from financeiro_financeiro", con)

#tratamento dados
df["data_pagamento"] = pd.to_datetime(df["data_pagamento"])
df["valor_pago"] = pd.to_numeric(df["valor_pago"])
#

df.sort_values(by="data_pagamento")

df["Month"] = df["data_pagamento"].apply(lambda x: str(x.month) + "-" + str(x.year))
#print(df["Month"])
#print(df["data_pagamento"])

month = st.sidebar.selectbox("Mês", df["Month"].unique())
df_filtered = df[df["Month"] == month]

#st.write(df_filtered) imprimir db


#coluna 1 faturamento mes
mes_total = df_filtered.groupby("Month")["valor_pago"].sum()
fig_total = px.bar(mes_total, title = "Faturamento do mês")

st.metric("Faturamento Total do mês", mes_total)

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
col5, = st.columns(1)


#1
col1.plotly_chart(fig_total, use_container_width=True)


#coluna 2 faturamento dia
fig_date = px.bar(df_filtered, x = "data_pagamento", y="valor_pago", color="cliente_id" ,title = "Faturamento por dia")
col2.plotly_chart(fig_date, use_container_width=True)

#print(df.dtypes)


#coluna 3 - ano
df["Year"] = df["data_pagamento"].apply(lambda x: str(x.year))
year = st.sidebar.selectbox("Ano", df["Year"].unique())
df_filtered2 = df[df["Year"] == year]
ano_total = df_filtered2.groupby("Year")["valor_pago"].sum()
fig_ano = px.bar(ano_total, title="Faturamento anual")
col3.plotly_chart(fig_ano, use_container_width=True)

#st.write(df)

#coluna 4
#
anos = df.groupby("Year")["valor_pago"].sum()
fig_hist_fat = px.line(anos, title= "Evolução de Faturamento/Ano", markers = True)
col4.plotly_chart(fig_hist_fat, use_container_width=True)



#coluna 5
todos_meses = df.groupby("Month")["valor_pago"].sum()
fig_hist_mes = px.line(todos_meses, title = "Evolução de Faturamento/Mês", markers = True)
col5.plotly_chart(fig_hist_mes, use_container_width=True)



con.close()
