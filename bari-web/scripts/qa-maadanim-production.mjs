import { chromium } from "playwright";
import { readFileSync } from "node:fs";

const URL = "http://localhost:3000/hashvaot/maadanim";
const json = JSON.parse(
  readFileSync("src/data/comparisons/maadanim_frontend_v2.json", "utf-8")
);
const expectedTop10 = json.products.slice(0, 10).map((p) => p.name);
const expandTargets = [
  "יופלה GO מועשר בחלבון",
  "יופלה GO דובדבן 0.7%",
  "דנונ.פרו ללא סוכר פיסטוק",
  "מילקי בטעם שוקולד",
];
const sectionLabels = [
  "מה עובד לטובת המוצר?",
  "מה מגביל את הציון?",
  "בשורה התחתונה",
  "הקשר במדף",
];

const defects = [];

function defect(id, detail) {
  defects.push({ id, detail });
}

const browser = await chromium.launch({ headless: true });
const consoleErrors = [];
const page = await browser.newPage();
page.on("console", (msg) => {
  if (msg.type() === "error") consoleErrors.push(msg.text());
});
page.on("pageerror", (err) => consoleErrors.push(String(err)));

async function runViewport(width, height, tag) {
  await page.setViewportSize({ width, height });
  await page.goto(URL, { waitUntil: "networkidle" });
  await page.waitForSelector("text=מה שווה לקחת מהמדף");

  if (!page.url().includes("/hashvaot/maadanim")) {
    defect(`${tag}-route`, `Wrong URL: ${page.url()}`);
  }

  const order = await page.$$eval(
    '[role="button"][aria-label]',
    (nodes) =>
      nodes
        .map((n) => n.getAttribute("aria-label"))
        .filter(
          (n) =>
            n &&
            !["הצג הכל", "סגור"].includes(n) &&
            !n.includes("מתוק") &&
            !n.includes("חלבון גבוה") &&
            !n.includes("רשימת רכיבים")
        )
  );

  const top10 = order.slice(0, 10);
  if (JSON.stringify(top10) !== JSON.stringify(expectedTop10)) {
    defect(
      `${tag}-order`,
      `Top 10 mismatch.\nExpected: ${expectedTop10.join(" | ")}\nActual:   ${top10.join(" | ")}`
    );
  }

  const frame = page.locator(".sm\\:max-w-\\[375px\\]");
  if (tag === "desktop") {
    const box = await frame.boundingBox();
    if (!box || box.width > 400) {
      defect("desktop-frame", `Phone frame width unexpected: ${box?.width}`);
    }
  }

  if (tag === "mobile") {
    const vw = page.viewportSize()?.width;
    if (vw !== 375) defect("mobile-viewport", `Viewport is ${vw}, expected 375`);
  }

  for (const name of expandTargets) {
    const product = json.products.find((p) => p.name === name);
    const row = page.locator(`[aria-label="${name}"]`).first();
    await row.scrollIntoViewIfNeeded();
    const expanded = await row.getAttribute("aria-expanded");
    if (expanded !== "true") await row.click();
    await page.waitForSelector(`[aria-label="${name}"][aria-expanded="true"]`, {
      timeout: 8000,
    });
    const article = page.locator("article").filter({
      has: page.locator(`[aria-label="${name}"]`),
    });
    const text = await article.innerText();
    const exp = product?.expansion ?? {};
    if ((exp.positiveSignals?.length ?? 0) > 0 && !text.includes("מה עובד")) {
      defect(`${tag}-positive-${name}`, "positiveSignals not rendered");
    }
    if ((exp.limitingFactors?.length ?? 0) > 0 && !text.includes("מה מגביל")) {
      defect(`${tag}-limiting-${name}`, "limitingFactors not rendered");
    }
    if (exp.bottomLine?.trim() && !text.includes("בשורה התחתונה")) {
      defect(`${tag}-bottom-${name}`, "bottomLine not rendered");
    }
    if (exp.comparisonContext?.trim() && !text.includes("הקשר במדף")) {
      defect(`${tag}-comparison-${name}`, "comparisonContext not rendered");
    }
  }

  const totalRows = await page.locator("article").count();
  await page.getByRole("button", { name: "פחות מתוק" }).click();
  await page.waitForTimeout(400);
  const filteredRows = await page.locator("article").count();
  if (filteredRows >= totalRows) {
    defect(
      `${tag}-filter`,
      `"פחות מתוק" did not reduce rows (${totalRows} → ${filteredRows})`
    );
  }
  await page.getByRole("button", { name: "פחות מתוק" }).click();

  const brokenImages = await page.$$eval("article img", (imgs) =>
    imgs
      .filter((img) => img.complete && img.naturalWidth === 0)
      .map((img) => img.src)
  );
  if (brokenImages.length) {
    defect(`${tag}-images`, `${brokenImages.length} broken images`);
  }

  await page.screenshot({
    path: `public/qa/maadanim-v2/qa-${tag}.png`,
    fullPage: true,
  });
}

await runViewport(375, 844, "mobile");
await runViewport(1280, 900, "desktop");

if (consoleErrors.length) {
  defect("console", consoleErrors.join("\n"));
}

await browser.close();

if (defects.length === 0) {
  console.log("NO_DEFECTS");
} else {
  console.log(JSON.stringify(defects, null, 2));
}
