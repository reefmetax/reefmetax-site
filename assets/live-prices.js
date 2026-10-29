/* Live crypto prices for reefmetax.com. Fetches CoinGecko's public API on load and every 60 s,
   updates the baked-in table in place, and keeps the build-time snapshot if a fetch fails. */
(function () {
  "use strict";
  var CG = "https://api.coingecko.com/api/v3";
  var BASE = 60000, MAX = 600000, delay = BASE, timer = null;
  var table = document.querySelector("table.prices[data-live]");
  if (!table || !window.fetch) return;
  var rows = table.querySelectorAll("tr[data-coin]");
  var note = document.getElementById("price-note");
  var ids = [];
  for (var i = 0; i < rows.length; i++) ids.push(rows[i].getAttribute("data-coin"));

  function fmtPrice(v) {
    if (typeof v !== "number" || !isFinite(v)) return null;
    var d = v >= 1000 ? 0 : v >= 1 ? 2 : 4;
    return "$" + v.toLocaleString("en-US", { minimumFractionDigits: d, maximumFractionDigits: d });
  }
  function fmtChg(c) {
    if (typeof c !== "number" || !isFinite(c)) return { t: "n/a", cls: "flat" };
    return { t: (c >= 0 ? "+" : "") + c.toFixed(2) + "%", cls: c >= 0 ? "up" : "down" };
  }
  function etTime(d) {
    return d.toLocaleTimeString("en-US", { timeZone: "America/New_York", hour: "numeric", minute: "2-digit" }) + " ET";
  }
  function getJSON(url) {
    return fetch(url, { headers: { Accept: "application/json" }, cache: "no-store" }).then(function (r) {
      if (!r.ok) throw new Error("http " + r.status);
      return r.json();
    });
  }

  function apply(data) {
    var n = 0;
    for (var i = 0; i < rows.length; i++) {
      var q = data && data[rows[i].getAttribute("data-coin")];
      var p = q && fmtPrice(q.usd);
      if (!p) continue;
      var pc = rows[i].querySelector('[data-f="price"]'), cc = rows[i].querySelector('[data-f="chg"]');
      var c = fmtChg(q.usd_24h_change);
      if (pc) pc.textContent = p;
      if (cc) { cc.textContent = c.t; cc.className = "num " + c.cls; }
      n++;
    }
    if (n && note) note.textContent = "Live prices from CoinGecko, updated " + etTime(new Date()) + ".";
    return n;
  }

  function schedule() { clearTimeout(timer); timer = setTimeout(tick, delay); }
  function tick() {
    if (document.hidden) { schedule(); return; }
    var url = CG + "/simple/price?ids=" + encodeURIComponent(ids.join(",")) + "&vs_currencies=usd&include_24hr_change=true";
    getJSON(url).then(function (d) {
      delay = apply(d) ? BASE : Math.min(delay * 2, MAX);
    }, function () {
      delay = Math.min(delay * 2, MAX); /* keep the snapshot, back off quietly */
    }).then(schedule, schedule);
  }

  /* Optional: redraw the 7-day BTC chart once on load. */
  function chart() {
    var box = document.getElementById("btc-chart");
    if (!box) return;
    getJSON(CG + "/coins/bitcoin/market_chart?vs_currency=usd&days=7").then(function (d) {
      var all = (d && d.prices) || [], pts = [];
      var step = Math.max(1, Math.floor(all.length / 84));
      for (var i = 0; i < all.length; i += step) pts.push(all[i][1]);
      if (all.length && (all.length - 1) % step) pts.push(all[all.length - 1][1]);
      if (pts.length < 2) return;
      var w = 640, h = 180, pad = 10, lo = Math.min.apply(null, pts), hi = Math.max.apply(null, pts), rng = (hi - lo) || 1;
      var xy = pts.map(function (v, i) {
        return [(pad + i * (w - 2 * pad) / (pts.length - 1)).toFixed(1), (pad + (hi - v) * (h - 2 * pad) / rng).toFixed(1)];
      });
      var line = xy.map(function (p) { return p[0] + "," + p[1]; }).join(" ");
      var col = pts[pts.length - 1] >= pts[0] ? "#2ee6c5" : "#ff8a3d";
      var svg = box.querySelector("svg");
      if (!svg) return;
      var pl = svg.querySelector("polyline"), pg = svg.querySelector("polygon"), ci = svg.querySelector("circle"), st = svg.querySelectorAll("stop");
      if (!pl || !pg || !ci) return;
      pl.setAttribute("points", line); pl.setAttribute("stroke", col);
      pg.setAttribute("points", xy[0][0] + "," + h + " " + line + " " + xy[xy.length - 1][0] + "," + h);
      ci.setAttribute("cx", xy[xy.length - 1][0]); ci.setAttribute("cy", xy[xy.length - 1][1]); ci.setAttribute("fill", col);
      for (var j = 0; j < st.length; j++) st[j].setAttribute("stop-color", col);
      var rg = document.getElementById("btc-range");
      if (rg) rg.textContent = "Low " + fmtPrice(lo) + " \u00b7 High " + fmtPrice(hi);
    }, function () { /* keep the baked-in chart */ });
  }

  document.addEventListener("visibilitychange", function () { if (!document.hidden && delay > BASE) { delay = BASE; schedule(); } });
  tick();
  chart();
})();
