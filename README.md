# Quantum Optimization for Industrial Engineers — Companion Code

Code for the book *Quantum Optimization for Industrial Engineers: A Step-by-Step Journey from Quantum Ideas to Metaheuristics and IBM Quantum Computers*, by Mostafa Hajiaghaei-Keshteli and Fatemeh Gholian-Jouybari.

Every number, table, and figure printed in the book is produced by a script in this repository. Each `chapterNN/` folder holds the scripts of that chapter (`listing_*.py`, `ex*.py`, `exNN_*.py`), the shared modules it imports, and, from Chapter 10 on, the saved outputs (`outputs/*.txt`) and the figure scripts (`fig/`).

## Install

```text
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

The printed outputs were produced with Python 3.12.3, qiskit 2.5.2, qiskit-aer 0.17.2, and qiskit-ibm-runtime 0.50.0 (October 2026). With other versions, random seeds may give slightly different counts.

## Run

Run every script from inside its own chapter folder, for example:

```text
cd chapter13
python ex08_optimizer.py
```

Scripts that need a file written by an earlier example (for example `angles.json` in Chapters 13 and 14) say so in their first lines; the file is included.

## A note on hardware results

All hardware results in the book come from IBM's simulators and from calibration snapshots of real IBM devices (`FakeFez`, `FakeMarrakesh`, `FakeKingston`, `FakeTorino`). They are simulations with recorded calibration data, not runs on the devices themselves. The scripts `chapter10/real_hw.py` and `chapter14/real_hw_tsp.py` are optional: they run the same circuits on a real IBM quantum processor with your own IBM Quantum account. Never put your API key in shared code.

## Map of the chapters

| Folder | Chapter |
|---|---|
| chapter02 | Why Quantum for an Industrial Engineer? (rules, enumeration, 2-opt) |
| chapter03 | The Mathematical Toolkit (NumPy versions of all examples) |
| chapter04 | Qubits, Measurement, and Circuits (a 40-line simulator) |
| chapter05 | Quantum Algorithms and Their Lessons |
| chapter06 | The Q-bit Chromosome (QEA) |
| chapter07 | Quantum-Inspired Metaheuristics and the Keshtel Algorithm |
| chapter08 | From an Industrial Model to QUBO |
| chapter09 | Solving QUBO Classically; Fair Experiments |
| chapter10 | My First Circuit on IBM |
| chapter11 | From Orders and Tours to Bit Strings |
| chapter12 | Grover Search |
| chapter13 | QAOA for the Single-Machine Workshop |
| chapter14 | QAOA for the TSP, and Real Hardware |
| chapter15 | Quantum versus Heuristics, Head to Head |
| appendix | Appendices A and B (Python as needed; installation and versions) |
| answers | Programs that verify the answers to the exercises of Chapters 1 to 11 (Chapters 12 to 15 keep `check_answers.py` in their own folders) |

## License

MIT (see `LICENSE`). If you use this code in teaching or research, please cite the book.
