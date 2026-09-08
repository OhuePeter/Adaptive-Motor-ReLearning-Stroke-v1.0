# Schematic figure: upper-limb Inkscape workflow

Goal: an editable upper-limb schematic for Fig. 1, same style as Fig. 1 in the first paper.

## Step 1 — Get a reference image you're legally allowed to redraw

Do not trace a random Google Images result. Use one of these instead:

- OpenStax Anatomy & Physiology (CC BY 4.0): https://openstax.org/details/books/anatomy-and-physiology-2e — search "upper limb" or "shoulder girdle."
- Wikimedia Commons: https://commons.wikimedia.org — search "upper limb skeleton" or "arm bones diagram." Check the license tag on the file page before using it.
- BodyParts3D / Anatomography (CC BY-SA, on Wikimedia) — simple line-art style, easy to trace.
- Gray's Anatomy 1918 plates — public domain, mirrored on Wikimedia Commons.

Save the URL and license. You'll need one line of attribution in the caption.

## Step 2 — Set up the tracing layer in Inkscape

1. File → Import → select your reference image.
2. Open the Layers panel (Layer → Layers...).
3. Click the padlock icon next to that layer to lock it. Locked layers can't be edited, so you won't accidentally drag the reference around.
4. Layer → Add Layer → name it "artwork". This is where you'll draw.

## Step 3 — Draw the limb outline

1. Select the pen/Bezier tool (keyboard shortcut: `B`).
2. Click node by node along the arm outline in the reference image, following the shoulder, upper arm, elbow, forearm, and hand.
3. Press `Enter` to finish the path.
4. Select the path, then use the node tool (`N`) to smooth curves: select a node, click "make selected nodes smooth" in the toolbar.

If you'd rather start from an automatic trace and clean it up:
1. Select the reference image (unlock it first).
2. Path → Trace Bitmap (`Shift+Alt+B`).
3. Choose "Edge detection", click OK.
4. Re-lock the reference, then use the node tool to delete/simplify the extra nodes the auto-trace adds; auto-trace alone is too messy to publish as-is.

## Step 4 — Add joint markers and angles

1. Ellipse tool (`E`): draw a small filled circle at the shoulder, elbow, and wrist. These mark your state variables, same convention as Fig. 1 in paper 1.
2. Arc tool (also under the ellipse tool, set to "arc" mode in the toolbar): draw the joint-angle arc at the elbow.
3. Text tool (`T`): label each marker and angle. Use Arial or Helvetica to match your other figures.

## Step 5 — Match the existing colour palette

Use the same hex codes as `presentation/poster/create_poster.py`:

| Colour | Hex |
|---|---|
| Deep blue | `#00355f` |
| Teal | `#2a9d8f` |
| Coral | `#e76f51` |
| Gold | `#f0c040` |

To set a fill/stroke colour: select the object, open Fill & Stroke (`Shift+Ctrl+F`), type the hex code in the RGBA field.

## Step 6 — Organize layers before export

Put each element type on its own layer: outline, joint markers, angle arcs, text labels. This makes later edits (a reviewer asking to change a label, for example) fast: you just toggle or edit one layer.

## Step 7 — Delete the reference layer

Layer → select the locked reference layer → Layer → Delete Current Layer. Do this before exporting, or the reference image will show up in your export.

## Step 8 — Export

- SVG: File → Save As → choose "Plain SVG" from the file-type dropdown. This is `paper/figures/fig1_schematic.svg`.
- PNG: File → Export PNG Image (`Shift+Ctrl+E`). Set DPI to 600 in the export panel. Make sure "export area" is set to the drawing, not the full page (otherwise you get extra white space). Save as `paper/figures/fig1_schematic.png`.

## Step 9 — Add the attribution line

In the figure caption or in `ACKNOWLEDGEMENTS.md`, write one line, e.g.:

> Upper-limb schematic adapted from [source name], [license], redrawn in Inkscape.

