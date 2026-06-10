/* plant-hero-engine.js — Bari sprout: assemble → breathe → shatter-into-constellation → reform.
   Drives 5 pixel-sliced logo pieces (full-frame, so they stack into the exact logo).
   Vanilla, RAF-driven. */
"use strict";

var PIECES = [
  // id, scatter direction (unit-ish), scatter rotation (deg), assemble order, sway
  { id: "navyL", dir: [-0.85, 0.55], rot: -52, order: 0.00, sway: 2.2, ph: 0.0, dot: false },
  { id: "navyR", dir: [ 0.85, 0.55], rot:  52, order: 0.08, sway: 2.2, ph: 3.1, dot: false },
  { id: "greenL", dir: [-0.80, -0.62], rot: -38, order: 0.42, sway: 3.0, ph: 1.4, dot: false },
  { id: "greenR", dir: [ 0.80, -0.62], rot:  38, order: 0.50, sway: 3.0, ph: 4.2, dot: false },
  { id: "dot",   dir: [ 0.00, -1.00], rot:   0, order: 0.86, sway: 0.0, ph: 0.0, dot: true },
];
// normalized centroids of each piece within the frame (for constellation nodes)
var CENTROID = {
  dot: [0.50, 0.317], greenL: [0.427, 0.476], greenR: [0.576, 0.477],
  navyL: [0.382, 0.645], navyR: [0.619, 0.644],
};
// constellation edges (which nodes connect) — a little signal network
var EDGES = [["dot","greenL"],["dot","greenR"],["greenL","greenR"],
  ["greenL","navyL"],["greenR","navyR"],["navyL","navyR"],["dot","navyL"],["dot","navyR"]];

var FRAME_W = 643, FRAME_H = 663, ASPECT = FRAME_H / FRAME_W;

function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
function easeOutCubic(t) { return 1 - Math.pow(1 - t, 3); }
function easeOutBack(t) { var c1=1.70158, c3=c1+1; return 1 + c3*Math.pow(t-1,3) + c1*Math.pow(t-1,2); }

function PlantHero(opts) {
  this.cfg = Object.assign({
    stage: null, assetBase: "assets/plant/",
    size: 520, opacity: 0.2, mode: "watermark",
    shatter: true, period: 7.0, constellation: true,
    particles: 0.6, parallax: true,
  }, opts || {});
  this.reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  this._build();
  this._t0 = performance.now();
  this._mode = "intro"; this._idleStart = 0;
  this._px = 0; this._py = 0; this._tpx = 0; this._tpy = 0; this._scroll = 0;
  this._bind();
  this._tick = this._tick.bind(this);
  this._rafId = requestAnimationFrame(this._tick);
}

PlantHero.prototype._build = function () {
  var st = this.cfg.stage; st.classList.add("plant-stage");
  st.innerHTML = "";
  // constellation svg
  var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("class", "plant-constellation"); svg.setAttribute("viewBox", "0 0 100 " + (100*ASPECT).toFixed(2));
  svg.setAttribute("preserveAspectRatio", "none");
  this._lines = {}; this._nodes = {};
  var g = document.createElementNS(svg.namespaceURI, "g"); g.setAttribute("class", "plant-net"); svg.appendChild(g);
  EDGES.forEach(function (e, i) {
    var ln = document.createElementNS(svg.namespaceURI, "line");
    ln.setAttribute("class", "plant-edge"); g.appendChild(ln); this._lines[i] = ln;
  }, this);
  Object.keys(CENTROID).forEach(function (id) {
    var c = document.createElementNS(svg.namespaceURI, "circle");
    c.setAttribute("class", "plant-node"); c.setAttribute("r", "0.9"); g.appendChild(c); this._nodes[id] = c;
  }, this);
  this._svg = svg; this._net = g; st.appendChild(svg);
  // plant + pieces
  var plant = document.createElement("div"); plant.className = "plant"; this._plant = plant;
  this._els = {};
  PIECES.forEach(function (p) {
    var d = document.createElement("div"); d.className = "piece piece-" + p.id;
    var img = document.createElement("img"); img.src = this.cfg.assetBase + p.id + ".png"; img.alt = "";
    img.draggable = false; d.appendChild(img); plant.appendChild(d); this._els[p.id] = d;
  }, this);
  st.appendChild(plant);
  // particles layer
  var pl = document.createElement("div"); pl.className = "plant-particles"; this._pLayer = pl;
  st.parentNode.appendChild(pl); this._spawnParticles();
  this._applyLayout();
};

PlantHero.prototype._applyLayout = function () {
  var c = this.cfg, st = c.stage;
  st.style.setProperty("--plant-size", c.size + "px");
  st.dataset.mode = c.mode;
  this._plant.style.opacity = c.mode === "mascot" ? 1 : c.opacity;
  this._svg.style.opacity = (c.constellation && c.mode !== "mascot") ? 1 : (c.constellation ? 0.7 : 0);
  this._pLayer.style.display = c.particles > 0 ? "block" : "none";
};

PlantHero.prototype.setConfig = function (partial) {
  var hadParts = this.cfg.particles;
  Object.assign(this.cfg, partial);
  this._applyLayout();
  if (partial.particles !== undefined && partial.particles !== hadParts) this._spawnParticles();
};

PlantHero.prototype.replay = function () { this._t0 = performance.now(); this._mode = "intro"; };

PlantHero.prototype._spawnParticles = function () {
  var pl = this._pLayer; if (!pl) return; pl.innerHTML = "";
  var n = Math.round(this.cfg.particles * 18);
  if (this.reduced) n = 0;
  for (var i = 0; i < n; i++) {
    var s = document.createElement("span");
    var leaf = Math.random() < 0.45;
    s.className = "ppart " + (leaf ? "ppart-leaf" : "ppart-seed");
    var sz = leaf ? (10 + Math.random() * 16) : (4 + Math.random() * 5);
    s.style.left = (Math.random() * 100) + "%";
    s.style.top = (Math.random() * 100) + "%";
    s.style.width = sz + "px"; s.style.height = sz + "px";
    var dur = 9 + Math.random() * 12, delay = -Math.random() * dur;
    s.style.animationDuration = dur + "s, " + (3 + Math.random() * 3) + "s";
    s.style.animationDelay = delay + "s, " + delay + "s";
    s.style.setProperty("--drift", (Math.random() * 40 - 20) + "px");
    pl.appendChild(s);
  }
};

PlantHero.prototype._bind = function () {
  // eslint-disable-next-line @typescript-eslint/no-this-alias
  var self = this;
  if (this.reduced) return;
  this._onMove = function (e) {
    self._tpx = (e.clientX / innerWidth - 0.5) * 2; self._tpy = (e.clientY / innerHeight - 0.5) * 2;
  };
  this._onScroll = function () { self._scroll = scrollY; };
  window.addEventListener("pointermove", this._onMove, { passive: true });
  window.addEventListener("scroll", this._onScroll, { passive: true });
};

PlantHero.prototype.destroy = function () {
  cancelAnimationFrame(this._rafId);
  if (this._onMove) window.removeEventListener("pointermove", this._onMove);
  if (this._onScroll) window.removeEventListener("scroll", this._onScroll);
  if (this._pLayer && this._pLayer.parentNode) this._pLayer.parentNode.removeChild(this._pLayer);
  if (this.cfg.stage) this.cfg.stage.innerHTML = "";
};

PlantHero.prototype._shatterAmt = function (t) {
  if (!this.cfg.shatter || this.reduced) return 0;
  var c = this.cfg, cycle = (t - this._idleStart) % c.period;
  var out = 1.15, hold = 0.55, inn = 1.45;
  if (cycle < out) return easeOutCubic(cycle / out);
  if (cycle < out + hold) return 1;
  if (cycle < out + hold + inn) return 1 - easeOutBack((cycle - out - hold) / inn);
  return 0;
};

PlantHero.prototype._tick = function (now) {
  var t = (now - this._t0) / 1000, c = this.cfg;
  var size = c.size, spread = size * 0.52;
  // parallax smoothing
  this._px += (this._tpx - this._px) * 0.06; this._py += (this._tpy - this._py) * 0.06;
  if (c.parallax && !this.reduced) {
    var sc = clamp(this._scroll, 0, 800);
    c.stage.style.transform = "translate3d(" + (this._px * 14) + "px," + (this._py * 10 + sc * 0.12) + "px,0)";
    this._pLayer.style.transform = "translate3d(" + (this._px * 26) + "px," + (this._py * 18 - sc * 0.05) + "px,0)";
  } else if (this._parallaxWasOn !== false) {
    c.stage.style.transform = ""; this._pLayer.style.transform = ""; this._parallaxWasOn = false;
  }
  if (c.parallax) this._parallaxWasOn = true;
  var breathe = this.reduced ? 1 : 1 + 0.013 * Math.sin(t * 0.9);
  var shatterD = 0;
  if (this._mode === "idle") shatterD = this._shatterAmt(t);

  var introDur = 1.5, allDone = true;
  for (var i = 0; i < PIECES.length; i++) {
    var p = PIECES[i], el = this._els[p.id], d, op;
    if (this._mode === "intro" && !this.reduced) {
      var lp = clamp((t - 0.15 - p.order * 0.5) / introDur, 0, 1);
      var e = easeOutBack(lp); d = 1 - e; op = clamp(lp * 1.7, 0, 1);
      if (lp < 1) allDone = false;
    } else { d = shatterD; op = 1 - 0.08 * shatterD; }
    var sway = (this.reduced || p.dot) ? 0 : p.sway * Math.sin(t * 0.9 + p.ph);
    var bob = (this.reduced || !p.dot) ? 0 : Math.sin(t * 1.15) * size * 0.012;
    var tx = p.dir[0] * spread * d, ty = p.dir[1] * spread * d + bob;
    var rot = sway + p.rot * d, scl = breathe * (1 - 0.34 * d);
    el.style.transform = "translate(" + tx.toFixed(2) + "px," + ty.toFixed(2) + "px) rotate(" + rot.toFixed(2) + "deg) scale(" + scl.toFixed(3) + ")";
    el.style.opacity = op.toFixed(3);
    // node position (percent of frame)
    var cen = CENTROID[p.id];
    var nx = cen[0] * 100 + (tx / size) * 100;
    var node = this._nodes[p.id];
    node.setAttribute("cx", nx.toFixed(2)); node.setAttribute("cy", (cen[1]*100*ASPECT + (ty/size)*100*ASPECT).toFixed(2));
    this._np = this._np || {}; this._np[p.id] = [nx, cen[1]*100*ASPECT + (ty/size)*100*ASPECT];
  }
  if (this._mode === "intro" && (allDone || this.reduced)) { this._mode = "idle"; this._idleStart = t; }
  // constellation edges + opacity
  var netOp = (this._mode === "idle") ? shatterD : 0;
  this._net.style.opacity = (c.constellation ? netOp * 0.85 : 0).toFixed(3);
  if (this._np) {
    for (var k = 0; k < EDGES.length; k++) {
      var a = this._np[EDGES[k][0]], b = this._np[EDGES[k][1]], ln = this._lines[k];
      if (a && b) { ln.setAttribute("x1", a[0]); ln.setAttribute("y1", a[1]); ln.setAttribute("x2", b[0]); ln.setAttribute("y2", b[1]); }
    }
  }
  this._rafId = requestAnimationFrame(this._tick);
};

export default PlantHero;
