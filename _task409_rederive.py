# -*- coding: utf-8 -*-
"""TASK-409 re-derive script. Scores clean BSIP1 corpus, updates frontend JSONs to staging dir."""
import sys, json, glob, os, importlib, datetime, hashlib, collections

WT = r"C:\Bari\.claude\worktrees\task409"
SRC = os.path.join(WT, "03_operations", "bsip2", "proto_v0", "src")
ANALYSIS = os.path.join(WT, "03_operations", "bsip2", "proto_v0", "analysis")
sys.path.insert(0, SRC)
sys.path.insert(0, ANALYSIS)

STAGING = os.path.join(WT, "_task409_staging")
os.makedirs(STAGING, exist_ok=True)

NOW = datetime.datetime.now().isoformat(timespec="seconds")
TODAY = datetime.datetime.now().strftime("%Y%m%d")

ALL_FLAGS = [
    "BARI_SHELF_RELATIVE_V1","BARI_SODIUM_SHELF_RELATIVE_V1","BARI_FAT_TECH_V1","BARI_RECAL_P0",
    "BARI_RECAL_P0_YOGURT_TRIM","BARI_GRAD_SODIUM_V1","BARI_DAIRY_PROTEIN_REWEIGHT_V1","BARI_REDLABEL_V1",
    "BARI_SODIUM_CEREAL","BARI_D4_SCORE_V1","BARI_HC002_NOVA1","BARI_GLASSBOX_W2","BARI_GLASSBOX_D5D6",
    "BARI_GLASSBOX_W15","BARI_TASK144_FIXES","BARI_TASK250_CONF","BARI_DAIRY_SAT_FAT_INFER","BARI_W4_WFI_V1",
    "BARI_DECHAIN_V1","BARI_INGCONF_V1","BARI_HC_DAIRY_SATFAT_V1","BARI_GRAN_SUGAR_25G_V1","BARI_FAT_SENTINEL_V1",
    "BARI_ADDITIVE_PARSE_FIX_V1","BARI_PALM_HYDRO_V1","BARI_PROTEIN_BAR_V1","BARI_GLASSBOX_W4","BARI_FIBER_FERMENT_V1",
]

def apply_flags(flags):
    for k in ALL_FLAGS:
        os.environ[k] = "off"
    os.environ["BARI_GLASSBOX_W4"] = "on"
    for k, v in flags.items():
        os.environ[k] = str(v)

def reload_engine():
    import score_engine, nova_proxy, signal_extractor
    importlib.reload(nova_proxy)
    importlib.reload(signal_extractor)
    importlib.reload(score_engine)
    return score_engine

def apply_shelf_rel(sr, eng):
    if not sr:
        return
    if sr.get("api") == "sodium_ev056":
        eng.set_shelf_sodium_stats(sr["median"], sr["scale"])
    elif sr.get("nutrient"):
        eng.set_shelf_stats(sr["nutrient"], sr["median"], sr["scale"], sr.get("scale_type", "iqr"))

def score_one_product(eng, rec):
    from signal_extractor import extract_signals
    from router_v2 import classify_category
    from nova_proxy import infer_nova
    from evaluation_scope import assign_evaluation_scope
    try:
        sig = extract_signals(rec)
        cat = classify_category(rec)
        nov = infer_nova(rec, sig["L3_inferred_classifications"])
        ev = assign_evaluation_scope(rec, cat["category"])
        sr = eng.score_product(rec, sig, cat, nov, ev)
        return sr if isinstance(sr, dict) else None
    except Exception as e:
        return None

def update_product(live_prod, engine_result, render_fields):
    updated = dict(live_prod)
    new_score = engine_result.get("final_score_estimate")
    new_grade = engine_result.get("grade_estimate")
    if new_score is not None:
        updated["score"] = round(new_score, 1)
    if new_grade is not None:
        updated["grade"] = new_grade
    rf = render_fields or []
    if "novaGroup" in rf:
        nova = engine_result.get("nova_proxy") or engine_result.get("nova_group")
        if nova is not None:
            updated["novaGroup"] = nova
    if "d4_additives" in rf:
        d4 = engine_result.get("d4_additives") or engine_result.get("detect_additives_d4")
        if d4 is not None:
            updated["d4_additives"] = d4
    if "confidence_level" in rf:
        conf = engine_result.get("data_sufficiency") or engine_result.get("confidence_level")
        if conf is not None:
            updated["confidence_level"] = conf
    return updated

def load_bsip1_dir(corpus_dirs, bsip1_glob="bsip1_*.json", barcode_set=None):
    """Load bsip1 records from list of corpus dirs. Dedup by barcode (last wins if dupes)."""
    records = {}
    for d in corpus_dirs:
        # Remap only the bare C:\Bari prefix (not already worktree paths)
        if d.startswith(r"C:\Bari\.claude") or d.startswith(r"C:/Bari/.claude"):
            pass  # already a worktree path, use as-is
        else:
            d = d.replace("C:\\Bari", WT).replace("C:/Bari", WT)
        files = glob.glob(os.path.join(d, bsip1_glob))
        for f in files:
            try:
                j = json.load(open(f, encoding="utf-8"))
            except Exception:
                continue
            bc = str(j.get("barcode", os.path.basename(f).replace("bsip1_","").replace(".json","")))
            if barcode_set is not None and bc not in barcode_set:
                continue
            records[bc] = j
    return records

def get_engine_sha():
    try:
        import subprocess
        r = subprocess.run(["git", "-C", WT, "rev-parse", "HEAD"], capture_output=True, text=True)
        return r.stdout.strip()
    except Exception:
        return "unknown"

def load_frontend(path):
    # Only remap plain C:\Bari (not worktree paths which already start with C:\Bari\.claude)
    if "worktrees" not in path:
        path = path.replace("C:\\Bari", WT).replace("C:/Bari", WT)
    j = json.load(open(path, encoding="utf-8"))
    if isinstance(j, dict) and "products" in j:
        return j, j["products"]
    elif isinstance(j, list):
        return {"products": j}, j
    return j, []

def save_staged(cat_key, frontend_data, products_list):
    out_path = os.path.join(STAGING, f"{cat_key}_frontend_staged.json")
    if isinstance(frontend_data, dict) and "products" in frontend_data:
        frontend_data["products"] = products_list
    else:
        frontend_data = {"products": products_list}
    json.dump(frontend_data, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return out_path

# Load chocolate barcode sets
def load_choc_barcode_sets():
    bars_path = os.path.join(WT, "bari-web", "src", "data", "comparisons", "chocolate_bars_frontend_v1.json")
    tabs_path = os.path.join(WT, "bari-web", "src", "data", "comparisons", "chocolate_tablets_frontend_v1.json")
    bars_j = json.load(open(bars_path, encoding="utf-8"))
    tabs_j = json.load(open(tabs_path, encoding="utf-8"))
    bars_barcodes = {str(p["barcode"]) for p in bars_j.get("products", [])}
    tabs_barcodes = {str(p["barcode"]) for p in tabs_j.get("products", [])}
    return bars_barcodes, tabs_barcodes

BARS_BC, TABS_BC = load_choc_barcode_sets()
CHOC_CORPUS_DIR = os.path.join(WT, "03_operations", "bsip1", "fresh_rescore_task391_20260624_113405", "output")

CATEGORIES = {
    "cheese": {
        "rederive": True,
        "corpus_dirs": [os.path.join(WT, "03_operations", "bsip1", "run_cheese_003", "output")],
        "flags": {"BARI_SHELF_RELATIVE_V1":"on","BARI_FAT_TECH_V1":"on","BARI_RECAL_P0":"on",
                  "BARI_SODIUM_SHELF_RELATIVE_V1":"off","BARI_DAIRY_PROTEIN_REWEIGHT_V1":"off",
                  "BARI_REDLABEL_V1":"off","BARI_SODIUM_CEREAL":"off","BARI_GRAD_SODIUM_V1":"off"},
        "shelf_rel": {"nutrient":"fat_saturated_g","median":16.05,"scale":2.0756,"scale_type":"iqr"},
        "bsip1_glob": "bsip1_*.json",
        "barcode_set": None,
        "frontend_file": os.path.join(WT, "bari-web","src","data","comparisons","cheese_frontend_v4.json"),
        "render_fields": ["novaGroup","confidence_level","d4_additives"],
        "exclusions": {"7290014217492","4127800","4127862","48185","4127817","47942"},
    },
    "milk": {
        "rederive": True,
        "corpus_dirs": [os.path.join(WT, "03_operations", "bsip1", "run_milk_002", "output")],
        "flags": {"BARI_RECAL_P0":"off","BARI_FAT_TECH_V1":"on","BARI_SHELF_RELATIVE_V1":"on",
                  "BARI_REDLABEL_V1":"off","BARI_DAIRY_SAT_FAT_INFER":"off",
                  "BARI_SODIUM_SHELF_RELATIVE_V1":"off","BARI_DAIRY_PROTEIN_REWEIGHT_V1":"off",
                  "BARI_GRAD_SODIUM_V1":"off","BARI_SODIUM_CEREAL":"off"},
        "shelf_rel": None,
        "bsip1_glob": "bsip1_*.json",
        "barcode_set": None,
        "frontend_file": os.path.join(WT, "bari-web","src","data","comparisons","milk_frontend_v1.json"),
        "render_fields": ["novaGroup","confidence_level","d4_additives"],
        "exclusions": {"7290110324773","7290114313285"},
    },
    "cereals": {
        "rederive": True,
        "corpus_dirs": [os.path.join(WT, "03_operations", "bsip1", "run_cereals_008", "output")],
        "flags": {"BARI_RECAL_P0":"on","BARI_SHELF_RELATIVE_V1":"off","BARI_SODIUM_SHELF_RELATIVE_V1":"off",
                  "BARI_FAT_TECH_V1":"on","BARI_GRAD_SODIUM_V1":"off","BARI_DAIRY_PROTEIN_REWEIGHT_V1":"off",
                  "BARI_REDLABEL_V1":"off","BARI_SODIUM_CEREAL":"off"},
        "shelf_rel": None,
        "bsip1_glob": "bsip1_*.json",
        "barcode_set": None,
        "frontend_file": os.path.join(WT, "bari-web","src","data","comparisons","cereals_frontend_v2.json"),
        "render_fields": ["confidence_level","d4_additives"],
        "exclusions": {"1164266","1164273","1343845","5018357006731","5018357006755","6582751",
                       "7290011131050","7290011131371","7290011131388","7290011131395","7290011131968",
                       "7290011131975","7290011668587","7290013433091","7290013433107","7290013433244",
                       "7290013433336","7290014471412","7290014471429","7290014471436","7290014471443",
                       "7290016883176","7290016883183","7290017325910","7290017962023","7290017962047",
                       "7290106771161","7290106771314","7290106771369","7290106773714","7290112494351",
                       "7290112495228","7290112497994","7290112498007","7290116530482","7290116534619",
                       "7290116535371","7290118420811","7613035622623","7613035635845","7613037012095",
                       "8445290964595","884912126115"},
    },
    "bread": {
        "rederive": True,
        "corpus_dirs": [os.path.join(WT, "03_operations", "bsip1", "run_bread_conform_001", "output")],
        "flags": {"BARI_RECAL_P0":"on","BARI_SHELF_RELATIVE_V1":"off","BARI_SODIUM_SHELF_RELATIVE_V1":"off",
                  "BARI_FAT_TECH_V1":"on","BARI_GRAD_SODIUM_V1":"off","BARI_DAIRY_PROTEIN_REWEIGHT_V1":"off",
                  "BARI_REDLABEL_V1":"off","BARI_SODIUM_CEREAL":"off"},
        "shelf_rel": None,
        "bsip1_glob": "bsip1_*.json",
        "barcode_set": None,
        "frontend_file": os.path.join(WT, "bari-web","src","data","comparisons","bread_frontend_v3.json"),
        "render_fields": ["confidence_level","d4_additives"],
        "exclusions": {"2026","7296073641568"},
    },
    "cakes": {
        "rederive": True,
        "corpus_dirs": [os.path.join(WT, "03_operations", "bsip1", "run_cakes_001", "output")],
        "flags": {"BARI_SHELF_RELATIVE_V1":"on","BARI_FAT_TECH_V1":"on","BARI_RECAL_P0":"off",
                  "BARI_SODIUM_SHELF_RELATIVE_V1":"off","BARI_DAIRY_PROTEIN_REWEIGHT_V1":"off",
                  "BARI_REDLABEL_V1":"off","BARI_SODIUM_CEREAL":"off","BARI_GRAD_SODIUM_V1":"off"},
        "shelf_rel": {"nutrient":"sugars_g","median":29.0,"scale":9.044,"scale_type":"iqr"},
        "bsip1_glob": "bsip1_cakes_*.json",
        "barcode_set": None,
        "frontend_file": os.path.join(WT, "bari-web","src","data","comparisons","cakes_hard_cookies_frontend_v1.json"),
        "render_fields": ["novaGroup","_has_phvo","_category_routed","_source_retailers","d4_additives"],
        "exclusions": {
            "313184","4006529002170","4017100198151","4017100364112","46214731552","46214930207",
            "4820180816552","4820180816576","4820180816590","4823077633317","5317194","5410126006049",
            "5410126116168","5410126726244","5410126806250","5901414200411","7290000061245","7290000075143",
            "7290011489625","7290013145406","7290013156006","7290013156921","7290013453068","7290013740014",
            "7290017724171","7290017962139","7290018893036","7290019293804","7290019816034","7290019816058",
            "7290019816232","7290019870463","7290019870470","7290020030184","7290101111986","7290105364784",
            "7290106571921","7290106571945","7290106656727","7290112340276","7290112961754","7290115206333",
            "7290118422617","7290118423904","7290118426615","7290119040513","7290119040568","7290119040605",
            "7290119040612","7290119040650","7290119040667","7290119040803","7290119040858","7290119041053",
            "7290119041107","7290119041152","7290119043095","7290119043149","7290119043743","7290119043897",
            "7290122781359","7290123330488","7296073161981","7296073162001","7296073453840","7296073453857",
            "7296073529019","7296073529026","7296073659969","7622201401900","7622201809188","7622210137234",
            "7622210453327","7622300356767","7622300489427","7622300489434","8000500366073","8410376037784",
            "8410376075915","8710502064814","8710502139017","8710502279010","8710502405204","8710502470028",
        },
    },
    "chocolate_bars": {
        "rederive": True,
        "corpus_dirs": [CHOC_CORPUS_DIR],
        "flags": {"BARI_SHELF_RELATIVE_V1":"off","BARI_FAT_TECH_V1":"on","BARI_RECAL_P0":"off",
                  "BARI_SODIUM_SHELF_RELATIVE_V1":"off","BARI_GRAD_SODIUM_V1":"off",
                  "BARI_DAIRY_PROTEIN_REWEIGHT_V1":"off","BARI_REDLABEL_V1":"off"},
        "shelf_rel": None,
        "bsip1_glob": "bsip1_*.json",
        "barcode_set": BARS_BC,
        "frontend_file": os.path.join(WT, "bari-web","src","data","comparisons","chocolate_bars_frontend_v1.json"),
        "render_fields": ["novaGroup","confidence_level","d4_additives"],
        "exclusions": set(),
    },
    "chocolate_tablets": {
        "rederive": True,
        "corpus_dirs": [CHOC_CORPUS_DIR],
        "flags": {"BARI_SHELF_RELATIVE_V1":"off","BARI_FAT_TECH_V1":"on","BARI_RECAL_P0":"off",
                  "BARI_SODIUM_SHELF_RELATIVE_V1":"off","BARI_GRAD_SODIUM_V1":"off",
                  "BARI_DAIRY_PROTEIN_REWEIGHT_V1":"off","BARI_REDLABEL_V1":"off"},
        "shelf_rel": None,
        "bsip1_glob": "bsip1_*.json",
        "barcode_set": TABS_BC,
        "frontend_file": os.path.join(WT, "bari-web","src","data","comparisons","chocolate_tablets_frontend_v1.json"),
        "render_fields": ["novaGroup","confidence_level","d4_additives"],
        "exclusions": set(),
    },
    # CONFIRM-NO-MOVE categories - from configs
    "brined_cheeses": {
        "rederive": False,
        "corpus_dirs": [os.path.join(WT, "03_operations", "bsip1", "run_brined_cheeses_002", "output")],
        "flags": {
            "BARI_RECAL_P0": "on",
            "BARI_RECAL_P0_YOGURT_TRIM": "off",
            "BARI_GRAD_SODIUM_V1": "on",
            "BARI_REDLABEL_V1": "off",
            "BARI_SODIUM_CEREAL": "off",
            "BARI_TASK144_FIXES": "off",
            "BARI_TASK250_CONF": "off",
            "BARI_GLASSBOX_D5D6": "off",
            "BARI_GLASSBOX_W15": "off",
            "BARI_GLASSBOX_W2": "off",
            "BARI_SODIUM_SHELF_RELATIVE_V1": "on",
            "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "on",
            "BARI_SHELF_RELATIVE_V1": "on",
            "BARI_FAT_TECH_V1": "on",
        },
        "shelf_rel": {"api":"sodium_ev056","median":1000.0,"scale":266.25,"scale_type":"stdev","nutrient":"sodium_mg"},
        "bsip1_glob": "bsip1_brinedcheese_*.json",
        "barcode_set": None,
        "frontend_file": os.path.join(WT, "bari-web","src","data","comparisons","brined_cheeses_frontend_v2.json"),
        "render_fields": ["novaGroup","d4_additives"],
        "exclusions": {"2107071","2385455","2511229","2511236","2511243","4861056","4861070",
                       "5992872","7290114310550","7296073644996","7296073730330","8606370"},
    },
    "granola": {
        "rederive": False,
        "corpus_dirs": [os.path.join(WT, "03_operations", "bsip1", "run_cereals_005", "output")],
        "flags": {
            "BARI_RECAL_P0": "on",
            "BARI_SHELF_RELATIVE_V1": "off",
            "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
            "BARI_FAT_TECH_V1": "on",
            "BARI_GRAD_SODIUM_V1": "off",
            "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
            "BARI_REDLABEL_V1": "off",
            "BARI_SODIUM_CEREAL": "off",
        },
        "shelf_rel": None,
        "bsip1_glob": "bsip1_*.json",
        "barcode_set": None,
        "frontend_file": os.path.join(WT, "bari-web","src","data","comparisons","granola_frontend_v1.json"),
        "render_fields": ["confidence_level","d4_additives"],
        "exclusions": set(),
    },
    "cookies_coffee": {
        "rederive": False,
        "corpus_dirs": [
            os.path.join(WT, "03_operations", "bsip1", "run_cookies_001", "output"),
            os.path.join(WT, "03_operations", "bsip1", "run_cakes_001", "output"),
        ],
        "flags": {
            "BARI_RECAL_P0": "off",
            "BARI_GRAD_SODIUM_V1": "off",
            "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
            "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
            "BARI_REDLABEL_V1": "off",
            "BARI_SODIUM_CEREAL": "off",
            "BARI_SHELF_RELATIVE_V1": "off",
            "BARI_FAT_TECH_V1": "on",
        },
        "shelf_rel": None,
        "bsip1_glob": "bsip1_*.json",
        "barcode_set": None,
        "frontend_file": os.path.join(WT, "bari-web","src","data","comparisons","cookies_coffee_frontend_v2.json"),
        "render_fields": ["novaGroup","d4_additives"],
        "exclusions": {
            "7290013453631","7290017962108","7290119040513","7290119040568","7290119040612","7290119040667",
            "1361177","1361207","2472087","2472117","2472148","2472186","2472193","2472223","2472254","2472261",
            "2472841","4170097","4170103","4504649","4504656","4504670","4504687","5431913","5431920","5718021",
            "5718038","5900020020710","5900020034991","5900020047915","6983770","6983787","6983794",
            "7290002026440","7290006775023","7290006775085","7290006775337","7290006983787","7290011570798",
            "7290012244032","7290012244056","7290013145406","7290013453624","7290013683595","7290013927996",
            "7290015726528","7290015726535","7290015879712","7290016162264","7290016416961","7290018043134",
            "7290018893487","7290018893661","7290019204701","7290019204800","7290019766018","7290105692498",
            "7290106578821","7290109581156","7290111534010","7290112495228","7290117384572","7290118421924",
            "7290119030095","7290119039746","7290119042302","7290119045013","7290123330280","7290123330334",
            "7290123330884","7290123331034","7296073132936","7296073132943","7296073132950","7296073140184",
            "7296073346333","7296073346340","7296073431817","7296073431879","7296073431893","7296073431909",
            "7296073431916","7296073473664","7296073473688","7613035622623","7613038451954","8410376044959",
            "9397642","9397697","9399288",
        },
    },
    "hummus_shelfrel_002": {
        "rederive": False,
        "corpus_dirs": [os.path.join(WT, "02_products", "hummus", "canonical_bsip1")],
        "flags": {
            "BARI_RECAL_P0": "on",
            "BARI_SHELF_RELATIVE_V1": "on",
            "BARI_FAT_TECH_V1": "on",
            "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
            "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
            "BARI_REDLABEL_V1": "off",
            "BARI_SODIUM_CEREAL": "off",
            "BARI_GRAD_SODIUM_V1": "off",
            "BARI_TASK144_FIXES": "off",
        },
        "shelf_rel": {"nutrient":"sodium_mg","median":390.0,"scale":31.88,"scale_type":"iqr"},
        "bsip1_glob": "bsip1_*.json",
        "barcode_set": None,
        "frontend_file": os.path.join(WT, "bari-web","src","data","comparisons","hummus_frontend_v5.json"),
        "render_fields": ["_product_type","glassBox","d3_processing_signal","d4_additives"],
        "exclusions": {
            "3643820","7296073005889","7296073006015","7296073705505","7296073733324","7296073733331",
            "208428","7290018359686","7296073733317","7296073733348","1990261","3643714",
        },
    },
    "juices": {
        "rederive": False,
        "corpus_dirs": [os.path.join(WT, "02_products", "juices", "bsip1_outputs")],
        "flags": {
            "BARI_SHELF_RELATIVE_V1": "on",
            "BARI_FAT_TECH_V1": "on",
            "BARI_RECAL_P0": "on",
            "BARI_SODIUM_SHELF_RELATIVE_V1": "off",
            "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
            "BARI_REDLABEL_V1": "off",
            "BARI_SODIUM_CEREAL": "off",
            "BARI_GRAD_SODIUM_V1": "off",
            "BARI_TASK144_FIXES": "off",
        },
        "shelf_rel": {"nutrient":"sugars_g","median":9.5,"scale":2.82,"scale_type":"iqr"},
        "bsip1_glob": "bsip1_*.json",
        "barcode_set": None,
        "frontend_file": os.path.join(WT, "bari-web","src","data","comparisons","juices_frontend_v3.json"),
        "render_fields": ["novaGroup","sugarPer100ml","kcalPer100ml","retailers","subPool","d4_additives"],
        "exclusions": {
            "7290000272696","7290004030148","7290018940761","7290019398516","7290106668577",
            "7290117034774","7290117765630","7290119385034","5411188115434","7290110325893","7290110558420",
        },
    },
}

engine_sha = get_engine_sha()
results = {}
grade_moves_all = {}

for cat_key, cfg in CATEGORIES.items():
    if cfg.get("skip_reason"):
        results[cat_key] = {"status": "SKIPPED", "reason": cfg["skip_reason"]}
        print(f"\n=== {cat_key}: SKIPPED ({cfg['skip_reason']}) ===")
        continue

    label = "REDERIVE" if cfg["rederive"] else "CONFIRM-NO-MOVE"
    print(f"\n=== {cat_key}: {label} ===")

    # Apply flags and reload engine
    apply_flags(cfg["flags"])
    eng = reload_engine()
    if cfg.get("shelf_rel"):
        apply_shelf_rel(cfg["shelf_rel"], eng)

    # Load bsip1 corpus
    corpus = load_bsip1_dir(cfg["corpus_dirs"], cfg.get("bsip1_glob","bsip1_*.json"), cfg.get("barcode_set"))
    excl = cfg.get("exclusions", set())
    corpus = {bc: rec for bc, rec in corpus.items() if bc not in excl}
    print(f"  corpus: {len(corpus)} records")

    if not corpus:
        results[cat_key] = {"status": "NO_CORPUS", "note": "No bsip1 records found"}
        print(f"  NO CORPUS FOUND")
        continue

    # Score all
    engine_results = {}
    failed = []
    for bc, rec in corpus.items():
        sr = score_one_product(eng, rec)
        if sr:
            engine_results[bc] = sr
        else:
            failed.append(bc)
    print(f"  scored: {len(engine_results)} | failed: {len(failed)}")

    # Load live frontend
    frontend_path = cfg.get("frontend_file")
    if not frontend_path:
        results[cat_key] = {"status": "NO_FRONTEND", "scored": len(engine_results)}
        print(f"  NO FRONTEND FILE configured")
        continue

    # frontend_file paths are already WT-absolute (built with os.path.join(WT,...))
    resolved_path = frontend_path if "worktrees" in frontend_path else frontend_path.replace("C:\\Bari", WT).replace("C:/Bari", WT)
    if not os.path.exists(resolved_path):
        results[cat_key] = {"status": "NO_FRONTEND", "scored": len(engine_results), "path": resolved_path}
        print(f"  NO FRONTEND FILE: {resolved_path}")
        continue

    frontend_data, products = load_frontend(frontend_path)

    # Build bc -> product map from frontend
    live_map = {}
    for p in products:
        bc = str(p.get("barcode", ""))
        if bc:
            live_map[bc] = p

    # Update products
    updated_products = []
    grade_moves = []
    not_in_corpus = []
    scored_count = 0

    for p in products:
        bc = str(p.get("barcode", ""))
        if bc in engine_results:
            er = engine_results[bc]
            old_score = p.get("score")
            old_grade = p.get("grade")
            updated = update_product(p, er, cfg.get("render_fields", []))
            new_score = updated.get("score")
            new_grade = updated.get("grade")
            updated_products.append(updated)
            scored_count += 1
            if old_grade != new_grade:
                grade_moves.append({
                    "bc": bc,
                    "name_he": p.get("name_he") or p.get("nameHe") or "",
                    "old_score": old_score,
                    "new_score": new_score,
                    "old_grade": old_grade,
                    "new_grade": new_grade,
                })
        else:
            updated_products.append(p)
            not_in_corpus.append(bc)

    print(f"  updated: {scored_count} | not_in_corpus: {len(not_in_corpus)} | grade_moves: {len(grade_moves)}")
    for gm in grade_moves:
        print(f"    GRADE MOVE: {gm['bc']} {gm['old_grade']}->{gm['new_grade']} {gm['old_score']}->{gm['new_score']}")

    # Add meta
    if isinstance(frontend_data, dict):
        frontend_data["_meta"] = {
            "run_id": f"task409_rederive_{cat_key}_{TODAY}",
            "corpus_dirs": cfg["corpus_dirs"],
            "flag_vector": cfg["flags"],
            "engine_sha": engine_sha,
            "task": "TASK-409 clean+traceable re-derive",
            "ts": NOW,
            "corpus_records": len(corpus),
            "scored": len(engine_results),
            "failed_barcodes": failed[:20],
        }

    # Save to staging
    staged_path = save_staged(cat_key, frontend_data, updated_products)
    print(f"  staged: {staged_path}")

    grade_moves_all[cat_key] = grade_moves
    results[cat_key] = {
        "status": label,
        "corpus_records": len(corpus),
        "scored": len(engine_results),
        "failed": failed[:20],
        "not_in_corpus": not_in_corpus[:20],
        "grade_moves": grade_moves,
        "grade_moves_count": len(grade_moves),
    }

# Write summary
summary = {
    "run_ts": NOW,
    "engine_sha": engine_sha,
    "results": results,
    "grade_moves_all": grade_moves_all,
}
outf = os.path.join(WT, "_task409_rederive_result.json")
json.dump(summary, open(outf, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"\n=== DONE. Results: {outf} ===")
