# -*- coding: utf-8 -*-
"""md2pdf.py <in.md> <out.pdf> [landscape|portrait] — pandoc -> HTML bergaya -> Chromium (Playwright) PDF."""
import sys, subprocess, os, tempfile, json
src, dst = sys.argv[1], sys.argv[2]
orient = sys.argv[3] if len(sys.argv) > 3 else "landscape"
body = subprocess.run(["pandoc", src, "-f", "gfm", "-t", "html5"], capture_output=True, text=True, check=True).stdout
css = """
body{font-family:'DejaVu Sans',Arial,sans-serif;font-size:9.3pt;color:#1d2433;line-height:1.45}
h1{font-size:18pt;color:#0b3d6e;border-bottom:3px solid #0b3d6e;padding-bottom:6px;margin:0 0 8px}
h2{font-size:13.5pt;color:#0b3d6e;margin-top:16px;border-left:5px solid #e0a100;padding-left:8px;break-after:avoid}
h3{font-size:11pt;color:#174f86;margin-top:12px;break-after:avoid}
h4{font-size:10pt;color:#2b2b2b;margin:10px 0 4px;break-after:avoid}
table{border-collapse:collapse;width:100%;margin:6px 0 10px;font-size:8pt}
tr{break-inside:avoid} th{background:#0b3d6e;color:#fff;padding:4px 5px;text-align:left}
td{border-bottom:1px solid #d6dbe3;padding:3px 5px;vertical-align:top} tr:nth-child(even) td{background:#f4f7fb}
blockquote{background:#fff7e0;border-left:4px solid #e0a100;margin:8px 0;padding:6px 10px;font-size:8.6pt}
code{background:#eef1f6;padding:0 3px;border-radius:3px;font-size:7.8pt}
ul,ol{margin:4px 0 8px 18px;padding:0} li{margin:2px 0}
p:has(+table),p:has(+ul){break-after:avoid}
"""
tmp = tempfile.mkdtemp()
html = os.path.join(tmp, "r.html")
open(html, "w", encoding="utf-8").write(f"<!doctype html><html lang='id'><head><meta charset='utf-8'><style>{css}</style></head><body>{body}</body></html>")
js = os.path.join(tmp, "p.js")
footer = '<div style="font-size:7pt;width:100%;text-align:center;color:#777">SahamExpertKB v2 · Kelompok 9 KBR · Halaman <span class="pageNumber"></span>/<span class="totalPages"></span></div>'
open(js, "w").write(f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{html}');await p.pdf({{path:{json.dumps(os.path.abspath(dst))},format:'A4',landscape:{'true' if orient=='landscape' else 'false'},printBackground:true,
displayHeaderFooter:true,headerTemplate:'<span></span>',footerTemplate:{json.dumps(footer)},margin:{{top:'13mm',bottom:'15mm',left:'11mm',right:'11mm'}}}});await b.close();}})();""")
subprocess.run(["node", js], check=True)
print("PDF:", dst)
