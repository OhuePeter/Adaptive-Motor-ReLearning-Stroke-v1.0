# Schematic figure workflow: upper-limb anatomy for Fig. 1

Goal: a clean, editable, publication-quality schematic of the upper limb (shoulder–elbow–wrist–hand chain) showing the reach plane, joint angles, and sensor placement — in the same visual style as Fig. 1 of `NeuroRL-ObstacleAvoidance-v1.0`.

## 1. Get a legally reusable anatomical reference (do not trace copyrighted stock art)

Do not screenshot/trace an arbitrary Google Images result — most upper-limb illustrations are copyrighted stock art or textbook figures. Use one of these public-domain / open-licensed sources instead:

- **OpenStax Anatomy & Physiology** (CC BY 4.0) — https://openstax.org/details/books/anatomy-and-physiology-2e — search "upper limb," "shoulder girdle," or "brachial plexus." Free to redraw/derive with attribution.
- **Wikimedia Commons** — https://commons.wikimedia.org — search "upper limb skeleton" or "arm bones diagram," filter by license (public domain / CC BY-SA). Check the file's license tag on its page before using.
- **BodyParts3D / Anatomography** (CC BY-SA, via Wikimedia) — simple, clean 3-D-derived line art good for tracing.
- Gray's Anatomy (1918 edition) plates — public domain (copyright expired), widely mirrored on Wikimedia Commons.

Record the source URL and license for your figure caption / methods (e.g., "Adapted from [source], CC BY 4.0").

## 2. Redraw (don't just re-export) in Inkscape

1. **Import as a locked tracing layer**: File → Import the reference PNG/JPG. Lock this layer (Layers panel → padlock icon) so you don't accidentally edit it.
2. **New layer on top** for your vector artwork.
3. **Trace Bitmap** (optional starting point): Path → Trace Bitmap (Shift+Alt+B) → "Edge detection" or "Multiple scans: grayscale" for a rough outline, then clean up nodes manually — don't rely on auto-trace alone, it produces messy paths.
4. **Manual redraw (preferred for a clean figure)**: Use the Bezier/pen tool (B) to trace the limb outline and joint landmarks freehand over the locked reference, snapping to key anatomical points (acromion/shoulder, lateral epicondyle/elbow, ulnar styloid/wrist).
5. Use the **Ellipse tool** (E) for joint markers (shoulder, elbow, wrist) as filled circles, consistent with how Fig. 1 in paper 1 marks its state variables.
6. Add joint-angle arcs with the **Arc tool** and label with the **Text tool** (T) — match the font used elsewhere in your figures (Arial/Helvetica, per `create_poster.py`'s `plt.rcParams`).
7. Delete or hide the locked reference layer before exporting (Layer → Delete, or just uncheck visibility and confirm it's excluded from export).

## 3. Style consistency with the rest of the paper

- Match the Queen's palette used in `presentation/poster/create_poster.py`: deep blue `#00355f`, teal `#2a9d8f`, coral `#e76f51`, gold `#f0c040`.
- Keep stroke widths and font sizes consistent with `paper/figures/fig1_schematic.svg` from paper 1 (open it in Inkscape side-by-side as a style reference).
- Use layers to separate: (1) anatomy outline, (2) joint markers, (3) angle/vector annotations, (4) text labels — this makes later edits/reviewer requests fast.

## 4. Export

- **SVG**: File → Save As → "Plain SVG" (keeps it editable, avoids Inkscape-specific metadata bloat). This becomes `paper/figures/fig1_schematic.svg`.
- **PNG**: File → Export PNG Image → set **600 DPI**, export only the drawing (not the page background) → save as `paper/figures/fig1_schematic.png`. This matches the workflow in `paper/convert_figures.py` used for paper 1.
- Double-check text is still selectable/editable in the SVG (not converted to paths) unless the submission portal requires outlined text.

## 5. Attribution

Add a one-line credit either in the figure caption or in `ACKNOWLEDGEMENTS.md`, e.g.:
> "Upper-limb schematic adapted from [OpenStax Anatomy & Physiology / Wikimedia Commons file], [license], redrawn in Inkscape."
