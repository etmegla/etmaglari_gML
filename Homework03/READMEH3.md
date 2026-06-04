# Homework 03 — Building Graph Representation

This homework is about turning a building model into a graph that a machine learning model can read and classify. The idea is to take a building designed in Rhino, break it down into spatial cells, and then describe the relationships between those cells as a network of nodes and edges. A pre-trained model then looks at that network and tells us how the building relates to the ground.

---

## The Building

<img src="./MyFloorPlan.png" alt="My Floor Plan" width="100%">

The building was modelled in Rhino and exported as four separate OBJ files — one for each type of space: the ground slab, the columns, the office volumes, and the core. Each file becomes a separate input in the notebook.

---

## Part 1 — Building the Graph (13A)

The first notebook takes those four OBJ files and turns them into a topological graph.

**Importing and tagging**

Each OBJ is loaded with `Topology.ByOBJPath`. The faces are extracted and merged into a solid volume using `Topology.SelfMerge`, which finds all the cells inside. Each cell gets labelled — ground, column, office, or core — along with a colour for visualisation. That label is stored in a small dictionary attached to a point placed inside the cell (called a selector).

**Building the CellComplex**

<img src="./CellComplex.png" alt="Cell Complex" width="100%">

All the cells from all four components are merged together into one unified `CellComplex`. Where two spaces share a wall, that wall becomes an internal face. This is the core topological model — a solid representation where every space knows its neighbours.

**Transferring the labels**

<img src="./TransferDictionaries.png" alt="Transfer Dictionaries" width="100%">

The labels from the selectors are transferred onto the cells of the merged model using `Topology.TransferDictionariesBySelectors`. After this step, every cell in the CellComplex knows what type it is.

**Making the graph**

`Graph.ByTopology` converts the CellComplex into a graph. Each cell becomes a node, and each shared face between two cells becomes an edge. To give the model something to work with, each node gets a one-hot encoded feature vector based on its type:

```
ground  → [1, 0, 0, 0, 0]
column  → [0, 1, 0, 0, 0]
office  → [0, 0, 0, 1, 0]
core    → [0, 0, 0, 0, 1]
```

These features are exported to CSV as `feature_00` through `feature_04`, along with the edges and a manually assigned graph label.

---

## Part 2 — Predicting the Label (13B)

The second notebook loads that CSV data, feeds it to a pre-trained Graph Neural Network, and asks: what kind of building-ground relationship does this graph describe?

**The five categories**

The model was trained on the Building–Ground Relationship dataset and recognises five types:

- **Separation** — the building floats above the ground, typically on pilotis. No direct contact between the occupied floors and the earth.
- **Separation with Plinth** — same idea, but a solid base element sits between the ground and the raised building. The building still lifts off, but the plinth anchors it visually and spatially.
- **Adherence** — the building simply sits on the ground, floors flush with the earth, no intermediary.
- **Adherence with Plinth** — sits on the ground but with a podium that extends the footprint and merges into the surrounding landscape.
- **Interlock** — the ground wraps into the building or vice versa. The boundary between inside and outside at ground level is deliberately blurred — think sunken courtyards or carved ground floors.

**Why Separation with Plinth is its own category**

It might seem like a minor variation, but topologically it is quite different. In pure Separation, the only bridge between the ground cells and the office cells is the column nodes — the graph is sparse and linear. Add a plinth and you get an entirely new layer of cells sitting between the ground and the columns. That changes the connectivity pattern significantly: more edges, more neighbours, a denser subgraph around the base. The GNN picks up on that structural difference, not just the shape.

**Reading the output**

After running the prediction, the notebook shows a table comparing the label you assigned manually to the one the model predicted, along with a confidence score.

If they match and confidence is high, the graph structure is cleanly encoding the spatial idea you had in mind. If they don't match, it's worth looking at the actual graph — sometimes the merge loses a connection, or a column doesn't end up adjacent to the ground the way you expected. If confidence is low even on a correct prediction, the building probably sits between two categories, which is itself a meaningful spatial observation.