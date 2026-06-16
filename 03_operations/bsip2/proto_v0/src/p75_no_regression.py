
"""P75 / EV-058 cross-corpus no-regression gate."""
import json, os, pathlib, sys
ROOT = pathlib.Path(r"C:/Bari")
SRC = pathlib.Path(__file__).parent
sys.path.insert(0, str(SRC))
_DEFAULT_FLAGS = {
    "BARI_TASK144_FIXES": "off", "BARI_DAIRY_SAT_FAT_INFER": "off", "BARI_RECAL_P0": "off",
    "BARI_RECAL_P0_YOGURT_TRIM": "off", "BARI_GLASSBOX_D5D6": "off", "BARI_GLASSBOX_W15": "off",
    "BARI_GLASSBOX_W2": "off", "BARI_GLASSBOX_W4": "on", "BARI_SODIUM_CEREAL": "off",
    "BARI_REDLABEL_V1": "off", "BARI_TASK250_CONF": "off", "BARI_GRAD_SODIUM_V1": "off",
    "BARI_SODIUM_SHELF_RELATIVE_V1": "off", "BARI_DAIRY_PROTEIN_REWEIGHT_V1": "off",
}
