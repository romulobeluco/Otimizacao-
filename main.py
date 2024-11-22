import pulp as pl

class SimplexSolver:
    def __init__(self, num_vars, c, A, b):
        self.num_vars = num_vars  # Número de variáveis
        self.c = c                # Coeficientes da função objetivo
        self.A = A                # Coeficientes das restrições
        self.b = b                # Lados direitos das restrições

    def solve(self):
        # Criar o modelo do problema
        model = pl.LpProblem("Maximize", pl.LpMaximize)

        # Criar as variáveis de decisão
        vars = [pl.LpVariable(f"x{i+1}", lowBound=0) for i in range(self.num_vars)]

        # Adicionar a função objetivo
        model += pl.lpDot(self.c, vars), "Função Objetivo"

        # Adicionar as restrições
        for i in range(len(self.A)):
            model += pl.lpDot(self.A[i], vars) <= self.b[i], f"Restrição {i+1}"

        # Resolver o problema
        model.solve()

        # Verificar se a solução é ótima
        if model.status != pl.LpStatusOptimal:
            raise ValueError("O problema não tem solução ótima.")

        # Obter os resultados
        solution = [v.varValue for v in vars]
        optimal_value = pl.value(model.objective)
        shadow_prices = [constraint.pi for name, constraint in model.constraints.items()]

        return solution, optimal_value, shadow_prices
