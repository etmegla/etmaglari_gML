# Homework 03 — Building Graph Representation (BGR)

## Overview

This homework models a building in Rhino, exports it as geometry, converts it into a graph, and uses a pre-trained Graph Machine Learning model to classify the building's relationship to the ground.

---

## Floor Plan

<img src="./MyFloorPlan.png" alt="My Floor Plan" width="100%">

The starting point is a building designed in Rhino. Four layers are exported as separate OBJ files:

| File | Layer Description |
|------|-------------------|
| `ground.obj` | Slab / podium |
| `columns.obj` | Structural columns |
| `offices.obj` | Office volumes |
| `core.obj` | Core + corridors |

---

## 13A — Creating the Building Graph (BGR Graph)

### Step 1 — Import Geometry

Each OBJ file is loaded using `Topology.ByOBJPath`. This produces a list of topology objects per building component.

### Step 2 — Assign Cell Categories

Faces from each component are flattened and merged into a `CellComplex` using `Topology.SelfMerge`. Each resulting cell is tagged with a dictionary containing:

- `cell_type` — integer category (0=ground, 1=column, 3=office, 4=core)
- `cell_name` — human-readable label
- `cell_color` — display color for visualisation

An internal vertex (selector) is placed inside each cell and carries this dictionary.

### Step 3 — Build the CellComplex

<img src="./CellComplex.png" alt="Cell Complex" width="100%">

All cells from all components are merged into a single `CellComplex` using `Topology.SelfMerge`. This creates a topologically consistent solid model where shared walls between adjacent spaces become internal faces.

### Step 4 — Transfer Dictionaries

<img src="./TransferDictionaries.png" alt="Transfer Dictionaries" width="100%">

The category dictionaries stored on the selectors are transferred onto the cells of the merged model using `Topology.TransferDictionariesBySelectors`. This links each spatial cell to its label (ground, column, office, core) so the graph can carry semantic information.

### Step 5 — Build the Adjacency Graph

`Graph.ByTopology(model)` converts the CellComplex into a graph where:

- **Nodes** = cells (spaces)
- **Edges** = shared faces (adjacency between spaces)

Each node is given a **one-hot encoded feature vector** from its `cell_type`:

```
cell_type 0 (ground)  → [1, 0, 0, 0, 0]
cell_type 1 (column)  → [0, 1, 0, 0, 0]
cell_type 3 (office)  → [0, 0, 0, 1, 0]
cell_type 4 (core)    → [0, 0, 0, 0, 1]
```

Features are stored as `feature_00` … `feature_04` on each vertex dictionary.

### Step 6 — Export to CSV

`Graph.ExportToCSV` writes three files used for model input:

| File | Contents |
|------|----------|
| `graphs.csv` | Graph-level label (manually assigned) |
| `nodes.csv` | Node IDs, features, and labels |
| `edges.csv` | Edge source/destination pairs |

---

## 13B — Predicting the Graph Label

### What the Model Does

A pre-trained **Graph Neural Network** (`bgr_model.pt`) was trained on the Building–Ground Relationship (BGR) dataset. It classifies a building graph into one of five categories based on how the building mass relates to the ground plane around it:

| Label | Category | Description |
|-------|----------|-------------|
| 0 | Separation | The building sits above the ground with a clear gap — no direct contact between the occupied floor and the ground surface. Typical of piloti structures. |
| 1 | Separation with Plinth | Same as Separation but a raised plinth or podium mediates the transition — the building still floats but a solid base element anchors it to the ground level visually and spatially. |
| 2 | Adherence | The building sits directly on the ground with no intermediate element — floors meet the ground plane flush. |
| 3 | Adherence with Plinth | The building sits on the ground but a plinth extends its footprint, giving it a broader base that blends into the surrounding landscape. |
| 4 | Interlock | The ground plane penetrates or wraps into the building — the boundary between interior and exterior ground is ambiguous. Typical of sunken courtyards or carved ground floors. |

### Why "Separation with Plinth" is its Own Category

**Separation with Plinth** (label 1) is distinct from pure Separation (label 0) because the plinth changes the topological structure of the graph. In Separation, the column nodes are the only elements bridging the ground and office layers — the graph has a sparse, linear connectivity. When a plinth is added, a new layer of cells (the podium volume) appears between the ground and the columns. This creates denser adjacency edges in the graph and a richer feature distribution. The GNN detects this structural difference in the node connectivity pattern, not just in the geometry shape.

---

### Pipeline

1. **Load dataset** — `PyG.ByCSVPath` reads the three CSV files into a PyTorch Geometric dataset
2. **Load model** — `pyg.LoadModel` loads the pre-trained weights from `bgr_model.pt`
3. **Set split** — The entire dataset is set as the test set (`split=(0.0, 0.0, 1.0)`)
4. **Predict** — `pyg.Predict()` runs inference and returns predicted labels, actual labels, and confidence scores

### Output

The output is a DataFrame with one row per graph (building):

| Column | Meaning |
|--------|---------|
| `Actual Value` | Integer label you manually assigned in `graphs.csv` (your assessment) |
| `Predicted Value` | Integer label the GNN assigned based on the graph structure |
| `Actual Label` | Human-readable name for your label |
| `Predicted Label` | Human-readable name for the model's prediction |
| `Confidence` | Probability the model assigned to its top prediction (0–1). A value close to 1.0 means the model is certain; a value around 0.2–0.4 means the graph sits ambiguously between categories. |

#### How to read the result

- **Match** (`Actual Label == Predicted Label`) — the model's learned graph patterns align with your spatial reading. This validates that the graph structure encodes the building-ground relationship correctly.
- **Mismatch** — the model sees a different structural pattern than you intended. This is worth investigating: check whether the adjacency graph has the topology you expect (e.g. are columns actually connecting ground to offices, or did the merge lose that connection?).
- **Low confidence on a correct prediction** — the building is topologically ambiguous, sitting between two categories. Consider whether the design intent is clearly expressed in the geometry.

The goal is to see whether the pre-trained model agrees with the designer's own assessment of how the building relates to the ground.
