# config.py ───────────────────────────────────────────────────────────────────
# Only edit REPO_ROOT to match where you cloned the repo on your machine.

REPO_ROOT = r"C:\Users\etmaglari\IAAC\etmaglari_gML"

# ── Camera: single floor (top down) ───────────────────────────────────────────
CAM_SINGLE     = [0, 0, 6]
CAM_SINGLE_CTR = [0, 0, 0]
CAM_SINGLE_UP  = [0, 0, 1]
CAM_SINGLE_PRJ = "orthographic"

# ── Camera: stacked multi-floor ───────────────────────────────────────────────
CAM_STACK      = [1.5, -1.5, 1.2]
CAM_STACK_CTR  = [0, 0, 0]
CAM_STACK_UP   = [0, 0, 1]
CAM_STACK_PRJ  = "orthographic"

# ── Graph styling (shared across notebooks) ───────────────────────────────────
GRAPH_NODE_SIZE_KEY  = "size"
GRAPH_NODE_COLOR_KEY = "color"
GRAPH_NODE_LABEL_KEY = "label"
GRAPH_EDGE_COLOR     = "#6F6F6F"
GRAPH_EDGE_WIDTH     = 3
GRAPH_BG_DARK        = "white"
GRAPH_BG_LIGHT       = "white"