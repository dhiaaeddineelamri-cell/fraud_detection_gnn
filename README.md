# Nexus AI: Graph-Based Detection of Organized Insurance Fraud

Interactive demo built by team **Pied Piper** for the **EY × Université Paris-Dauphine Tunis Hackathon 2025
("Smart Assurance")**, where the team won **1st place among 18 teams** (100+ participants).

Rule-based fraud checks look at claims one at a time and miss **collusion**: groups of patients, doctors,
pharmacies or car owners working together. This demo represents claims as a **network** and uses graph
analytics to surface organized fraud rings.

> Scope note: the competition model was a graph neural network (GNN) on a heterogeneous, multi-relational
> claims graph. This repository is the interactive **demo**: it uses classical graph algorithms (NetworkX)
> on synthetic data to illustrate the same idea. It does not contain the trained GNN.

## What it detects
- **Star topologies**: hub-based collusion (for example one doctor and one pharmacy linked to many patients)
- **Circular patterns**: staged-accident loops between car owners
- **Dense communities**: tightly connected groups of entities

## How it works
1. **Synthetic data** (`data_generator.py`): 500 normal claims with random associations, plus 2 injected rings:
   Ring A (1 doctor + 1 pharmacy + 20 patients) and Ring B (5 car owners in a collision loop).
2. **Graph analysis** (`graph_logic.py`): graph construction, Louvain community detection, degree centrality,
   clustering coefficient, and a combined 0–100 risk score per entity; ring identification and pattern typing.
3. **Dashboard** (`app.py`): Streamlit app with an interactive PyVis graph (risk colour-coding), summary metrics,
   rule-generated explanations for each detected ring, and a top-10 riskiest entities table.

Also included: `medical_fraud_detection_generator.py` and `medical_fraud_detection_dataset.csv`, a synthetic
pharmacy-prescription dataset (1,000 rows) for medical-insurance fraud experiments.

On the bundled synthetic data the demo flags both injected rings.

## Quick start
```bash
pip install -r requirements.txt
streamlit run app.py      # opens http://localhost:8501
```
Then click **"Ingest Data & Scan for Fraud"**, explore the graph, and read the ring reports.

## Project structure
```
app.py                               Streamlit dashboard
graph_logic.py                       graph construction, communities, risk scoring, ring detection
data_generator.py                    synthetic claims with two injected fraud rings
medical_fraud_detection_generator.py synthetic prescription dataset generator
medical_fraud_detection_dataset.csv  generated prescription dataset
requirements.txt
```

## Tech stack
Python, Streamlit, NetworkX, python-louvain, PyVis, pandas, Faker

## Context
Team Pied Piper, EY × Université Paris-Dauphine Tunis Hackathon 2025. All data in this repository is synthetic.
