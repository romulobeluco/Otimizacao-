import streamlit as st
import pandas as pd
from main import SimplexSolver

def main():
    st.title("Resolução de Problemas de Programação Linear com Simplex")

    st.markdown("### Defina o Problema")
    num_vars = st.number_input("Número de variáveis (produtos)", min_value=1, value=3)
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

    if st.button("Resolver"):
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
