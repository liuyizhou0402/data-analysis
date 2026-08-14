// Two-slide presentation deck — flat-vector editorial style.
// All icons and illustrations are hand-authored SVG, rasterised at build time.
const PptxGenJS = require("pptxgenjs");
const sharp = require("sharp");

/* ------------------------------------------------------------------ *
 * palette
 * ------------------------------------------------------------------ */
const C = {
  cream:    "FBF7F1",
  ink:      "12263A",
  inkSoft:  "3A5265",
  muted:    "7A8CA0",
  white:    "FFFFFF",
  hair:     "E7DFD4",

  teal:     "1F7A72",
  tealLt:   "DCEDEA",
  coral:    "D9532F",
  coralLt:  "FAE2D8",
  amber:    "E9A83B",

  navy:     "0E2136",
  navyCard: "17324C",
  navyLine: "27506F",
  navyText: "AFC4D6",
};
const FONT = "Arial";

/* ------------------------------------------------------------------ *
 * hand-authored SVG assets
 * ------------------------------------------------------------------ */

// speed / rapid triage
const icoBolt = (_c) => { const c = h(_c); return `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <path d="M37 5 L16 35 h12.5 L26 59 L48 27 H35.5 Z"
        fill="none" stroke="${c}" stroke-width="4"
        stroke-linejoin="round" stroke-linecap="round"/>
</svg>`; };

// continuous monitoring
const icoMonitor = (_c) => { const c = h(_c); return `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <circle cx="32" cy="32" r="23" fill="none" stroke="${c}" stroke-width="4"/>
  <path d="M17 32 h6.5 l4-9.5 l6 19 l4-9.5 H47"
        fill="none" stroke="${c}" stroke-width="4"
        stroke-linecap="round" stroke-linejoin="round"/>
</svg>`; };

// human connection — two figures sharing a heart
const icoPeople = (_c) => { const c = h(_c); return `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <path d="M32 17.5 c-2-3.6-7.5-3.2-7.5 1.4 0 3.6 5 6.6 7.5 8.6
           2.5-2 7.5-5 7.5-8.6 0-4.6-5.5-5-7.5-1.4 Z"
        fill="${c}" stroke="none"/>
  <circle cx="19" cy="33" r="6.5" fill="none" stroke="${c}" stroke-width="4"/>
  <circle cx="45" cy="33" r="6.5" fill="none" stroke="${c}" stroke-width="4"/>
  <path d="M7.5 55 a11.5 11.5 0 0 1 23 0" fill="none" stroke="${c}"
        stroke-width="4" stroke-linecap="round"/>
  <path d="M33.5 55 a11.5 11.5 0 0 1 23 0" fill="none" stroke="${c}"
        stroke-width="4" stroke-linecap="round"/>
</svg>`; };

// deployment fit — puzzle piece
const icoFit = (_c) => { const c = h(_c); return `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <path d="M13 20 a4 4 0 0 1 4-4 h8 a5.5 5.5 0 0 1 11 0 h8 a4 4 0 0 1 4 4
           v8 a5.5 5.5 0 0 0 0 11 v8 a4 4 0 0 1 -4 4 h-27 a4 4 0 0 1 -4-4 Z"
        fill="none" stroke="${c}" stroke-width="4" stroke-linejoin="round"/>
</svg>`; };

// acute trajectory — steep spike, quick resolution
const trajAcute = (_c, _d) => { const c = h(_c), dim = h(_d); return `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 64">
  <path d="M4 59 H236" stroke="${dim}" stroke-width="2"
        stroke-dasharray="3 5" stroke-linecap="round"/>
  <path d="M4 54 L52 54 L68 8 L86 54 L236 54"
        fill="none" stroke="${c}" stroke-width="4.5"
        stroke-linejoin="round" stroke-linecap="round"/>
  <circle cx="68" cy="8" r="6" fill="${c}"/>
</svg>`; };

// chronic trajectory — long elevated plateau
const trajChronic = (_c, _d) => { const c = h(_c), dim = h(_d); return `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 64">
  <path d="M4 54 H236" stroke="${dim}" stroke-width="2"
        stroke-dasharray="3 5" stroke-linecap="round"/>
  <path d="M4 54 C30 54 38 24 66 24 C96 24 100 34 126 29
           C152 24 162 33 190 28 C214 24 220 30 236 28"
        fill="none" stroke="${c}" stroke-width="4.5"
        stroke-linejoin="round" stroke-linecap="round"/>
  <circle cx="66" cy="24" r="6" fill="${c}"/>
  <circle cx="236" cy="28" r="6" fill="${c}"/>
</svg>`; };

// decorative concentric ring
const ring = (_c, o) => { const c = h(_c); return `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
  <circle cx="100" cy="100" r="94" fill="none" stroke="${c}"
          stroke-width="3" opacity="${o}"/>
  <circle cx="100" cy="100" r="68" fill="none" stroke="${c}"
          stroke-width="3" opacity="${o}"/>
  <circle cx="100" cy="100" r="42" fill="none" stroke="${c}"
          stroke-width="3" opacity="${o}"/>
</svg>`; };

const h = (c) => (String(c).startsWith("#") ? c : "#" + c);

async function png(svg, width) {
  const buf = await sharp(Buffer.from(svg), { density: 400 })
    .resize({ width })
    .png()
    .toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

/* ------------------------------------------------------------------ */
(async () => {
  const A = {
    bolt:     await png(icoBolt(C.coral), 320),
    monitor:  await png(icoMonitor(C.teal), 320),
    people:   await png(icoPeople(C.navy), 320),
    fit:      await png(icoFit(C.navy), 320),
    acute:    await png(trajAcute(C.coral, C.hair), 900),
    chronic:  await png(trajChronic(C.teal, C.hair), 900),
    ringWarm: await png(ring(C.coral, 0.20), 800),
    ringCool: await png(ring(C.navyLine, 0.85), 800),
  };

  const pres = new PptxGenJS();
  pres.layout = "LAYOUT_WIDE";
  pres.title = "Illness Trajectory and AI Deployment Logic";

  const M = 0.85;                  // page margin
  const W = 13.333 - M * 2;        // 11.633

  /* ================================================================ *
   * SLIDE 1 — Finding 01
   * ================================================================ */
  {
    const s = pres.addSlide();
    s.background = { color: C.cream };

    // soft field + ring, top right
    s.addShape(pres.ShapeType.ellipse, {
      x: 10.15, y: -1.55, w: 4.9, h: 4.9, fill: { color: C.tealLt },
      line: { color: C.tealLt, width: 0 },
    });
    s.addImage({ data: A.ringWarm, x: 10.62, y: 0.32, w: 2.5, h: 2.5 });

    s.addText("FINDING 01   ·   CARE TRAJECTORY", {
      x: M, y: 0.62, w: 8.0, h: 0.3, margin: 0,
      fontFace: FONT, fontSize: 11.5, bold: true, color: C.coral,
      charSpacing: 3.2, valign: "middle",
    });

    s.addText("Different Illness Trajectories\nNeed Different AI Logics", {
      x: M, y: 1.02, w: 9.4, h: 1.5, margin: 0,
      fontFace: FONT, fontSize: 38, bold: true, color: C.ink,
      lineSpacing: 46, valign: "middle",
    });

    // ---- comparison cards -----------------------------------------
    const cw = (W - 0.5) / 2, cy = 2.9, ch = 3.6;
    const cards = [
      {
        tag: "ACUTE CARE", accent: C.coral, tint: C.coralLt,
        icon: A.bolt, head: "Front-Line AI",
        body: "Leverages front-line AI for speed and rapid triage.",
        traj: A.acute, note: "Short, steep trajectory",
      },
      {
        tag: "CHRONIC CARE", accent: C.teal, tint: C.tealLt,
        icon: A.monitor, head: "Behind-the-Scenes AI",
        body: "Relies on behind-the-scenes AI for long-term monitoring.",
        traj: A.chronic, note: "Long, sustained trajectory",
      },
    ];

    cards.forEach((c, i) => {
      const x = M + i * (cw + 0.5);
      s.addShape(pres.ShapeType.roundRect, {
        x, y: cy, w: cw, h: ch, rectRadius: 0.14,
        fill: { color: C.white },
        line: { color: C.hair, width: 1 },
      });

      s.addShape(pres.ShapeType.roundRect, {
        x: x + 0.42, y: cy + 0.42, w: 1.62, h: 0.36, rectRadius: 0.17,
        fill: { color: c.accent }, line: { color: c.accent, width: 0 },
      });
      s.addText(c.tag, {
        x: x + 0.42, y: cy + 0.42, w: 1.62, h: 0.36, margin: 0,
        fontFace: FONT, fontSize: 9, bold: true, color: C.white,
        charSpacing: 1.4, align: "center", valign: "middle",
      });

      s.addShape(pres.ShapeType.ellipse, {
        x: x + cw - 1.36, y: cy + 0.34, w: 0.94, h: 0.94,
        fill: { color: c.tint }, line: { color: c.tint, width: 0 },
      });
      s.addImage({
        data: c.icon, x: x + cw - 1.13, y: cy + 0.57, w: 0.48, h: 0.48,
      });

      s.addText(c.head, {
        x: x + 0.42, y: cy + 1.06, w: cw - 0.84, h: 0.46, margin: 0,
        fontFace: FONT, fontSize: 23, bold: true, color: C.ink,
        valign: "middle",
      });
      s.addText(c.body, {
        x: x + 0.42, y: cy + 1.6, w: cw - 0.9, h: 0.86, margin: 0,
        fontFace: FONT, fontSize: 14, color: C.inkSoft,
        lineSpacing: 21, valign: "top",
      });

      s.addImage({
        data: c.traj, x: x + 0.42, y: cy + 2.5, w: cw - 0.84, h: 0.62,
      });
      s.addText(c.note, {
        x: x + 0.42, y: cy + 3.14, w: cw - 0.84, h: 0.26, margin: 0,
        fontFace: FONT, fontSize: 10, bold: true, color: c.accent,
        charSpacing: 0.8, valign: "middle",
      });
    });

    s.addText("Acute vs. chronic care demand fundamentally different roles for AI.", {
      x: M, y: 6.72, w: W, h: 0.3, margin: 0,
      fontFace: FONT, fontSize: 10.5, color: C.muted, valign: "middle",
    });
    s.addNotes(
      "Finding 01. The trajectory of the illness — not the technology — sets " +
      "the deployment logic. Acute care compresses decisions into minutes, so " +
      "AI sits at the front line for triage speed. Chronic care unfolds over " +
      "years, so AI works in the background on monitoring."
    );
  }

  /* ================================================================ *
   * SLIDE 2 — Findings 02 & 03
   * ================================================================ */
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };

    s.addShape(pres.ShapeType.ellipse, {
      x: 10.5, y: -1.9, w: 5.2, h: 5.2, fill: { color: C.navyCard },
      line: { color: C.navyCard, width: 0 },
    });
    s.addImage({ data: A.ringCool, x: 10.95, y: 0.28, w: 2.4, h: 2.4 });

    s.addText("FINDINGS 02 & 03   ·   IMPLEMENTATION", {
      x: M, y: 0.62, w: 8.5, h: 0.3, margin: 0,
      fontFace: FONT, fontSize: 11.5, bold: true, color: C.amber,
      charSpacing: 3.2, valign: "middle",
    });

    s.addText("Two Conditions for Clinical Success", {
      x: M, y: 1.02, w: 9.6, h: 0.8, margin: 0,
      fontFace: FONT, fontSize: 36, bold: true, color: C.white,
      valign: "middle",
    });

    const rows = [
      {
        n: "02", accent: C.teal, icon: A.people,
        head: "Preserving Human Connection",
        body: "Patients with chronic conditions prioritize trust and emotional " +
              "support, requiring face-to-face physician interaction that " +
              "technology cannot replace.",
      },
      {
        n: "03", accent: C.coral, icon: A.fit,
        head: "Deployment Fit Defines Success",
        body: "Mismatching AI’s role — forcing standalone AI where human trust " +
              "is critical — is the primary driver of clinical implementation " +
              "failure.",
      },
    ];

    const rh = 1.94;
    rows.forEach((r, i) => {
      const y = 2.34 + i * (rh + 0.26);
      s.addShape(pres.ShapeType.roundRect, {
        x: M, y, w: W, h: rh, rectRadius: 0.13,
        fill: { color: C.navyCard },
        line: { color: C.navyLine, width: 1 },
      });

      s.addShape(pres.ShapeType.ellipse, {
        x: M + 0.5, y: y + 0.42, w: 1.1, h: 1.1,
        fill: { color: r.accent }, line: { color: r.accent, width: 0 },
      });
      s.addImage({
        data: r.icon, x: M + 0.775, y: y + 0.695, w: 0.55, h: 0.55,
      });

      s.addText(r.n, {
        x: M + 2.05, y: y + 0.32, w: 0.6, h: 0.3, margin: 0,
        fontFace: FONT, fontSize: 12, bold: true, color: r.accent,
        charSpacing: 1.2, valign: "middle",
      });
      s.addText(r.head, {
        x: M + 2.05, y: y + 0.6, w: W - 2.6, h: 0.44, margin: 0,
        fontFace: FONT, fontSize: 22, bold: true, color: C.white,
        valign: "middle",
      });
      s.addText(r.body, {
        x: M + 2.05, y: y + 1.06, w: W - 2.75, h: 0.72, margin: 0,
        fontFace: FONT, fontSize: 13.5, color: C.navyText,
        lineSpacing: 20, valign: "top",
      });
    });

    s.addText("Fit the role to the trajectory — or implementation fails.", {
      x: M, y: 6.72, w: W, h: 0.3, margin: 0,
      fontFace: FONT, fontSize: 10.5, color: "6E8BA5", valign: "middle",
    });
    s.addNotes(
      "Findings 02 and 03. Trust is the constraint chronic care cannot trade " +
      "away, so face-to-face time has to survive automation. Failure is " +
      "usually not a model problem — it is a role-assignment problem: " +
      "standalone AI deployed where human trust was the active ingredient."
    );
  }

  const f = await pres.writeFile({ fileName: "AI_Trajectory_Deck.pptx" });
  console.log("written:", f);
})();
