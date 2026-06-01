# Source-Aware Satiety Framework

**Status:** Design document — conceptual phase. No formulas or scoring thresholds are defined here.  
**Purpose:** Replace the simplistic `satiety_support` dimension logic with a framework that distinguishes structurally-driven satiety from engineered macronutrient density.  
**Context:** Current formula: `(protein_g × 3 + fiber_g × 5) / max(50, kcal) × 400`. This rewards protein and fiber quantity regardless of source, allowing engineered protein bars to score satiety=100 while structurally coherent whole-food products with moderate protein may score 40–60.

---

## The problem stated precisely

Satiety is a biological experience. It is produced by a cascade of physiological signals: mechanical distension of the stomach, hormonal responses (GLP-1, PYY, CCK, ghrelin suppression), substrate signals (amino acid sensing in the portal vein and hypothalamus), and neural signals from the gut-brain axis. These signals are produced at different intensities by different food structures — not just by different macronutrient quantities.

The current BSIP2 formula measures macronutrient quantity as a proxy for satiety. This is approximately right for the average food. It fails systematically for:

1. **Engineered protein foods** — protein isolates in high concentration trigger protein sensing signals without the structural satiety mechanisms that accompany whole-food protein
2. **Added fiber foods** — extracted soluble fiber (inulin) contributes gram counts without the mechanical and viscosity mechanisms of intact dietary fiber
3. **Liquid products** — the same macros in liquid form produce significantly weaker satiety signals than in solid form
4. **Air-incorporated products** — volume-inflated products (aerated desserts, puffed snacks) trigger stomach distension without caloric substance

The formula's simplicity is a feature when data is limited. Its failure mode is that it enables systematic gaming: a manufacturer who knows that (protein×3 + fiber×5)/kcal is the satiety signal can optimize that ratio using the cheapest isolated sources of protein and fiber, producing a perfect satiety score in a product with no structural satiety properties.

---

## The physiology of satiety: what actually drives it

Understanding why source matters requires brief engagement with the mechanism.

**Cephalic phase (before eating):**  
The sight, smell, and anticipation of food trigger preparatory signals — salivation, gastric acid secretion, early insulin response. Processed foods that are palatable but structurally simple may trigger strong cephalic responses (high palatability) without the structural complexity that sustains those responses through and after eating.

**Mechanical distension:**  
Stomach stretch receptors signal satiety. Volume matters — but volume is determined by the product's structural form, not its macronutrient content. Whole food with intact cell walls that resist compression produces more distension per calorie than food dissolved or liquefied. A solid whole-food meal distends the stomach more than the same calories in liquid form.

**Chewing effort and oral processing time:**  
Harder, more fibrous foods require more chewing. Chewing time itself is a satiety signal — it provides time for early hormonal satiety signals to develop. Soft, highly processed foods with minimal chewing requirement may be eaten faster than satiety signals can develop, leading to overconsumption before satiety is registered.

**Small intestinal signals (the most important hormonal layer):**  
As nutrients enter the small intestine, L-cells and I-cells produce GLP-1, PYY, and CCK in response to fat, protein, and fiber. The rate at which nutrients enter the intestine is a key variable. Nutrients from an intact food matrix — released gradually as digestion works through cell walls, fiber networks, and structural complexity — produce a different hormonal response profile than nutrients from an isolate, which are absorbed almost immediately upon gastric emptying. The isolate produces a sharp hormone spike; the intact food produces a sustained response.

**Protein sensing:**  
Amino acids from dietary protein are sensed in the portal vein and by the hypothalamus, contributing to satiety and (over time) to lean mass preservation. But the amino acid response profile depends on protein source. Whey protein isolate produces a rapid, high amino acid spike that triggers strong short-term satiety signals but may be followed by faster return to hunger. Whole food protein — arriving with co-factors, releasing amino acids gradually through structural digestion — produces a more sustained but less acute signal.

**Fiber fermentation in the large intestine:**  
Insoluble and some soluble fibers resist digestion in the small intestine and enter the large intestine, where gut bacteria ferment them to short-chain fatty acids (SCFAs). SCFAs, particularly propionate and butyrate, are hormonal signals in their own right — they stimulate GLP-1 secretion and suppress appetite through multiple mechanisms. This is a delayed satiety mechanism that operates hours after eating. **Viscous soluble fibers (beta-glucan from oats, pectin from fruit) produce stronger SCFA-mediated satiety than non-viscous fibers and isolated inulin at the same gram quantity.** The fiber gram count on a label does not capture this distinction.

---

## Why "protein grams + fiber grams" is wrong as a satiety measure

The current formula weights protein at 3 and fiber at 5, normalized by calories. This is calibrated to the macronutrient-level correlation between these nutrients and satiety ratings across populations. It is directionally correct as a statistical proxy.

It fails for the following specific structural reasons:

**1. Protein absorption rate is source-dependent**  
Whey protein isolate is rapidly absorbed — nearly fully absorbed within 2 hours. Casein forms a gel in the stomach and is slowly released over 5–7 hours. Whole food protein embedded in a fibrous matrix may be partially malabsorbed (10–25% for very intact structures like whole nuts) or slowly released. The same grams of protein from these three sources produce different satiety durations. The formula treats them identically.

**2. Isolate protein lacks satiety co-factors**  
Whole food protein arrives with fat (in dairy, nuts, meat), with fiber (in legumes, grains), with water (in most animal proteins). These co-factors extend satiety beyond the protein signal itself. An almond provides protein + fat + fiber in an intact matrix that slows digestion and produces satiety through multiple channels. Whey isolate provides protein without any of these co-factors — it must be eaten in a matrix manufactured for it.

**3. Fiber source affects fermentation yield**  
At identical gram quantities, oat beta-glucan, wheat bran (insoluble), and chicory root inulin produce different SCFA profiles, different fermentation rates, and different hormonal satiety outputs. The formula cannot distinguish these; it treats all fiber as equivalent satiety substrate. In reality: viscous soluble fiber > non-viscous soluble fiber ≈ mixed insoluble fiber > isolated inulin (which, while fermented, is fermented differently and may cause digestive discomfort at high doses that would reduce real-world satiety).

**4. The liquid penalty is absent**  
A protein shake at 20g protein and 5g fiber (achievable) would score identically to an equivalent solid food. But the solid food produces greater satiety per calorie in controlled trials — consistently and substantially. This is one of the most robust findings in satiety research. The formula ignores it entirely.

**5. The mechanical load is not captured**  
Chewing harder, more fibrous foods produces earlier satiety onset. Soft, aerated, or liquid products with identical macros produce later satiety onset because the mechanical signal arrives later relative to consumption speed. This is especially important for snack foods — the category that constitutes the bulk of the BSIP2 dataset.

---

## Framework for source-aware satiety

A source-aware satiety assessment should be built from four components that capture the mechanisms above:

---

### Component 1: Protein quality factor

Protein contributes to satiety proportionally to its macronutrient quantity, but the source modulates this contribution through absorption rate and co-factor context.

**Proposed factor levels (draft for design discussion, not calibration):**

| Protein source type | Satiety quality factor | Rationale |
|---|---|---|
| Whole food (legumes, nuts, whole dairy, eggs, fish) | 1.0 | Full absorption in structural context; co-factors present |
| Mechanically transformed (natural nut butter, whole-grain flour, Greek yogurt) | 0.90 | Matrix largely intact; co-factors co-present |
| Concentrate (whey concentrate, pea protein concentrate at 60–70%) | 0.70 | Some co-factors removed; absorption faster than whole food |
| Isolate (whey isolate, pea isolate, oat isolate >85%) | 0.50 | No matrix co-factors; rapid absorption; engineered satiety profile |
| Hydrolysate / pre-digested | 0.30 | Designed for rapid absorption; satiety persistence minimal |

This factor should be applied to the protein gram contribution to the satiety calculation — not as a flat modifier but as a weight that reflects the quality of the protein's satiety delivery.

**Detection requirement:** BSIP2's current `protein_source` classification (L3) distinguishes whole_food / mixed / isolate / unknown. This is the prototype of Component 1. Extension to concentrate vs. isolate distinction would improve precision.

---

### Component 2: Fiber structural context factor

Fiber contributes to satiety through multiple mechanisms — viscosity in the small intestine, fermentation in the large intestine, and mechanical bulk. The structural context determines how effectively fiber exercises each mechanism.

| Fiber form | Structural context factor | Rationale |
|---|---|---|
| Intact grain fiber (rolled oats, whole grain) | 1.0 | Beta-glucan in natural form; maximum viscosity; intact matrix |
| Whole food fiber from legumes/vegetables | 0.95 | Mixed fiber with natural co-factors; fermentation profile good |
| Mechanically transformed (oat flour — fiber intact but starch more exposed) | 0.80 | Fiber present but partially disrupted; viscosity reduced |
| Isolated viscous fiber (oat beta-glucan concentrate, pectin) | 0.65 | Fiber is real and viscous, but removed from food context; single-dimension delivery |
| Isolated non-viscous fiber (inulin, FOS, chicory fiber) | 0.45 | Fermented but not viscous; satiety mechanism is delayed and limited; can cause distress at high doses |
| Added isolated insoluble fiber (cellulose, wheat bran extract as additive) | 0.40 | Bulk effect only; minimal fermentation; satiety mechanism limited |

**Detection requirement:** The current architecture detects fiber gram quantity but not fiber source type. Ingredient-level fiber taxonomy is needed — distinguishing "grain fiber from rolled oats in the ingredient list" from "chicory root fiber as an additive." This requires the ingredient fragmentation taxonomy developed in the companion framework.

---

### Component 3: Physical form factor

The physical state of the food at consumption modulates the mechanical satiety mechanisms independent of macronutrient content.

| Physical form | Satiety form factor | Rationale |
|---|---|---|
| Solid, cohesive (nut, bar, solid food) | 1.0 | Chewing required; gastric distension; slower gastric emptying |
| Solid, crispy/puffed (extruded, aerated) | 0.75 | Rapid collapse in mouth; high volume but low structural resistance; rapid gastric emptying |
| Semi-solid, dense (Greek yogurt, hummus, nut butter) | 0.85 | Slow gastric emptying; volume satiety present |
| Semi-solid, aerated (mousse, whipped product, foam) | 0.55 | Air content reduces real density; fast gastric emptying |
| Liquid, fiber-containing (smoothie, thick shake) | 0.65 | No chewing; faster gastric emptying than solid; fiber still present |
| Liquid, low-fiber (protein shake, juice) | 0.45 | No mechanical satiety mechanism; fast gastric emptying |

**Detection approach:** Physical form can be partially inferred from product category (snack_bar_granola → solid, beverage → liquid) and from additive markers (aerated products often contain whipping agents, carrageenan for thickening, gas-forming agents). This is an L3 inference that requires development.

---

### Component 4: Matrix coherence bonus

Where protein and fiber arrive together from the same source food's intact matrix — rather than from separate isolated additions — there is a co-factor synergy that enhances satiety persistence. This bonus reflects the difference between "whole almonds" (protein + fat + fiber from the same food) and "almond butter + added chicory fiber" (protein-fat from processed almonds, fiber from a different plant entirely).

**Proposed binary or graduated detection:**
- **Coherence present:** Primary protein and primary fiber sources are the same food or the same plant matrix (oats providing both protein and beta-glucan; chickpeas providing both protein and fiber; dairy providing protein in a fat-fiber context)
- **Coherence absent:** Primary protein source and primary fiber source are different extracted fractions from different source foods (whey isolate for protein; chicory inulin for fiber)

This is the signal that specifically identifies reconstructed satiety profiles — protein from one source, fiber from another, the combination designed to score well on a satiety formula but lacking the co-factor coherence that makes whole-food satiety robust.

---

## The resulting satiety structure

Rather than:
```
satiety_score = (protein_g × 3 + fiber_g × 5) / max(50, kcal) × 400
```

A source-aware satiety model would compute:
```
effective_protein = protein_g × protein_quality_factor
effective_fiber   = fiber_g × fiber_context_factor
structural_satiety = (effective_protein × 3 + effective_fiber × 5) / max(50, kcal) × 400
final_satiety = structural_satiety × physical_form_factor × (1 + matrix_coherence_bonus)
```

This is a design sketch, not a calibrated formula. The multipliers require data analysis to set. The important design properties are:

1. **Source-agnostic quantity is still the foundation** — grams of protein and fiber remain inputs; the framework modulates them by quality, not replaces them
2. **Isolate protein cannot reach satiety=100** — the quality factor of 0.5 for isolates means maximum isolate-protein contribution is halved; a product would need very high quantities to compensate, and those high quantities would also trigger other concerns
3. **Added fiber cannot rescue a structurally fiber-poor product** — the context factor of 0.45 for isolated inulin means added fiber is credited at less than half its gram value; this substantially reduces the gaming value of inulin addition
4. **Physical form matters** — an aerated product or liquid product is assessed against its form's satiety profile, not a neutral baseline

---

## Anti-gaming properties

**Gaming vector 1: Add more protein isolate**  
Under source-aware satiety, protein isolate is credited at 0.50× its gram contribution. To reach the same satiety score as a moderate-protein whole-food product, a manufacturer would need to add ~2× the protein quantity — which at high concentrations also changes other aspects of the product and increases cost substantially. The gaming remains possible but expensive.

**Gaming vector 2: Add more inulin**  
Inulin is credited at 0.45× its fiber contribution. Additionally, products with high inulin content face real consumer tolerance limits (inulin causes digestive discomfort at doses above ~10–15g in many people). The gaming window is narrower than simple gram addition would suggest.

**Gaming vector 3: Claim whole-food sources for isolated ingredients**  
This is the label-engineering risk. If a manufacturer labels whey isolate as "milk protein" or inulin as "chicory root," the detection system may misclassify them. The solution is two-level detection: (a) explicit terms ("isolate," "concentrate," specific enzyme-treated terms), and (b) nutritional plausibility check — if the declared protein quantity greatly exceeds what the declared whole-food ingredients could plausibly deliver, the excess is likely from undeclared or obfuscated isolates.

**Gaming vector 4: Add moisture to fake physical form**  
Adding water to a semi-solid product to claim "liquid — more filling per calorie" is not a coherent gaming vector because liquid products score lower on the physical form factor, not higher. The form factor penalizes liquidity; it cannot be gamed by adding water.

---

## What this framework changes in practice

**Products that gain from source-aware satiety:**
- Whole-food nut bars (almonds, dates, oats as first ingredients with intact fiber and matrix-coherent protein)
- Greek yogurt and similar strained dairy products
- Products where the declared protein and fiber are both from the same primary ingredient
- Traditional hummus, nut butters, whole-grain-forward products

**Products that lose from source-aware satiety:**
- Protein isolate bars (satiety score reduced by protein quality factor applied to majority protein source)
- Products with high added inulin (fiber contribution reduced by context factor)
- Aerated desserts and puffed snacks (physical form factor applied)
- Protein shakes and liquid formats (physical form factor applied)

**Products unaffected:**
- Products with genuinely moderate protein and fiber from mixed sources where all factors approach neutral

This directional change is precisely the goal: whole-food structural satiety becomes a genuine upward signal; engineered satiety optimization loses its current scoring advantage.
