"""Week 3 studio — starter (formulation + the four algorithms).

You fill in three things. Run ``python3 test_search.py`` as you go.

  Task 1  MissionariesAndCannibals  -- formulate the five components (graded).
  Task 2  bfs / dfs / ucs / ids     -- four algorithms, one search loop.
  Task 3  the measurement harness    -- run all four on the 8-puzzle bank.

The provided tests include ``test_bfs_suboptimal_nonuniform_cost``, which asserts
that BFS returns a NON-optimal path. That is not a broken test: BFS's optimality
claim has a condition (uniform step costs), and this instance violates it. Watching
a guarantee fail once is how you learn the guarantee is real.
"""
from search import Problem, Node, search


# ---- Task 1: formulate missionaries & cannibals -----------------------------
# Three missionaries, three cannibals, one boat that carries 1 or 2 and cannot
# cross empty. If cannibals ever outnumber missionaries on EITHER bank (and a
# missionary is present), the missionaries are eaten. Get everyone to the far
# bank. Formulation is a design decision -- you must be able to defend whether
# illegal states are excluded by ``actions()`` or by ``result()``.
#
# Suggested state: (m_left, c_left, boat_side) where boat_side is 0=left, 1=right
# and m_left/c_left count the people on the LEFT bank. Initial (3, 3, 0),
# goal (0, 0, 1). But this is YOUR call -- justify it in the demo.

class MissionariesAndCannibals(Problem):
    # Orden fijo: facilita reproducir la misma solución en cada ejecución.
    LOADS = ((1, 0), (0, 1), (2, 0), (0, 2), (1, 1))

    def __init__(self):
        super().__init__((3, 3, 0), (0, 0, 1))

    @staticmethod
    def is_valid(state):
        """Verificamos cantidades y seguridad en AMBAS orillas."""
        m, c, boat = state
        return (0 <= m <= 3 and 0 <= c <= 3 and boat in (0, 1)
                and (m == 0 or m >= c)
                and (3 - m == 0 or 3 - m >= 3 - c))

    def actions(self, state):
        # La búsqueda recibe únicamente acciones legales; result transforma.
        if not self.is_valid(state):
            return []
        m, c, boat = state
        available_m, available_c = (m, c) if boat == 0 else (3 - m, 3 - c)
        return [load for load in self.LOADS
                if load[0] <= available_m and load[1] <= available_c
                and self.is_valid(self.result(state, load))]

    def result(self, state, action):
        # Precondición: action pertenece a actions(state).
        # Al salir de la izquierda restamos; al regresar sumamos.
        m, c, boat = state
        dm, dc = action
        direction = -1 if boat == 0 else 1
        return (m + direction * dm, c + direction * dc, 1 - boat)

    def is_goal(self, state):
        return state == self.goal

    # Heredamos step_cost = 1: minimizar costo equivale a minimizar cruces.


# ---- Task 2: the four algorithms -- one search loop, four frontiers ---------
# search(problem, frontier_kind) is GIVEN in search.py. Three of these are one
# line: pick the frontier discipline. IDS is the interesting one -- it does NOT
# use search(); you write a depth-limited DFS and iterate the limit, buying BFS's
# completeness at DFS's O(bd) memory by re-doing the shallow work.

def bfs(problem):
    """Breadth-first search. Complete; optimal only when step costs are uniform."""
    return search(problem, "fifo")


def dfs(problem):
    """Depth-first (graph) search. The explored set is what makes it terminate on
    cyclic graphs -- do not remove it. Not optimal."""
    return search(problem, "lifo")


def ucs(problem):
    """Uniform-cost search. Optimal for any non-negative step costs."""
    return search(problem, "priority")


def depth_limited(problem, limit):
    """Recursive tree search to a fixed depth.

    Return (node, expansions, hit_limit): ``node`` is the goal Node or None;
    ``expansions`` counts expanded nodes; ``hit_limit`` is True iff the search was
    cut off by the depth limit (as opposed to exhausting the subtree). The
    hit_limit flag is what lets ids() know whether deepening further can help.

    Hint: skip the immediate parent state to avoid trivial 2-cycles at no memory
    cost, then recurse with limit-1.
    """
    if not isinstance(limit, int) or limit < 0:
        raise ValueError("limit debe ser un entero no negativo")
    expansions = 0
    on_path = {problem.initial}

    def visit(node, remaining):
        nonlocal expansions
        if problem.is_goal(node.state):
            return node, False
        if remaining == 0:
            # Un límite en una hoja agotada no es un corte real.
            # Inspeccionar sucesores aquí no se cuenta como expandir:
            # no creamos nodos ni continuamos por sus ramas.
            can_continue = any(problem.result(node.state, action) not in on_path
                               for action in problem.actions(node.state))
            return None, can_continue

        expansions += 1
        hit_limit = False
        for action in problem.actions(node.state):
            state = problem.result(node.state, action)
            if state in on_path:
                continue
            child = Node(state, node, action,
                         node.g + problem.step_cost(node.state, action))
            on_path.add(state)
            found, cutoff = visit(child, remaining - 1)
            on_path.remove(state)
            if found is not None:
                return found, False
            hit_limit = hit_limit or cutoff
        return None, hit_limit

    found, hit_limit = visit(Node(problem.initial), limit)
    return found, expansions, hit_limit


def ids(problem, max_depth=40):
    """Iterative deepening: call depth_limited with limit = 0, 1, 2, ... until a
    goal is found. Return (node, total_expansions). If a level reports it was NOT
    cut off and found nothing, the space is exhausted -- return (None, total)."""
    if not isinstance(max_depth, int) or max_depth < 0:
        raise ValueError("max_depth debe ser un entero no negativo")
    total = 0
    for limit in range(max_depth + 1):
        node, expansions, hit_limit = depth_limited(problem, limit)
        total += expansions
        if node is not None or not hit_limit:
            return node, total
    # None también puede significar que alcanzamos max_depth, no imposibilidad.
    return None, total


# ---- Task 3: measurement (fill in after Task 2 passes) ----------------------
def measure(bank=None):
    """Run all four on the 8-puzzle bank and return rows of
    (depth, algorithm, expansions, solution_length). Then plot expansions vs.
    depth on a LOG y-axis -- that log-scale plot is the deliverable."""
    from search import load_instances, EightPuzzle
    bank = load_instances() if bank is None else bank
    rows = []
    for depth in sorted(bank):
        for state in bank[depth]:
            p = EightPuzzle(state)
            for name, algo in [("BFS", bfs), ("DFS", dfs),
                               ("UCS", ucs), ("IDS", ids)]:
                node, exp = algo(p)
                if node is None:
                    raise RuntimeError(f"{name} no resolvió la instancia de profundidad {depth}")
                rows.append((depth, name, exp, len(node.path())))
    return rows


if __name__ == "__main__":
    # Smoke test: solve the depth-8 instance with each algorithm you've filled in.
    from search import EightPuzzle, D8
    p = EightPuzzle(D8)
    for name, algo in [("bfs", bfs), ("dfs", dfs), ("ucs", ucs), ("ids", ids)]:
        try:
            node, exp = algo(p)
        except NotImplementedError:
            print(f"  {name:<5} not implemented yet")
            continue
        print(f"  {name:<5} len={len(node.path()):>4}  expansions={exp:,}")
