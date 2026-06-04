# Homework 02 — Spatial Intelligence

[![My Floor Plan](Homework02/Images/MyFloorPlan.png)](Homework02/Images/MyFloorPlan.png)

My house has two programmatic wings. The long horizontal bar to the left holds my public and service spaces — Entry, Pantry, WC, Kitchen, Dining, and Living Room. The vertical block to the right holds my private programme — Bedrooms 1, 2, and 3, Bath, Family Room, and Closet. The junction between the two wings is the spatial hinge of my home, and it becomes the most important point in every analysis that follows.

---

## Image 1 — My Base Floor Plan

[![Image 1](Homework02/Images/Image1.png)](Homework02/Images/Image1.png)

This is my house loaded from the OBJ file and projected flat into a top-down 2D view. I can clearly read my two programmatic wings: the long horizontal bar to the left holds my public and service spaces — Entry, Pantry, WC, Kitchen, Dining, and Living Room — while the vertical block to the right holds my private programme — Bedrooms 1, 2, and 3, Bath, Family Room, and Closet. The junction between the two wings is the spatial hinge of my home, and it becomes the most important point in every analysis that follows.

---

## Image 2 — My Floor Plan with a 1-Unit Grid

[![Image 2](Homework02/Images/Image2.png)](Homework02/Images/Image2.png)

Here I drape a fine uniform grid over my entire floor plan. Every cell that falls inside my walkable area will become a node in my graph. The grid respects my walls and door openings — it does not simply tile space blindly, it reads my geometry.

---

## Image 3 — Grid Clipped to My Floor Area

[![Image 3](Homework02/Images/Image3.png)](Homework02/Images/Image3.png)

This is my grid after trimming. Every cell outside my walls is removed, leaving only the walkable interior. What remains is a pixelated version of my house — this is the discretised space my graph algorithms will analyse. The small service rooms on the left (Pantry, WC, Storage) already show up as tight clusters of cells compared to the generous open cells of my Living Room.

---

## Image 4 — My Topologic Graph

[![Image 4](Homework02/Images/Image4.png)](Homework02/Images/Image4.png)

Each surviving grid cell becomes a red node, and adjacent walkable cells are connected by red edges. The result is a graph that faithfully represents my floor plan as a network. I can see the irregular clusters near my Pantry, WC, and Storage — those small rooms force the graph to navigate around walls and openings rather than connecting freely. My Living Room, by contrast, reads as a dense, well-connected mesh.

---

## Image 5 — My Shortest Path vs Straightened Path

[![Image 5](Homework02/Images/Image5.png)](Homework02/Images/Image5.png)

I compute a route between two points — roughly from my Entry/Foyer end to the Family Room and Closet in the lower-right of my bedroom wing:

- **Red** — the true grid-shortest path, stepping cell by cell. It stair-cases along the corridor exactly as the graph sees it.
- **Blue** — a post-processed straightened version. The diagonal line I would actually walk if the space were clear.

Both paths converge through the junction between my two wings. This confirms something I already know intuitively about my plan: there is one unavoidable bottleneck between my public and private zones, and every journey in my house passes through it.

---

## Image 6 — Closeness Centrality: How Integrated Is Each Space?

[![Image 6](Homework02/Images/Image6.png)](Homework02/Images/Image6.png)

The colour scale runs from **dark purple (least integrated)** through orange to **bright yellow (most integrated)**. A cell scores high if it is on average closest to every other cell in my house — it is easy to reach and easy to leave from.

- **Yellow** — the corridor junction between my Living Room and the entrance to my bedroom wing. This is the spatial core of my home — the single point most reachable from everywhere else.
- **Orange** — my Living Room and Dining area. These perform very well — open-plan design rewards integration.
- **Cool purple/blue** — my far ends: the Pantry and WC cluster on the left, and Bedroom 2 at the top and the Closet at the bottom-right. These are my most segregated spaces. They are intentionally tucked away, and the graph confirms it — you have to travel to reach them, and you do not pass through them on the way to anywhere else.

My open-plan Living and Dining zone is the spatial heart of my home by every measure.

---

## Image 7 — Betweenness Centrality: Which Path Does Everyone Use?

[![Image 7](Homework02/Images/Image7.png)](Homework02/Images/Image7.png)

The colour scale runs from **near-black (never traversed)** to **bright purple/violet (most traversed)**. A cell scores high if it appears on the greatest number of shortest routes between all pairs of spaces in my house.

- **Bright violet line** — my main corridor spine, running from the Living Room through to the bedroom wing entrance. This thin line is the entire circulation skeleton of my house — any journey between my private bedrooms and my public living spaces must pass through it.
- **Everything else near black** — my rooms themselves carry almost no through-traffic. They are destinations, not connectors.

What this tells me is that my corridor is architecturally irreplaceable. It is not wasted space — it is the one element holding both halves of my house together. If it were narrowed or obstructed, my plan would functionally split into two disconnected zones.

---

## Image 8 — Community Detection: My House Splits Into Two Zones

[![Image 8](Homework02/Images/Image8.png)](Homework02/Images/Image8.png)

After clustering the graph, my floor plan naturally partitions into two spatial communities. Red dots mark zone centroids; red lines connect adjacent zones:

- **Left community** — my public and service zone: Entry, Pantry, WC, Kitchen, Dining, Living Room.
- **Right community** — my private zone: Bedrooms 1–3, Bath, Family Room, Closet.

There is a single connecting edge between the two centroids — the junction. This confirms that my plan has a clean public/private separation with one controlled threshold between them. The graph found my programmatic logic without being told what the rooms were.

---

## Image 9 — Degree Centrality: Which Spaces Have the Most Immediate Neighbours?

[![Image 9](Homework02/Images/Image9.png)](Homework02/Images/Image9.png)

The colour scale runs from **dark blue (few direct neighbours)** to **yellow/orange (many direct neighbours)**. Unlike closeness centrality — which measures how reachable a space is globally — degree centrality is purely local: it counts only the cells immediately touching each node.

- **Yellow/orange** — my open-plan Living Room and the junction area. Large unobstructed spaces have cells touching them in all four directions, so they score high.
- **Cool blue** — my narrow corridor spine and my small service rooms. Even though the corridor is the most-traversed path in the house (as betweenness showed), it scores low here because it is narrow — few cells sit directly beside it.

Together, Images 6 and 9 tell me something important: my **Living Room is both locally rich and globally central** — it has many immediate neighbours and is easy to reach from everywhere. My **corridor is globally critical but locally thin** — essential for movement, but not a place to linger. My **service rooms are intentionally isolated** in both measures. My plan does exactly what I designed it to do.
