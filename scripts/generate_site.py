#!/usr/bin/env python3
"""Generate the dependency-free visual guide from repository data."""

from __future__ import annotations

import argparse
import html
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(relative_path: str) -> dict:
    with (ROOT / relative_path).open(encoding="utf-8") as handle:
        return json.load(handle)


def escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def render() -> str:
    claims = load_json("data/claims.json")
    architecture = load_json("data/architecture.json")
    maturity = load_json("data/maturity.json")

    counts = Counter(claim["kind"] for claim in claims["claims"])
    layer_cards = []
    for layer in sorted(architecture["layers"], key=lambda item: item["order"]):
        responsibilities = "".join(
            f"<li>{escape(item)}</li>" for item in layer["responsibilities"]
        )
        examples = " · ".join(escape(item) for item in layer["examples"])
        claim_ids = ", ".join(escape(item) for item in layer["claims"])
        layer_cards.append(
            f"""
            <article class="layer">
              <div class="layer-number">{layer["order"]}</div>
              <div>
                <p class="eyebrow">{escape(layer["owner"])}</p>
                <h3>{escape(layer["name"])}</h3>
                <ul>{responsibilities}</ul>
                <p class="examples">{examples}</p>
                <p class="claims">Evidence: {claim_ids}</p>
              </div>
            </article>"""
        )

    maturity_rows = []
    for surface in maturity["surfaces"]:
        maturity_rows.append(
            "<tr>"
            f"<td>{escape(surface['name'])}</td>"
            f"<td><span class=\"status {escape(surface['status'])}\">"
            f"{escape(surface['status'])}</span></td>"
            f"<td>{escape(surface['guide_policy'])}</td>"
            "</tr>"
        )

    claim_details = []
    for claim in claims["claims"]:
        evidence = claim.get("evidence", [])
        if evidence:
            source = "; ".join(
                f"{item['path']} — {item['section']}" for item in evidence
            )
        else:
            source = "Derived from " + ", ".join(claim["derived_from"])
        claim_details.append(
            f"""
            <details>
              <summary><code>{escape(claim["id"])}</code>
                <span>{escape(claim["statement"])}</span>
              </summary>
              <p><strong>{escape(claim["kind"])}</strong> ·
                {escape(claim["category"])} · {escape(claim["status"])}</p>
              <p>{escape(source)}</p>
            </details>"""
        )

    document = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Agency under the hood</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #172033;
      --muted: #5b6474;
      --paper: #f7f5ef;
      --panel: #ffffff;
      --line: #d9d4c9;
      --blue: #1456d8;
      --cyan: #20a4b8;
      --amber: #c77800;
      --green: #247a4d;
      --red: #b42318;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Segoe UI", system-ui, sans-serif;
      color: var(--ink);
      background: var(--paper);
      line-height: 1.55;
    }}
    header {{
      padding: 5rem max(1.5rem, calc((100vw - 1120px) / 2));
      color: white;
      background:
        radial-gradient(circle at 90% 10%, #27a7b8 0, transparent 35%),
        linear-gradient(135deg, #0f2f68, #1e57ba 60%, #154892);
    }}
    header p {{ max-width: 760px; font-size: 1.2rem; }}
    h1 {{ max-width: 820px; margin: 0; font-size: clamp(2.5rem, 6vw, 5.2rem); line-height: .98; }}
    main {{ width: min(1120px, calc(100% - 3rem)); margin: 0 auto; }}
    section {{ padding: 4rem 0; }}
    h2 {{ font-size: clamp(1.8rem, 4vw, 3rem); margin-bottom: .5rem; }}
    .lede {{ max-width: 780px; color: var(--muted); font-size: 1.1rem; }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
      gap: 1rem;
      margin-top: -2rem;
    }}
    .metric, .layer, .loop-step {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 16px;
      box-shadow: 0 12px 30px rgb(20 34 60 / 8%);
    }}
    .metric {{ padding: 1.4rem; }}
    .metric strong {{ display: block; font-size: 2rem; color: var(--blue); }}
    .architecture {{ display: grid; gap: 1rem; margin-top: 2rem; }}
    .layer {{
      display: grid;
      grid-template-columns: 64px 1fr;
      gap: 1rem;
      padding: 1.25rem;
    }}
    .layer-number {{
      display: grid;
      width: 48px;
      height: 48px;
      place-items: center;
      border-radius: 50%;
      color: white;
      background: var(--blue);
      font-size: 1.2rem;
      font-weight: 700;
    }}
    .layer h3 {{ margin: .1rem 0 .5rem; font-size: 1.35rem; }}
    .layer ul {{ margin: .4rem 0; padding-left: 1.25rem; }}
    .eyebrow {{ margin: 0; color: var(--blue); text-transform: uppercase; letter-spacing: .08em; font-size: .75rem; font-weight: 700; }}
    .examples {{ color: var(--muted); }}
    .claims {{ color: var(--blue); font-size: .85rem; }}
    .loop {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: .75rem; margin-top: 2rem; }}
    .loop-step {{ padding: 1rem; text-align: center; font-weight: 700; }}
    table {{ width: 100%; border-collapse: collapse; background: var(--panel); margin-top: 1.5rem; }}
    th, td {{ padding: .9rem; border: 1px solid var(--line); text-align: left; vertical-align: top; }}
    th {{ background: #edf2fb; }}
    .status {{ padding: .2rem .55rem; border-radius: 999px; font-size: .8rem; font-weight: 700; }}
    .released {{ color: var(--green); background: #e6f4ec; }}
    .experimental {{ color: var(--amber); background: #fff1d6; }}
    .excluded {{ color: var(--red); background: #feeceb; }}
    details {{ padding: .85rem 0; border-bottom: 1px solid var(--line); }}
    summary {{ cursor: pointer; display: flex; gap: .75rem; }}
    summary code {{ min-width: 52px; color: var(--blue); }}
    details p {{ margin-left: 64px; color: var(--muted); }}
    footer {{ padding: 3rem; text-align: center; color: var(--muted); }}
    @media (max-width: 620px) {{
      header {{ padding-top: 3rem; padding-bottom: 4rem; }}
      .layer {{ grid-template-columns: 48px 1fr; }}
      th:nth-child(3), td:nth-child(3) {{ display: none; }}
      details p {{ margin-left: 0; }}
    }}
  </style>
</head>
<body>
  <header>
    <p class="eyebrow" style="color:#bdeef3">Evidence-backed field guide</p>
    <h1>Agency under the hood</h1>
    <p>Agency is an integration, governance, and execution control plane around
    supported agent engines. This view separates what Agency owns, what the engine
    owns, and what your tools, credentials, and validation must still prove.</p>
    <p>Evidence pin: Agency {escape(claims["agency_release"])}</p>
  </header>
  <main>
    <div class="metrics">
      <div class="metric"><strong>{counts["fact"]}</strong>documented facts</div>
      <div class="metric"><strong>{counts["interpretation"]}</strong>architectural interpretations</div>
      <div class="metric"><strong>{counts["recommendation"]}</strong>operating recommendations</div>
      <div class="metric"><strong>{len(architecture["layers"])}</strong>architecture layers</div>
    </div>
    <section>
      <h2>Six-layer mental model</h2>
      <p class="lede">The model keeps portable agent content separate from Agency's
      control functions and from the selected engine's runtime loop.</p>
      <div class="architecture">{''.join(layer_cards)}</div>
    </section>
    <section>
      <h2>Improvement loop</h2>
      <p class="lede">Observe real outcomes, encode the lesson in the strongest
      practical mechanism, prove it, govern distribution, and measure again.</p>
      <div class="loop">
        <div class="loop-step">Observe</div>
        <div class="loop-step">Classify</div>
        <div class="loop-step">Encode</div>
        <div class="loop-step">Evaluate</div>
        <div class="loop-step">Govern</div>
        <div class="loop-step">Measure</div>
      </div>
    </section>
    <section>
      <h2>Maturity handling</h2>
      <p class="lede">Experimental commands stay visible but version-sensitive.
      Unshipped and internal-only systems are excluded rather than inferred.</p>
      <table>
        <thead><tr><th>Surface</th><th>Status</th><th>Guide policy</th></tr></thead>
        <tbody>{''.join(maturity_rows)}</tbody>
      </table>
    </section>
    <section>
      <h2>Claim ledger</h2>
      <p class="lede">Facts point to installed documentation. Interpretations and
      recommendations identify the claims from which they were derived.</p>
      {''.join(claim_details)}
    </section>
  </main>
  <footer>Generated from repository data. No external assets or scripts.</footer>
</body>
</html>
"""
    return "\n".join(line.rstrip() for line in document.splitlines()) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    target = ROOT / "site" / "index.html"
    expected = render()
    if args.check:
        if not target.exists() or target.read_text(encoding="utf-8") != expected:
            print("site/index.html is out of date; run python scripts/generate_site.py")
            return 1
        print("site/index.html is current")
        return 0

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(expected, encoding="utf-8", newline="\n")
    print(f"wrote {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
