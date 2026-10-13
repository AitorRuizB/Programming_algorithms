# 🧭 A* & A*-Epsilon Pathfinding Visualizer in 2D Multi-Terrain Grids

<p align="center">
  <img src="https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python">
  <img src="https://img.shields.io/badge/Pygame-GUI-008000?style=for-the-badge&logo=python&logoColor=white" alt="Pygame">
  <img src="https://img.shields.io/badge/Algorithm-A*%20%2F%20A*ε-FF5722?style=for-the-badge" alt="Pathfinding">
</p>

<p align="center">
  <!-- Optional: Add a GIF or screenshot of your Pygame interface here -->
  <img src="docs/demo.gif" alt="A* Pathfinding Demo" width="500">
</p>

## 📌 Overview

This project implements an informed heuristic search engine featuring both the classic **A* (A-Star)** algorithm and its bounded suboptimal variant, **A*-Epsilon ($A^*_\epsilon$)**, on a 2D multi-terrain grid environment. Built with **Python** and **Pygame**, the interactive visualizer allows users to place start and goal coordinates, switch between heuristics in real time, and analyze the trade-off between path distance ($f$) and terrain traversal energy cost (calories).

---

## ⚙️ Core Features & Algorithmic Details

### 1. 8-Directional Movement & Geometric Cost ($g$)

The agent can move in 8 possible directions from any given cell:

* **Horizontal / Vertical movements:** Base movement cost of $g = 1.0$.
* **Diagonal movements:** Base movement cost of $g = 1.5$.

### 2. Implemented Heuristics ($h$)

The algorithm evaluates $f(n) = g(n) + h(n)$ using four selectable admissible heuristics:

* **Trivial ($h = 0$):** Behaves like a standard uninformed uniform-cost / Dijkstra search, expanding nodes radially.
* **Euclidean Distance ($h = 1$):** $\sqrt{(dx - ox)^2 + (dy - oy)^2}$ — Ideal for open diagonal trajectories.
* **Manhattan Distance ($h = 2$):** $|dx - ox| + |dy - oy|$ — Demonstrated to be the most efficient heuristic in terms of minimum explored nodes across the test benchmark maps.
* **Diagonal / Octile Distance ($h = 3$):** $\max(|ox - dx|, |oy - dy|)$.

### 3. Multi-Terrain Calorie System & A*-Epsilon ($A^*_\epsilon$)

Standard A* optimizes strictly for geometric distance ($f$). However, different terrains require different energy expenditures:

| Terrain Type | Map Symbol | Grid Color | Energy Cost (Calories) |
| :--- | :---: | :---: | :---: |
| **Impassable Obstacle** | `#` (0) | Black | Non-traversable |
| **Valley / Plains** | `.` (1) | Beige / Orange | `2 cal` |
| **Swamp / Wetland** | `~` (2) | Light Blue | `4 cal` |
| **Mountain / Rocky** | `*` (3) | Dark Brown | `6 cal` |

When executing **A*-Epsilon (`A*e`)**, the strict optimality restriction is relaxed using a focal list ($L_{\text{focal}}$) governed by an $\epsilon$ factor:

$$L_{\text{focal}} = \{ n \in \text{Frontier} \mid f(n) \le (1 + \epsilon) \cdot \min_{m \in \text{Frontier}} f(m) \}$$

Instead of blindly picking the node with the lowest $f(n)$, the algorithm filters candidate nodes within the $(1 + \epsilon)$ suboptimality bound and selects the path that minimizes **accumulated calories (`cal`)**. This allows the agent to take slightly longer detours through plains (`2 cal`) to avoid exhausting swamps (`4 cal`) or mountains (`6 cal`).

---

## 📂 Repository Structure

* `main.py`: Pygame graphical interface, map parser, mouse event handler, and performance metrics logger (execution time, path cost `f`, total calories, and expanded nodes).
* `astar.py`: Core implementation of the `Nodo` class, heuristic evaluators, focal list builder (`construir_focal`), and the unified `astar()` search loop.
* `mapa_*.txt`: 2D ASCII grid maps representing diverse terrain distributions and obstacle layouts.
* `img_*.png`: UI sprites for the agent (rabbit), goal target (carrot), and control buttons.
* `docs/`: Technical report (`Práctica1_Aitor_Ruiz.pdf`) containing node expansion benchmarks and $\epsilon$-sensitivity analysis.

---

## 💻 How to Run

### 1. Prerequisites

Ensure you have Python 3 installed along with the `pygame` library:

    pip install pygame

### 2. Basic Execution (Interactive Mode)

Run `main.py` directly. By default, if no arguments are passed, it loads `mapa_12x12_variado.txt`:

    python3 main.py

To load a specific map file (e.g., `mapa5.txt` or `mapa_traza_eps.txt`):

    python3 main.py mapa5.txt

### 3. Advanced CLI Execution

You can also pre-configure the origin `(filO, colO)`, destination `(filD, colD)`, initial heuristic `(0-3)`, and `epsilon` value via command-line arguments:

    python3 main.py <map_file.txt> <filO> <colO> <filD> <colD> <heuristic_id>

Example:

    python3 main.py mapa_12x12_variado.txt 1 1 10 10 2

---

## 🎮 Interactive GUI Controls

Once the Pygame window is open:

1. **Left-Click** on any valid terrain cell to place the **Start Agent (Rabbit 🐰)**.
2. **Right-Click** on any valid terrain cell to place the **Goal Target (Carrot 🥕)**.
3. **Bottom-Right Buttons:**
   * **`Heur`:** Cycles through the 4 available heuristics (*Trivial -> Euclidean -> Manhattan -> Diagonal*).
   * **`A*`:** Computes and draws the shortest geometric path ($\epsilon = 0$) in yellow.
   * **`A*e`:** Computes and draws the calorie-optimized path using the relaxed focal search ($\epsilon > 0$).
4. Check the bottom-left HUD (or terminal output) to inspect the resulting distance cost (`f`), energy spent (`Cal`), number of explored nodes, and computation time.

---
*Developed by Aitor Ruiz Bautista — Intelligent Systems, Robotics Engineering at Universidad de Alicante.*
