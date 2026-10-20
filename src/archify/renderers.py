"""
Architecture Renderers: Interactive HTML & Scalable Vector Graphics (SVG)
"""

import os
from datetime import datetime
from typing import Dict, Any, Optional
from .scanner import scan_architecture

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Architecture Map - {target_name}</title>
  <style>
    :root {{
      --bg: #090d16;
      --card-bg: rgba(22, 28, 45, 0.85);
      --border: rgba(99, 102, 241, 0.25);
      --accent: #6366f1;
      --accent-glow: rgba(99, 102, 241, 0.35);
      --text: #f8fafc;
      --text-dim: #94a3b8;
      --cyan: #38bdf8;
      --green: #4ade80;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 32px;
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}
    .header {{
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--border);
      padding-bottom: 20px;
      margin-bottom: 24px;
      gap: 16px;
    }}
    .title {{
      font-size: 26px;
      font-weight: 700;
      background: linear-gradient(135deg, #818cf8, #38bdf8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .subtitle {{
      color: var(--text-dim);
      font-size: 14px;
      margin-top: 4px;
    }}
    .search-bar {{
      padding: 8px 14px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border);
      border-radius: 8px;
      color: var(--text);
      font-size: 14px;
      width: 260px;
      outline: none;
      transition: border 0.2s;
    }}
    .search-bar:focus {{
      border-color: var(--cyan);
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 20px;
    }}
    .node {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px;
      backdrop-filter: blur(12px);
      box-shadow: 0 4px 24px rgba(0,0,0,0.4);
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .node:hover {{
      border-color: var(--accent);
      box-shadow: 0 10px 32px var(--accent-glow);
      transform: translateY(-3px);
    }}
    .node-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 10px;
    }}
    .node-title {{
      font-size: 17px;
      font-weight: 600;
      color: var(--cyan);
      word-break: break-all;
    }}
    .node-type {{
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      padding: 3px 8px;
      background: rgba(99, 102, 241, 0.18);
      border-radius: 4px;
      color: #c7d2fe;
      white-space: nowrap;
    }}
    .node-details {{
      font-size: 13px;
      color: var(--text-dim);
      line-height: 1.6;
    }}
    .badges {{
      margin-top: 12px;
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }}
    .badge {{
      background: rgba(255, 255, 255, 0.06);
      padding: 4px 8px;
      border-radius: 5px;
      font-size: 11px;
      color: #cbd5e1;
    }}
    .badge-lang {{
      background: rgba(56, 189, 248, 0.15);
      color: #7dd3fc;
    }}
  </style>
</head>
<body>
  <div class="header">
    <div>
      <div class="title">⚡ Architecture Map: {target_name}</div>
      <div class="subtitle">Generated on {timestamp} | Explorable Component & Module Topology</div>
    </div>
    <div style="display: flex; gap: 16px; align-items: center;">
      <input type="text" id="searchInput" class="search-bar" placeholder="Filter components...">
      <div style="font-size: 14px; color: var(--text-dim);">Total Nodes: <b>{total_nodes}</b> | Files: <b>{total_files}</b></div>
    </div>
  </div>
  <div class="grid" id="nodeGrid">
    {cards_html}
  </div>

  <script>
    const search = document.getElementById('searchInput');
    const nodes = document.querySelectorAll('.node');
    search.addEventListener('input', (e) => {{
      const q = e.target.value.toLowerCase();
      nodes.forEach(n => {{
        const text = n.innerText.toLowerCase();
        n.style.display = text.includes(q) ? 'block' : 'none';
      }});
    }});
  </script>
</body>
</html>
"""

def generate_html(target_path: str = ".", output_path: Optional[str] = None) -> str:
    data = scan_architecture(target_path)
    target_name = data["target_name"]

    cards = []
    for n in data["nodes"]:
        card = f"""
        <div class="node">
          <div class="node-header">
            <div class="node-title">{n['name']}</div>
            <div class="node-type">{n['kind']}</div>
          </div>
          <div class="node-details">
            <div>Files in Tree: <b>{n['files']}</b></div>
            <div class="badges">
              <span class="badge badge-lang">{n['language']}</span>
              <span class="badge">{'Directory' if n['is_dir'] else 'Artifact'}</span>
            </div>
          </div>
        </div>
        """
        cards.append(card)

    html = HTML_TEMPLATE.format(
        target_name=target_name,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total_nodes=data["total_nodes"],
        total_files=data["total_files"],
        cards_html="\n".join(cards)
    )

    if not output_path:
        output_path = os.path.join(data["target_path"], f"architecture-{target_name}.html")

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return os.path.abspath(output_path)

def generate_svg(target_path: str = ".", output_path: Optional[str] = None) -> str:
    data = scan_architecture(target_path)
    nodes = data["nodes"]
    target_name = data["target_name"]

    node_width = 240
    node_height = 80
    cols = 3
    spacing_x = 24
    spacing_y = 20
    padding = 32

    rows = (len(nodes) + cols - 1) // cols if nodes else 1
    svg_width = padding * 2 + cols * node_width + (cols - 1) * spacing_x
    svg_height = padding * 2 + 60 + rows * (node_height + spacing_y)

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">',
        '  <defs>',
        '    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#090d16" />',
        '      <stop offset="100%" stop-color="#111827" />',
        '    </linearGradient>',
        '    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#1e293b" />',
        '      <stop offset="100%" stop-color="#0f172a" />',
        '    </linearGradient>',
        '  </defs>',
        f'  <rect width="{svg_width}" height="{svg_height}" rx="12" fill="url(#bgGrad)" stroke="#374151" stroke-width="1"/>',
        f'  <text x="{padding}" y="{padding + 22}" fill="#818cf8" font-family="system-ui, sans-serif" font-size="20" font-weight="700">⚡ Architecture: {target_name}</text>',
        f'  <text x="{padding}" y="{padding + 42}" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="12">Components: {data["total_nodes"]} | Files: {data["total_files"]}</text>'
    ]

    for idx, n in enumerate(nodes):
        r = idx // cols
        c = idx % cols
        x = padding + c * (node_width + spacing_x)
        y = padding + 60 + r * (node_height + spacing_y)

        name = n["name"][:24]
        kind = n["kind"][:20]
        lang = n["language"]

        svg_parts.extend([
            f'  <g transform="translate({x}, {y})">',
            f'    <rect width="{node_width}" height="{node_height}" rx="8" fill="url(#cardGrad)" stroke="#6366f1" stroke-width="1.2" stroke-opacity="0.4"/>',
            f'    <text x="14" y="24" fill="#38bdf8" font-family="system-ui, sans-serif" font-size="13" font-weight="600">{name}</text>',
            f'    <text x="14" y="44" fill="#a5b4fc" font-family="system-ui, sans-serif" font-size="10">{kind}</text>',
            f'    <text x="14" y="62" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="10">{lang} ({n["files"]} files)</text>',
            '  </g>'
        ])

    svg_parts.append('</svg>')
    svg_content = "\n".join(svg_parts)

    if not output_path:
        output_path = os.path.join(data["target_path"], f"architecture-{target_name}.svg")

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    return os.path.abspath(output_path)
