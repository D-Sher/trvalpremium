#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Galilee Tours Travel Agency Style Generator for print-handbook.html
Re-architects the handbook to match the exact Galileo Tours (加利利旅行社) brochure style
"""

# Reusable SVG Icons
ICON_CLOCHE = '''<svg class="galilee-spec-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 4a2 2 0 0 0-2 2h4a2 2 0 0 0-2-2zM3 17h18a1 1 0 0 1 1 1v1H2v-1a1 1 0 0 1 1-1zm1-2a8 8 0 0 1 16 0H4z"/></svg>'''
ICON_HOTEL = '''<svg class="galilee-spec-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 21h18M5 21V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16M9 7h2M9 11h2M9 15h2M13 7h2M13 11h2M13 15h2"/></svg>'''
ICON_INCLUDED = '''<svg class="galilee-spec-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/><polygon points="12,11 13.5,14 17,14.5 14.5,17 15,20.5 12,18.8 9,20.5 9.5,17 7,14.5 10.5,14" fill="#b8862d" stroke="none"/></svg>'''

ICON_TRAIN = '''<svg class="galilee-timeline-icon" viewBox="0 0 24 24"><path d="M12 2c-4.4 0-8 .6-8 4v10a3 3 0 0 0 3 3l-1.5 1.5V21h13v-.5L17 19a3 3 0 0 0 3-3V6c0-3.4-3.6-4-8-4zm-6 4a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v4H6V6zm2 10a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm8 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3z"/></svg>'''
ICON_BUS = '''<svg class="galilee-timeline-icon" viewBox="0 0 24 24"><path d="M4 16V6a3 3 0 0 1 3-3h10a3 3 0 0 1 3 3v10a2 2 0 0 1-2 2v2a1 1 0 0 1-1 1h-1a1 1 0 0 1-1-1v-2H9v2a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1v-2a2 2 0 0 1-2-2zm2-8h12V6a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1v2zm0 2v4h12v-4H6zm1.5 5.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3zm11 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3z"/></svg>'''
ICON_FERRY = '''<svg class="galilee-timeline-icon" viewBox="0 0 24 24"><path d="M20 21c-1.4 0-2.5-.6-3.4-1.5-.9.9-2 1.5-3.4 1.5s-2.5-.6-3.4-1.5c-.9.9-2 1.5-3.4 1.5-1.4 0-2.5-.6-3.4-1.5L2 20.3V18c.8.6 1.9 1 3 1s2.2-.4 3-1c.8.6 1.9 1 3 1s2.2-.4 3-1c.8.6 1.9 1 3 1s2.2-.4 3-1l1 .7V20c-.9.6-2 1-3 1zM4.5 15.5l1.8-7.5H11v-4h2v4h4.7l1.8 7.5c-.8-.3-1.6-.5-2.5-.5-1.4 0-2.5.5-3.5 1.3-.9-.8-2-1.3-3.5-1.3-.9 0-1.7.2-2.5.5z"/></svg>'''
ICON_MEAL = '''<svg class="galilee-timeline-icon" viewBox="0 0 24 24"><path d="M11 2v9a2 2 0 0 1-2 2H8v9H6v-9H5a2 2 0 0 1-2-2V2h2v6h1V2h2v6h1V2h1zm7 0a4 4 0 0 1 4 4v5a2 2 0 0 1-2 2h-1v9h-2v-9h-1a2 2 0 0 1-2-2V6a4 4 0 0 1 4-4z"/></svg>'''
ICON_SIGHT = '''<svg class="galilee-timeline-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" fill="none" stroke="#000" stroke-width="2"/><circle cx="12" cy="12" r="4" fill="#000"/></svg>'''
ICON_PLANE = '''<svg class="galilee-timeline-icon" viewBox="0 0 24 24"><path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z"/></svg>'''
ICON_SHOP = '''<svg class="galilee-timeline-icon" viewBox="0 0 24 24"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4H6zm10 8a4 4 0 0 1-8 0" fill="none" stroke="#000" stroke-width="2"/></svg>'''
ICON_HOTEL_NODE = '''<svg class="galilee-timeline-icon" viewBox="0 0 24 24"><path d="M19 7h-8v8H3V5H1v15h2v-3h18v3h2v-9a4 4 0 0 0-4-4zm-12 6a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/></svg>'''

def build_timeline(nodes):
    """
    nodes: list of dicts with:
      icon: SVG string
      time: "09:30"
      label: "開通通票"
      dur: "搭乘M3地鐵" (optional)
    """
    items_html = []
    for n in nodes:
        dur_html = f'<div class="galilee-t-dur">{n.get("dur", "")}</div>' if n.get("dur") else ''
        items_html.append(f'''
        <div class="galilee-timeline-node">
          <div class="galilee-t-icon-box">{n['icon']}</div>
          <div class="galilee-t-time">{n['time']}</div>
          <div class="galilee-t-label">{n['label']}</div>
          {dur_html}
        </div>''')
    
    return f'''
      <div class="galilee-timeline-wrap">
        <div class="galilee-timeline-track"></div>
        <div class="galilee-timeline-nodes">
          {''.join(items_html)}
        </div>
      </div>'''

def build_footer_specs(b_lunch_dinner, hotel, included):
    return f'''
      <div class="galilee-spec-footer">
        <div class="galilee-spec-cell">
          {ICON_CLOCHE}
          <div class="galilee-spec-body">
            <div><strong>早餐：</strong>{b_lunch_dinner[0]}</div>
            <div><strong>午餐：</strong>{b_lunch_dinner[1]}</div>
            <div><strong>晚餐：</strong>{b_lunch_dinner[2]}</div>
          </div>
        </div>
        <div class="galilee-spec-cell">
          {ICON_HOTEL}
          <div class="galilee-spec-body">
            <div>{hotel}</div>
          </div>
        </div>
        <div class="galilee-spec-cell">
          {ICON_INCLUDED}
          <div class="galilee-spec-body">
            <div><strong>【團費包含】</strong>{included}</div>
          </div>
        </div>
      </div>'''

def build_page_footer(page_num):
    return f'''
      <div class="page-footer">
        <span class="page-footer-brand">TRAVEL EURO · 隨身慢活手冊</span>
        <span class="page-footer-num">{page_num:02d}</span>
      </div>'''

print("Helper functions ready.")
