# Homework 03 — Building Graph Representation

I modelled a building in Rhino, converted it into a spatial graph, and used a pre-trained GNN to classify how it relates to the ground.

---

## My Building

<img src="./MyFloorPlan.png" alt="My Floor Plan" width="100%">

I exported four OBJ files from Rhino — ground slab, columns, office volumes, and core — one per space type. Each becomes a separate input in the notebook.

---

## Part 1 — Building the Graph (13A)

**Importing and tagging**

I loaded each OBJ with `Topology.ByOBJPath`, merged the faces into solid volumes with `Topology.SelfMerge`, and tagged every cell with its type (ground, column, office, core) and a colour. Each label is stored in a dictionary attached to a selector point inside the cell.

**Building the CellComplex**

<img src="./CellComplex.png" alt="Cell Complex" width="100%">

I merged all cells into one `CellComplex`. Where two spaces share a wall, that wall becomes an internal face — every cell now knows its neighbours.

**Transferring the labels**

<img src="./TransferDictionaries.png" alt="Transfer Dictionaries" width="100%">

I transferred the selector dictionaries onto the merged cells using `Topology.TransferDictionariesBySelectors`, so every cell in the CellComplex carries its type label.

**Making the graph**

I ran `Graph.ByTopology` to convert the CellComplex into a graph — each cell is a node, each shared face is an edge. I one-hot encoded each node's type as features:

```
ground  → [1, 0, 0, 0, 0]
column  → [0, 1, 0, 0, 0]
office  → [0, 0, 0, 1, 0]
core    → [0, 0, 0, 0, 1]
```

I exported the result to CSV as `feature_00` through `feature_04`, ready for the model.

---

## Part 2 — Predicting the Label (13B)

I loaded the CSV into a PyTorch Geometric dataset, loaded the pre-trained `bgr_model.pt`, and ran `Predict()`. The model classifies each graph into one of five building-ground relationship types:

- **Separation** — the building floats above the ground on pilotis, no direct contact with the earth
- **Separation with Plinth** — same, but a solid base mediates between ground and the raised building
- **Adherence** — floors sit flush on the ground, no intermediary
- **Adherence with Plinth** — on the ground, but a podium extends and anchors the footprint
- **Interlock** — the ground penetrates into the building; the boundary is deliberately blurred

The output compares my manually assigned label against the model's prediction and shows a confidence score.

---

## Why My Building Was Classified as Separation with Plinth

I assigned label 0 (Separation), but the model predicted label 1 (Separation with Plinth).

Looking at my model, the green ground slab is thick, continuous, and spans the full footprint of both volumes — it sits below the columns, not around them. In the graph, the single ground node connects to all **27 column nodes**, which is a very dense connection for what I thought was a simple raised floor. That high-degree base node looks exactly like a plinth to the model. In a true pilotis building, you'd expect far fewer, widely spaced columns and a sparse ground connection.

The model read my ground slab as a plinth because, structurally, it behaves like one.
