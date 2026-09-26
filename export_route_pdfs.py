#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Export all 17 routes to individual PDF files in /Users/sher/Documents/trvalpremium/route/
and merge them into route/all_routes.pdf.
"""

import os
import subprocess
import time
import fitz
from build_all_routes import ROUTES_DATA

OUTPUT_DIR = "/Users/sher/Documents/trvalpremium/route"
CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SCRATCH_DIR = "/Users/sher/.gemini/antigravity-ide/brain/fcdcd534-0006-4243-b243-98e37fb8cd7c/scratch"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(SCRATCH_DIR, exist_ok=True)

def generate_single_route_html(r, temp_html_path):
    alert_html = f'<div class="transit-alert">{r["alert"]}</div>' if r.get("alert") else ""
    
    is_super_stops = len(r["stops"]) > 20
    is_many_stops = len(r["stops"]) > 10
    map_height = "195px" if is_super_stops else ("250px" if is_many_stops else "350px")
    card_padding = "10px 18px" if is_super_stops else "16px 20px"
    details_padding = "10px 14px" if is_super_stops else "14px 18px"
    fare_margin = "8px" if is_super_stops else "12px"
    map_margin = "8px" if is_super_stops else "12px"
    series_class = "stop-series two-cols" if is_many_stops else "stop-series"
    
    stops_rows = []
    for s in r["stops"][1:-1]:
        stops_rows.append(f"""
          <div class="stop-row">
            <span class="stop-dot"></span>
            <span class="stop-t">{s["time"]}</span>
            <span>{s["name"]}</span>
          </div>
        """)
    stops_html = "".join(stops_rows)

    stops_coords = [[s["coord"][0], s["coord"][1]] for s in r["stops"]]
    import json
    stops_json = json.dumps(stops_coords)

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="utf-8">
<title>{r['title']}</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
  @page {{
    size: A4 portrait;
    margin: 8mm 10mm;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #202124;
    background: #fff;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
  .page-box {{
    width: 100%;
    max-width: 740px;
    margin: 0 auto;
    background: #fff;
    border: 1px solid #dadce0;
    border-radius: 12px;
    padding: {card_padding};
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  }}
  .route-header-top {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 1px solid #e8eaed;
    padding-bottom: 8px;
    margin-bottom: 10px;
  }}
  .day-hero-badge {{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    flex-shrink: 0;
    white-space: nowrap;
  }}
  .day-hero-num {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Outfit", sans-serif;
    font-size: 28px;
    font-weight: 900;
    letter-spacing: -0.5px;
    color: #1a365d;
    line-height: 1;
  }}
  .day-hero-date {{
    display: inline-block;
    margin-top: 5px;
    font-size: 13px;
    font-weight: 700;
    color: #996515;
    background: #fdf7ea;
    border: 1px solid rgba(184, 134, 45, 0.4);
    padding: 2px 8px;
    border-radius: 4px;
    letter-spacing: 0.2px;
    white-space: nowrap;
  }}
  .route-info-col {{
    text-align: right;
  }}
  .route-day-tag {{
    display: inline-block;
    background: #f7eed7;
    color: #8c6a28;
    border: 1px solid rgba(184,134,45,0.3);
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 700;
    margin-bottom: 4px;
  }}
  .route-title-text {{
    font-size: 16px;
    font-weight: 700;
    color: #202124;
  }}
  .route-addr-text {{
    font-size: 11px;
    color: #70757a;
    margin-top: 2px;
  }}
  .route-time-text {{
    font-size: 14px;
    font-weight: 700;
    color: #1a73e8;
    margin-top: 3px;
  }}

  .map-box {{
    width: 100%;
    height: {map_height};
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid #dadce0;
    margin-bottom: {map_margin};
    position: relative;
  }}
  #map {{
    width: 100%;
    height: 100%;
  }}
  .map-credit {{
    position: absolute;
    bottom: 8px;
    right: 8px;
    background: rgba(255,255,255,0.92);
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 10px;
    color: #5f6368;
    z-index: 1000;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2);
  }}

  .details-box {{
    border: 1px solid #dadce0;
    border-radius: 8px;
    padding: {details_padding};
    background: #fff;
  }}
  .fare-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #e8eaed;
    padding-bottom: 8px;
    margin-bottom: {fare_margin};
  }}
  .fare-title {{
    font-size: 13px;
    font-weight: 700;
    color: #202124;
  }}
  .fare-desc {{
    font-size: 11px;
    color: #5f6368;
  }}
  .fare-val {{
    font-size: 14px;
    font-weight: 700;
    color: #188038;
  }}

  .transit-timeline {{
    position: relative;
    padding-left: 26px;
  }}
  .t-node {{
    position: relative;
    padding-bottom: 14px;
  }}
  .t-node:last-child {{
    padding-bottom: 0;
  }}
  .t-pin {{
    position: absolute;
    left: -26px;
    top: 2px;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: #fff;
    border: 3px solid #70757a;
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  .t-pin.start {{
    border-color: #1a73e8;
  }}
  .t-pin.end {{
    border-color: {r['line_color']};
    background: {r['line_color']};
  }}
  .t-pin.end::after {{
    content: '';
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: #fff;
  }}
  .t-line {{
    position: absolute;
    left: -18px;
    top: 18px;
    bottom: -2px;
    width: 3px;
    background: #dadce0;
  }}
  .t-line.transit-active {{
    background: {r['line_color']};
  }}

  .t-header {{
    display: flex;
    align-items: baseline;
    gap: 8px;
  }}
  .t-time {{
    font-size: 13px;
    font-weight: 700;
    color: #202124;
    min-width: 50px;
  }}
  .t-name {{
    font-size: 13px;
    font-weight: 700;
    color: #202124;
  }}
  .t-addr {{
    font-size: 11px;
    color: #70757a;
    margin-top: 1px;
    margin-left: 58px;
  }}

  .transit-card-inner {{
    margin: 8px 0 8px 58px;
    padding: 10px 14px;
    background: #f8f9fa;
    border-radius: 6px;
    border-left: 4px solid {r['line_color']};
  }}
  .badge-transit {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: {r['line_color']};
    color: #fff;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 700;
  }}
  .transit-meta {{
    font-size: 12px;
    font-weight: 600;
    color: #3c4043;
    margin-top: 5px;
  }}
  .transit-op {{
    font-size: 11px;
    color: #70757a;
    margin-top: 2px;
  }}
  .transit-alert {{
    margin-top: 6px;
    padding: 5px 8px;
    background: #fef7e0;
    border: 1px solid #f9ab00;
    border-radius: 4px;
    font-size: 11px;
    color: #b06000;
  }}

  .stop-series {{
    margin: 6px 0 0 58px;
    border-left: 2px solid #dadce0;
    padding-left: 12px;
  }}
  .stop-series.two-cols {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2px 14px;
    padding-left: 10px;
  }}
  .stop-row {{
    font-size: 10px;
    color: #5f6368;
    margin-bottom: 2px;
    display: flex;
    gap: 6px;
    align-items: center;
  }}
  .stop-dot {{
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: #70757a;
  }}
  .stop-t {{
    color: #80868b;
    min-width: 40px;
  }}

  .footer-url {{
    margin-top: 12px;
    padding-top: 8px;
    border-top: 1px solid #e8eaed;
    font-size: 10px;
    color: #1a73e8;
    display: flex;
    justify-content: space-between;
    word-break: break-all;
  }}
</style>
</head>
<body>
<div class="page-box">
  <div class="route-header-top">
    <div class="day-hero-badge">
      <div class="day-hero-num">{r['day']}</div>
      <div class="day-hero-date">{r['date']}</div>
    </div>
    <div class="route-info-col">
      <span class="route-day-tag">{r['day_badge']}</span>
      <div class="route-title-text">{r['title']}</div>
      <div class="route-addr-text">{r['origin_addr'][:30]}... 至 {r['dest_addr'][:30]}...</div>
      <div class="route-time-text">{r['dep_time']} - {r['arr_time']}（{r['duration']}）</div>
    </div>
  </div>

  <div class="map-box">
    <div id="map"></div>
    <div class="map-credit">地圖資料 &copy; OpenStreetMap | 路線規劃：{r['duration']}</div>
  </div>

  <div class="details-box">
    <div class="fare-row">
      <div>
        <div class="fare-title">{r['ticket_title']}</div>
        <div class="fare-desc">{r['ticket_sub']}</div>
      </div>
      <div class="fare-val">{r['ticket_price']}</div>
    </div>

    <div class="transit-timeline">
      <div class="t-node">
        <div class="t-pin start"></div>
        <div class="t-line"></div>
        <div class="t-header">
          <span class="t-time">{r['dep_time']}</span>
          <span class="t-name">{r['origin_name']}</span>
        </div>
        <div class="t-addr">{r['origin_addr']}</div>
      </div>

      <div class="t-node">
        <div class="t-pin" style="border-color: {r['line_color']}; background: {r['line_color']};"></div>
        <div class="t-line transit-active"></div>
        <div class="t-header">
          <span class="t-time">{r['dep_time']}</span>
          <span class="t-name">搭乘 {r['transit_badge']}</span>
        </div>
        <div class="transit-card-inner">
          <span class="badge-transit">{r['transit_badge']}</span>
          <div class="transit-meta">{r['duration']} · 營運單位：{r['operator']}</div>
          <div class="transit-op">{r['operator_note']}</div>
          {alert_html}
        </div>

        <div class="{series_class}">
          {stops_html}
        </div>
      </div>

      <div class="t-node">
        <div class="t-pin end"></div>
        <div class="t-header">
          <span class="t-time">{r['arr_time']}</span>
          <span class="t-name">抵達：{r['dest_name']}</span>
        </div>
        <div class="t-addr">{r['dest_addr']}</div>
      </div>
    </div>

    <div class="footer-url">
      <span>導航連結：{r['gmaps_url']}</span>
      <span>1/1</span>
    </div>
  </div>
</div>

<script>
  var stops = {stops_json};
  var map = L.map('map', {{
    zoomControl: false,
    attributionControl: false
  }});

  var tiles = L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
    maxZoom: 18,
    attribution: 'OpenStreetMap'
  }}).addTo(map);

  var poly = L.polyline(stops, {{
    color: '{r['line_color']}',
    weight: 6,
    opacity: 0.9,
    lineCap: 'round',
    lineJoin: 'round'
  }}).addTo(map);

  map.fitBounds(poly.getBounds(), {{
    padding: [40, 40], maxZoom: 15
  }});

  // Start Marker
  L.circleMarker(stops[0], {{
    radius: 8,
    color: '#1a73e8',
    fillColor: '#fff',
    fillOpacity: 1,
    weight: 3
  }}).addTo(map);

  // End Marker
  L.circleMarker(stops[stops.length - 1], {{
    radius: 8,
    color: '{r['line_color']}',
    fillColor: '{r['line_color']}',
    fillOpacity: 1,
    weight: 3
  }}).addTo(map);

  // Intermediate markers
  for (var i = 1; i < stops.length - 1; i++) {{
    L.circleMarker(stops[i], {{
      radius: 4,
      color: '{r['line_color']}',
      fillColor: '#fff',
      fillOpacity: 1,
      weight: 2
    }}).addTo(map);
  }}
</script>
</body>
</html>
"""
    with open(temp_html_path, "w", encoding="utf-8") as f:
        f.write(html)

from build_all_routes import ROUTES_DATA, ROUTE_PDF_MAPPING

def export_all():
    generated_pdfs = []
    print(f"Total routes to export: {len(ROUTES_DATA)}")

    for idx, r in enumerate(ROUTES_DATA):
        num_str = f"{idx+1:02d}"
        pdf_name = ROUTE_PDF_MAPPING.get(r['id'], f"{num_str}_{r['id']}.pdf")
        pdf_path = os.path.join(OUTPUT_DIR, pdf_name)
        temp_html = os.path.join(SCRATCH_DIR, f"temp_{num_str}.html")

        generate_single_route_html(r, temp_html)

        cmd = [
            CHROME_BIN,
            "--headless",
            "--disable-gpu",
            "--virtual-time-budget=3500",
            f"--print-to-pdf={pdf_path}",
            temp_html
        ]

        print(f"[{idx+1}/{len(ROUTES_DATA)}] Generating {os.path.basename(pdf_path)}...")
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15)
            if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 1000:
                print(f"  ✓ Success: {os.path.getsize(pdf_path):,} bytes")
                generated_pdfs.append(pdf_path)
            else:
                print(f"  ✗ Failed to create {pdf_path}: {res.stderr.decode('utf-8')[:200]}")
        except Exception as e:
            print(f"  ✗ Exception: {e}")

    # Also merge all into all_routes.pdf
    if generated_pdfs:
        merged_pdf_path = os.path.join(OUTPUT_DIR, "all_routes.pdf")
        print(f"\nMerging {len(generated_pdfs)} route PDFs into {merged_pdf_path}...")
        merged_doc = fitz.open()
        for p in generated_pdfs:
            doc = fitz.open(p)
            merged_doc.insert_pdf(doc)
        merged_doc.save(merged_pdf_path)
        print(f"✓ Created {merged_pdf_path} ({os.path.getsize(merged_pdf_path):,} bytes, {len(merged_doc)} pages)")

if __name__ == "__main__":
    export_all()
