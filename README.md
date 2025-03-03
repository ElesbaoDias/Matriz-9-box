# Avaliação de Desempenho 9 Box

Bem-vindo ao **Avaliação de Desempenho 9 Box**, uma aplicação web construída com Streamlit para visualizar e analisar o desempenho e o potencial de colaboradores usando a Matriz 9 Box. Este projeto permite carregar dados de uma planilha Excel, aplicar filtros dinâmicos e gerar relatórios em PDF com detalhes sobre a avaliação de cada colaborador.

## Sobre o Projeto

A Matriz 9 Box é uma ferramenta amplamente utilizada em gestão de Recursos Humanos para classificar colaboradores com base em dois eixos: **Desempenho** e **Potencial**. Este projeto automatiza o processo de cálculo e visualização, oferecendo:

- Cálculo automático das médias de desempenho (perguntas 1 a 5) e potencial (perguntas 6 a 10).
- Visualização interativa da Matriz 9 Box com quadrantes coloridos e posicionamento dos colaboradores.
- Filtros dinâmicos por data, função, loja e nome.
- Geração de relatórios em PDF para avaliações individuais, incluindo explicações e planos de ação por quadrante.

## Funcionalidades

- **Upload de Planilha**: Carregue um arquivo Excel com os dados dos colaboradores.
- **Filtros Interativos**: Filtre os dados por data, função, loja ou nome diretamente na interface.
- **Matriz 9 Box**: Visualize os colaboradores em uma matriz 3x3 com quadrantes como "Alto Potencial", "Enigma", "Insuficiente", etc.
- **Relatórios em PDF**: Gere relatórios detalhados para um único colaborador, incluindo respostas às perguntas, explicações e planos de ação.
- **Flexibilidade**: Funciona com perguntas numeradas (ex.: "1-Atingimento de metas"), eliminando a dependência de posições fixas nas colunas.

## Estrutura da Planilha

A aplicação espera uma planilha Excel com a aba chamada "Planilha1" e as seguintes colunas:

- **Nome**: Nome do colaborador.
- **Data**: Data da avaliação (formato: DD/MM/AAAA).
- **Função**: Cargo ou função do colaborador.
- **Loja**: Local de trabalho (opcional).
- **1-[Pergunta] a 5-[Pergunta]**: 5 perguntas de desempenho (ex.: "1-Atingimento de metas"), com valores de 1 a 5.
- **6-[Pergunta] a 10-[Pergunta]**: 5 perguntas de potencial (ex.: "6-Potencial 1"), com valores de 1 a 5.

## Pré-requisitos

- Python 3.8 ou superior
- Bibliotecas Python:
  - `streamlit`
  - `pandas`
  - `matplotlib`
  - `numpy`
  - `reportlab`
  - `pillow`

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/[seu-usuario]/avaliacao-9box.git
   cd avaliacao-9box

2. Instalar as dependências:

   pip install -r requirements.txt

3. (Opcional) Crie um arquivo requisitos.txt com:

   - `streamlit`
   - `pandas`
   - `matplotlib`
   - `numpy`
   - `reportlab`
   - `pillow`
        
## Como usar

1. Executar uma aplicação:

   streamlit run app.py

2. Abra o navegador em http://localhost:8501 .

3. Faça upload de uma planilha Excel no formato esperado.

4. Use os filtros na barra lateral para explorar os dados.

5. Visualize a Matriz 9 Box e, se houver apenas um colaborador filtrado, gere o relatório em PDF clicando no botão de download.

6. Ou abra o aplicativo diretamente em https://matriz-9-box.streamlit.app 

## Exemplos de uso

1. Carregue uma planilha com dados de colaboradores.

2. Filtre por "Função: Gerente" e "Loja: Loja A".

3. Veja a Matriz 9 Box com os gerentes da Loja A posicionados nos quadrantes.

4. Selecione um único colaborador para ver os detalhes e baixar o relatório em PDF.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir problemas ou enviar pull requests com melhorias, como:

- `Suporte a mais formatos de entrada (CSV, etc.).`
- `Personalização dos quadrantes ou critérios de avaliação.`
- `Melhorias na interface do usuário.`

## Licença

Este projeto está licenciado sob a Licença MIT .

## Contato

Se tiver dúvidas ou sugestões, entre em contato pelo GitHub ou abra uma issue.




   
