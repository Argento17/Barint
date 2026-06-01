from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient

# ---------------------------------------------------
# AZURE CONFIG
# ---------------------------------------------------

ENDPOINT = "https://bsip0ocr.cognitiveservices.azure.com/"

KEY = "AZURE_DI_KEY_REMOVED"

IMAGE_PATH = r"C:\Bari\03_operations\bsip0\pipeline\data\raw\snack_bars\product_001\nutrition1.png"

# ---------------------------------------------------
# CLIENT
# ---------------------------------------------------

client = DocumentIntelligenceClient(
    endpoint=ENDPOINT,
    credential=AzureKeyCredential(KEY)
)

# ---------------------------------------------------
# READ IMAGE
# ---------------------------------------------------

with open(IMAGE_PATH, "rb") as f:
    poller = client.begin_analyze_document(
        "prebuilt-layout",
        body=f
    )

result = poller.result()

# ---------------------------------------------------
# PRINT OCR
# ---------------------------------------------------

print("\n----- OCR RESULT -----\n")

for page in result.pages:

    for line in page.lines:
        print(line.content)