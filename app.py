import streamlit as st
import pandas as pd
from main import SimplexSolver

# Estilização
st.markdown(
    """
    <style>
    body {
        background-color: #f0f8ff;
        color: #333333;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #6A5ACD;
        color: white;
        border-radius: 10px;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #483D8B;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    st.markdown("<h1 style='text-align: center; color: #6A5ACD;'>Resolução de Problemas de Programação Linear</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Resolva problemas de forma eficiente e otimizada!</p>", unsafe_allow_html=True)
    st.image("logo.png", width=100)

    st.markdown("---")
    st.markdown("### Configurar Problema")

    # Inputs organizados em colunas
    col1, col2 = st.columns(2)
    with col1:
        num_vars = st.number_input("Número de variáveis (produtos)", min_value=1, value=3)
    with col2:
        num_constraints = st.number_input("Número de restrições", min_value=1, value=2)

    st.markdown("### Coeficientes da Função Objetivo")
    c = [st.number_input(f"Coeficiente x{i+1}", value=1.0, key=f"c_{i}") for i in range(num_vars)]

    st.markdown("### Restrições")
    A = []
    b = []
    for j in range(num_constraints):
        st.markdown(f"**Restrição {j+1}**")
        row = [st.number_input(f"Coeficiente x{i+1} para a restrição {j+1}", value=1.0, key=f"A_{j}_{i}") for i in range(num_vars)]
        A.append(row)
        rhs = st.number_input(f"Valor à direita da restrição {j+1} (≤)", value=10.0, key=f"b_{j}")
        b.append(rhs)

    # Botão personalizado
    if st.button("🚀 Resolver Problema"):
        try:
            solver = SimplexSolver(num_vars, c, A, b)
            solution, optimal_value, shadow_prices = solver.solve()

            st.success("Solução encontrada!")
            st.write("**Valores das Variáveis:**")
            for i, val in enumerate(solution):
                st.write(f"x{i+1} = {val:.2f}")
            st.write(f"**Valor Ótimo (Lucro Máximo):** {optimal_value:.2f}")

            st.write("**Preços-Sombra:**")
            shadow_df = pd.DataFrame({
                "Restrição": [f"Restrição {i+1}" for i in range(len(shadow_prices))],
                "Preço-Sombra": shadow_prices
            })
            st.table(shadow_df)

        except ValueError as e:
            st.error(str(e))

if __name__ == "__main__":
    main()
