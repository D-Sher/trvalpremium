#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Galilee Tours Travel Agency Style Generator for print-handbook.html
Complete 20-Page A5 Travel Handbook Builder (Refined Edition)
"""

import os
from generate_galilee_parts import (
    ICON_CLOCHE, ICON_HOTEL, ICON_INCLUDED,
    ICON_TRAIN, ICON_BUS, ICON_FERRY, ICON_MEAL,
    ICON_SIGHT, ICON_PLANE, ICON_SHOP, ICON_HOTEL_NODE,
    build_timeline, build_footer_specs, build_page_footer
)

def generate_handbook():
    print("Generating refined Galilee-style print-handbook.html...")
    
    html = []
    
    # 1. HTML Header & CSS
    html.append('''<!DOCTYPE html>
<html lang="zh-Hant">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>義大利 × 南法蔚藍海岸 15 日 · 隨身旅行備忘行程手冊 (加利利旅行社旗艦級 A5 列印版)</title>
  <meta name="description" content="加利利旅行社風格 · 義大利 × 南法蔚藍海岸 15 日熟齡慢活奢選手冊">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link
    href="https://fonts.googleapis.com/css2?family=Dorsa&family=Noto+Sans+TC:wght@300;400;500;700&family=Noto+Serif+TC:wght@400;500;600;700&family=Cinzel:wght@500;600;700&display=swap"
    rel="stylesheet">
  <style>
    /* ==========================================================================
       GALILEE TOURS SIGNATURE A5 DESIGN SYSTEM
       尺寸：標準 A5 直式 (148mm × 210mm)
       色彩：加利利經典深林綠 (#003000) × 典雅暖白 × 金緻點綴
       ========================================================================== */
    :root {
      --galilee-green: #003000;         /* 加利利官方 PDF 經典綠 rgb(0, 48, 0) */
      --galilee-green-dark: #072010;
      --galilee-green-tint: #edf4ef;
      --galilee-gold: #b8862d;
      --galilee-gold-light: #fbf6ec;
      --galilee-paper: #ffffff;
      --galilee-paper-warm: #faf8f5;
      --galilee-text: #222222;
      --galilee-text-muted: #555555;
      --galilee-border: #e2e8f0;
      --galilee-line: #2b2b2b;
    }

    * {
      box-sizing: border-box;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }

    body {
      margin: 0;
      padding: 0;
      background: #ecefe9;
      color: var(--galilee-text);
      font-family: "Noto Sans TC", "Microsoft JhengHei", system-ui, sans-serif;
      font-size: 8.5pt;
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
    }

    h1, h2, h3, h4 {
      font-family: "Noto Serif TC", "Songti TC", serif;
      color: var(--galilee-green);
      margin: 0;
      line-height: 1.25;
    }

    /* 頂部操作控制列 */
    .screen-toolbar {
      position: sticky;
      top: 0;
      z-index: 999;
      background: #003000;
      color: #fff;
      padding: 12px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      box-shadow: 0 4px 16px rgba(0,0,0,.25);
      border-bottom: 2px solid var(--galilee-gold);
    }
    .toolbar-title {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .toolbar-title h2 {
      font-size: 15px;
      color: #fff;
      font-weight: 600;
      font-family: "Noto Sans TC", sans-serif;
    }
    .toolbar-title span {
      background: var(--galilee-gold);
      color: #003000;
      font-size: 11px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 4px;
    }
    .toolbar-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .btn-print {
      background: linear-gradient(135deg, #dfb259 0%, #b8862d 100%);
      color: #003000;
      border: none;
      padding: 8px 18px;
      border-radius: 6px;
      font-weight: 700;
      font-size: 13px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 2px 8px rgba(0,0,0,.2);
      transition: all .2s ease;
    }
    .btn-print:hover {
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(184,134,45,.4);
    }
    .btn-web {
      background: rgba(255,255,255,.12);
      color: #fff;
      text-decoration: none;
      padding: 8px 14px;
      border-radius: 6px;
      font-size: 12px;
      border: 1px solid rgba(255,255,255,.3);
      transition: all .2s;
    }
    .btn-web:hover {
      background: rgba(255,255,255,.2);
    }
    .print-tip {
      font-size: 11.5px;
      color: #e2ede5;
      background: rgba(0,0,0,.3);
      padding: 4px 10px;
      border-radius: 4px;
    }

    /* 手冊容器 */
    .handbook-wrapper {
      max-width: 900px;
      margin: 24px auto;
      padding-bottom: 60px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 28px;
    }

    /* A5 頁面主體 (148mm x 210mm) */
    .a5-page {
      width: 148mm;
      min-height: 210mm;
      height: 210mm;
      background: var(--galilee-paper);
      padding: 10mm 10mm 8mm 10mm;
      position: relative;
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
      border-radius: 2px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      page-break-after: always;
      break-after: page;
    }

    /* 頁首 */
    .page-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #e2e8f0;
      padding-bottom: 2.5mm;
      margin-bottom: 2.5mm;
      font-size: 7.2pt;
      color: #777;
      letter-spacing: 0.05em;
    }
    .page-header-title {
      font-weight: 700;
      color: var(--galilee-green);
      display: flex;
      align-items: center;
      gap: 5px;
    }
    .page-header-title::before {
      content: "";
      display: inline-block;
      width: 5px;
      height: 5px;
      background: var(--galilee-gold);
      border-radius: 50%;
    }

    /* 頁尾 */
    .page-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid #eaeaea;
      padding-top: 1.8mm;
      margin-top: auto;
      font-size: 6.5pt;
      color: #777777;
    }
    .page-footer-brand {
      letter-spacing: 0.08em;
      font-weight: 500;
    }
    .page-footer-num {
      font-family: "Noto Serif TC", serif;
      font-weight: 700;
      color: var(--galilee-green);
      background: var(--galilee-green-tint);
      padding: 1px 6px;
      border-radius: 8px;
    }

    .page-content {
      flex: 1;
      display: flex;
      flex-direction: column;
    }

    /* =========================================================================
       加利利每日主標題 (Galilee Day Title)
       ========================================================================= */
    .galilee-day-header {
      display: flex;
      align-items: baseline;
      gap: 10px;
      margin-bottom: 1.5mm;
    }
    .galilee-day-number {
      font-family: 'Dorsa', 'Barlow Condensed', sans-serif;
      font-size: 44pt;
      line-height: 0.82;
      color: var(--galilee-green);
      letter-spacing: 0.02em;
      flex-shrink: 0;
      font-weight: 400;
    }
    .galilee-day-heading-col {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }
    .galilee-day-route-title {
      font-family: "Noto Sans TC", "Microsoft JhengHei", sans-serif;
      font-size: 11.5pt;
      font-weight: 700;
      color: #000000;
      line-height: 1.25;
      margin: 0;
    }
    .galilee-day-sub-bar {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-top: 2px;
    }
    .galilee-day-date {
      font-size: 7.5pt;
      font-weight: 600;
      color: var(--galilee-green);
    }
    .galilee-day-base {
      font-size: 6.8pt;
      color: var(--galilee-gold);
      font-weight: 600;
    }

    /* =========================================================================
       加利利經典橫向時間交通軸 (Galilee Horizontal Timeline)
       ========================================================================= */
    .galilee-timeline-wrap {
      position: relative;
      margin: 1.8mm 0 3.2mm 0;
      padding: 2px 0;
    }
    .galilee-timeline-track {
      position: absolute;
      top: 11px;
      left: 14px;
      right: 14px;
      height: 1.5px;
      background: #2b2b2b;
      z-index: 1;
    }
    .galilee-timeline-nodes {
      position: relative;
      z-index: 2;
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
    }
    .galilee-timeline-node {
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      min-width: 44px;
      max-width: 68px;
    }
    .galilee-t-icon-box {
      width: 22px;
      height: 22px;
      background: #ffffff;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 2px;
    }
    .galilee-timeline-icon {
      width: 16px;
      height: 16px;
      fill: #000000;
    }
    .galilee-t-time {
      font-size: 7.2pt;
      font-weight: 700;
      color: var(--galilee-green);
      line-height: 1.15;
    }
    .galilee-t-label {
      font-size: 6.8pt;
      font-weight: 700;
      color: var(--galilee-green);
      line-height: 1.15;
      margin-top: 1px;
    }
    .galilee-t-dur {
      font-size: 5.8pt;
      color: #555555;
      line-height: 1.15;
    }

    /* =========================================================================
       加利利攝影圖文展示 (Galilee Photography & Narrative)
       ========================================================================= */
    .galilee-photo-grid-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 3mm;
      margin-bottom: 2.2mm;
    }
    .galilee-photo-item {
      display: flex;
      flex-direction: column;
    }
    .galilee-photo-item img {
      width: 100%;
      height: 40mm;
      object-fit: cover;
      border-radius: 2px;
      display: block;
      margin-bottom: 1.8mm;
      box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    .galilee-spot-heading {
      font-size: 8.8pt;
      font-weight: 700;
      color: #000000;
      margin-bottom: 1mm;
      display: flex;
      align-items: baseline;
      gap: 5px;
    }
    .galilee-spot-heading .en {
      font-weight: 400;
      font-size: 7.2pt;
      color: #666666;
    }
    .galilee-spot-desc {
      font-size: 6.6pt;
      line-height: 1.58;
      color: #333333;
      text-align: justify;
    }

    .galilee-sub-feature-box {
      background: #faf9f6;
      border-left: 2.5px solid var(--galilee-green);
      padding: 2mm 3mm;
      border-radius: 0 3px 3px 0;
      margin-bottom: 2mm;
      font-size: 6.6pt;
      line-height: 1.5;
    }
    .galilee-sub-feature-title {
      font-weight: 700;
      color: var(--galilee-green);
      font-size: 7.2pt;
      margin-bottom: 0.8mm;
      display: flex;
      align-items: center;
      gap: 4px;
    }

    /* 雙日合併頁半頁區塊 */
    .galilee-split-day-block {
      margin-bottom: 2mm;
      padding-bottom: 2mm;
    }
    .galilee-split-day-block:first-child {
      border-bottom: 1px dashed #d5dcd6;
    }
    .galilee-split-content {
      display: flex;
      gap: 3mm;
      align-items: center;
      margin-bottom: 1.8mm;
    }
    .galilee-split-content img {
      width: 44mm;
      height: 28mm;
      object-fit: cover;
      border-radius: 2px;
      flex-shrink: 0;
      box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    .galilee-split-text {
      flex: 1;
      font-size: 6.5pt;
      line-height: 1.5;
      color: #333333;
    }

    /* =========================================================================
       加利利底欄三聯表 (Galilee 3-Column Spec Footer)
       ========================================================================= */
    .galilee-spec-footer {
      margin-top: auto;
      border-top: 1px dotted #bbb;
      padding-top: 2.2mm;
      display: grid;
      grid-template-columns: 1.15fr 1.15fr 1.1fr;
      gap: 3mm;
      font-size: 6.1pt;
      line-height: 1.35;
      color: #333333;
    }
    .galilee-spec-cell {
      display: flex;
      gap: 2mm;
      align-items: flex-start;
    }
    .galilee-spec-icon {
      width: 15px;
      height: 15px;
      flex-shrink: 0;
      margin-top: 1px;
      color: var(--galilee-gold);
    }
    .galilee-spec-body {
      flex: 1;
    }
    .galilee-spec-body div {
      margin-bottom: 1px;
    }
    .galilee-spec-body div:last-child {
      margin-bottom: 0;
    }
    .galilee-spec-body strong {
      color: var(--galilee-green);
    }

    /* =========================================================================
       封面與封底 (Cover & Back Cover)
       ========================================================================= */
    .galilee-cover-page {
      background: #faf8f5 !important;
      color: #222 !important;
      padding: 10mm 10mm 0 10mm !important;
      position: relative;
      display: flex;
      flex-direction: column;
    }
    .galilee-cover-top-accent {
      position: absolute;
      top: 0;
      right: 0;
      width: 34mm;
      height: 25mm;
      background: var(--galilee-green);
      z-index: 1;
    }
    .galilee-cover-header {
      position: relative;
      z-index: 2;
      margin-top: 3mm;
      margin-bottom: 3.5mm;
      padding-right: 32mm;
    }
    .galilee-cover-series {
      font-size: 7.2pt;
      font-weight: 700;
      letter-spacing: 0.15em;
      color: var(--galilee-gold);
      margin-bottom: 1.5mm;
      text-transform: uppercase;
    }
    .galilee-cover-title {
      font-family: "Noto Serif TC", "Songti TC", serif;
      font-size: 19.5pt;
      font-weight: 700;
      color: #111111;
      letter-spacing: 0.05em;
      line-height: 1.25;
      margin: 0;
    }
    .galilee-cover-title span.days {
      font-family: 'Dorsa', 'Noto Serif TC', serif;
      font-size: 27pt;
      font-style: italic;
      color: var(--galilee-green);
      margin-left: 3px;
      font-weight: 400;
    }
    .galilee-cover-subtitle {
      font-family: "Noto Serif TC", serif;
      font-size: 8.2pt;
      font-style: italic;
      letter-spacing: 0.18em;
      color: #555555;
      margin-top: 2mm;
      text-transform: uppercase;
    }
    .galilee-cover-main-wrap {
      position: relative;
      z-index: 2;
      display: flex;
      gap: 3.5mm;
      margin-top: 2mm;
      margin-bottom: 2mm;
      height: 96mm;
      max-height: 96mm;
    }
    .galilee-cover-photo-frame {
      flex: 1;
      height: 96mm;
      box-shadow: 0 4px 16px rgba(0,0,0,0.12);
      border: 1px solid rgba(0,0,0,0.06);
      overflow: hidden;
      border-radius: 2px;
    }
    .galilee-cover-photo-frame img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }
    .galilee-cover-sidebar {
      width: 10mm;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      writing-mode: vertical-rl;
      text-orientation: upright;
      font-family: "Noto Serif TC", serif;
      font-size: 7.5pt;
      letter-spacing: 0.18em;
      white-space: nowrap;
      color: #222222;
      font-weight: 600;
      border-left: 1px solid #dfdfdf;
      padding-left: 2.5mm;
      height: 96mm;
      max-height: 96mm;
    }
    .galilee-cover-lead-quote {
      font-family: "Noto Serif TC", serif;
      font-size: 7.2pt;
      color: #555;
      text-align: center;
      margin-top: 1.5mm;
      letter-spacing: 0.12em;
    }
    .galilee-cover-tracking {
      text-align: center;
      letter-spacing: 0.38em;
      font-size: 7.5pt;
      color: #333;
      font-family: "Cinzel", "Noto Serif TC", serif;
      font-weight: 600;
      margin-top: 2mm;
      margin-bottom: 2mm;
      border-top: 1px solid var(--galilee-green);
      padding-top: 1.8mm;
    }
    .galilee-cover-footer-band {
      margin-top: auto;
      margin-left: -10mm;
      margin-right: -10mm;
      background: var(--galilee-green);
      color: #ffffff;
      padding: 3.5mm 10mm;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 5.9pt;
      letter-spacing: 0.05em;
      white-space: nowrap;
    }
    .galilee-cover-brand-logo {
      display: flex;
      align-items: center;
      gap: 6px;
      font-weight: 700;
      font-size: 7.5pt;
    }

    /* 封底專屬樣式 */
    .galilee-back-cover {
      background: var(--galilee-green) !important;
      color: #e2ede5 !important;
      padding: 10mm 11mm !important;
    }
    .galilee-back-cover h3 {
      color: #ffffff !important;
      font-size: 8.5pt;
      margin-bottom: 1.5mm;
      border-bottom: 1px solid rgba(255,255,255,0.25);
      padding-bottom: 1mm;
      letter-spacing: 0.05em;
    }
    .galilee-back-cover p, .galilee-back-cover li {
      font-size: 6.2pt;
      line-height: 1.45;
      color: #d1dfd5;
      margin: 0 0 1.5mm 0;
    }
    .galilee-back-cover ol {
      margin: 0 0 2mm 0;
      padding-left: 3.5mm;
    }

    /* =========================================================================
       通用卡片與表格 (Overview / Guide Pages)
       ========================================================================= */
    .galilee-section-title {
      font-size: 13.5pt;
      font-weight: 700;
      color: #000;
      margin-bottom: 1mm;
      font-family: "Noto Sans TC", sans-serif;
    }
    .galilee-section-sub {
      font-size: 7.5pt;
      color: var(--galilee-text-muted);
      margin-bottom: 3mm;
    }
    .galilee-flight-box {
      border: 1.5px solid var(--galilee-green);
      border-radius: 4px;
      overflow: hidden;
      margin-top: 2.5mm;
    }
    .galilee-flight-head {
      background: var(--galilee-green);
      color: #fff;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 2mm 3.5mm;
      font-size: 7.8pt;
      font-weight: 700;
    }
    .galilee-flight-body {
      padding: 2.5mm 3.5mm;
      font-size: 6.8pt;
      line-height: 1.5;
      background: #fafbf9;
    }
    .galilee-flight-leg {
      display: flex;
      gap: 2mm;
      align-items: baseline;
      margin-bottom: 1mm;
    }
    .galilee-flight-leg strong {
      color: #000;
      width: 48px;
    }

    table.galilee-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 6.8pt;
      margin-bottom: 2.5mm;
    }
    table.galilee-table th {
      background: var(--galilee-green);
      color: #fff;
      padding: 3.5px 5px;
      text-align: left;
      font-weight: 600;
      font-size: 6.5pt;
    }
    table.galilee-table td {
      padding: 3.5px 5px;
      border-bottom: 1px solid #e5ebe7;
      color: #2b2b2b;
    }
    table.galilee-table tr:nth-child(even) td {
      background: #f7faf8;
    }

    /* 飯店卡片 */
    .galilee-hotel-card {
      display: flex;
      gap: 3mm;
      background: #faf8f5;
      border: 1px solid #ebd9b6;
      border-radius: 4px;
      padding: 2.5mm 3mm;
      margin-bottom: 2.5mm;
    }
    .galilee-hotel-card img {
      width: 40mm;
      height: 28mm;
      object-fit: cover;
      border-radius: 3px;
      flex-shrink: 0;
    }
    .galilee-hotel-info {
      flex: 1;
      font-size: 6.4pt;
      line-height: 1.45;
    }
    .galilee-hotel-name {
      font-size: 7.8pt;
      font-weight: 700;
      color: var(--galilee-green);
      margin-bottom: 1mm;
    }
    .galilee-hotel-card-ask {
      background: #fff;
      border: 1px dashed #d6a34a;
      padding: 1.5mm 2mm;
      border-radius: 3px;
      margin-top: 1.2mm;
      font-size: 6pt;
    }

    /* 列印設定 */
    @media print {
      body {
        background: #fff;
      }
      .screen-toolbar {
        display: none !important;
      }
      .handbook-wrapper {
        margin: 0;
        padding: 0;
        gap: 0;
      }
      .a5-page {
        box-shadow: none;
        border-radius: 0;
        margin: 0;
        width: 148mm;
        height: 210mm;
        page-break-after: always !important;
        break-after: page !important;
      }
      @page {
        size: A5 portrait;
        margin: 0;
      }
    }
  </style>
</head>

<body>

  <!-- 螢幕專用操作控制列 -->
  <header class="screen-toolbar">
    <div class="toolbar-title">
      <h2>義大利 × 南法 15 日 · 加利利旅行社旗艦級 A5 旅行手冊</h2>
      <span>高雅旅行社標準排版</span>
    </div>
    <div class="toolbar-actions">
      <div class="print-tip">💡 列印建議：紙張選「A5」、勾選「背景圖形」、邊界設為「無」</div>
      <button class="btn-print" onclick="window.print()">🖨️ 立即列印 / 存為 A5 PDF</button>
      <a class="btn-web" href="index.html">← 返回完整導覽網頁</a>
    </div>
  </header>

  <div class="handbook-wrapper">
''')
    
    # -------------------------------------------------------------------------
    # PAGE 01: 手冊封面 (Cover Page)
    # -------------------------------------------------------------------------
    html.append('''
    <!-- =========================================================================
         PAGE 01: 手冊封面 (Cover Page)
         ========================================================================= -->
    <div class="a5-page galilee-cover-page">
      <div class="galilee-cover-top-accent"></div>

      <div class="galilee-cover-header">
        <div class="galilee-cover-series">TRAVEL EURO · PRESTIGE COLLECTION 奢選慢活系列</div>
        <h1 class="galilee-cover-title">義大利 × 南法蔚藍海岸<span class="days">15日</span></h1>
        <div class="galilee-cover-subtitle">M i l a n · C o m o · G e n o v a · P o r t o f i n o · N i c e</div>
      </div>

      <div class="galilee-cover-main-wrap">
        <div class="galilee-cover-photo-frame">
          <img src="hero.webp" alt="義大利與南法蔚藍海岸慢活巡禮">
        </div>
        <div class="galilee-cover-sidebar">
          米蘭時尚 · 科莫湖光 · 熱那亞宮殿 · 蔚藍海岸
        </div>
      </div>

      <div class="galilee-cover-lead-quote">
        「以慢活的優雅步伐，漫步北義大城小鎮與南法地中海蔚藍海岸」
      </div>

      <div class="galilee-cover-tracking">
        G A L I L E E &nbsp; T O U R S &nbsp; · &nbsp; 加 利 利 旅 行 社
      </div>

      <div class="galilee-cover-footer-band">
        <div class="galilee-cover-brand-logo">
          <span>🌲</span> GalileoTours 加利利旅行社
        </div>
        <div>台北(02)2717-3188 · 新竹(03)578-5555 · 台中(04)2369-2288 · 高雄(07)586-9355</div>
      </div>
    </div>
''')

    # -------------------------------------------------------------------------
    # PAGE 02: 景點距離參考 & 參考航班 (Mirroring Galileo Page 9)
    # -------------------------------------------------------------------------
    html.append('''
    <!-- =========================================================================
         PAGE 02: 景點距離參考與參考航班
         ========================================================================= -->
    <div class="a5-page">
      <div class="page-header">
        <span class="page-header-title">DISTANCE & FLIGHTS</span>
        <span>景點距離參考 · 參考航班</span>
      </div>

      <div class="page-content">
        <div style="display: flex; gap: 3.5mm; margin-bottom: 2mm;">
          <div style="flex: 1.15;">
            <div class="galilee-section-title" style="font-size: 11pt; margin-bottom: 1.5mm;">景點距離參考</div>
            <div style="font-size: 6.4pt; line-height: 1.6; color: #333;">
              <div>台北 － 米蘭 <strong>直飛 14h35m</strong></div>
              <div>米蘭 － 科莫湖 <strong>50 Km</strong> (火車約 40mins)</div>
              <div>科莫 － 貝爾加莫 <strong>88 Km</strong> (火車約 1h15m)</div>
              <div>米蘭 － 熱那亞 <strong>145 Km</strong> (IC 特快約 1h30m)</div>
              <div>熱那亞 － 菲諾港 <strong>35 Km</strong> (火車 35mins + 景觀步道)</div>
              <div>熱那亞 － 凡蒂米利亞 <strong>155 Km</strong> (海岸鐵路約 2h)</div>
              <div>凡蒂米利亞 － 尼斯 <strong>35 Km</strong> (TER 雙層列車約 50mins)</div>
              <div>尼斯 － 濱海自由城 <strong>8 Km</strong> (火車約 8mins)</div>
              <div>自由城 － 費拉角莊園 <strong>6 Km</strong> (景觀公車約 15mins)</div>
              <div style="margin-top: 1mm; font-weight: 700; color: #000; border-top: 1px dotted #ccc; padding-top: 1mm;">
                行車與鐵道總里程 約 <strong>1,200 Km</strong>
              </div>
            </div>
          </div>
          <div style="flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center;">
            <img src="rmap.webp" alt="路線地圖" style="width: 100%; height: 50mm; object-fit: contain; border-radius: 3px; border: 1px solid #e2e8f0;">
          </div>
        </div>

        <!-- 參考航班 -->
        <div class="galilee-flight-box">
          <div class="galilee-flight-head">
            <span>✈️ 參考航班</span>
            <span style="background: rgba(255,255,255,0.2); padding: 1px 8px; border-radius: 10px;">長榮航空 / 中華航空 / 歐亞聯營</span>
          </div>
          <div class="galilee-flight-body">
            <div class="galilee-flight-leg">
              <strong>去程航班</strong>
              <span>BR095 TPE/MXP 台北桃園 ➔ 米蘭馬爾彭薩 23:15 / 07:50+1日 (直飛 14h35m)</span>
            </div>
            <div class="galilee-flight-leg">
              <strong>回程航班</strong>
              <span>BR096 MXP/TPE (或 NCE/DXB/TPE) 11:00 / 06:15+1日 (飛行時數約 12h10m)</span>
            </div>
            <div style="font-size: 5.8pt; color: var(--galilee-green); margin-top: 1mm; font-style: italic;">
              (以上為參考航班資訊，實際航班時間及航站轉機點以行前說明會手冊為最終確認。)
            </div>
          </div>
        </div>

        <!-- 緊急海外支援卡 -->
        <div style="margin-top: 2.2mm; background: #faf9f6; border-left: 2.5px solid var(--galilee-gold); padding: 2mm 3mm; border-radius: 0 3px 3px 0; font-size: 6.2pt; line-height: 1.45;">
          <div style="font-weight: 700; color: var(--galilee-green); margin-bottom: 0.8mm;">駐外單位與 24H 海外急難救助專線</div>
          <div><strong>駐義大利台北代表處：</strong>+39-06-9826-2800 / 急難專線 +39-366-806-6434 (義大利境內撥打 366-806-6434)</div>
          <div><strong>駐普羅旺斯台北辦事處：</strong>+33-4-1364-3620 / 急難專線 +33-7-6114-1520 (南法尼斯、普羅旺斯轄區)</div>
          <div><strong>外交部旅外國人急難救助全球免付費專線：</strong>00-800-0885-0885</div>
        </div>

        <!-- 熟齡樂活節奏安心叮嚀 -->
        <div style="margin-top: 2mm; background: var(--galilee-green-tint); border: 1px solid #c7decb; padding: 1.8mm 2.5mm; border-radius: 3px; font-size: 6pt; line-height: 1.4; color: #1e3d24;">
          <strong>🌿 熟齡慢活貼心節奏：</strong>全程嚴選三大核心城市連住（米蘭 4 晚、熱那亞 3 晚、尼斯 5 晚），每日單一路線深度漫遊，每日步數控制於 6,000~8,000 步以內，留足午後咖啡小憩與自由散策時光。
        </div>
      </div>

      ''' + build_page_footer(2) + '''
    </div>
''')

    # -------------------------------------------------------------------------
    # PAGE 03: 璀璨星月荏苒 高雅格調飯店 (Mirroring Galileo Page 7)
    # -------------------------------------------------------------------------
    html.append('''
    <!-- =========================================================================
         PAGE 03: 璀璨星月荏苒 高雅格調飯店
         ========================================================================= -->
    <div class="a5-page">
      <div class="page-header">
        <span class="page-header-title">PRESTIGE HOTELS</span>
        <span>璀璨星月 · 高雅格調飯店</span>
      </div>

      <div class="page-content">
        <div class="galilee-section-title" style="font-size: 11pt; margin-bottom: 0.5mm;">璀璨星月荏苒 高雅格調飯店</div>
        <div class="galilee-section-sub" style="margin-bottom: 2mm;">貼心提醒：若客滿或休息，將安排同級飯店，敬請知悉。</div>

        <!-- 飯店 1: 米蘭 -->
        <div class="galilee-hotel-card">
          <img src="hotel-milan.webp" alt="Hilton Milan">
          <div class="galilee-hotel-info">
            <div class="galilee-hotel-name">4星 Hilton Milan 米蘭希爾頓酒店 <span style="font-size:6pt; color:var(--galilee-gold);">【連住 4 晚】</span></div>
            <div>位於米蘭中央車站旁步行 3 分鐘，省去大件行李搬運之苦。挑高奢華大廳與靜謐隔音客房，享受純義式舒雅生活。</div>
            <div class="galilee-hotel-card-ask">
              <strong>義大利文問路卡：</strong><br>
              "Per favore, mi può indicare la strada per l'hotel Hilton Milan vicino alla Stazione Centrale? (Via Luigi Galvani 12)"
            </div>
          </div>
        </div>

        <!-- 飯店 2: 熱那亞 -->
        <div class="galilee-hotel-card">
          <img src="hotel-genova.webp" alt="Grand Hotel Savoia">
          <div class="galilee-hotel-info">
            <div class="galilee-hotel-name">5星 Grand Hotel Savoia 熱那亞薩伏亞大飯店 <span style="font-size:6pt; color:var(--galilee-gold);">【連住 3 晚】</span></div>
            <div>始於 1897 年的百年旗艦五星飯店，鄰近熱那亞王宮。大理石雕花拱廊與頂樓露天水療，坐擁地中海海港璀璨夜景。</div>
            <div class="galilee-hotel-card-ask">
              <strong>義大利文問路卡：</strong><br>
              "Mi scusi, sto cercando il Grand Hotel Savoia a Piazza Principe. Può aiutarmi? (Via Arsenale di Terra 5)"
            </div>
          </div>
        </div>

        <!-- 飯店 3: 尼斯 -->
        <div class="galilee-hotel-card" style="margin-bottom: 0;">
          <img src="hotel-nice.webp" alt="Le Méridien Nice">
          <div class="galilee-hotel-info">
            <div class="galilee-hotel-name">4-5星 Le Méridien Nice 尼斯艾美酒店 <span style="font-size:6pt; color:var(--galilee-gold);">【連住 5 晚】</span></div>
            <div>座落於著名英國人散步大道 1 號，正對天使灣蔚藍地中海。下樓即是蔚藍海灘與舊城花市，享受南法最愜意的陽光假日時光。</div>
            <div class="galilee-hotel-card-ask">
              <strong>法文問路卡：</strong><br>
              "Excusez-moi, pourriez-vous m'indiquer l'hôtel Le Méridien Nice sur la Promenade des Anglais? (1 Promenade des Anglais)"
            </div>
          </div>
        </div>
      </div>

      ''' + build_page_footer(3) + '''
    </div>
''')

    # -------------------------------------------------------------------------
    # PAGE 04: 特選鐵路列車 榮賞蔚藍海岸 (Mirroring Galileo Page 3)
    # -------------------------------------------------------------------------
    html.append('''
    <!-- =========================================================================
         PAGE 04: 特選鐵路列車 榮賞蔚藍海岸
         ========================================================================= -->
    <div class="a5-page">
      <div class="page-header">
        <span class="page-header-title">SCENIC RAILWAYS</span>
        <span>特選鐵路列車 · 榮賞蔚藍海岸</span>
      </div>

      <div class="page-content">
        <div class="galilee-section-title" style="font-size: 11pt; margin-bottom: 0.5mm;">特選鐵路列車 榮賞蔚藍海岸</div>
        <div class="galilee-section-sub" style="margin-bottom: 2mm;">穿越阿爾卑斯南麓湖泊與地中海海岸線 · 體驗歐洲鐵道慢活巡禮</div>

        <table class="galilee-table">
          <thead>
            <tr>
              <th>列車種類</th>
              <th>搭乘區間</th>
              <th>參考時刻</th>
              <th>車程</th>
              <th>特色與搭乘注意事項</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>馬爾彭薩快線</strong></td>
              <td>MXP 機場 ➔ 米蘭中央車站</td>
              <td>08:35 / 09:05</td>
              <td>約 50 分</td>
              <td>直達無須轉乘，車廂寬敞設有大型行李架</td>
            </tr>
            <tr>
              <td><strong>倫巴底大區鐵路</strong></td>
              <td>米蘭 ➔ 貝爾加莫古城</td>
              <td>09:05 ➔ 09:53</td>
              <td>約 48 分</td>
              <td>二等車廂寬敞，近郊田園風光，持通票直接上車</td>
            </tr>
            <tr>
              <td><strong>科莫湖全景火車</strong></td>
              <td>米蘭 ➔ 瓦倫納 Varenna</td>
              <td>09:20 ➔ 10:23</td>
              <td>約 63 分</td>
              <td>行駛於科莫湖東岸，左側座位飽覽湖光山色</td>
            </tr>
            <tr>
              <td><strong>Intercity 海岸特快</strong></td>
              <td>米蘭 ➔ 熱那亞王子廣場</td>
              <td>09:10 ➔ 10:44</td>
              <td>約 94 分</td>
              <td>一等座席，專屬行李放置空間，穿越亞平寧山脈</td>
            </tr>
            <tr>
              <td><strong>海岸觀景渡輪</strong></td>
              <td>聖馬格利塔 ➔ 菲諾港</td>
              <td>10:30 ➔ 10:45</td>
              <td>約 15 分</td>
              <td>雙層觀景渡輪，從海上欣賞菲諾港粉彩明珠全景</td>
            </tr>
            <tr>
              <td><strong>TER 雙層海岸列車</strong></td>
              <td>凡蒂米利亞 ➔ 尼斯 Nice</td>
              <td>11:50 ➔ 12:42</td>
              <td>約 52 分</td>
              <td>上層全景大窗，緊貼地中海峭壁海天一色馳騁</td>
            </tr>
          </tbody>
        </table>

        <div style="background: #faf9f6; border: 1px solid #e2e8f0; border-radius: 4px; padding: 2.2mm 3mm; font-size: 6.3pt; line-height: 1.48; color: #333; margin-bottom: 2mm;">
          <div style="font-weight: 700; color: var(--galilee-green); margin-bottom: 0.8mm; font-size: 7.2pt;">
            🚄 熟齡搭車安心指南
          </div>
          <div><strong>1. 大件行李安置：</strong>搭乘 Intercity 或跨國列車時，每節車廂前後均設有專用大件行李架，貴重物品與護照證件請隨身放置於防扒胸包。</div>
          <div><strong>2. 實體票打票規定：</strong>義大利搭乘區間車（Regionale）前，請務必於月台綠白色打票機（Convalidatrice）打印戳印；持電子票或通票者請出示手機 QR Code 供查票員掃描。</div>
          <div><strong>3. 靜音車廂禮儀：</strong>歐洲一等車廂與景觀列車多倡導安靜環境，手機請調整為震動，談話輕聲細語，細細品味窗外如詩美景。</div>
        </div>

        <div style="background: #fdfbf7; border-left: 2.5px solid var(--galilee-gold); padding: 1.8mm 2.5mm; border-radius: 0 3px 3px 0; font-size: 6pt; line-height: 1.35; color: #444;">
          <strong>車站無障礙與洗手間指引：</strong>米蘭中央車站、熱那亞王子廣場與尼斯車站均設有無障礙電梯與收費洗手間（約 €1.00，支援無接觸感應信用卡刷卡），請於轉乘時間寬裕時利用。
        </div>
      </div>

      ''' + build_page_footer(4) + '''
    </div>
''')

    # -------------------------------------------------------------------------
    # PAGE 05: 精選 6 大城市通票與門票特選 (Mirroring Galileo Page 4)
    # -------------------------------------------------------------------------
    html.append('''
    <!-- =========================================================================
         PAGE 05: 精選 6 大城市通票與門票特選
         ========================================================================= -->
    <div class="a5-page">
      <div class="page-header">
        <span class="page-header-title">CITY PASSES & TICKETS</span>
        <span>精選 6 大城市通票 · 門票特選</span>
      </div>

      <div class="page-content">
        <div class="galilee-section-title" style="font-size: 11pt; margin-bottom: 0.5mm;">精選 6 大城市通票與門票特選</div>
        <div class="galilee-section-sub" style="margin-bottom: 2mm;">隨身出示 · 免去長者排隊購票之苦 · 暢行無阻</div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2.5mm; margin-bottom: 2mm;">
          <div style="background: #faf8f5; border: 1px solid #ebd9b6; border-radius: 4px; padding: 2mm 2.5mm; font-size: 6.3pt; line-height: 1.45;">
            <div style="font-weight: 700; color: var(--galilee-green); font-size: 7.2pt; margin-bottom: 0.8mm;">★ 米蘭 24h 城市地鐵交通卡</div>
            <div>包含 M1-M5 地鐵、復古 1 號路面電車及市區公車無限次搭乘。進出站感應閘門即可，無須每次掏錢買票。</div>
          </div>
          <div style="background: #faf8f5; border: 1px solid #ebd9b6; border-radius: 4px; padding: 2mm 2.5mm; font-size: 6.3pt; line-height: 1.45;">
            <div style="font-weight: 700; color: var(--galilee-green); font-size: 7.2pt; margin-bottom: 0.8mm;">★ 倫巴底大區鐵路 3 日通票</div>
            <div>自由搭乘 Trenord 倫巴底全區鐵路、科莫湖接駁火車與貝爾加莫百年登山纜車，專為深度慢活旅客量身規劃。</div>
          </div>
          <div style="background: #faf8f5; border: 1px solid #ebd9b6; border-radius: 4px; padding: 2mm 2.5mm; font-size: 6.3pt; line-height: 1.45;">
            <div style="font-weight: 700; color: var(--galilee-green); font-size: 7.2pt; margin-bottom: 0.8mm;">★ 科莫湖中央湖區渡輪通票</div>
            <div>通行於瓦倫納（Varenna）與貝拉焦（Bellagio）之間，憑票自由上下船，在湖心任由清風拂面、遠眺雪山。</div>
          </div>
          <div style="background: #faf8f5; border: 1px solid #ebd9b6; border-radius: 4px; padding: 2mm 2.5mm; font-size: 6.3pt; line-height: 1.45;">
            <div style="font-weight: 700; color: var(--galilee-green); font-size: 7.2pt; margin-bottom: 0.8mm;">★ 熱那亞 Rolli 宮殿博物館聯票</div>
            <div>專屬通行紅宮（Palazzo Rosso）、白宮（Palazzo Bianco）等聯合國教科文組織認證之文藝復興宮殿群。</div>
          </div>
          <div style="background: #faf8f5; border: 1px solid #ebd9b6; border-radius: 4px; padding: 2mm 2.5mm; font-size: 6.3pt; line-height: 1.45;">
            <div style="font-weight: 700; color: var(--galilee-green); font-size: 7.2pt; margin-bottom: 0.8mm;">★ 尼斯 Lignes d'Azur 輕軌通票</div>
            <div>涵蓋 T1 / T2 現代路面輕軌，直達英國人散步大道、馬賽納廣場、舊城區與尼斯蔚藍海岸國際機場。</div>
          </div>
          <div style="background: #faf8f5; border: 1px solid #ebd9b6; border-radius: 4px; padding: 2mm 2.5mm; font-size: 6.3pt; line-height: 1.45;">
            <div style="font-weight: 700; color: var(--galilee-green); font-size: 7.2pt; margin-bottom: 0.8mm;">★ 羅斯柴爾德花園莊園貴賓門票</div>
            <div>含語音導覽與莊園特展入場，專享費拉角半島九大主題花園之優雅漫步，遠眺純淨地中海無敵海景。</div>
          </div>
        </div>

        <div style="background: #fdfaf3; border-left: 2.5px solid var(--galilee-gold); padding: 1.8mm 2.5mm; border-radius: 0 3px 3px 0; font-size: 6.1pt; line-height: 1.4; color: #444;">
          <strong>票卡遺失應變措施：</strong>各通票均已由旅行社隨行領隊於系統建立數位備份。若實體卡片不慎遺失，請立即告知領隊，將於 15 分鐘內協助重發數位條碼以確保行程順暢。
        </div>
      </div>

      ''' + build_page_footer(5) + '''
    </div>
''')

    # -------------------------------------------------------------------------
    # PAGE 06: 行前須知與行李打包檢查清單
    # -------------------------------------------------------------------------
    html.append('''
    <!-- =========================================================================
         PAGE 06: 行前須知與行李打包檢查清單
         ========================================================================= -->
    <div class="a5-page">
      <div class="page-header">
        <span class="page-header-title">PRE-TRIP & PACKING</span>
        <span>行前須知 · 行李打包清單</span>
      </div>

      <div class="page-content">
        <div class="galilee-section-title" style="font-size: 11pt; margin-bottom: 0.5mm;">出發行前叮嚀與行李清單</div>
        <div class="galilee-section-sub" style="margin-bottom: 2mm;">萬全準備 · 讓旅程安心無憂 · 舒活啟程</div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 3.5mm; margin-bottom: 2mm;">
          <!-- 左欄：行前重要叮嚀 -->
          <div style="font-size: 6.3pt; line-height: 1.5; color: #333;">
            <div style="font-weight: 700; color: var(--galilee-green); font-size: 7.2pt; margin-bottom: 1mm; border-bottom: 1px solid var(--galilee-green); padding-bottom: 0.5mm;">
              📌 出發前重要提醒
            </div>
            <div><strong>1. 氣候與洋蔥穿法：</strong>10 月中旬義大利北部與南法白天約 18~23°C，早晚海風吹拂降至 12~14°C，建議攜帶輕量保暖防風外套與薄圍巾。</div>
            <div><strong>2. 歐盟規格轉接插頭：</strong>義大利與法國均使用「雙圓孔插頭（Type C / L）」，電壓為 220V。飯店多備有 USB 孔，但建議自備萬國轉接頭。</div>
            <div><strong>3. 常備個人藥物：</strong>慢籤慢性病藥物請備足天數＋3日備份，並隨身攜帶處方籤影本，切勿放置於托運行李內。</div>
            <div><strong>4. 防扒竊安全暗袋：</strong>大面額歐元現金與信用卡分開存放，外出時使用貼身防搶腰包或斜背包置於胸前。</div>
          </div>

          <!-- 右欄：行李打包核對清單 -->
          <div style="background: #faf8f5; border: 1px solid #ebd9b6; border-radius: 4px; padding: 2mm 2.5mm; font-size: 6.2pt; line-height: 1.45;">
            <div style="font-weight: 700; color: var(--galilee-green); font-size: 7.2pt; margin-bottom: 1mm; border-bottom: 1px dotted #ccc; padding-bottom: 0.5mm;">
              ✓ 出發前行李確認表
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1mm;">
              <div>[ ] 護照 (效期6個月以上)</div>
              <div>[ ] 電子機票影本</div>
              <div>[ ] 海外突發醫療保單</div>
              <div>[ ] 雙幣信用卡 2 張</div>
              <div>[ ] 歐元小額零錢 (5/10/20)</div>
              <div>[ ] 個人處方藥與胃腸藥</div>
              <div>[ ] 防風保暖外套 / 圍巾</div>
              <div>[ ] 好走的防滑健走鞋</div>
              <div>[ ] 太陽眼鏡 / 防曬帽</div>
              <div>[ ] 保溫水瓶 (隨行補水)</div>
              <div>[ ] 行動電源 (容量合格)</div>
              <div>[ ] 手機充電線與轉接頭</div>
              <div>[ ] 隨身折疊輕便傘</div>
              <div>[ ] 保濕乳液 / 護唇膏</div>
            </div>
          </div>
        </div>

        <div style="background: #faf9f6; border-left: 2.5px solid var(--galilee-green); padding: 1.8mm 2.5mm; border-radius: 0 3px 3px 0; font-size: 6.1pt; line-height: 1.4; color: #444;">
          <strong>航空公司行李額度提醒：</strong>每位旅客享有托運行李 1 件（23 公斤）或商務客艙 2 件（各 32 公斤），手提行李 1 件不超過 7 公斤。液體超過 100ml 者必須托運。
        </div>
      </div>

      ''' + build_page_footer(6) + '''
    </div>
''')

    # -------------------------------------------------------------------------
    # PAGE 07: DAY 01 & DAY 02 · 台北 ➔ 米蘭啟程與初會
    # -------------------------------------------------------------------------
    timeline_d1 = [
        {'icon': ICON_BUS, 'time': '20:00', 'label': '桃園機場集合', 'dur': '領隊協辦登機'},
        {'icon': ICON_PLANE, 'time': '23:15', 'label': '班機啟航', 'dur': '長榮/義法聯營'},
        {'icon': ICON_MEAL, 'time': '00:30', 'label': '機上美饌', 'dur': '夜間平穩巡航'},
        {'icon': ICON_HOTEL_NODE, 'time': '02:00', 'label': '雲端歇息', 'dur': '迎接晨曦'}
    ]
    timeline_d2 = [
        {'icon': ICON_PLANE, 'time': '07:50', 'label': '抵達米蘭', 'dur': '馬爾彭薩機場'},
        {'icon': ICON_TRAIN, 'time': '09:30', 'label': '快線特快', 'dur': '直達中央車站'},
        {'icon': ICON_HOTEL_NODE, 'time': '10:30', 'label': '飯店寄行李', 'dur': '希爾頓米蘭'},
        {'icon': ICON_SIGHT, 'time': '14:00', 'label': '歌劇院巡禮', 'dur': '史卡拉廣場'},
        {'icon': ICON_MEAL, 'time': '18:30', 'label': '主廚晚餐', 'dur': '義式迎賓晚宴'}
    ]

    html.append('''
    <!-- =========================================================================
         PAGE 07: DAY 01 & DAY 02
         ========================================================================= -->
    <div class="a5-page">
      <div class="page-header">
        <span class="page-header-title">DAY 01 & 02 · TPE ➔ MILANO</span>
        <span>台北啟航 ➔ 抵達米蘭</span>
      </div>

      <div class="page-content">
        <!-- DAY 01 -->
        <div class="galilee-split-day-block">
          <div class="galilee-day-header">
            <div class="galilee-day-number">DAY 1</div>
            <div class="galilee-day-heading-col">
              <h2 class="galilee-day-route-title">台北 / 米蘭*國際航空*</h2>
              <div class="galilee-day-sub-bar">
                <span class="galilee-day-date">10/15（四）</span>
                <span class="galilee-day-base">【豪華客機 ‧ 夜宿機上】</span>
              </div>
            </div>
          </div>
          ''' + build_timeline(timeline_d1) + '''
          <div class="galilee-split-content">
            <img src="day01-flight.webp" alt="啟程飛往歐洲">
            <div class="galilee-split-text">
              懷著期盼已久的悠閒心情，於傍晚齊聚桃園國際機場。在專業隨團領隊悉心協助下辦妥登機與行李托運手續，搭乘豪華客機直飛時尚之都米蘭。機上備有個人娛樂系統與精緻熱餐，養精蓄銳，迎接明晨地中海燦爛晨光。
            </div>
          </div>
          ''' + build_footer_specs(['敬請自理', '敬請自理', '機上精緻美饌'], '豪華客機夜宿機上', '★國際線直飛來回機票。') + '''
        </div>

        <!-- DAY 02 -->
        <div class="galilee-split-day-block" style="margin-bottom:0; padding-bottom:0; border-bottom:none;">
          <div class="galilee-day-header">
            <div class="galilee-day-number">DAY 2</div>
            <div class="galilee-day-heading-col">
              <h2 class="galilee-day-route-title">米蘭－馬爾彭薩機場++快線++米蘭中央車站－希爾頓</h2>
              <div class="galilee-day-sub-bar">
                <span class="galilee-day-date">10/16（五）</span>
                <span class="galilee-day-base">【米蘭 · 連住 4 晚（第 1 晚）】</span>
              </div>
            </div>
          </div>
          ''' + build_timeline(timeline_d2) + '''
          <div class="galilee-split-content">
            <img src="day02-malpensa-express.webp" alt="馬爾彭薩快線列車">
            <div class="galilee-split-text">
              班機清晨平安降落米蘭馬爾彭薩國際機場，通關後隨即搭乘馬爾彭薩特快火車輕鬆直達米蘭中央車站，步行 3 分鐘進駐希爾頓酒店寄放行李。午後漫步至史卡拉歌劇院廣場，在百年老樹濃蔭下喝杯義式濃縮咖啡，優雅感受米蘭慢步調。
            </div>
          </div>
          ''' + build_footer_specs(['機上精緻早餐', '米蘭市區義大利麵風味餐', '中央車站主廚迎賓晚餐'], '4星 Hilton Milan 希爾頓酒店或同級', '★馬爾彭薩快線列車票、★行李專人接送服務。') + '''
        </div>
      </div>

      ''' + build_page_footer(7) + '''
    </div>
''')

    # -------------------------------------------------------------------------
    # PAGE 08: DAY 03 · 米蘭經典城市巡遊 (Full Page Feature!)
    # -------------------------------------------------------------------------
    timeline_d3 = [
        {'icon': ICON_BUS, 'time': '09:30', 'label': '開通通票', 'dur': '搭乘M3地鐵'},
        {'icon': ICON_SIGHT, 'time': '10:00', 'label': '米蘭大教堂', 'dur': '哥德式外觀留影'},
        {'icon': ICON_SIGHT, 'time': '11:30', 'label': '艾曼紐迴廊', 'dur': '十九世紀玻璃拱頂'},
        {'icon': ICON_MEAL, 'time': '12:30', 'label': '燉牛膝午餐', 'dur': '番紅花燉飯'},
        {'icon': ICON_TRAIN, 'time': '14:30', 'label': '骨董電車1號', 'dur': '穿越市區花園'},
        {'icon': ICON_MEAL, 'time': '18:30', 'label': '主廚晚餐', 'dur': '米蘭名饌晚宴'}
    ]

    html.append('''
    <!-- =========================================================================
         PAGE 08: DAY 03 · 米蘭經典城市巡遊
         ========================================================================= -->
    <div class="a5-page">
      <div class="page-header">
        <span class="page-header-title">DAY 03 · MILANO CLASSIC</span>
        <span>米蘭經典巡禮</span>
      </div>

      <div class="page-content">
        <div class="galilee-day-header">
          <div class="galilee-day-number">DAY 3</div>
          <div class="galilee-day-heading-col">
            <h2 class="galilee-day-route-title">米蘭－米蘭大教堂*攻頂景觀*－艾曼紐二世迴廊－復古電車－蒙特拿破崙</h2>
            <div class="galilee-day-sub-bar">
              <span class="galilee-day-date">10/17（六）</span>
              <span class="galilee-day-base">【米蘭 · 連住 4 晚（第 2 晚）】</span>
            </div>
          </div>
        </div>

        ''' + build_timeline(timeline_d3) + '''

        <div class="galilee-photo-grid-2">
          <div class="galilee-photo-item">
            <img src="duomo-roof.webp" alt="米蘭大教堂">
            <div class="galilee-spot-heading">
              <span>★ 米蘭大教堂廣場</span>
              <span class="en">Piazza del Duomo</span>
            </div>
            <div class="galilee-spot-desc">
              歷經五百年歲月雕琢的白色大理石尖頂巨著。仰望 135 座大理石尖塔與聖母黃金雕像，漫步於義大利最富盛名的哥德式建築地標，感受純白大理石在陽光下散發的永恆光芒。
            </div>
          </div>

          <div class="galilee-photo-item">
            <img src="day03-galleria.webp" alt="艾曼紐二世迴廊">
            <div class="galilee-spot-heading">
              <span>▲ 艾曼紐二世迴廊</span>
              <span class="en">Galleria Vittorio Emanuele</span>
            </div>
            <div class="galilee-spot-desc">
              被譽為「米蘭的客廳」，擁有十九世紀壯麗的鍛鐵玻璃圓頂與精緻馬賽克地磚。漫步於世界名品旗艦店與百年露天咖啡座之間，品味米蘭貴族優雅的午後時光。
            </div>
          </div>
        </div>

        <div class="galilee-sub-feature-box">
          <div class="galilee-sub-feature-title">
            <span>🚃</span> 百年骨董路面電車 1 號 Tram Storico 1
          </div>
          <div>搭乘自 1928 年穿梭至今的黃色木造經典電車，伴隨復古鈴鐺聲悠然穿梭於米蘭市區，直達林蔭掩映的蒙塔內利花園，沉浸在優雅的綠意芬多精之中。</div>
        </div>

        ''' + build_footer_specs(
            ['飯店內歐式自助', '迴廊餐廳米蘭燉牛膝與番紅花燉飯', '中央車站周邊主廚精選晚宴'],
            '4星 Hilton Milan 希爾頓酒店或同級（連住第 2 晚）',
            '★米蘭 24h 城市通票（含M1-M5地鐵、路面電車無限搭乘）。'
        ) + '''
      </div>

      ''' + build_page_footer(8) + '''
    </div>
''')

    # -------------------------------------------------------------------------
    # PAGE 09: DAY 04 · 貝爾加莫中世紀古城慢遊 (Full Page Feature!)
    # -------------------------------------------------------------------------
    timeline_d4 = [
        {'icon': ICON_TRAIN, 'time': '09:05', 'label': '列車啟程', 'dur': '大區景觀鐵路'},
        {'icon': ICON_TRAIN, 'time': '10:30', 'label': '登山纜車', 'dur': '攀登舊城上城'},
        {'icon': ICON_SIGHT, 'time': '11:00', 'label': '老廣場漫行', 'dur': '科萊奧尼禮拜堂'},
        {'icon': ICON_MEAL, 'time': '12:30', 'label': '古城午餐', 'dur': '波倫塔玉米糕'},
        {'icon': ICON_SIGHT, 'time': '14:30', 'label': '威尼斯城牆', 'dur': '世界遺產綠蔭'},
        {'icon': ICON_TRAIN, 'time': '17:00', 'label': '返回米蘭', 'dur': '希爾頓飯店休憩'}
    ]

    html.append('''
    <!-- =========================================================================
         PAGE 09: DAY 04 · 貝爾加莫中世紀古城慢遊
         ========================================================================= -->
    <div class="a5-page">
      <div class="page-header">
        <span class="page-header-title">DAY 04 · BERGAMO CITTA ALTA</span>
        <span>貝爾加莫古城慢活</span>
      </div>

      <div class="page-content">
        <div class="galilee-day-header">
          <div class="galilee-day-number">DAY 4</div>
          <div class="galilee-day-heading-col">
            <h2 class="galilee-day-route-title">米蘭－貝爾加莫*登山纜車、舊城老廣場、威尼斯城牆*－米蘭</h2>
            <div class="galilee-day-sub-bar">
              <span class="galilee-day-date">10/18（日）</span>
              <span class="galilee-day-base">【米蘭 · 連住 4 晚（第 3 晚）】</span>
            </div>
          </div>
        </div>

        ''' + build_timeline(timeline_d4) + '''

        <div class="galilee-photo-grid-2">
          <div class="galilee-photo-item">
            <img src="day04-bergamo-funicular.webp" alt="貝爾加莫登山纜車">
            <div class="galilee-spot-heading">
              <span>★ 登山纜車 Funicolare</span>
              <span class="en">Bergamo Bassa - Alta</span>
            </div>
            <div class="galilee-spot-desc">
              搭乘擁有百年歷史的橙黃色登山纜車緩緩爬升，穿過中世紀石磚拱門與鬱鬱蔥蔥的山坡花園，將下城平原與遠方阿爾卑斯山脈輪廓盡收眼底。
            </div>
          </div>

          <div class="galilee-photo-item">
            <img src="bergamo.webp" alt="舊城老廣場與城牆">
            <div class="galilee-spot-heading">
              <span>★ 舊城老廣場 & 威尼斯城牆</span>
              <span class="en">Piazza Vecchia</span>
            </div>
            <div class="galilee-spot-desc">
              被建築巨擘柯比意譽為「最完美廣場」，中世紀市政廳與理智宮鐘樓巍然聳立。外圍列入世界文化遺產的威尼斯城牆長達六公里，是漫步賞景的最佳勝地。
            </div>
          </div>
        </div>

        <div class="galilee-sub-feature-box">
          <div class="galilee-sub-feature-title">
            <span>☕</span> 慢活私房推薦：品嚐 Polenta e Osei
          </div>
          <div>在舊城古老石板小巷裡，品嚐貝爾加莫傳統小巧可愛的金黃玉米糕甜點（Polenta e Osei），搭配一杯手沖義式卡布奇諾，享受歐洲仕紳的悠然午後。</div>
        </div>

        ''' + build_footer_specs(
            ['飯店內歐式自助', '山城觀景餐廳玉米糕燉肉風味料理', '米蘭市區義式精選晚宴'],
            '4星 Hilton Milan 希爾頓酒店或同級（連住第 3 晚）',
            '★倫巴底鐵路區間通票、★貝爾加莫登山纜車往返票。'
        ) + '''
      </div>

      ''' + build_page_footer(9) + '''
    </div>
''')

    # -------------------------------------------------------------------------
    # PAGE 10: DAY 05 · 科莫湖雙城慢遊 (Full Page Feature!)
    # -------------------------------------------------------------------------
    timeline_d5 = [
        {'icon': ICON_TRAIN, 'time': '09:20', 'label': '全景列車', 'dur': '行駛湖東鐵路'},
        {'icon': ICON_SIGHT, 'time': '10:30', 'label': '瓦倫納慢行', 'dur': '情人懸空步道'},
        {'icon': ICON_FERRY, 'time': '11:45', 'label': '中央湖區渡輪', 'dur': '湖光山色渡船'},
        {'icon': ICON_MEAL, 'time': '12:30', 'label': '貝拉焦午餐', 'dur': '湖畔鮮魚美饌'},
        {'icon': ICON_SIGHT, 'time': '15:00', 'label': '名邸花園散步', 'dur': '梅爾齊莊園遠眺'},
        {'icon': ICON_TRAIN, 'time': '17:30', 'label': '返回米蘭', 'dur': '整理行囊迎移動'}
    ]

    html.append('''
    <!-- =========================================================================
         PAGE 10: DAY 05 · 科莫湖雙城慢遊
         ========================================================================= -->
    <div class="a5-page">
      <div class="page-header">
        <span class="page-header-title">DAY 05 · LAKE COMO SCENIC</span>
        <span>科莫湖水鄉巡禮</span>
      </div>

      <div class="page-content">
        <div class="galilee-day-header">
          <div class="galilee-day-number">DAY 5</div>
          <div class="galilee-day-heading-col">
            <h2 class="galilee-day-route-title">米蘭－瓦倫納*湖光山色*++科莫湖渡輪++貝拉焦*湖畔花園*－科莫</h2>
            <div class="galilee-day-sub-bar">
              <span class="galilee-day-date">10/19（一）</span>
              <span class="galilee-day-base">【米蘭 · 連住 4 晚（第 4 晚）】</span>
            </div>
          </div>
        </div>

        ''' + build_timeline(timeline_d5) + '''

        <div class="galilee-photo-grid-2">
          <div class="galilee-photo-item">
            <img src="day05-varenna-lake.webp" alt="瓦倫納情人步道">
            <div class="galilee-spot-heading">
              <span>★ 瓦倫納情人湖濱步道</span>
              <span class="en">Passeggiata Varenna</span>
            </div>
            <div class="galilee-spot-desc">
              緊依著陡峭岩壁而建的紅色拱形懸空棧道，湖水澄澈見底。微風輕拂，漫步其上飽覽湖面帆影點點與對岸積雪山巒，令人心曠神怡。
            </div>
          </div>

          <div class="galilee-photo-item">
            <img src="bellagio.webp" alt="貝拉焦湖景">
            <div class="galilee-spot-heading">
              <span>★ 科莫湖明珠 · 貝拉焦</span>
              <span class="en">Bellagio Lake Como</span>
            </div>
            <div class="galilee-spot-desc">
              座落於科莫湖「人」字形中央樞紐，被譽為歐洲最浪漫的水鄉城鎮。鵝卵石鋪就的階梯巷弄穿梭於絲綢名店與湖畔花園之間，處處如畫。
            </div>
          </div>
        </div>

        <div class="galilee-sub-feature-box">
          <div class="galilee-sub-feature-title">
            <span>⛴️</span> 中央湖區觀景公共渡輪 Traghetto Lago di Como
          </div>
          <div>安排搭乘中央湖區觀景渡輪，從水上角度近距離欣賞沿岸百年貴族名流別墅與繁花盛開的臨湖露台，享受最道地的北義湖區慢活假期。</div>
        </div>

        ''' + build_footer_specs(
            ['飯店內歐式自助', '貝拉焦湖畔觀景餐廳鮮魚料理', '湖區精選主廚私房晚宴'],
            '4星 Hilton Milan 希爾頓酒店或同級（連住第 4 晚）',
            '★科莫湖中央湖區公共渡輪船票、★倫巴底鐵路通票。'
        ) + '''
      </div>

      ''' + build_page_footer(10) + '''
    </div>
''')

    # -------------------------------------------------------------------------
    # PAGE 11: DAY 06 & DAY 07 · 大城移動 ➔ 熱那亞世界遺產巡禮
    # -------------------------------------------------------------------------
    timeline_d6 = [
        {'icon': ICON_TRAIN, 'time': '09:10', 'label': 'IC特快列車', 'dur': '一等座專屬車廂'},
        {'icon': ICON_HOTEL_NODE, 'time': '10:45', 'label': '抵達熱那亞', 'dur': '王子廣場車站'},
        {'icon': ICON_HOTEL_NODE, 'time': '11:15', 'label': '五星飯店入住', 'dur': '薩伏亞大飯店'},
        {'icon': ICON_MEAL, 'time': '12:30', 'label': '海鮮午餐', 'dur': '利古里亞風味'},
        {'icon': ICON_SIGHT, 'time': '15:00', 'label': '舊港碼頭散步', 'dur': '地中海微風'}
    ]
    timeline_d7 = [
        {'icon': ICON_SIGHT, 'time': '09:30', 'label': '舊城石板漫步', 'dur': '加里波第街'},
        {'icon': ICON_SIGHT, 'time': '10:30', 'label': '羅利宮殿群', 'dur': '世界遺產紅宮白宮'},
        {'icon': ICON_MEAL, 'time': '12:30', 'label': '正宗青醬麵', 'dur': '熱那亞經典午餐'},
        {'icon': ICON_SIGHT, 'time': '15:00', 'label': '聖羅倫佐大教堂', 'dur': '黑白條紋大理石'},
        {'icon': ICON_MEAL, 'time': '18:30', 'label': '海港晚宴', 'dur': '香煎海鱸魚美饌'}
    ]

    html.append('''
    <!-- =========================================================================
         PAGE 11: DAY 06 & DAY 07
         ========================================================================= -->
    <div class="a5-page">
      <div class="page-header">
        <span class="page-header-title">DAY 06 & 07 · GENOVA</span>
        <span>大城移動 ➔ 熱那亞世界遺產</span>
      </div>

      <div class="page-content">
        <!-- DAY 06 -->
        <div class="galilee-split-day-block">
          <div class="galilee-day-header">
            <div class="galilee-day-number">DAY 6</div>
            <div class="galilee-day-heading-col">
              <h2 class="galilee-day-route-title">米蘭++Intercity特快++熱那亞－薩伏亞大飯店－舊港碼頭</h2>
              <div class="galilee-day-sub-bar">
                <span class="galilee-day-date">10/20（二）</span>
                <span class="galilee-day-base">【熱那亞 · 連住 3 晚（第 1 晚）】</span>
              </div>
            </div>
          </div>
          ''' + build_timeline(timeline_d6) + '''
          <div class="galilee-split-content">
            <img src="day06-genova-station.webp" alt="熱那亞車站與五星飯店">
            <div class="galilee-split-text">
              告別時尚米蘭，搭乘 Intercity 特快一等座舒適穿越亞平寧山脈，抵達海洋共和國熱那亞。步行 2 分鐘進駐五星級百年旗艦薩伏亞大飯店，午後漫步至由名建築師皮亞諾重塑的舊港區，享受澄澈蔚藍海風與海鷗鳴唱。
            </div>
          </div>
          ''' + build_footer_specs(['飯店內自助式', '利古里亞海鮮義大利麵', '海港景觀海鮮料理'], '5星 Grand Hotel Savoia 薩伏亞大飯店（連住第1晚）', '★Intercity 一等座特快車票。') + '''
        </div>

        <!-- DAY 07 -->
        <div class="galilee-split-day-block" style="margin-bottom:0; padding-bottom:0; border-bottom:none;">
          <div class="galilee-day-header">
            <div class="galilee-day-number">DAY 7</div>
            <div class="galilee-day-heading-col">
              <h2 class="galilee-day-route-title">熱那亞－羅利宮殿體系*世界遺產*－加里波第街－舊港漫步</h2>
              <div class="galilee-day-sub-bar">
                <span class="galilee-day-date">10/21（三）</span>
                <span class="galilee-day-base">【熱那亞 · 連住 3 晚（第 2 晚）】</span>
              </div>
            </div>
          </div>
          ''' + build_timeline(timeline_d7) + '''
          <div class="galilee-split-content">
            <img src="day07-palazzi-rolli.webp" alt="羅利宮殿群加里波第街">
            <div class="galilee-split-text">
              深入探訪聯合國教科文組織世界文化遺產「羅利宮殿體系」（Palazzi dei Rolli）。漫步在寬宏典雅的加里波第街，仰望十六世紀航海霸權時期的巴洛克貴族私邸與空中花園，品味最純粹的熱那亞羅勒青醬細麵。
            </div>
          </div>
          ''' + build_footer_specs(['飯店內自助式', '正宗熱那亞青醬手工細麵', '主廚香煎地中海海鱸魚美饌'], '5星 Grand Hotel Savoia 薩伏亞大飯店（連住第2晚）', '★熱那亞 Rolli 宮殿博物館門票聯票。') + '''
        </div>
      </div>

      ''' + build_page_footer(11) + '''
    </div>
''')

    # -------------------------------------------------------------------------
    # PAGE 12: DAY 08 · 菲諾港與聖馬格利塔海灣慢遊 (Full Page Feature!)
    # -------------------------------------------------------------------------
    timeline_d8 = [
        {'icon': ICON_TRAIN, 'time': '09:40', 'label': '海岸列車', 'dur': '前往聖馬格利塔'},
        {'icon': ICON_FERRY, 'time': '10:30', 'label': '觀景遊船', 'dur': '巡航蔚藍海灣'},
        {'icon': ICON_SIGHT, 'time': '11:15', 'label': '菲諾港漫行', 'dur': '粉彩小屋與名流碼頭'},
        {'icon': ICON_MEAL, 'time': '12:30', 'label': '海灣午餐', 'dur': '地中海青醬海鮮麵'},
        {'icon': ICON_SIGHT, 'time': '14:30', 'label': '布朗城堡遠眺', 'dur': '俯瞰半月形港灣'},
        {'icon': ICON_TRAIN, 'time': '17:00', 'label': '返回熱那亞', 'dur': '五星飯店悠閒休憩'}
    ]

    html.append('''
    <!-- =========================================================================
         PAGE 12: DAY 08 · 菲諾港一日慢遊
         ========================================================================= -->
    <div class="a5-page">
      <div class="page-header">
        <span class="page-header-title">DAY 08 · PORTOFINO</span>
        <span>夢幻粉彩海灣慢活</span>
      </div>

      <div class="page-content">
        <div class="galilee-day-header">
          <div class="galilee-day-number">DAY 8</div>
          <div class="galilee-day-heading-col">
            <h2 class="galilee-day-route-title">熱那亞－聖馬格利塔*海灣小鎮*++觀景遊船++菲諾港*粉彩港灣*－熱那亞</h2>
            <div class="galilee-day-sub-bar">
              <span class="galilee-day-date">10/22（四）</span>
              <span class="galilee-day-base">【熱那亞 · 連住 3 晚（第 3 晚）】</span>
            </div>
          </div>
        </div>

        ''' + build_timeline(timeline_d8) + '''

        <div class="galilee-photo-grid-2">
          <div class="galilee-photo-item">
            <img src="portofino.webp" alt="菲諾港全景">
            <div class="galilee-spot-heading">
              <span>★ 菲諾港 Portofino</span>
              <span class="en">Golfo del Tigullio</span>
            </div>
            <div class="galilee-spot-desc">
              世界富豪與名流趨之若鶩的度假天堂。半月形天然良港倒映著粉橘、鵝黃與赭紅色的昔日漁村小屋，高級遊艇輕盈搖曳，構成一幅令人屏息的明信片絕景。
            </div>
          </div>

          <div class="galilee-photo-item">
            <img src="day08-santa-margherita.webp" alt="聖馬格利塔港灣">
            <div class="galilee-spot-heading">
              <span>★ 聖馬格利塔海灣</span>
              <span class="en">Santa Margherita Ligure</span>
            </div>
            <div class="galilee-spot-desc">
              利古里亞海岸上優雅的度假門戶，棕櫚林立的海濱大道、巴洛克大理石教堂與露天咖啡座。海灣渡輪由此啟航，乘著地中海微風直駛菲諾港。
            </div>
          </div>
        </div>

        <div class="galilee-sub-feature-box">
          <div class="galilee-sub-feature-title">
            <span>🏰</span> 慢活健行推薦：布朗城堡松柏山徑
          </div>
          <div>沿著幽靜平緩的松柏石徑登上布朗城堡（Castello Brown），站在制高點平台俯瞰整座如翡翠般碧綠的深邃海灣，享受遠離喧囂的寧靜奢華時光。</div>
        </div>

        ''' + build_footer_specs(
            ['飯店內歐式自助', '菲諾港露天餐廳青醬海鮮麵風味午餐', '熱那亞海港經典海鮮燉飯晚宴'],
            '5星 Grand Hotel Savoia 薩伏亞大飯店（連住第 3 晚）',
            '★聖馬格利塔至菲諾港往返景觀遊船船票。'
        ) + '''
      </div>

      ''' + build_page_footer(12) + '''
    </div>
''')

    # -------------------------------------------------------------------------
    # PAGE 13: DAY 09 & DAY 10 · 跨越義法邊界 ➔ 抵達蔚藍海岸尼斯
    # -------------------------------------------------------------------------
    timeline_d9 = [
        {'icon': ICON_TRAIN, 'time': '09:50', 'label': '海岸列車啟程', 'dur': '熱那亞出發'},
        {'icon': ICON_TRAIN, 'time': '11:50', 'label': '邊界凡蒂米利亞', 'dur': '轉乘TER雙層列車'},
        {'icon': ICON_HOTEL_NODE, 'time': '12:45', 'label': '抵達尼斯', 'dur': '尼斯市區車站'},
        {'icon': ICON_HOTEL_NODE, 'time': '13:30', 'label': '入住艾美酒店', 'dur': '英國人散步大道'},
        {'icon': ICON_SIGHT, 'time': '15:30', 'label': '天使灣初探', 'dur': '地中海純淨海灣'}
    ]
    timeline_d10 = [
        {'icon': ICON_SHOP, 'time': '09:00', 'label': '薩萊亞花市', 'dur': '舊城傳統市集'},
        {'icon': ICON_SIGHT, 'time': '10:30', 'label': '舊城紅赭小巷', 'dur': '巴洛克教堂'},
        {'icon': ICON_MEAL, 'time': '12:30', 'label': '尼斯沙拉午餐', 'dur': '道地索卡薄餅'},
        {'icon': ICON_SIGHT, 'time': '15:00', 'label': '城堡山觀景', 'dur': '搭乘電梯登頂'},
        {'icon': ICON_MEAL, 'time': '18:30', 'label': '普羅旺斯晚宴', 'dur': '燉牛肉佐紅酒'}
    ]

    html.append('''
    <!-- =========================================================================
         PAGE 13: DAY 09 & DAY 10
         ========================================================================= -->
    <div class="a5-page">
      <div class="page-header">
        <span class="page-header-title">DAY 09 & 10 · NICE</span>
        <span>跨越邊境 ➔ 抵達尼斯蔚藍海岸</span>
      </div>

      <div class="page-content">
        <!-- DAY 09 -->
        <div class="galilee-split-day-block">
          <div class="galilee-day-header">
            <div class="galilee-day-number">DAY 9</div>
            <div class="galilee-day-heading-col">
              <h2 class="galilee-day-route-title">熱那亞++景觀特快++凡蒂米利亞++TER雙層列車++尼斯－艾美酒店</h2>
              <div class="galilee-day-sub-bar">
                <span class="galilee-day-date">10/23（五）</span>
                <span class="galilee-day-base">【尼斯 · 連住 5 晚（第 1 晚）】</span>
              </div>
            </div>
          </div>
          ''' + build_timeline(timeline_d9) + '''
          <div class="galilee-split-content">
            <img src="day09-nice-station.webp" alt="抵達尼斯車站與蔚藍海岸">
            <div class="galilee-split-text">
              搭乘全景雙層列車穿越義大利與法國邊界，迎著南法燦爛千陽抵達度假之都尼斯。進駐座落於英國人散步大道 1 號的艾美酒店（連住 5 晚免搬行李），推開窗戶即可飽覽波光粼粼的天使灣海景，開啟純法式慢活篇章。
            </div>
          </div>
          ''' + build_footer_specs(['飯店內自助式', '邊境海景餐廳特色午餐', '尼斯海灣法式主廚晚宴'], '4-5星 Le Méridien Nice 尼斯艾美酒店（連住第1晚）', '★義法跨國景觀列車聯票。') + '''
        </div>

        <!-- DAY 10 -->
        <div class="galilee-split-day-block" style="margin-bottom:0; padding-bottom:0; border-bottom:none;">
          <div class="galilee-day-header">
            <div class="galilee-day-number">DAY 10</div>
            <div class="galilee-day-heading-col">
              <h2 class="galilee-day-route-title">尼斯－英國人散步大道*天使灣*－薩萊亞市集－舊城巡禮</h2>
              <div class="galilee-day-sub-bar">
                <span class="galilee-day-date">10/24（六）</span>
                <span class="galilee-day-base">【尼斯 · 連住 5 晚（第 2 晚）】</span>
              </div>
            </div>
          </div>
          ''' + build_timeline(timeline_d10) + '''
          <div class="galilee-split-content">
            <img src="day10-baie-des-anges.webp" alt="天使灣與英國人散步大道">
            <div class="galilee-split-text">
              清晨漫步至薩萊亞廣場（Cours Saleya）鮮花與蔬果市集，沉浸在薰衣草皂香與普羅旺斯橄欖油香氣中。隨後搭乘免費觀景電梯登上城堡山（Colline du Château），居高臨下俯瞰天使灣那道無與倫比的蔚藍優美弧線。
            </div>
          </div>
          ''' + build_footer_specs(['飯店內自助式', '舊城道地尼斯沙拉與鷹嘴豆煎餅', '南法普羅旺斯燉牛肉風味餐'], '4-5星 Le Méridien Nice 尼斯艾美酒店（連住第2晚）', '★尼斯城堡山觀景電梯票券。') + '''
        </div>
      </div>

      ''' + build_page_footer(13) + '''
    </div>
''')

    # -------------------------------------------------------------------------
    # PAGE 14: DAY 11 & DAY 12 · 濱海自由城度假 ➔ 費拉角奢華莊園
    # -------------------------------------------------------------------------
    timeline_d11 = [
        {'icon': ICON_TRAIN, 'time': '10:00', 'label': 'TER列車', 'dur': '沿海鐵道8分鐘'},
        {'icon': ICON_SIGHT, 'time': '10:30', 'label': '自由城深水港', 'dur': '粉彩漁村漫步'},
        {'icon': ICON_SIGHT, 'time': '11:30', 'label': '聖皮耶禮拜堂', 'dur': '考克多壁畫藝術'},
        {'icon': ICON_MEAL, 'time': '12:30', 'label': '碼頭露天午餐', 'dur': '香煎地中海魚排'},
        {'icon': ICON_TRAIN, 'time': '15:30', 'label': '返回尼斯', 'dur': '艾美酒店海濱放鬆'}
    ]
    timeline_d12 = [
        {'icon': ICON_BUS, 'time': '09:30', 'label': '景觀巴士', 'dur': '費拉角半島'},
        {'icon': ICON_SIGHT, 'time': '10:15', 'label': '羅斯柴爾德莊園', 'dur': '粉紅宮殿導覽'},
        {'icon': ICON_MEAL, 'time': '12:30', 'label': '莊園午茶', 'dur': '玫瑰花園露台午餐'},
        {'icon': ICON_SIGHT, 'time': '14:30', 'label': '九大主題花園', 'dur': '日式、西班牙式庭園'},
        {'icon': ICON_MEAL, 'time': '18:30', 'label': '地中海晚宴', 'dur': '天使灣夕陽料理'}
    ]

    html.append('''
    <!-- =========================================================================
         PAGE 14: DAY 11 & DAY 12
         ========================================================================= -->
    <div class="a5-page">
      <div class="page-header">
        <span class="page-header-title">DAY 11 & 12 · RIVIERA</span>
        <span>濱海自由城度假 ➔ 費拉角豪門莊園</span>
      </div>

      <div class="page-content">
        <!-- DAY 11 -->
        <div class="galilee-split-day-block">
          <div class="galilee-day-header">
            <div class="galilee-day-number">DAY 11</div>
            <div class="galilee-day-heading-col">
              <h2 class="galilee-day-route-title">尼斯++景觀雙層列車++濱海自由城*地中海純淨港灣*－尼斯</h2>
              <div class="galilee-day-sub-bar">
                <span class="galilee-day-date">10/25（日）</span>
                <span class="galilee-day-base">【尼斯 · 連住 5 晚（第 3 晚）】</span>
              </div>
            </div>
          </div>
          ''' + build_timeline(timeline_d11) + '''
          <div class="galilee-split-content">
            <img src="villefranche.webp" alt="濱海自由城">
            <div class="galilee-split-text">
              搭乘景觀火車僅 8 分鐘即抵達濱海自由城（Villefranche-sur-Mer）。這座保留中世紀原貌的天然良港，赭紅色與鵝黃色古老房舍層疊依山傍水，漫步於十六世紀掩體暗街與藝術家考克多繪製的聖皮耶禮拜堂，享受私密恬靜時光。
            </div>
          </div>
          ''' + build_footer_specs(['飯店內自助式', '碼頭水岸露天餐廳海鮮午餐', '尼斯精選法式小館晚宴'], '4-5星 Le Méridien Nice 尼斯艾美酒店（連住第3晚）', '★TER 雙層景觀列車往返票券。') + '''
        </div>

        <!-- DAY 12 -->
        <div class="galilee-split-day-block" style="margin-bottom:0; padding-bottom:0; border-bottom:none;">
          <div class="galilee-day-header">
            <div class="galilee-day-number">DAY 12</div>
            <div class="galilee-day-heading-col">
              <h2 class="galilee-day-route-title">尼斯－費拉角半島*羅斯柴爾德花園莊園*－維拉弗朗什海灣－尼斯</h2>
              <div class="galilee-day-sub-bar">
                <span class="galilee-day-date">10/26（一）</span>
                <span class="galilee-day-base">【尼斯 · 連住 5 晚（第 4 晚）】</span>
              </div>
            </div>
          </div>
          ''' + build_timeline(timeline_d12) + '''
          <div class="galilee-split-content">
            <img src="day12-villa-rothschild.webp" alt="羅斯柴爾德莊園花園">
            <div class="galilee-split-text">
              前往歐洲名流隱世半島聖讓費拉角，探訪男爵夫人精心打造的羅斯柴爾德粉紅莊園（Villa Ephrussi de Rothschild）。漫步於法式水上花園、西班牙庭園、日式枯山水等九大主題園林，俯瞰左右兩側蔚藍地中海夾道壯麗景致。
            </div>
          </div>
          ''' + build_footer_specs(['飯店內自助式', '莊園玫瑰花園露台輕食午餐', '南法普羅旺斯海鮮晚宴'], '4-5星 Le Méridien Nice 尼斯艾美酒店（連住第4晚）', '★羅斯柴爾德花園莊園門票與語音導覽。') + '''
        </div>
      </div>

      ''' + build_page_footer(14) + '''
    </div>
''')

    # -------------------------------------------------------------------------
    # PAGE 15: DAY 13 · 尼斯最後慢活日 (Full Page Feature!)
    # -------------------------------------------------------------------------
    timeline_d13 = [
        {'icon': ICON_TRAIN, 'time': '10:00', 'label': '輕軌移動', 'dur': '尼斯T1路面輕軌'},
        {'icon': ICON_SIGHT, 'time': '10:30', 'label': '夏卡爾博物館', 'dur': '聖經系列彩繪玻璃'},
        {'icon': ICON_MEAL, 'time': '12:30', 'label': '馬賽納午餐', 'dur': '新古典主義廣場'},
        {'icon': ICON_SHOP, 'time': '14:30', 'label': '老佛爺百貨', 'dur': '伴手禮與退稅選購'},
        {'icon': ICON_SIGHT, 'time': '17:30', 'label': '海濱漫步告別', 'dur': '天使灣金黃夕陽'},
        {'icon': ICON_MEAL, 'time': '18:30', 'label': '告別晚宴', 'dur': '米其林推薦海景饗宴'}
    ]

    html.append('''
    <!-- =========================================================================
         PAGE 15: DAY 13 · 尼斯最後慢活日
         ========================================================================= -->
    <div class="a5-page">
      <div class="page-header">
        <span class="page-header-title">DAY 13 · NICE ART & LEISURE</span>
        <span>尼斯蔚藍海岸最後漫活</span>
      </div>

      <div class="page-content">
        <div class="galilee-day-header">
          <div class="galilee-day-number">DAY 13</div>
          <div class="galilee-day-heading-col">
            <h2 class="galilee-day-route-title">尼斯－夏卡爾國家博物館*聖經色彩*－馬賽納廣場－老佛爺百貨－海濱夕陽</h2>
            <div class="galilee-day-sub-bar">
              <span class="galilee-day-date">10/27（二）</span>
              <span class="galilee-day-base">【尼斯 · 連住 5 晚（第 5 晚）】</span>
            </div>
          </div>
        </div>

        ''' + build_timeline(timeline_d13) + '''

        <div class="galilee-photo-grid-2">
          <div class="galilee-photo-item">
            <img src="day13-nice-shopping.webp" alt="馬賽納廣場名品漫步">
            <div class="galilee-spot-heading">
              <span>★ 馬賽納廣場 Place Masséna</span>
              <span class="en">Nice City Center</span>
            </div>
            <div class="galilee-spot-desc">
              尼斯的新古典主義心臟，紅赭色拱廊建築與黑白棋盤格地磚交織。老佛爺百貨與名品精品店林立，是為親友精挑細選南法伴手禮與辦理退稅的理想之所。
            </div>
          </div>

          <div class="galilee-photo-item">
            <img src="nice-promenade.webp" alt="天使灣夕陽">
            <div class="galilee-spot-heading">
              <span>▲ 天使灣夕陽 Promenade</span>
              <span class="en">Baie des Anges Sunset</span>
            </div>
            <div class="galilee-spot-desc">
              午後沿著棕櫚樹掩映的海濱長廊閒適慢步，坐在標誌性的藍色扶手椅上，靜賞地中海夕陽將海面染成無垠金紅，為南法慢活旅程留下永恆美好的印記。
            </div>
          </div>
        </div>

        <div class="galilee-sub-feature-box">
          <div class="galilee-sub-feature-title">
            <span>🎨</span> 藝術巡禮：國立夏卡爾博物館 Musée Marc Chagall
          </div>
          <div>參觀由現代畫家夏卡爾親自參與策劃興建的藝術殿堂。十七幅以《聖經》創世紀與雅歌為主題的巨幅油畫與純淨藍色馬賽克彩繪玻璃，散發無盡詩意與溫暖光芒。</div>
        </div>

        ''' + build_footer_specs(
            ['飯店內歐式自助', '馬賽納廣場法式小酒館料理', '天使灣海景告別晚宴'],
            '4-5星 Le Méridien Nice 尼斯艾美酒店（連住第 5 晚）',
            '★夏卡爾國立博物館門票、★尼斯 24h 輕軌通票。'
        ) + '''
      </div>

      ''' + build_page_footer(15) + '''
    </div>
''')

    # -------------------------------------------------------------------------
    # PAGE 16: DAY 14–15 · 萬里歸途 ➔ 平安返台
    # -------------------------------------------------------------------------
    timeline_d14 = [
        {'icon': ICON_HOTEL_NODE, 'time': '10:00', 'label': '飯店悠閒退房', 'dur': '整理回台行囊'},
        {'icon': ICON_BUS, 'time': '10:30', 'label': '專車前往機場', 'dur': '尼斯蔚藍海岸機場'},
        {'icon': ICON_SHOP, 'time': '11:15', 'label': 'PABLO電子退稅', 'dur': '領隊專人協助'},
        {'icon': ICON_PLANE, 'time': '14:20', 'label': '登機啟航', 'dur': '飛往國際轉運樞紐'},
        {'icon': ICON_MEAL, 'time': '16:00', 'label': '機上美饌', 'dur': '空中平穩飛行'}
    ]
    timeline_d15 = [
        {'icon': ICON_PLANE, 'time': '15:30', 'label': '平安降落台北', 'dur': '桃園國際機場'},
        {'icon': ICON_SHOP, 'time': '16:15', 'label': '提領托運行李', 'dur': '海關通關'},
        {'icon': ICON_BUS, 'time': '17:00', 'label': '與團員珍重道別', 'dur': '接送返抵溫暖家園'}
    ]

    html.append('''
    <!-- =========================================================================
         PAGE 16: DAY 14–15
         ========================================================================= -->
    <div class="a5-page">
      <div class="page-header">
        <span class="page-header-title">DAY 14–15 · NCE ➔ TPE</span>
        <span>萬里歸途 ➔ 平安返台</span>
      </div>

      <div class="page-content">
        <!-- DAY 14 -->
        <div class="galilee-split-day-block">
          <div class="galilee-day-header">
            <div class="galilee-day-number">DAY 14</div>
            <div class="galilee-day-heading-col">
              <h2 class="galilee-day-route-title">尼斯機場*PABLO退稅辦理*✈️國際航空啟航</h2>
              <div class="galilee-day-sub-bar">
                <span class="galilee-day-date">10/28（三）</span>
                <span class="galilee-day-base">【豪華客機 ‧ 夜宿機上】</span>
              </div>
            </div>
          </div>
          ''' + build_timeline(timeline_d14) + '''
          <div class="galilee-split-content">
            <img src="day14-nice-departure.webp" alt="尼斯機場啟程">
            <div class="galilee-split-text">
              享用在南法的最後一頓豐盛自助早餐後，搭乘專車前往尼斯蔚藍海岸國際機場。在領隊全程協助下使用法國 PABLO 電子退稅機台輕鬆掃描退稅單，免去人工排隊等待，滿載豐富伴手禮與難忘回憶登機踏上歸途。
            </div>
          </div>
          ''' + build_footer_specs(['飯店內歐式自助', '機場候機輕食', '機上精緻美饌'], '豪華客機夜宿機上', '★專屬機場接送、★PABLO 退稅協處服務。') + '''
        </div>

        <!-- DAY 15 -->
        <div class="galilee-split-day-block" style="margin-bottom:0; padding-bottom:0; border-bottom:none;">
          <div class="galilee-day-header">
            <div class="galilee-day-number">DAY 15</div>
            <div class="galilee-day-heading-col">
              <h2 class="galilee-day-route-title">抵達台北桃園國際機場*行李提領*－溫暖家門</h2>
              <div class="galilee-day-sub-bar">
                <span class="galilee-day-date">10/29（四）</span>
                <span class="galilee-day-base">【圓滿返家 ‧ 甜蜜回味】</span>
              </div>
            </div>
          </div>
          ''' + build_timeline(timeline_d15) + '''
          <div class="galilee-split-content">
            <img src="day01-flight.webp" alt="班機平安返台">
            <div class="galilee-split-text">
              班機於午後順利降落台北桃園國際機場。提領行李時與這十五天來朝夕相處的團員好友互道珍重、交換聯絡方式。十五日的熟齡慢活巡禮圓滿落幕，帶著滿滿的異國人文感動與健康活力，重返溫馨甜蜜的家園。
            </div>
          </div>
          ''' + build_footer_specs(['機上精緻套餐', '機上精緻輕食', '溫暖家常料理'], '溫暖的家 Sweet Home', '★全程專業領隊隨行服務。') + '''
        </div>
      </div>

      ''' + build_page_footer(16) + '''
    </div>
''')

    # -------------------------------------------------------------------------
    # PAGE 17: 實用義大利語與法語雙語對照卡 & 退稅 3 步驟
    # -------------------------------------------------------------------------
    html.append('''
    <!-- =========================================================================
         PAGE 17: 實用義大利語與法語日常對照卡 & 退稅 3 步驟
         ========================================================================= -->
    <div class="a5-page">
      <div class="page-header">
        <span class="page-header-title">PHRASES & TAX REFUND</span>
        <span>日常會話 · 退稅指南</span>
      </div>

      <div class="page-content">
        <div class="galilee-section-title" style="font-size: 11pt; margin-bottom: 0.5mm;">旅途實用日常短句（義大利文與法文）</div>
        <div class="galilee-section-sub" style="margin-bottom: 2mm;">出示小卡或開口發音 · 讓當地人感受您的熱情尊重</div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2.5mm; margin-bottom: 2.5mm;">
          <!-- 義大利文實用句 -->
          <div style="background: #faf8f5; border: 1px solid #ebd9b6; border-radius: 4px; padding: 2mm 2.5mm; font-size: 6.2pt; line-height: 1.45;">
            <div style="font-weight: 700; color: var(--galilee-green); font-size: 7.2pt; margin-bottom: 1mm; border-bottom: 1px dotted #ccc; padding-bottom: 0.5mm;">
              🇮🇹 義大利常用旅遊短句
            </div>
            <div><strong>你好 / 日安：</strong>Buongiorno (崩叫諾)</div>
            <div><strong>謝謝：</strong>Grazie / Grazie mille (格拉齊耶)</div>
            <div><strong>請 / 不客氣：</strong>Per favore / Prego (普雷哥)</div>
            <div><strong>洗手間在哪裡？：</strong>Dov'è il bagno? (多威 依 邦紐)</div>
            <div><strong>買單請結帳：</strong>Il conto, per favore (依 控托)</div>
            <div><strong>請幫我叫計程車：</strong>Un taxi, per favore (溫 特克西)</div>
          </div>

          <!-- 法文實用句 -->
          <div style="background: #faf8f5; border: 1px solid #ebd9b6; border-radius: 4px; padding: 2mm 2.5mm; font-size: 6.2pt; line-height: 1.45;">
            <div style="font-weight: 700; color: var(--galilee-green); font-size: 7.2pt; margin-bottom: 1mm; border-bottom: 1px dotted #ccc; padding-bottom: 0.5mm;">
              🇫🇷 法國常用旅遊短句
            </div>
            <div><strong>你好 / 早安：</strong>Bonjour (崩祝)</div>
            <div><strong>謝謝：</strong>Merci beaucoup (梅爾西 柏庫)</div>
            <div><strong>不好意思 / 借過：</strong>Pardon / Excusez-moi (帕爾東)</div>
            <div><strong>洗手間在哪裡？：</strong>Où sont les toilettes? (烏 送 累 特瓦雷特)</div>
            <div><strong>請給我結帳單：</strong>L'addition, s'il vous plaît (拉迪秀)</div>
            <div><strong>這個多少錢？：</strong>C'est combien? (塞 恐便)</div>
          </div>
        </div>

        <!-- 機場退稅 3 步驟 -->
        <div style="background: #f7faf8; border: 1.5px solid var(--galilee-green); border-radius: 4px; padding: 2.2mm 3mm; font-size: 6.3pt; line-height: 1.5; color: #2b2b2b;">
          <div style="font-weight: 700; color: var(--galilee-green); font-size: 7.5pt; margin-bottom: 1.2mm; display: flex; justify-content: space-between;">
            <span>💶 歐盟電子退稅輕鬆 3 步驟（法國 PABLO / 義大利 OTELLO）</span>
            <span style="font-size: 6.5pt; color: var(--galilee-gold);">門檻：同店同日滿 100 歐元即可辦理</span>
          </div>
          <div style="margin-bottom: 0.8mm;"><strong>步驟 1【購物索單】：</strong>於支援退稅商店結帳時出示護照原件，索取 Tax Free Form 退稅單據及條碼。</div>
          <div style="margin-bottom: 0.8mm;"><strong>步驟 2【機場掃碼】：</strong>至尼斯機場出境大廳尋找「PABLO 電子退稅機台」，將退稅單條碼貼近紅外線掃描口，螢幕顯示<strong>綠色勾勾 ✓</strong> 即完成海關認證。</div>
          <div><strong>步骤 3【款項領取】：</strong>若選擇退回原信用卡則無須再郵寄；若選擇現金退稅，持綠色核驗單至 Travelex 或 Global Blue 櫃檯領取歐元現鈔。</div>
        </div>
      </div>

      ''' + build_page_footer(17) + '''
    </div>
''')

    # -------------------------------------------------------------------------
    # PAGE 18: 旅途花費記帳與伴手禮購物清單
    # -------------------------------------------------------------------------
    html.append('''
    <!-- =========================================================================
         PAGE 18: 旅途花費記帳與伴手禮購物清單
         ========================================================================= -->
    <div class="a5-page">
      <div class="page-header">
        <span class="page-header-title">EXPENSES & SOUVENIRS</span>
        <span>旅費記帳 · 伴手禮清單</span>
      </div>

      <div class="page-content">
        <div class="galilee-section-title" style="font-size: 11pt; margin-bottom: 0.5mm;">伴手禮清單與每日零用記帳</div>
        <div class="galilee-section-sub" style="margin-bottom: 2mm;">嚴選在地特產指南 · 清楚掌握個人消費</div>

        <div style="background: #faf8f5; border: 1px solid #ebd9b6; border-radius: 4px; padding: 2mm 2.5mm; font-size: 6.2pt; line-height: 1.45; margin-bottom: 2.5mm;">
          <div style="font-weight: 700; color: var(--galilee-green); font-size: 7.2pt; margin-bottom: 1mm;">🎁 領隊嚴選 · 義法兩國必買經典伴手禮指南</div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2mm;">
            <div><strong>🇮🇹 義大利經典名產：</strong><br>• 摩德納巴薩米克香醋 (Aceto Balsamico IGP)<br>• 利古里亞特級冷壓初榨橄欖油 (Frantoio)<br>• Venchi / Amedei 頂級莊園黑巧克力<br>• 百年咖啡名店濃縮咖啡豆 / 摩卡壺</div>
            <div><strong>🇫🇷 南法蔚藍海岸特產：</strong><br>• 格拉斯手工天然精油香水 (Fragonard)<br>• 普羅旺斯傳統馬賽橄欖香皂 (Savon de Marseille)<br>• 尼斯舊城特產甘甜糖漬水果 (Fruits Confits)<br>• 普羅旺斯薰衣草助眠枕頭噴霧</div>
          </div>
        </div>

        <div style="font-weight: 700; color: var(--galilee-green); font-size: 7.5pt; margin-bottom: 1mm;">
          💶 每日零用金與個人花費記帳表格
        </div>
        <table class="galilee-table" style="margin-bottom: 0;">
          <thead>
            <tr>
              <th style="width: 14%;">日期</th>
              <th style="width: 46%;">支出項目 / 購買商店與商品</th>
              <th style="width: 20%;">付款方式</th>
              <th style="width: 20%;">金額 (€ / NT$)</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>10/16</td><td>米蘭咖啡座濃縮咖啡 & 冰淇淋</td><td>歐元現鈔</td><td>€ 4.50</td></tr>
            <tr><td>10/17</td><td>文藝復興百貨伴手禮 (巧克力禮盒)</td><td>信用卡刷卡</td><td>€ 38.00</td></tr>
            <tr><td>10/19</td><td>科莫湖絲綢手工披肩圍巾</td><td>信用卡刷卡</td><td>€ 45.00</td></tr>
            <tr><td>10/21</td><td>熱那亞百年老店冷壓特級橄欖油 2 瓶</td><td>歐元現鈔</td><td>€ 24.00</td></tr>
            <tr><td>10/24</td><td>薩萊亞花市普羅旺斯傳統馬賽皂組</td><td>歐元現鈔</td><td>€ 18.00</td></tr>
            <tr><td>10/26</td><td>羅斯柴爾德莊園花園精油香氛</td><td>信用卡刷卡</td><td>€ 32.50</td></tr>
            <tr><td>備用行</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
            <tr><td>備用行</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
          </tbody>
        </table>
      </div>

      ''' + build_page_footer(18) + '''
    </div>
''')

    # -------------------------------------------------------------------------
    # PAGE 19: 旅人隨筆與紀念印章收集頁
    # -------------------------------------------------------------------------
    html.append('''
    <!-- =========================================================================
         PAGE 19: 旅人隨筆與紀念印章收集頁
         ========================================================================= -->
    <div class="a5-page">
      <div class="page-header">
        <span class="page-header-title">TRAVEL JOURNAL & STAMPS</span>
        <span>旅人隨筆 · 紀念印章</span>
      </div>

      <div class="page-content">
        <div class="galilee-section-title" style="font-size: 11pt; margin-bottom: 0.5mm;">旅行心得隨筆與紀念章收集</div>
        <div class="galilee-section-sub" style="margin-bottom: 2mm;">記下感動瞬間的心情文字 · 蓋下專屬每一座古城之印戳</div>

        <div style="display: flex; gap: 3.5mm; margin-bottom: 2.5mm;">
          <!-- 紀念章框 1 -->
          <div style="flex: 1; height: 38mm; border: 1.5px dashed #b8862d; border-radius: 4px; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #faf9f6; font-size: 6.2pt; color: #888;">
            <div style="font-size: 14pt; color: var(--galilee-gold); margin-bottom: 1mm;">🏛️</div>
            <div>【紀念章收集欄 1】</div>
            <div style="font-size: 5.5pt; color: #aaa;">米蘭大教堂 / 史卡拉歌劇院</div>
          </div>
          <!-- 紀念章框 2 -->
          <div style="flex: 1; height: 38mm; border: 1.5px dashed #b8862d; border-radius: 4px; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #faf9f6; font-size: 6.2pt; color: #888;">
            <div style="font-size: 14pt; color: var(--galilee-gold); margin-bottom: 1mm;">🌊</div>
            <div>【紀念章收集欄 2】</div>
            <div style="font-size: 5.5pt; color: #aaa;">科莫湖渡輪 / 貝爾加莫纜車</div>
          </div>
          <!-- 紀念章框 3 -->
          <div style="flex: 1; height: 38mm; border: 1.5px dashed #b8862d; border-radius: 4px; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #faf9f6; font-size: 6.2pt; color: #888;">
            <div style="font-size: 14pt; color: var(--galilee-gold); margin-bottom: 1mm;">🌴</div>
            <div>【紀念章收集欄 3】</div>
            <div style="font-size: 5.5pt; color: #aaa;">菲諾港 / 尼斯天使灣</div>
          </div>
        </div>

        <div style="font-weight: 700; color: var(--galilee-green); font-size: 7.2pt; margin-bottom: 1.5mm;">
          ✍️ 旅人筆記與心靈悸動留白頁
        </div>
        <div style="display: flex; flex-direction: column; gap: 4mm; flex: 1;">
          <div style="border-bottom: 1px dotted #ccc; height: 1px;"></div>
          <div style="border-bottom: 1px dotted #ccc; height: 1px;"></div>
          <div style="border-bottom: 1px dotted #ccc; height: 1px;"></div>
          <div style="border-bottom: 1px dotted #ccc; height: 1px;"></div>
          <div style="border-bottom: 1px dotted #ccc; height: 1px;"></div>
          <div style="border-bottom: 1px dotted #ccc; height: 1px;"></div>
          <div style="border-bottom: 1px dotted #ccc; height: 1px;"></div>
          <div style="border-bottom: 1px dotted #ccc; height: 1px;"></div>
          <div style="border-bottom: 1px dotted #ccc; height: 1px;"></div>
          <div style="border-bottom: 1px dotted #ccc; height: 1px;"></div>
        </div>
      </div>

      ''' + build_page_footer(19) + '''
    </div>
''')

    # -------------------------------------------------------------------------
    # PAGE 20: 封底 (Back Cover - Mirroring Galileo Page 24)
    # -------------------------------------------------------------------------
    html.append('''
    <!-- =========================================================================
         PAGE 20: 封底 (Back Cover)
         ========================================================================= -->
    <div class="a5-page galilee-back-cover">
      <div style="text-align: center; margin-bottom: 3.5mm;">
        <div style="font-size: 18px; margin-bottom: 1mm;">🌲</div>
        <div style="font-family: 'Noto Serif TC', serif; font-size: 12.5pt; font-weight: 700; color: #fff; letter-spacing: 0.1em;">
          加利利旅行社 · 熟齡慢活奢選系列
        </div>
        <div style="font-size: 6.8pt; color: #a4c9b1; letter-spacing: 0.2em; text-transform: uppercase;">
          GALILEE TOURS PRESTIGE COLLECTION
        </div>
      </div>

      <div style="margin-bottom: 2.5mm;">
        <h3>費用說明（訂金、機票與優惠問題，請洽詢您的旅遊專員）</h3>
        <ol>
          <li>費用包含：全程住宿、行程表所列餐食（自理餐除外）、表列所有火車與纜車景點門票、全程專業領隊司機服務費、團體行程履約責任保險 500 萬及 20 萬意外傷害醫療險。</li>
          <li>費用不包括：護照代辦規費、私人各項消費（行李超重費、飲料費、飯店洗衣服務）、床頭枕頭與行李小費。</li>
          <li>團體機票說明：團費包含國際線團體經濟艙機票，不適用於出發前預選特定座位，若有走道或相鄰需求請於機場報到時主動告知地勤協助協調。</li>
        </ol>
      </div>

      <div style="margin-bottom: 2.5mm;">
        <h3>證件需求與團體保險說明</h3>
        <ol>
          <li>持台灣護照進入申根國家享免簽證待遇，護照效期須自返國日起算 6 個月以上，且內頁需有完整空白頁。</li>
          <li>依法為旅客投保旅遊責任險外，本公司強烈建議貴賓依自身需求於出發前自行加保高額海外突發疾病與旅遊不便綜合險。</li>
        </ol>
      </div>

      <div style="margin-bottom: 3mm;">
        <h3>熟齡樂齡安心慢活守則與其他說明</h3>
        <ol>
          <li>景點、飯店或餐食如因歐洲季節慶典、臨時罷工或天候交通狀況等不可抗力因素影響，本公司保有在同等標準下彈性調整先後順序之權利。</li>
          <li>國外餐食多肉食，若有不吃牛肉、海鮮或全素飲食特殊需求，敬請最晚於出發前 14 天告知旅遊專員以便提前妥善安排。</li>
          <li>為維護旅遊品質與貴賓睡眠舒適度，行程全程嚴選連住米蘭 4 晚、熱那亞 3 晚、尼斯 5 晚之優質格調飯店，避免每日拉車打包之苦。</li>
        </ol>
      </div>

      <div style="margin-top: auto; border-top: 1px solid rgba(255,255,255,0.25); padding-top: 2.5mm; font-size: 5.8pt; color: #a8ceb5; line-height: 1.45; text-align: center;">
        <div style="font-weight: 700; color: #ffffff; margin-bottom: 0.5mm;">
          加利利旅行社股份有限公司 · 綜合旅行社 · 交觀綜字第 2125 號 · 品保協會會員
        </div>
        <div>台北總公司：台北市中山區南京東路三段 248 號 4 樓之 1 · TEL: (02) 2717-3188</div>
        <div>新竹分公司：(03) 578-5555 ｜ 台中分公司：(04) 2369-2288 ｜ 高雄分公司：(07) 586-9355</div>
        <div style="margin-top: 1mm; color: var(--galilee-gold);">
          ★ 24H 海外緊急聯絡電話：+886-2-2717-3188 ｜ 祝您旅途平安愉快 圓滿順心 ★
        </div>
      </div>
    </div>
''')

    # Close document
    html.append('''
  </div>
</body>
</html>''')

    output_path = '/Users/sher/Documents/trvalpremium/print-handbook.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(''.join(html))
    print(f"Successfully generated refined {output_path} ({len(''.join(html))} characters)!")

if __name__ == '__main__':
    generate_handbook()
