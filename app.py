import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

def gerar_pdf_demonstrativo(dados):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.drawString(100, 800, "DEMONSTRATIVO DE IMPORTAÇÃO - DO SERVIÇOS")
    c.drawString(100, 780, f"Adquirente: {dados['adquirente']}")
    c.drawString(100, 760, f"Valor Aduaneiro (R$): {dados['valor_aduaneiro']:,.2f}")
    c.save()
    buffer.seek(0)
    return buffer

st.set_page_config(page_title="Simulador de Importação Do Serviços", layout="wide")
st.title("Sistema de Gestão de Importação - Do Serviços")

tab1, tab2, tab3, tab4 = st.tabs(["Dados Gerais", "Valores Internacionais", "Parâmetros", "Resultado"])

with tab1:
    adquirente = st.text_input("Adquirente")
    incoterm = st.selectbox("Incoterm", ["FOB", "EXW", "CIF", "CFR", "CIP", "CPT", "FCA", "FAS"])

with tab2:
    col1, col2 = st.columns(2)
    valor_fob = col1.number_input("Valor FOB/EXW (USD)", value=0.0, format="%.2f")
    frete = col1.number_input("Frete Internacional (USD)", value=0.0, format="%.2f")
    seguro = col2.number_input("Seguro (USD)", value=0.0, format="%.2f")
    cambio = col2.number_input("Câmbio (R$)", value=4.73, format="%.4f")

with tab3:
    st.subheader("Parâmetros de Cálculo")
    despesas_10 = st.number_input("Despesas (10%)", value=0.0, format="%.2f")
    lucros_10 = st.number_input("Lucros (10%)", value=0.0, format="%.2f")
    impostos_manual = st.number_input("Impostos (Valor Total)", value=0.0, format="%.2f")

with tab4:
    if st.button("Gerar Demonstrativo"):
        valor_aduaneiro = (valor_fob + frete + seguro) * cambio
        st.success("Cálculo Finalizado")
        dados_simulacao = {'adquirente': adquirente, 'valor_aduaneiro': valor_aduaneiro}
        pdf = gerar_pdf_demonstrativo(dados_simulacao)
        st.download_button("Baixar Demonstrativo (PDF)", data=pdf, file_name="Demonstrativo.pdf")