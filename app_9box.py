import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus import Image as ReportLabImage
from reportlab.lib.utils import ImageReader
import io
from PIL import Image

# Função para calcular "Desempenho" e "Potencial"
def calcular_desempenho_potencial(df):
    # Encontrar colunas de desempenho (perguntas 1 a 5)
    colunas_desempenho = [col for col in df.columns if col.split(
        '-')[0].isdigit() and 1 <= int(col.split('-')[0]) <= 5]
    
    # Encontrar colunas de potencial (perguntas 6 a 10)
    colunas_potencial = [col for col in df.columns if col.split(
        '-')[0].isdigit() and 6 <= int(col.split('-')[0]) <= 10]

    # Verificar se encontramos o número correto de colunas
    if len(colunas_desempenho) != 5 or len(colunas_potencial) != 5:
        raise ValueError(
            f"Esperava-se 5 colunas de desempenho e 5 de potencial. Encontrado: {len(colunas_desempenho)} desempenho, {len(colunas_potencial)} potencial.")

    # Converter para numérico, tratando erros como NaN
    df[colunas_desempenho] = df[colunas_desempenho].apply(
        pd.to_numeric, errors='coerce')
    df[colunas_potencial] = df[colunas_potencial].apply(
        pd.to_numeric, errors='coerce')

    # Calcular médias
    df["Desempenho_Media"] = df[colunas_desempenho].mean(axis=1)
    df["Potencial_Media"] = df[colunas_potencial].mean(axis=1)

    # Classificar desempenho e potencial
    df["Desempenho"] = df["Desempenho_Media"].apply(
        lambda x: "Excepcional" if x >= 4 else "Mediano" if x >= 2.5 else "Insuficiente"
    )
    df["Potencial"] = df["Potencial_Media"].apply(
        lambda x: "Muito Bom" if x >= 4 else "Aceitável" if x >= 2.5 else "Baixo"
    )

    # Remover colunas temporárias
    return df.drop(columns=["Desempenho_Media", "Potencial_Media"])

# Função para criar a Matriz 9 Box
def criar_matriz_9box(df):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)

    for x in range(1, 3):
        ax.axvline(x, color='black', linestyle='-', linewidth=1)
    for y in range(1, 3):
        ax.axhline(y, color='black', linestyle='-', linewidth=1)

    ax.set_xticks([0.5, 1.5, 2.5])
    ax.set_xticklabels(['Insuficiente', 'Mediano', 'Excepcional'])
    ax.set_yticks([0.5, 1.5, 2.5])
    ax.set_yticklabels(['Baixo', 'Aceitável', 'Muito Bom'], rotation=90)

    ax.set_xlabel('Desempenho', fontsize=12)
    ax.set_ylabel('Potencial', fontsize=12)
    ax.set_title('Matriz 9 Box', fontsize=16)

    ax.annotate("", xy=(3, 0), xytext=(0, 0), arrowprops=dict(
        arrowstyle="->", color="black", linewidth=2))
    ax.annotate("", xy=(0, 3), xytext=(0, 0), arrowprops=dict(
        arrowstyle="->", color="black", linewidth=2))

    cores = [
        '#fa1e1e', '#f78b16', '#e0e024',
        '#f78b16', '#e0e024', '#14f718',
        '#e0e024', '#14f718', '#47c1f5'
    ]

    titulos = [
        "Insuficiente", "Eficaz", "Comprometido",
        "Questionável", "Mantenedor", "Forte Desempenho",
        "Enigma", "Forte Potencial", "Alto Potencial"
    ]

    for i in range(3):
        for j in range(3):
            ax.fill_between([j, j+1], [i, i], [i+1, i+1],
                            color=cores[i*3 + j], alpha=0.6)
            ax.text(j + 0.05, i + 0.95, titulos[i*3 + j], ha='left',
                    va='top', fontsize=10, color='black', fontweight='bold')

    map_desempenho = {'Insuficiente': 0, 'Mediano': 1, 'Excepcional': 2}
    map_potencial = {'Baixo': 0, 'Aceitável': 1, 'Muito Bom': 2}

    box_counts = df.groupby(["Desempenho", "Potencial"]
                            ).size().reset_index(name="Quantidade")
    total_candidatos = len(df)

    for _, row in box_counts.iterrows():
        x = map_desempenho[row['Desempenho']]
        y = map_potencial[row['Potencial']]
        quantidade = row["Quantidade"]
        candidatos = df[(df["Desempenho"] == row['Desempenho']) & (
            df["Potencial"] == row['Potencial'])]["Nome"].tolist()

        if quantidade == 1:
            ax.scatter(x + 0.5, y + 0.7, color='blue', s=100)
            ax.text(x + 0.5, y + 0.5, candidatos[0], ha='center',
                    va='top', fontsize=10, fontweight='bold', color='black')
        else:
            porcentagem = (quantidade / total_candidatos) * 100
            ax.text(x + 0.5, y + 0.5, str(quantidade), ha='center',
                    va='center', fontsize=14, fontweight='bold', color='black')
            ax.text(x + 0.5, y + 0.3, f"{porcentagem:.1f}%",
                    ha='center', va='center', fontsize=10, color='black')

    single_candidate = None
    if len(df) == 1:
        single_candidate = df.iloc[0]

    return fig, ax, single_candidate

# Função para filtrar dinamicamente as opções disponíveis
def get_opcoes(df, col, filtros):
    df_filtrado = df.copy()
    for c, v in filtros.items():
        if c != col and v:
            if c == "Data":
                df_filtrado = df_filtrado[df_filtrado[c].dt.strftime(
                    '%d/%m/%Y').isin(v)]
            else:
                df_filtrado = df_filtrado[df_filtrado[c].isin(v)]

    if col == "Data":
        return sorted(df_filtrado[col].dt.strftime('%d/%m/%Y').unique())
    return sorted(df_filtrado[col].unique())

# Função de callback para atualizar os filtros
def update_filtro(col):
    st.session_state.filtros[col] = st.session_state[f"filtro_{col}"]

# Função para criar o PDF
def criar_pdf_avaliacao(single_candidate, quadrante, explicacoes, matriz_9box_img, perguntas_formatadas, respostas):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72,
                            leftMargin=72, topMargin=72, bottomMargin=18)
    styles = getSampleStyleSheet()
    flowables = []

    # Título
    flowables.append(Paragraph("Resultado da Avaliação", styles['Title']))
    flowables.append(Spacer(1, 12))

    # Adicionar a imagem da matriz 9box
    img_width = 400
    img_height = img_width * matriz_9box_img.height / matriz_9box_img.width

    img_buffer = BytesIO()
    matriz_9box_img.save(img_buffer, format='PNG')
    img_buffer.seek(0)

    flowables.append(ReportLabImage(
        img_buffer, width=img_width, height=img_height))
    flowables.append(Spacer(1, 12))

    # Informações do candidato
    flowables.append(
        Paragraph(f"Nome: {single_candidate['Nome']}", styles['Normal']))
    flowables.append(Paragraph(
        f"Data da Avaliação: {single_candidate['Data'].strftime('%d/%m/%Y')}", styles['Normal']))
    flowables.append(
        Paragraph(f"Posição na Matriz 9box: {quadrante}", styles['Normal']))
    flowables.append(Spacer(1, 12))

    info_quadrante = explicacoes.get(quadrante, {
        "nome": "Não classificado", "explicacao": "Não há explicação disponível para este quadrante.", "plano_acao": "Não há plano de ação definido."
    })

    # Quadrante
    flowables.append(
        Paragraph(f"Quadrante: {info_quadrante['nome']}", styles['Heading2']))
    flowables.append(Spacer(1, 6))

    # Explicação
    flowables.append(Paragraph("Explicação:", styles['Heading3']))
    flowables.append(Paragraph(info_quadrante['explicacao'], styles['Normal']))
    flowables.append(Spacer(1, 12))

    # Plano de Ação
    flowables.append(Paragraph("Plano de Ação:", styles['Heading3']))
    flowables.append(Paragraph(info_quadrante['plano_acao'], styles['Normal']))

    # Perguntas de Desempenho
    flowables.append(Paragraph("Perguntas de Desempenho", styles['Heading2']))
    flowables.append(Spacer(1, 6))

    for i in range(5):  # Ajustado para 5 perguntas de desempenho
        flowables.append(
            Paragraph(f"{perguntas_formatadas[i]}: {respostas[i]}", styles['Normal']))
        flowables.append(Spacer(1, 3))

    flowables.append(Spacer(1, 12))

    # Perguntas de Potencial
    flowables.append(Paragraph("Perguntas de Potencial", styles['Heading2']))
    flowables.append(Spacer(1, 6))

    for i in range(5, 10):  # Ajustado para 5 perguntas de potencial (6 a 10)
        flowables.append(
            Paragraph(f"{perguntas_formatadas[i]}: {respostas[i]}", styles['Normal']))
        flowables.append(Spacer(1, 3))

    doc.build(flowables)
    buffer.seek(0)
    return buffer

# Função para salvar a matriz 9box como imagem
def salvar_matriz_9box(fig):
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    return Image.open(img_buffer)

def main():
    st.title("Avaliação de desempenho 9 Box")
    st.write("Faça upload da planilha de avaliação para visualizar a Matriz 9 Box.")

    uploaded_file = st.file_uploader("📂 Carregar arquivo Excel", type=["xlsx"])

    if uploaded_file:
        df = pd.read_excel(uploaded_file, sheet_name="Planilha1")
        df["Data"] = pd.to_datetime(df["Data"])
        df = calcular_desempenho_potencial(df)

        if 'filtros' not in st.session_state:
            st.session_state.filtros = {col: []
                                        for col in ["Data", "Função", "Loja", "Nome"]}

        st.sidebar.title("Filtros")

        for col in ["Data", "Função", "Loja", "Nome"]:
            opcoes = get_opcoes(df, col, st.session_state.filtros)

            if col == "Data":
                selecionadas = st.session_state.filtros[col]
            else:
                selecionadas = st.session_state.filtros[col]

            st.session_state.filtros[col] = st.sidebar.multiselect(
                col,
                options=opcoes,
                default=selecionadas,
                key=f"filtro_{col}",
                on_change=update_filtro,
                args=(col,)
            )

        df_filtrado = df.copy()
        for col, valores in st.session_state.filtros.items():
            if valores:
                if col == "Data":
                    df_filtrado = df_filtrado[df_filtrado[col].dt.strftime(
                        '%d/%m/%Y').isin(valores)]
                else:
                    df_filtrado = df_filtrado[df_filtrado[col].isin(valores)]

        st.subheader("📊 Matriz 9 Box")
        if df_filtrado.empty:
            st.write("Nenhum candidato corresponde aos filtros selecionados.")
        else:
            st.write(f"Exibindo {len(df_filtrado)} de {len(df)} registros.")
            fig, ax, single_candidate = criar_matriz_9box(df_filtrado)
            st.pyplot(fig)

            if single_candidate is not None:
                st.subheader("Resultado da Avaliação")
                st.write(f"**Nome:** {single_candidate['Nome']}")
                st.write(
                    f"**Data da Avaliação:** {single_candidate['Data'].strftime('%d/%m/%Y')}")

                quadrante = f"{single_candidate['Desempenho']} - {single_candidate['Potencial']}"
                st.write(f"**Posição na Matriz 9box:** {quadrante}")

                # Dicionário com explicações e planos de ação para cada quadrante
                explicacoes = {
                    "Insuficiente - Baixo": {
                        "nome": "Insuficiente - baixo potencial e baixo desempenho",
                        "explicacao": "O quadrante insuficiente é um forte indício de má contratação, visto que a pessoa não apresenta nem potencial, nem desempenho minimamente satisfatórios.",
                        "plano_acao": "Principais alternativas: 1- Identificar fatores que impedem o bom desempenho e montar um plano de desenvolvimento direcionado; 2- Verificar aptidão para outra função e considerar movimentação lateral interna; 3- Considerar a substituição do colaborador."
                    },
                    "Mediano - Baixo": {
                        "nome": "Eficaz - baixo potencial e médio desempenho",
                        "explicacao": "O quadrante Eficaz representa os colaboradores que entregam suas tarefas conforme o esperado e apenas isso. Não se esforçam ou demonstram qualquer anseio por ir além do que é demandado e tendem a apresentar um comportamento de constante estagnação.",
                        "plano_acao": "Dar feedbacks mais frequentes sobre seu desempenho e utilizar estratégias para aumentar sua motivação e engajamento com a empresa. A criação de um PDI e um esclarecimento sobre plano de carreira pode ser ótimos aliados."
                    },
                    "Excepcional - Baixo": {
                        "nome": "Comprometido - baixo potencial e alto desempenho",
                        "explicacao": "Neste grupo estão as pessoas que fazem muito bem tudo o que lhes é demandado, desde que seja demandado, ou seja, são pessoas com pouca ou nenhuma iniciativa. São excelentes aliados para o fortalecimento da cultura.",
                        "plano_acao": "Manter a motivação alta e garantir sua retenção. Estimular a iniciativa para prepará-los para assumir cargos de maior responsabilidade."
                    },
                    "Insuficiente - Aceitável": {
                        "nome": "Questionável - médio potencial e baixo desempenho",
                        "explicacao": "Os profissionais deste quadrante estão suficientemente motivados, mas não conseguem entregar aquilo que se espera deles.",
                        "plano_acao": "Investigar as causas do baixo desempenho. Alguns questionamentos são válidos: 1- Esses colaboradores sabem, com clareza, o que devem entregar? 2- Como foi o onboarding dessas pessoas? 3- Esses colaboradores estão passando por algum tipo de dificuldade em sua vida pessoal? 4- Esses colaboradores têm alguma deficiência de conhecimentos em processos, ferramentas ou tecnologias inerentes à sua função? De acordo com esses questionamentos, monte um plano de desenvolvimento. "
                    },
                    "Mediano - Aceitável": {
                        "nome": "Mantenedor - médio potencial e médio desempenho",
                        "explicacao": "Aqui estão os profissionais bons no que fazem e têm potencial para alcançar novos patamares.",
                        "plano_acao": "Garantir que não haja retrocessos e que se mantenham motivados. Considerar para promoção e, mesmo que não haja oportunidade imediata, reconhecer e recompensar de alguma forma."
                    },
                    "Excepcional - Aceitável": {
                        "nome": "Forte desempenho - médio potencial e alto desempenho",
                        "explicacao": "Entregas que vão além do esperado com um bom potencial de desenvolvimento são características que tornam esse grupo de pessoas bastante positivo para a empresa.",
                        "plano_acao": "Identificar o momento certo para uma promoção. Manter motivados, reconhecer conquistas e colocá-los em contato com outras áreas da empresa para ampliar a percepção do impacto de suas entregas."
                    },
                    "Insuficiente - Muito Bom": {
                        "nome": "Enigma - alto potencial e baixo desempenho",
                        "explicacao": "Esse é o quadrante mais desafiador, pois representa as pessoas com um potencial acima da média, mas que estão muito aquém em suas entregas.",
                        "plano_acao": "Realizar um forte trabalho de investigação. Compreender essas pessoas de forma mais ampla, inclusive sua vida pessoal. Identificar fatores que impactam o desempenho e criar um plano de ação para cada um. Realizar acompanhamento próximo."
                    },
                    "Mediano - Muito Bom": {
                        "nome": "Forte potencial - alto potencial e médio desempenho",
                        "explicacao": "Os profissionais desse grupo são valiosos para a organização já que sustentam a cultura de trabalho e atendem a todas as expectativas de desempenho.",
                        "plano_acao": "Proporcionar oportunidades de treinamento e desenvolvimento, tarefas mais desafiadoras e uma gestão mais especializada do progresso. Garantir clareza nos indicadores de desempenho e dar espaço para crescerem."
                    },
                    "Excepcional - Muito Bom": {
                        "nome": "Alto potencial - alto potencial e alto desempenho",
                        "explicacao": "Aqui está o supra sumo da sua organização. Esses são os profissionais que todos da empresa admiram e se inspiram.",
                        "plano_acao": "Focar na retenção desses colaboradores. Mantê-los motivados com desafios constantes e reconhecimento adequado. Considerar promoções frequentes e valorização pública. Aproveitar em programas internos de mentoria."
                    }
                }

                info_quadrante = explicacoes.get(quadrante, {
                    "nome": "Não classificado", "explicacao": "Não há explicação disponível para este quadrante.", "plano_acao": "Não há plano de ação definido."
                })

                st.write(f"**Quadrante:** {info_quadrante['nome']}")
                st.write("**Explicação:**")
                st.write(info_quadrante['explicacao'])
                st.write("**Plano de Ação:**")
                st.write(info_quadrante['plano_acao'])

                # Encontrar as colunas das perguntas pelo número no início
                perguntas_colunas = [col for col in df.columns if col.split(
                    '-')[0].isdigit() and 1 <= int(col.split('-')[0]) <= 10]

                # Ordenar as colunas pelo número da pergunta
                perguntas_colunas.sort(key=lambda x: int(x.split('-')[0]))

                # Verificar se temos exatamente 10 perguntas
                if len(perguntas_colunas) != 10:
                    st.error(
                        f"Número inesperado de perguntas: {len(perguntas_colunas)}. Esperava-se 10.")
                    st.write("Perguntas encontradas:", perguntas_colunas)
                    return

                # Obter as perguntas e respostas do single_candidate
                perguntas = perguntas_colunas
                respostas = [single_candidate[col]
                             for col in perguntas_colunas]

                # Converter as respostas de np.int64 para int regular
                respostas = [int(r) if isinstance(
                    r, np.integer) else r for r in respostas]

                # Formatar as perguntas
                perguntas_formatadas = []
                for p in perguntas:
                    numero, texto = p.split('-', 1)
                    perguntas_formatadas.append(f"{numero}. {texto.strip()}")

                # Salvar a matriz 9box como imagem
                matriz_9box_img = salvar_matriz_9box(fig)

                # Criar o PDF
                pdf = criar_pdf_avaliacao(
                    single_candidate, quadrante, explicacoes, matriz_9box_img, perguntas_formatadas, respostas
                )

                # Adicionar o botão de download
                st.download_button(
                    label="📥 Baixar Resultado da Avaliação (PDF)",
                    data=pdf,
                    file_name=f"avaliacao_{single_candidate['Nome']}.pdf",
                    mime="application/pdf"
                )

if __name__ == "__main__":
    main()