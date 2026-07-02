# -*- coding: utf-8 -*-
from pathlib import Path

html = '''<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Bari Homepage — v5 layout preview</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;600;700;800;900&display=swap" rel="stylesheet" />
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: "Heebo", "Noto Sans Hebrew", Arial, sans-serif;
      background:
        radial-gradient(ellipse 65% 60% at 18% 38%, rgba(47,174,130,0.09) 0%, transparent 65%),
        radial-gradient(ellipse 55% 50% at 88% 78%, rgba(245,243,236,0.95) 0%, transparent 70%),
        #F7F7F2;
      color: #111318;
      -webkit-font-smoothing: antialiased;
    }
    .container { max-width: 1280px; margin: 0 auto; padding: 0 2rem; }
    .hero { padding: 62px 0 48px; border-bottom: 1px solid rgba(0,0,0,0.06); }
    .hero-grid {
      direction: ltr;
      display: grid;
      grid-template-areas: "visual copy";
      grid-template-columns: minmax(340px, 1.05fr) minmax(300px, 0.95fr);
      gap: 4rem;
      min-height: 580px;
      align-items: center;
    }
    @media (max-width: 767px) {
      .hero-grid { grid-template-areas: "copy" "visual"; grid-template-columns: 1fr; min-height: auto; gap: 2rem; }
    }
    .hero-visual {
      grid-area: visual;
      position: relative;
      overflow: hidden;
      border-radius: 38px;
      border: 1px solid rgba(0,0,0,0.06);
      background: linear-gradient(to bottom, #FAFAF7, #F0F2EC);
      box-shadow: 0 32px 80px -24px rgba(17,19,24,0.18);
      min-height: 520px;
      display: flex; align-items: center; justify-content: center;
    }
    .hero-visual::before {
      content: "";
      position: absolute; top: 0; right: 0;
      width: 18rem; height: 18rem;
      background: #2FAE82; border-radius: 50%;
      opacity: 0.12; filter: blur(64px);
    }
    .hero-visual img { position: relative; z-index: 1; width: 100%; max-height: 520px; object-fit: contain; }
    .hero-copy {
      grid-area: copy;
      direction: rtl;
      display: flex; flex-direction: column; align-items: flex-start; gap: 1.75rem;
      text-align: right;
    }
    .eyebrow { font-size: 0.78rem; font-weight: 800; letter-spacing: 0.08em; color: #167A58; }
    .hero-h1 { font-size: clamp(2.75rem, 6.5vw, 5rem); font-weight: 900; line-height: 1.02; letter-spacing: -0.045em; }
    .hero-h1 .green { color: #167A58; }
    .subline { font-size: 1.2rem; line-height: 1.65; color: #4E5663; max-width: 36rem; font-weight: 500; }
    .cta-block { display: flex; flex-direction: column; gap: 0.75rem; width: 100%; max-width: 390px; }
    .cta-btn {
      height: 70px; font-size: 1.05rem; font-weight: 800;
      border-radius: 1rem; border: none;
      background: linear-gradient(to right, #167A58, #1A9168);
      color: #F7F7F2;
      box-shadow: 0 20px 48px -16px rgba(22,122,88,0.55);
      display: flex; align-items: center; justify-content: center; gap: 0.5rem;
      text-decoration: none; cursor: pointer; font-family: inherit;
    }
    .secondary-cta { font-size: 0.875rem; font-weight: 700; color: #9A9FA6; }
    .comparisons-section { padding: 3.5rem 0 5rem; }
    .section-head { display: flex; flex-direction: column; align-items: center; gap: 0.75rem; text-align: center; margin-bottom: 2.5rem; direction: rtl; }
    .section-eyebrow { font-size: 0.875rem; font-weight: 800; color: #167A58; }
    .section-title { font-size: clamp(1.6rem, 4vw, 2.25rem); font-weight: 900; letter-spacing: -0.045em; }
    .section-subtitle { font-size: 1rem; color: #4E5663; max-width: 32rem; line-height: 1.6; font-weight: 600; }
    .section-link { font-size: 0.875rem; font-weight: 700; color: #1F8F6A; text-decoration: none; margin-top: 0.25rem; }
    .comparison-shell {
      max-width: 1180px; margin: 0 auto;
      border-radius: 34px;
      border: 1px solid rgba(0,0,0,0.06);
      background: rgba(255,255,255,0.86);
      padding: 18px;
      box-shadow: 0 16px 48px -20px rgba(17,19,24,0.14);
    }
    .comparison-shell img { width: 100%; display: block; border-radius: 24px; }
    .banner { background: #fde8e8; color: #7a2020; text-align: center; padding: 0.5rem; font-size: 0.8rem; font-weight: 700; }
  </style>
</head>
<body>
  <div class="banner">תצוגה מקומית — פתחו את הקובץ הזה בדפדפן. הטקסט בעברית + תמונות מ-assets/</div>

  <section class="hero">
    <div class="container">
      <div class="hero-grid">
        <div class="hero-visual">
          <img src="assets/hero-product-stage.png" alt="הדמיית ניתוח מוצרי מזון" />
        </div>
        <div class="hero-copy">
          <p class="eyebrow">ניתוח מוצרים · המדף הישראלי</p>
          <h1 class="hero-h1">
            <span style="display:block">האריזה מספרת סיפור.</span>
            <span class="green" style="display:block">בארי בודקת את<br />הרכיבים.</span>
          </h1>
          <p class="subline">חפשו מוצר מהסופר וקבלו תשובה פשוטה: מה טוב, מה בעייתי, ומה בעיקר שיווק.</p>
          <div class="cta-block">
            <a class="cta-btn" href="#">חפשו מוצר</a>
            <p class="secondary-cta">סריקת ברקוד בקרוב</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="comparisons-section">
    <div class="container">
      <div class="section-head">
        <p class="section-eyebrow">ניתוחי קטגוריה · מוצרים אמיתיים</p>
        <h2 class="section-title">השוואות מהמוצרים שאתם צורכים ביום יום</h2>
        <p class="section-subtitle">לא כל מה שנראה דומה — באמת דומה.</p>
        <a class="section-link" href="#">כל ההשוואות ←</a>
      </div>
      <div class="comparison-shell">
        <img src="assets/featured-cereal-duel-stage.png" alt="דוגמת השוואת דגני בוקר" />
      </div>
    </div>
  </section>
</body>
</html>
'''

out = Path(r"c:\Bari\project_gen_z\prototypes\mocks\hero-pass4-preview.html")
out.write_text(html, encoding="utf-8")
print("written", out.stat().st_size)
