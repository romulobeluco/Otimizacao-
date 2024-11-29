import streamlit as st
import pandas as pd
from main import SimplexSolver

def main():
    st.title("Resolução de Problemas  com Simplex")
    st.subheader("Ferramenta para resolver problemas de maximização")

    # Entrada de dados: número de variáveis e restrições
    st.sidebar.header("Configuração do Problema")
    num_vars = st.sidebar.number_input("Número de variáveis", min_value=1, value=3)
    num_constraints = st.sidebar.number_input("Número de restrições", min_value=1, value=2)

    # Configuração da função objetivo
    with st.expander("Definir Função Objetivo", expanded=True):
        st.markdown("**Coeficientes da Função Objetivo:**")
        c = [
            st.number_input(f"Coeficiente x{i+1}", value=1.0, key=f"c_{i}") 
            for i in range(num_vars)
        ]

    # Configuração das restrições
    A = []
    b = []
    with st.expander("Definir Restrições", expanded=True):
        for j in range(num_constraints):
            st.markdown(f"**Restrição {j+1}**")
            col1, col2 = st.columns([3, 1])
            with col1:
                row = [
                    st.number_input(
                        f"Coeficiente x{i+1} para a restrição {j+1}",
                        value=1.0,
                        key=f"A_{j}_{i}"
                    ) 
                    for i in range(num_vars)
                ]
                A.append(row)
            with col2:
                rhs = st.number_input(
                    f"Valor à direita (≤)",
                    value=10.0,
                    key=f"b_{j}"
                )
                b.append(rhs)

    # Botão de solução
    if st.button("Resolver"):
        try:
            # Resolver o problema usando SimplexSolver
            solver = SimplexSolver(num_vars, c, A, b)
            solution, optimal_value, shadow_prices = solver.solve()

            # Exibir resultados
            st.success("Solução encontrada!")
            
            # Solução das variáveis
            st.markdown("### Valores das Variáveis")
            solution_df = pd.DataFrame({
                "Variável": [f"x{i+1}" for i in range(len(solution))],
                "Valor": solution
            })
            st.table(solution_df)

            # Valor ótimo
            st.markdown(f"### Valor Ótimo (Lucro Máximo): **{optimal_value:.2f}**")

            # Preços-sombra
            st.markdown("### Preços-Sombra")
            shadow_df = pd.DataFrame({
                "Restrição": [f"Restrição {i+1}" for i in range(len(shadow_prices))],
                "Preço-Sombra": shadow_prices
            })
            st.table(shadow_df)

        except ValueError as e:
            st.error(f"Erro: {str(e)}")

if __name__ == "__main__":
    main()
