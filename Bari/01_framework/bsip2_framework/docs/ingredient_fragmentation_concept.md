# Ingredient Fragmentation Concept

**Purpose:** Explore "ingredient fragmentation" and "food reconstruction" as a future Bari analytical concept — a more precise alternative to relying solely on NOVA classification as a processing quality proxy. No formulas are defined here. This document establishes the vocabulary and conceptual structure.

---

## The problem with NOVA as the sole processing signal

NOVA is a population-level classification system that produces four bins. For epidemiological research, this is sufficient. For per-product analytical scoring, it is not. Two products assigned to NOVA 4 can have fundamentally different relationships with industrial processing:

- A bread with calcium propionate and mono- and diglycerides: NOVA 4, but the degree of ingredient transformation is moderate — wheat flour still has its protein and starch largely intact
- A plant-based burger made from soy protein isolate, methylcellulose, rice protein concentrate, beet extract, sunflower oil, and natural flavors: NOVA 4, with every component an industrial extract or fraction of a source food

Both are "ultra-processed." The second represents a qualitatively different relationship with its source ingredients — one where the original food structure has been almost entirely destroyed and reconstructed. NOVA does not distinguish these.

**Ingredient fragmentation is an attempt to make this distinction explicit.**

---

## The fragmentation spectrum

Ingredient fragmentation describes the degree to which a food's components have been separated from their original matrix and recombined. It exists on a spectrum:

```
Whole food → Mechanical transformation → Fractional extraction → Molecular reconstruction
```

**Whole food:** The ingredient is used with its full matrix intact.
- Example: rolled oats in muesli, whole almonds, whole egg

**Mechanical transformation:** The ingredient is physically restructured but its matrix components remain present.
- Example: oat flour (ground oats — fiber, protein, and starch still co-present), almond butter (ground almonds — fat and protein still in physical relationship), cold-pressed oil (fat physically extracted, but from an intact source)

**Fractional extraction:** A specific component of the food is extracted, purifying one fraction and discarding others.
- Example: oat protein isolate (protein extracted; fiber and most starch discarded), whey protein isolate (protein extracted from whey; most fat and lactose removed), maltodextrin (starch fraction extracted from corn or wheat; all protein and fat removed), inulin added from chicory root (fiber fraction extracted; rest of chicory discarded)

**Molecular reconstruction:** The original food structure is irreversibly destroyed and the desired macronutrient or textural profile is rebuilt from extracted components.
- Example: restructured plant-based meat (soy protein isolate + methylcellulose + beet extract + sunflower oil + flavorings — no original food matrix is present; the product is constructed from components); extruded breakfast cereal (refined grain starch processed under heat and pressure into a texture that has no relationship to the source grain's structure)

---

## The engineering intensity axis

Ingredient fragmentation describes what happened to the source ingredients. Engineering intensity describes how much industrial design was required to produce the final product.

A product can have high fragmentation with low engineering intent (whey protein isolate in a simple shake — one extracted ingredient, minimal construction). A product can have lower fragmentation with higher engineering intent (a bread formulated with dough conditioners, emulsifiers, and enzymes to produce specific textural properties from relatively intact flour — some whole grain, heavily engineered process).

These are two dimensions, not one:

| | Low engineering intensity | High engineering intensity |
|-|--------------------------|--------------------------|
| **Low fragmentation** | Plain rolled oats | Fermented grain bread with enzymes, dough conditioners |
| **High fragmentation** | Plain whey isolate shake | Plant-based burger from 12 extracted components |

The NOVA system collapses these into one axis (NOVA 1–4). The distinction between fragmentation and engineering intensity may be more analytically useful.

---

## The oats case study

Oats illustrate fragmentation across the full spectrum:

**Stage 1: Whole oat groat**
The oat grain is intact. All structural components — beta-glucan fiber in the outer layers, protein (~17%) distributed through the grain, fat (~7%), starch in the endosperm — are physically co-located. This is the highest-integrity form.

**Stage 2: Rolled oats**
The oat groat is steamed and rolled flat. The cell structure is disrupted but all nutritional components remain present. Beta-glucan is still intact. Protein, fat, and starch are still in their original physical relationship. Fragmentation is minimal; this is mechanical transformation only.

**Stage 3: Oat flour**
Ground oats. Surface area dramatically increased — starch is far more exposed. Glycemic behaviour changes significantly. All components still present, but their structural relationship is altered. Beta-glucan is present but its viscosity-forming properties in digestion are reduced compared to intact rolled oats.

**Stage 4: Oat bran**
The outer layer of the oat is separated from the inner endosperm. The fiber-rich fraction is retained; the starch-rich fraction is largely discarded (or used elsewhere). High fiber concentration, but this is already a fractional extraction.

**Stage 5: Oat protein concentrate (20–30% protein)**
Partial extraction — protein enriched by removing some starch. Still contains some fiber. Partway along the fragmentation spectrum.

**Stage 6: Oat protein isolate (>85% protein)**
Industrial fractional extraction — protein purified from oat flour through wet milling, pH adjustment, precipitation, and centrifugation. Essentially all fiber and fat have been removed. The resulting product is oat in name but has no structural relationship to the oat grain.

**Stage 7: Extruded puffed oat cereal**
The oat grain (usually in flour form) is mixed with other ingredients and forced through an extruder under heat and pressure. The starch is gelatinised and the protein network is destroyed. The product expands into a puffed form. The original oat cell structure is gone. Even if rolled oats or oat flour were used as input, the output has undergone molecular reconstruction.

**The scoring implication:**
BSIP2 currently treats "oats" in an ingredient list as a marker of whole-grain presence. But oats in an extruded puffed cereal are not structurally equivalent to oats in rolled oat muesli. The ingredient word "oats" appears in both; the food structure is entirely different. Ingredient fragmentation would distinguish these; ingredient list parsing alone cannot.

---

## The protein fragmentation case

Protein is the most commercially fragmented macronutrient:

| Source form | Fragmentation level | What's retained | What's discarded |
|-------------|-------------------|-----------------|-----------------|
| Whole legume | None | Complete matrix | Nothing |
| Legume flour | Minimal | Protein, fiber, starch | Cell structure partially |
| Legume protein concentrate (60–70%) | Moderate | Most protein, some fiber | Most starch, some fat |
| Legume protein isolate (>90%) | High | Protein | Almost all fiber, fat, starch |
| Hydrolysed protein (pre-digested) | Very high | Specific amino acid fractions | All matrix structure |

The nutritional delivery of protein is related to, but not equivalent to, the quantity of protein. Protein in a whole legume matrix is digested differently, arrives in the bloodstream differently, and is accompanied by different co-factors than the same gram quantity of isolate protein. BSIP2 currently captures this only through the binary `protein_isolate` marker.

A fragmentation-aware model would treat protein quality as a function of fragmentation level, not a binary isolate/not-isolate flag.

---

## Reconstruction intensity

Reconstruction intensity measures the complexity of the industrial process required to build the product from its component parts. It is distinct from fragmentation — it describes the assembly step, not the extraction step.

**Low reconstruction intensity:** Mix whole or minimally processed ingredients together. A trail mix (nuts + seeds + dried fruit) has zero reconstruction intensity even if the individual ingredients are commercial products.

**Moderate reconstruction intensity:** Combine extracted components through standard food processing (baking, cooking, fermentation). A bread made from flour, water, salt, and yeast has moderate reconstruction intensity — the ingredients are transformed in combination through a reversible-ish process (you could approximate it at home).

**High reconstruction intensity:** Use industrial processes to construct a food matrix that could not be produced without specialist equipment or conditions. Extrusion, high-pressure homogenisation, transglutaminase cross-linking, controlled crystallisation, emulsion engineering. The "home kitchen test" — could a competent home cook produce this? — is NOVA's own formulation. High reconstruction intensity = fails the home kitchen test definitively.

---

## Why this concept may be more useful than NOVA alone

1. **Continuous, not categorical.** Fragmentation is a spectrum; NOVA is a bin. Continuous assessment is more discriminating.

2. **Product-specific, not category-general.** Two NOVA 4 products can have vastly different fragmentation levels. Two NOVA 2 products can have surprisingly different reconstruction intensities.

3. **Traceable to ingredients, not to category perception.** Fragmentation can be assessed from the ingredient list itself — which ingredients are whole foods, which are concentrates, which are isolates, which are molecular fractions. This makes it explainable: "this product contains protein isolate, maltodextrin, and extracted fiber — all three are processed fractions of their source foods."

4. **Separates the processing criticism from the additive criticism.** Current BSIP2 conflates two different concerns within NOVA and the additive marker system: (a) the food matrix has been destroyed and reconstructed, and (b) additives have been added to control texture, shelf life, or palatability. These are related but distinct. Fragmentation addresses (a); additive burden addresses (b).

---

## What this concept does NOT propose

- No new scoring dimension yet — this is conceptual exploration
- No formula for measuring fragmentation — that requires ingredient taxonomy work that is not yet done
- No modification to the existing NOVA proxy or additive marker system — those remain in place while this concept is developed
- No claim that fragmentation is always bad — high-fragmentation products (whey protein isolate) can serve legitimate nutritional purposes; the question is whether the score correctly represents the tradeoff
