#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate comprehensive origin-to-destination route maps for all 18 transit legs
of the 15-day Northern Italy and French Riviera tour, referencing 1.pdf and 2.pdf.
"""

import json
import os
import subprocess
import time
import fitz

ROUTES_DATA = [
    {
        "id": "route_01",
        "day": "DAY 02",
        "day_badge": "D02 · 機場入境與抵達米蘭",
        "title": "馬爾彭薩機場第一航廈 至 米蘭中央車站",
        "origin_name": "馬爾彭薩機場第一航廈（MXP T1）",
        "origin_addr": "Aeroporto di Milano Malpensa Terminal 1, 21010 Ferno VA, 義大利",
        "dest_name": "米蘭中央車站（Milano Centrale）",
        "dest_addr": "Piazza Duca d'Aosta 1, 20124 Milano MI, 義大利",
        "dep_time": "16:11",
        "arr_time": "17:07",
        "duration": "56 分（8 站）",
        "ticket_title": "購票 · 單程成人票價",
        "ticket_sub": "北方鐵路 Trenord / 現場售票機與線上均可購票",
        "ticket_price": "單程 €15.00 起",
        "operator": "北方鐵路 Trenord",
        "operator_note": "上車前務必於黃綠色打票機打票啟用；車廂設有專屬大件行李架",
        "transit_type": "train",
        "transit_badge": "🚆 RE 2951 / RE 512977 Milano Centrale",
        "line_color": "#d93025",
        "gmaps_url": "https://maps.app.goo.gl/7iYW9aFGebMAmSUJA",
        "alert": None,
        "stops": [
            {"time": "16:11", "name": "馬爾彭薩機場第一航廈（MXP T1）", "coord": [45.62737, 8.71244], "is_start": True},
            {"time": "16:16", "name": "Ferno-Lonate Pozzolo", "coord": [45.6083, 8.7561]},
            {"time": "16:21", "name": "Busto Arsizio FN", "coord": [45.6111, 8.8519]},
            {"time": "16:24", "name": "Castellanza", "coord": [45.6089, 8.8928]},
            {"time": "16:30", "name": "Rescaldina", "coord": [45.6133, 8.9483]},
            {"time": "16:36", "name": "Saronno（重要轉乘樞紐）", "coord": [45.5997, 9.0272]},
            {"time": "16:49", "name": "Milano Bovisa Politecnico", "coord": [45.5019, 9.1625]},
            {"time": "16:56", "name": "Milano Porta Garibaldi", "coord": [45.4842, 9.1872]},
            {"time": "17:07", "name": "米蘭中央車站（Milano Centrale）", "coord": [45.48714, 9.20482], "is_end": True}
        ]
    },
    {
        "id": "route_02",
        "day": "DAY 03",
        "day_badge": "D03 · 米蘭經典城市巡遊",
        "title": "米蘭中央車站 至 米蘭大教堂",
        "origin_name": "米蘭中央車站（Centrale FS）",
        "origin_addr": "Piazza Duca d'Aosta 1, 20124 Milano MI, 義大利",
        "dest_name": "米蘭大教堂站（Duomo M3）",
        "dest_addr": "Piazza del Duomo, 20123 Milano MI, 義大利",
        "dep_time": "09:30",
        "arr_time": "09:36",
        "duration": "6 分（4 站）",
        "ticket_title": "通票資訊 · 米蘭都會大眾運輸",
        "ticket_sub": "米蘭城市通票（Milano Pass 24h）無限搭乘",
        "ticket_price": "持米蘭城市通票搭乘（24H 無限次）",
        "operator": "米蘭大眾運輸 ATM",
        "operator_note": "持米蘭城市通票 Milano Pass 感應進站；出站直達米蘭大教堂廣場",
        "transit_type": "metro",
        "transit_badge": "Ⓜ️ 3 San Donato（M3 黃線）",
        "line_color": "#f9ba00",
        "gmaps_url": "https://maps.app.goo.gl/WQV7JywTpDj687Kr5",
        "alert": "提示：Duomo 站人潮較多，請留意隨身隨身包包與貴重物品。",
        "stops": [
            {"time": "09:30", "name": "Centrale FS", "coord": [45.48714, 9.20482], "is_start": True},
            {"time": "09:32", "name": "Repubblica", "coord": [45.4786, 9.1969]},
            {"time": "09:33", "name": "Turati", "coord": [45.4744, 9.1936]},
            {"time": "09:34", "name": "Montenapoleone（蒙特拿破崙名品街）", "coord": [45.4697, 9.1925]},
            {"time": "09:36", "name": "Duomo（大教堂站）", "coord": [45.46372, 9.1906], "is_end": True}
        ]
    },
    {
        "id": "route_03",
        "day": "DAY 03",
        "day_badge": "D03 · 復古電車漫遊花園",
        "title": "斯卡拉大劇院 至 蒙塔內利花園（P.za Cavour）",
        "origin_name": "斯卡拉大劇院（Teatro alla Scala）",
        "origin_addr": "Via Filodrammatici 2, 20121 Milano MI, 義大利",
        "dest_name": "蒙塔內利花園入口（Piazza Cavour 站）",
        "dest_addr": "Piazza Cavour, 20121 Milano MI, 義大利",
        "dep_time": "14:30",
        "arr_time": "14:36",
        "duration": "6 分（3 站直達）",
        "ticket_title": "通票資訊 · 米蘭復古路面電車",
        "ticket_sub": "米蘭城市通票（Milano Pass 24h）無限搭乘",
        "ticket_price": "持米蘭城市通票搭乘（24H 無限次）",
        "operator": "米蘭大眾運輸 ATM",
        "operator_note": "持米蘭通票搭乘復古路面電車 1 號沿 Via Manzoni 直行至 P.za Cavour（下車前一站：Pisoni）。出站穿過十九世紀拱門即入蒙塔內利花園，漫步杜尼亞尼宮綠地，傍晚穿越花園至威尼斯門街區晚餐",
        "transit_type": "tram",
        "transit_badge": "🚊 Tram 1（往 Greco Rovereto）",
        "line_color": "#e67e22",
        "gmaps_url": "https://maps.app.goo.gl/LVe87892ZJaP7SuJ9",
        "alert": "下車提示：前一站為 Pisoni，下一站即為 Piazza Cavour 站，下車正對古典拱門入口與杜尼亞尼宮。",
        "stops": [
            {"time": "14:30", "name": "Teatro alla Scala（斯卡拉大劇院前）", "coord": [45.4674, 9.18955], "is_start": True},
            {"time": "14:32", "name": "Montenapoleone M3（蒙特拿破崙街口）", "coord": [45.4699, 9.1926]},
            {"time": "14:34", "name": "Manzoni / Pisoni（下車前一站提示）", "coord": [45.4712, 9.1936]},
            {"time": "14:36", "name": "Piazza Cavour（下車即達蒙塔內利花園拱門）", "coord": [45.47278, 9.19578], "is_end": True}
        ]
    },
    {
        "id": "route_04",
        "day": "DAY 03",
        "day_badge": "D03 · 晚餐後從容返回飯店",
        "title": "威尼斯門 至 Via Galvani（加爾瓦尼站 · Hilton 門前）",
        "origin_name": "威尼斯門站（Porta Venezia M1）",
        "origin_addr": "Piazza Guglielmo Oberdan, 20129 Milano MI, 義大利",
        "dest_name": "加爾瓦尼站（Via Filzi - Via Galvani · Via Luigi Galvani 街口）",
        "dest_addr": "Via Fabio Filzi & Via Luigi Galvani, 20124 Milano MI, 義大利",
        "dep_time": "20:30",
        "arr_time": "20:38",
        "duration": "8 分（4 站直達）",
        "ticket_title": "通票資訊 · 米蘭都會輕軌電車",
        "ticket_sub": "米蘭城市通票（Milano Pass 24h）無限搭乘",
        "ticket_price": "持米蘭城市通票搭乘（24H 無限次）",
        "operator": "米蘭大眾運輸 ATM",
        "operator_note": "威尼斯門晚餐後持米蘭通票搭乘路面輕軌 9 號直達 Via Filzi - Via Galvani 站（加爾瓦尼站）。下車即為 Via Luigi Galvani 街口，轉角 1 分鐘即抵達 Hilton Milan 休息",
        "transit_type": "tram",
        "transit_badge": "🚊 Tram 9（往 Stazione Centrale）",
        "line_color": "#2e7d32",
        "gmaps_url": "https://maps.app.goo.gl/serExZnQmnax3RyZ8",
        "alert": "下車提示：前一站為 Filzi / Pirelli，下一站即為「Via Filzi - Via Galvani」（加爾瓦尼站）下車，站牌正對 Via Luigi Galvani 路口，轉角步行 1 分鐘即達 Hilton Milan（Via Luigi Galvani 12）。",
        "stops": [
            {"time": "20:30", "name": "P.ta Venezia M1（威尼斯門站）", "coord": [45.47418, 9.20595], "is_start": True},
            {"time": "20:32", "name": "V.le Vittorio Veneto", "coord": [45.4771, 9.2028]},
            {"time": "20:34", "name": "P.za Repubblica M3", "coord": [45.4786, 9.1970]},
            {"time": "20:36", "name": "Filzi / Pirelli（下車前一站提示）", "coord": [45.4831, 9.2008]},
            {"time": "20:38", "name": "Via Filzi / Via Galvani（加爾瓦尼站 · Via Galvani 街口）", "coord": [45.4854, 9.20097], "is_end": True}
        ]
    },
    {
        "id": "route_05",
        "day": "DAY 04",
        "day_badge": "D04 · 貝爾加莫中世紀慢遊",
        "title": "米蘭中央車站 至 貝爾加莫車站",
        "origin_name": "米蘭中央車站（Milano Centrale）",
        "origin_addr": "Piazza Duca d'Aosta 1, 20124 Milano MI, 義大利",
        "dest_name": "貝爾加莫車站（Bergamo Stazione FS）",
        "dest_addr": "Piazzale Guglielmo Marconi 7, 24122 Bergamo BG, 義大利",
        "dep_time": "09:05",
        "arr_time": "09:53",
        "duration": "48 分（4 站）",
        "ticket_title": "購票 · 單程成人票價",
        "ticket_sub": "Trenord 區域快車 / 班次密集準時",
        "ticket_price": "單程 €6.00 起",
        "operator": "北方鐵路 Trenord / 義大利國鐵",
        "operator_note": "持實體票需於月台黃色打票機打票；抵達後於站前廣場轉搭 1 號公車",
        "transit_type": "train",
        "transit_badge": "🚆 RE 2219 Bergamo（直達快車）",
        "line_color": "#1a73e8",
        "gmaps_url": "https://maps.app.goo.gl/cNjvrvYM8wyjngiB8",
        "alert": None,
        "stops": [
            {"time": "09:05", "name": "Milano Centrale", "coord": [45.48714, 9.20482], "is_start": True},
            {"time": "09:12", "name": "Milano Lambrate", "coord": [45.4849, 9.2372]},
            {"time": "09:19", "name": "Pioltello-Limito", "coord": [45.4764, 9.3247]},
            {"time": "09:38", "name": "Verdello-Dalmine", "coord": [45.6025, 9.6192]},
            {"time": "09:53", "name": "Bergamo FS", "coord": [45.69043, 9.67505], "is_end": True}
        ]
    },
    {
        "id": "route_06",
        "day": "DAY 04",
        "day_badge": "D04 · 貝爾加莫市區公車",
        "title": "Bergamo 7（車站前）至 Vittorio Emanuele 47（公車 1 號）",
        "origin_name": "Bergamo 7 站牌（火車站前廣場 · Piazzale Guglielmo Marconi 7）",
        "origin_addr": "Piazzale Guglielmo Marconi 7, 24122 Bergamo BG, 義大利",
        "dest_name": "V.le V. Emanuele II, 47（登山纜車站下站前）",
        "dest_addr": "V.le V. Emanuele II, 47, 24121 Bergamo BG, 義大利",
        "dep_time": "10:05",
        "arr_time": "10:15",
        "duration": "10 分（步行 3 分 + 4 站直達）",
        "ticket_title": "通票資訊 · ATB 貝爾加莫都會交通",
        "ticket_sub": "貝爾加莫 24h 交通通票（含市區公車與登山纜車）",
        "ticket_price": "持貝爾加莫 24h 通票搭乘（無限次）",
        "operator": "ATB Bergamo（Azienda Trasporti Bergamo）",
        "operator_note": "出火車站自 Piazzale Marconi 7 站牌（Bergamo 7）步行約 3 分鐘（160公尺）至「Papa Giovanni fermata 2」，搭乘 ATB Linea 1 號公車（往 Stazione - Citta' Alta 方向 · 車站 ID: 2），行經 4 站直達「Vittorio Emanuele 47」站下車，正對登山纜車下站（Funicolare Bassa），過馬路即可轉乘纜車登頂上城",
        "transit_type": "bus",
        "transit_badge": "🚌 ATB Linea 1（往 Stazione - Citta' Alta 方向 · 車站 ID: 2）",
        "line_color": "#ff6f00",
        "gmaps_url": "https://maps.app.goo.gl/KRgHnEdPraNa4FrD6",
        "alert": "下車提示：前一站為 Vittorio Emanuele 19，下一站即為「Vittorio Emanuele 47」站下車，下車正對登山纜車站（Funicolare Bassa）。",
        "stops": [
            {"time": "10:05", "name": "Bergamo 7（火車站前 Piazzale Marconi 7 · 步行出發）", "coord": [45.69043, 9.67505], "is_start": True},
            {"time": "10:08", "name": "Papa Giovanni fermata 2（1 號公車站牌 · 起點上車）", "coord": [45.6918, 9.6738]},
            {"time": "10:10", "name": "Porta Nuova Chiesa Grazie（新門感恩聖母堂）", "coord": [45.6953, 9.6704]},
            {"time": "10:12", "name": "Vittorio Emanuele 3", "coord": [45.6970, 9.6688]},
            {"time": "10:14", "name": "Vittorio Emanuele 19（下車前一站提示）", "coord": [45.6987, 9.6672]},
            {"time": "10:15", "name": "Vittorio Emanuele 47（終點下車 · 正對登山纜車站）", "coord": [45.70078, 9.66552], "is_end": True}
        ]
    },
    {
        "id": "route_07",
        "day": "DAY 04",
        "day_badge": "D04 · 聖賈科莫門午後返程",
        "title": "聖賈科莫城門 至 Paleocapa 1 車站前（公車 1 號返程）",
        "origin_name": "Delle Mura - San Giacomo 站牌（聖賈科莫古城門前）",
        "origin_addr": "Viale delle Mura & Via S. Giacomo, 24129 Bergamo BG, 義大利",
        "dest_name": "Paleocapa 1 站（火車站西側 · 步行 1 分鐘進車站月台）",
        "dest_addr": "Via Pietro Paleocapa 1, 24122 Bergamo BG, 義大利",
        "dep_time": "14:30",
        "arr_time": "14:42",
        "duration": "12 分（公車 1 號下山直達火車站前）",
        "ticket_title": "通票資訊 · ATB 貝爾加莫都會交通",
        "ticket_sub": "貝爾加莫 24h 交通通票（回程免再購票）",
        "ticket_price": "持貝爾加莫 24h 通票搭乘（無限次）",
        "operator": "ATB Bergamo",
        "operator_note": "漫步城牆後持貝爾加莫 24h 通票於門前站牌搭乘 1 號公車下山直達「Paleocapa 1」站，下車過街 1 分鐘進火車站月台搭乘 15:02 RE 2232 區域快車返米蘭",
        "transit_type": "bus",
        "transit_badge": "🚌 ATB Linea 1（往 Stazione FS / Aeroporto）",
        "line_color": "#d32f2f",
        "gmaps_url": "https://maps.app.goo.gl/bY3hHYGRUuS3kkuD8",
        "alert": "返程提示：於聖賈科莫古城門前「Delle Mura - San Giacomo」站牌搭乘 Linea 1 公車下山，於「Paleocapa 1」站下車，下車步行 1 分鐘即達 Bergamo 火車站大廳，搭乘 15:02 發車之 RE 2232 區域快車準時返回米蘭中央車站。",
        "stops": [
            {"time": "14:30", "name": "Delle Mura - San Giacomo（聖賈科莫門前站牌 · 起點上車）", "coord": [45.70138, 9.66289], "is_start": True},
            {"time": "14:33", "name": "Porta Sant'Agostino（穿出古城門）", "coord": [45.7022, 9.6645]},
            {"time": "14:36", "name": "V.le Vittorio Emanuele II / Funicolare", "coord": [45.6983, 9.6689]},
            {"time": "14:39", "name": "Porta Nuova（新門）", "coord": [45.6953, 9.6700]},
            {"time": "14:41", "name": "Viale Papa Giovanni XXIII（下車前一站提示）", "coord": [45.6940, 9.6715]},
            {"time": "14:42", "name": "Paleocapa 1（終點下車 · 火車站前 · 步行 1 分鐘進車站）", "coord": [45.69203, 9.67229], "is_end": True}
        ]
    },
    {
        "id": "route_08",
        "day": "DAY 05",
        "day_badge": "D05 · 科莫湖雙城慢遊",
        "title": "米蘭中央車站 至 瓦倫納-埃西諾車站",
        "origin_name": "米蘭中央車站（Milano Centrale）",
        "origin_addr": "Piazza Duca d'Aosta 1, 20124 Milano MI, 義大利",
        "dest_name": "瓦倫納-埃西諾車站（Varenna-Esino）",
        "dest_addr": "Varenna Esino, 23828 Perledo LC, 義大利",
        "dep_time": "09:20",
        "arr_time": "10:25",
        "duration": "65 分（5 站）",
        "ticket_title": "購票 · 單程成人票價",
        "ticket_sub": "Trenord 區域快車 / 建議坐火車前進方向左側欣賞湖景",
        "ticket_price": "單程 €7.40 起",
        "operator": "北方鐵路 Trenord",
        "operator_note": "列車過 Lecco 後左側窗外即展開壯麗科莫湖全景，抵達 Varenna 步行 5 分到湖畔",
        "transit_type": "train",
        "transit_badge": "🚆 RE 2818 Tirano（科莫湖景觀快車）",
        "line_color": "#0f9d58",
        "gmaps_url": "https://maps.app.goo.gl/UYq827fCUQDeTCmY7",
        "alert": None,
        "stops": [
            {"time": "09:20", "name": "Milano Centrale", "coord": [45.48714, 9.20482], "is_start": True},
            {"time": "09:31", "name": "Monza", "coord": [45.5786, 9.2736]},
            {"time": "09:41", "name": "Carnate-Usmate", "coord": [45.6517, 9.3789]},
            {"time": "10:02", "name": "Lecco（科莫湖南端轉角）", "coord": [45.8561, 9.3958]},
            {"time": "10:15", "name": "Mandello del Lario", "coord": [45.9189, 9.3178]},
            {"time": "10:25", "name": "Varenna-Esino", "coord": [46.01491, 9.28621], "is_end": True}
        ]
    },
    {
        "id": "route_09",
        "day": "DAY 05",
        "day_badge": "D05 · 科莫湖跨湖渡輪",
        "title": "瓦倫納碼頭 至 貝拉焦碼頭",
        "origin_name": "瓦倫納渡輪碼頭（Varenna Imbarcadero）",
        "origin_addr": "Via Imbarcadero Piazza Martiri Libertà, 23829 Varenna LC, 義大利",
        "dest_name": "貝拉焦渡輪碼頭（Bellagio Imbarcadero）",
        "dest_addr": "Piazza Giuseppe Mazzini 38, 22021 Bellagio CO, 義大利",
        "dep_time": "11:00",
        "arr_time": "11:15",
        "duration": "15 分（跨湖航行）",
        "ticket_title": "通票資訊 · 科莫湖中央湖區渡輪",
        "ticket_sub": "科莫湖中央湖區渡輪一日票（Centro Lago 一日通票）",
        "ticket_price": "持科莫湖渡輪一日通票搭乘（當日無限次）",
        "operator": "Navigazione Laghi",
        "operator_note": "持中央湖區渡輪一日通票登船，可至頂層戶外甲板，360 度飽覽科莫湖三叉水域與阿爾卑斯山倒影",
        "transit_type": "ferry",
        "transit_badge": "⛴️ Traghetto Navigazione Laghi",
        "line_color": "#0288d1",
        "gmaps_url": "https://maps.app.goo.gl/wvRt7pBbwpGbrCG66",
        "alert": None,
        "stops": [
            {"time": "11:00", "name": "Varenna 碼頭啟航", "coord": [46.01389, 9.28283], "is_start": True},
            {"time": "11:08", "name": "科莫湖中心水域（遠眺雙城全景）", "coord": [46.0020, 9.2710]},
            {"time": "11:15", "name": "抵達 Bellagio 渡輪碼頭", "coord": [45.98741, 9.26028], "is_end": True}
        ]
    },
    {
        "id": "route_10",
        "day": "DAY 06",
        "day_badge": "D06 · 南下熱那亞一等艙",
        "title": "米蘭中央車站 至 熱那亞王子廣場車站",
        "origin_name": "米蘭中央車站（Milano Centrale）",
        "origin_addr": "Piazza Duca d'Aosta 1, 20124 Milano MI, 義大利",
        "dest_name": "熱那亞王子廣場車站（Genova Piazza Principe）",
        "dest_addr": "Piazza del Principe, 16126 Genova GE, 義大利",
        "dep_time": "09:10",
        "arr_time": "10:48",
        "duration": "1 小時 38 分（5 站直達）",
        "ticket_title": "預訂席位 · 義鐵城際一等艙",
        "ticket_sub": "Trenitalia Intercity · 舒適對號座",
        "ticket_price": "單程 €22.00 起（持預訂一等艙對號票）",
        "operator": "義大利國鐵 Trenitalia Intercity",
        "operator_note": "一等艙空間寬敞含充電座，出站步行 2 分鐘直達五星 Grand Hotel Savoia",
        "transit_type": "train",
        "transit_badge": "🚆 Intercity IC 665（一等艙 Prima Classe）",
        "line_color": "#d93025",
        "gmaps_url": "https://maps.app.goo.gl/48Ey2uHb7NTHtRwP6",
        "alert": None,
        "stops": [
            {"time": "09:10", "name": "Milano Centrale", "coord": [45.48714, 9.20482], "is_start": True},
            {"time": "09:40", "name": "Pavia（帕維亞）", "coord": [45.1878, 9.1458]},
            {"time": "10:04", "name": "Voghera", "coord": [44.9961, 9.0069]},
            {"time": "10:20", "name": "Tortona", "coord": [44.8967, 8.8617]},
            {"time": "10:48", "name": "Genova Piazza Principe", "coord": [44.41651, 8.91849], "is_end": True}
        ]
    },
    {
        "id": "route_11",
        "day": "DAY 07",
        "day_badge": "D07 · 熱那亞地鐵核心漫遊",
        "title": "熱那亞王子廣場 至 法拉利廣場",
        "origin_name": "王子廣場地鐵站（Principe Metro）",
        "origin_addr": "Piazza Acquaverde / Principe Metro, 16126 Genova GE, 義大利",
        "dest_name": "法拉利廣場地鐵站（De Ferrari Metro）",
        "dest_addr": "Piazza Raffaele De Ferrari, 16121 Genova GE, 義大利",
        "dep_time": "09:30",
        "arr_time": "09:37",
        "duration": "7 分（4 站）",
        "ticket_title": "通票資訊 · 熱那亞城市通票",
        "ticket_sub": "Genova City Pass 24h（含 AMT 地鐵與市區公車）",
        "ticket_price": "持熱那亞城市通票搭乘（24H 無限次）",
        "operator": "熱那亞大眾運輸 AMT",
        "operator_note": "持熱那亞城市通票搭乘地鐵直達心臟地帶法拉利噴泉廣場，出站即達總督宮與卡洛·費利切劇院",
        "transit_type": "metro",
        "transit_badge": "🚇 Metropolitana Genova（往 Brignole）",
        "line_color": "#d93025",
        "gmaps_url": "https://maps.app.goo.gl/MxCjGBtwe5vxTroa7",
        "alert": None,
        "stops": [
            {"time": "09:30", "name": "Principe Metro（王子廣場站）", "coord": [44.41629, 8.91944], "is_start": True},
            {"time": "09:32", "name": "Darsena（舊港大學區）", "coord": [44.4139, 8.9264]},
            {"time": "09:34", "name": "San Giorgio（水族館站）", "coord": [44.4092, 8.9286]},
            {"time": "09:36", "name": "Sarzanese / Sant'Agostino", "coord": [44.4056, 8.9317]},
            {"time": "09:37", "name": "De Ferrari（法拉利廣場圓環噴泉）", "coord": [44.4076, 8.93439], "is_end": True}
        ]
    },
    {
        "id": "route_12",
        "day": "DAY 08",
        "day_badge": "D08 · 前往菲諾港門戶",
        "title": "熱那亞王子廣場 至 聖瑪格麗塔利古雷",
        "origin_name": "熱那亞王子廣場車站（Genova Piazza Principe）",
        "origin_addr": "Piazza del Principe, 16126 Genova GE, 義大利",
        "dest_name": "聖瑪格麗塔利古雷車站（S. Margherita Ligure）",
        "dest_addr": "Piazza Nobili 1 / S. Margherita F.S., 16038 Santa Margherita Ligure GE, 義大利",
        "dep_time": "09:47",
        "arr_time": "10:14",
        "duration": "27 分（2 站）",
        "ticket_title": "預訂席位 · 義鐵城際一等艙",
        "ticket_sub": "Trenitalia Intercity · 沿海快線對號座",
        "ticket_price": "單程 €12.50 起（持預訂一等艙對號票）",
        "operator": "義大利國鐵 Trenitalia Intercity",
        "operator_note": "出站即達聖瑪格麗塔站前公車圓環，無縫轉乘 782 號公車直達菲諾港",
        "transit_type": "train",
        "transit_badge": "🚆 Intercity IC 657（一等艙 Prima Classe）",
        "line_color": "#1a73e8",
        "gmaps_url": "https://maps.app.goo.gl/GsoUc1YVimFqa1756",
        "alert": None,
        "stops": [
            {"time": "09:47", "name": "Genova Piazza Principe", "coord": [44.41651, 8.91849], "is_start": True},
            {"time": "09:55", "name": "Genova Brignole", "coord": [44.4064, 8.9472]},
            {"time": "10:14", "name": "Santa Margherita Ligure-Portofino", "coord": [44.33645, 9.21618], "is_end": True}
        ]
    },
    {
        "id": "route_13",
        "day": "DAY 08",
        "day_badge": "D08 · 蔚藍海岸全景公車 · 19 站",
        "title": "聖瑪格麗塔車站 至 Portofino 終點站（782 號公車 · 19 站全景）",
        "origin_name": "聖瑪格麗塔車站（S. Margherita Ligure FS）",
        "origin_addr": "Piazza Nobili 1, 16038 Santa Margherita Ligure GE, 義大利",
        "dest_name": "Portofino 終點站（Portofino / Terminal · Piazza della Libertà）",
        "dest_addr": "Piazza della Libertà, 16034 Portofino GE, 義大利",
        "dep_time": "10:25",
        "arr_time": "10:43",
        "duration": "18 分（19 站緊貼懸崖碧海）",
        "ticket_title": "通票資訊 · AMT 菲諾港觀光公車",
        "ticket_sub": "MetDaily 一日票（含 782 觀光公車全日搭乘）",
        "ticket_price": "持 MetDaily 一日票搭乘（AMT APP 啟用）",
        "operator": "熱那亞大眾運輸 AMT",
        "operator_note": "持 MetDaily 一日票（AMT APP 啟用條碼）搭乘 782 號公車，緊貼利古里亞海岸線行駛直達 Portofino / Terminal 站（老港廣場旁）",
        "transit_type": "bus",
        "transit_badge": "🚌 AMT Linea 782（往 Portofino 終點站）",
        "line_color": "#0288d1",
        "gmaps_url": "https://maps.app.goo.gl/cBc8NDvorLvxuXHq8",
        "alert": "下車提示：782 號公車全程共 19 站，終點站即為「Portofino / Terminal」（菲諾港終點站）。前一站為 Chiesa S. Martino，下一站即抵達終點站下車，出站即是著名的菲諾港海灣與老港廣場（Piazza Martiri dell'Olivetta）！上車建議坐前進方向左側靠窗賞海景。",
        "stops": [
            {"time": "10:25", "name": "S. Margherita FS（火車站前起點站 Capolinea）", "coord": [44.33645, 9.21667], "is_start": True},
            {"time": "10:26", "name": "S. Margherita / Poste（郵局）", "coord": [44.3340, 9.2136]},
            {"time": "10:27", "name": "Bar Checco", "coord": [44.3335, 9.2135]},
            {"time": "10:28", "name": "Piazza Vittorio Veneto（海濱花園廣場）", "coord": [44.3325, 9.2140]},
            {"time": "10:29", "name": "Pizzerie", "coord": [44.3315, 9.2148]},
            {"time": "10:30", "name": "Pescheria（魚市碼頭）", "coord": [44.3305, 9.2152]},
            {"time": "10:31", "name": "Porto S. Margherita（遊艇港）", "coord": [44.3295, 9.2156]},
            {"time": "10:32", "name": "Hotel Regina Elena（麗晶酒店前）", "coord": [44.3275, 9.2160]},
            {"time": "10:33", "name": "Covo di Nord Est（傳奇懸崖俱樂部）", "coord": [44.3235, 9.2175]},
            {"time": "10:34", "name": "Baretto Punta Pedale", "coord": [44.3210, 9.2170]},
            {"time": "10:35", "name": "Bivio Via Repellini", "coord": [44.3190, 9.2165]},
            {"time": "10:36", "name": "Cervara（切爾瓦拉修道院角）", "coord": [44.3175, 9.2185]},
            {"time": "10:37", "name": "Capo Nord（北角懸崖）", "coord": [44.3140, 9.2180]},
            {"time": "10:38", "name": "Castello Paraggi（帕拉吉城堡）", "coord": [44.3120, 9.2150]},
            {"time": "10:39", "name": "Paraggi（帕拉吉翡翠海灣海灘）", "coord": [44.3105, 9.2130]},
            {"time": "10:40", "name": "Niasca（尼亞斯卡水上勝地）", "coord": [44.3075, 9.2110]},
            {"time": "10:41", "name": "Hotel Splendido（奢華酒店路口）", "coord": [44.3045, 9.2085]},
            {"time": "10:42", "name": "Portofino / Chiesa S. Martino（聖馬蒂諾教堂 · 下車前一站提示）", "coord": [44.3035, 9.2095]},
            {"time": "10:43", "name": "Portofino / Terminal（Capolinea 終點站 · 菲諾港老港廣場）", "coord": [44.30316, 9.20979], "is_end": True}
        ]
    },
    {
        "id": "route_14",
        "day": "DAY 09",
        "day_badge": "D09 · 跨越義法邊境第一段",
        "title": "熱那亞王子廣場 至 文提米利亞邊境車站",
        "origin_name": "熱那亞王子廣場車站（Genova Piazza Principe）",
        "origin_addr": "Piazza del Principe, 16126 Genova GE, 義大利",
        "dest_name": "文提米利亞邊境車站（Ventimiglia Stazione FS）",
        "dest_addr": "Piazza Cesare Battisti / Ventimiglia, 18039 Ventimiglia IM, 義大利",
        "dep_time": "08:58",
        "arr_time": "10:58",
        "duration": "2 小時 00 分（8 站沿海全景）",
        "ticket_title": "預訂席位 · 義鐵城際一等艙",
        "ticket_sub": "Trenitalia Intercity · 義大利里維埃拉海岸線",
        "ticket_price": "單程 €21.00 起（持預訂一等艙對號票）",
        "operator": "義大利國鐵 Trenitalia Intercity",
        "operator_note": "列車緊鄰地中海行駛，抵達後於 Sir Thomas 寄放行李並享用正宗熱那亞佛卡夏",
        "transit_type": "train",
        "transit_badge": "🚆 Intercity IC 633（一等艙 Prima Classe）",
        "line_color": "#d93025",
        "gmaps_url": "https://maps.app.goo.gl/GpCfwbp1WDjC1gyV9",
        "alert": None,
        "stops": [
            {"time": "08:58", "name": "Genova Piazza Principe", "coord": [44.41651, 8.91849], "is_start": True},
            {"time": "09:28", "name": "Savona（薩沃納）", "coord": [44.3072, 8.4714]},
            {"time": "09:42", "name": "Finale Ligure Marina", "coord": [44.1706, 8.3486]},
            {"time": "10:01", "name": "Albenga", "coord": [44.0489, 8.2167]},
            {"time": "10:09", "name": "Alassio", "coord": [44.0044, 8.1694]},
            {"time": "10:24", "name": "Imperia（因佩里亞）", "coord": [43.8894, 8.0417]},
            {"time": "10:38", "name": "Sanremo（聖雷莫音樂之城）", "coord": [43.8189, 7.7778]},
            {"time": "10:48", "name": "Bordighera", "coord": [43.7806, 7.6653]},
            {"time": "10:58", "name": "Ventimiglia（義法邊境車站）", "coord": [43.79245, 7.60973], "is_end": True}
        ]
    },
    {
        "id": "route_15",
        "day": "DAY 09",
        "day_badge": "D09 · 跨國雙層全景景觀列車",
        "title": "文提米利亞 至 尼斯城站",
        "origin_name": "文提米利亞邊境車站（Ventimiglia）",
        "origin_addr": "Piazza Cesare Battisti, 18039 Ventimiglia IM, 義大利",
        "dest_name": "尼斯中央車站（Gare de Nice-Ville）",
        "dest_addr": "Avenue Thiers, 06008 Nice, 法國",
        "dep_time": "15:00",
        "arr_time": "15:50",
        "duration": "50 分（10 站跨國海岸景觀）",
        "ticket_title": "購票 · 單程跨國區間車票價",
        "ticket_sub": "法國國鐵 SNCF TER PACA · 邊境站售票機現場購票",
        "ticket_price": "單程 €8.80（上車前黃色打票機打戳印）",
        "operator": "法國國鐵 SNCF TER PACA",
        "operator_note": "於文提米利亞邊境售票機購買 TER 區間票（上車前於黃機打卡），雙層景觀列車上層視野開闊，行經摩納哥、蒙頓、自由城直達尼斯",
        "transit_type": "train",
        "transit_badge": "🚆 SNCF TER Zou! 86060（雙層景觀列車）",
        "line_color": "#004b97",
        "gmaps_url": "https://maps.app.goo.gl/AWZJn2NJpk5uvbFv6",
        "alert": "座位推薦：請坐前進方向左側（靠海側），從芒通一路到尼斯享受無敵蔚藍海岸！",
        "stops": [
            {"time": "15:00", "name": "Ventimiglia（邊境起點）", "coord": [43.79124, 7.60759], "is_start": True},
            {"time": "15:07", "name": "Menton Garavan（跨入法國第一站）", "coord": [43.7844, 7.5186]},
            {"time": "15:12", "name": "Menton（芒通）", "coord": [43.7747, 7.4986]},
            {"time": "15:16", "name": "Carnolès", "coord": [43.7631, 7.4764]},
            {"time": "15:20", "name": "Roquebrune-Cap-Martin", "coord": [43.7583, 7.4569]},
            {"time": "15:26", "name": "Monaco-Monte-Carlo（摩納哥地下車站）", "coord": [43.7386, 7.4200]},
            {"time": "15:33", "name": "Èze-sur-Mer（艾茲懸崖下海濱）", "coord": [43.7225, 7.3606]},
            {"time": "15:37", "name": "Beaulieu-sur-Mer", "coord": [43.7078, 7.3328]},
            {"time": "15:40", "name": "Villefranche-sur-Mer（自由城海灣）", "coord": [43.7083, 7.3117]},
            {"time": "15:45", "name": "Nice Riquier", "coord": [43.7036, 7.2889]},
            {"time": "15:50", "name": "Nice-Ville（尼斯中央車站）", "coord": [43.70462, 7.26194], "is_end": True}
        ]
    },
    {
        "id": "route_16",
        "day": "DAY 10",
        "day_badge": "D10 · 盎格魯大道海景 BRT 快速公車",
        "title": "AC Hotel Nice 至 Opéra - Vieille Ville（公車 12+ 號）",
        "origin_name": "Grosso CUM / Promenade 站牌（AC Hotel 門前 · 盎格魯大道海景站）",
        "origin_addr": "Promenade des Anglais / Rue Honoré Sauvan, 06000 Nice, 法國",
        "dest_name": "Opéra - Vieille Ville 站（歌劇院旁 · 步行 1 分鐘進薩萊亞花市）",
        "dest_addr": "Quai des États-Unis / Rue Saint-François de Paule, 06300 Nice, 法國",
        "dep_time": "09:30",
        "arr_time": "09:36",
        "duration": "6 分（4 站沿海直達）",
        "ticket_title": "通票資訊 · 蔚藍海岸都會交通",
        "ticket_sub": "PASS SUD AZUR 南法通票感應卡（公車與輕軌全線通用）",
        "ticket_price": "持 PASS SUD AZUR 通票搭乘（上車感應）",
        "operator": "尼斯都會大眾運輸 Lignes d'Azur",
        "operator_note": "走出 AC Hotel 穿越馬路至盎格魯大道海邊站牌「Grosso CUM / Promenade」，搭乘 12+ 號快速公車（BHNS/BRT）沿蔚藍海岸行駛，直達「Opéra - Vieille Ville」站下車，下車過街穿過舊城拱門 1 分鐘即達薩萊亞花市（Cours Saleya）",
        "transit_type": "bus",
        "transit_badge": "🚌 Bus 12+（往 Hôpital Pasteur 方向 · 經舊城歌劇院）",
        "line_color": "#0288d1",
        "gmaps_url": "https://maps.app.goo.gl/NsS2bdp1kfg1Y53F9",
        "alert": "絕景下車提示：全程行駛於世界知名的盎格魯大道，右手邊即是天使灣地中海蔚藍波光！前一站為 Albert 1er / Verdun（阿爾貝一世花園），下一站即為「Opéra - Vieille Ville」站下車，下車穿過舊城拱門 1 分鐘直達薩萊亞花市（Cours Saleya）。",
        "stops": [
            {"time": "09:30", "name": "Grosso CUM / Promenade（AC Hotel 門前 · 盎格魯大道海邊站牌 · 起點上車）", "coord": [43.69231, 7.25074], "is_start": True},
            {"time": "09:32", "name": "Gambetta / Promenade", "coord": [43.6938, 7.2546]},
            {"time": "09:34", "name": "Congrès / Promenade（地中海宮殿酒店前）", "coord": [43.6955, 7.2608]},
            {"time": "09:35", "name": "Albert 1er / Verdun（阿爾貝一世花園 · 下車前一站提示）", "coord": [43.6963, 7.2676]},
            {"time": "09:36", "name": "Opéra - Vieille Ville（終點下車 · 歌劇院旁 · 步行 1 分鐘進薩萊亞花市）", "coord": [43.69748, 7.2734], "is_end": True}
        ]
    },
    {
        "id": "route_17",
        "day": "DAY 11",
        "day_badge": "D11 · 濱海自由城半日慢遊",
        "title": "尼斯城站 至 濱海自由城",
        "origin_name": "尼斯中央車站（Gare de Nice-Ville）",
        "origin_addr": "Avenue Thiers, 06008 Nice, 法國",
        "dest_name": "濱海自由城車站（Gare de Villefranche-sur-Mer）",
        "dest_addr": "Avenue Georges Clemenceau, 06230 Villefranche-sur-Mer, 法國",
        "dep_time": "09:45",
        "arr_time": "09:52",
        "duration": "7 分（2 站直達懸崖海灣）",
        "ticket_title": "通票資訊 · 蔚藍海岸鐵路與通票",
        "ticket_sub": "PASS SUD AZUR 蔚藍海岸通票（涵蓋 TER 尼斯↔自由城）",
        "ticket_price": "持 PASS SUD AZUR 通票搭乘（進出站免購票）",
        "operator": "法國國鐵 SNCF TER Zou!",
        "operator_note": "持 PASS SUD AZUR 通票搭乘 TER 懸崖景觀列車，出站走下一小段階梯即達金色細石沙灘與 Mayssa Beach 海景餐廳",
        "transit_type": "train",
        "transit_badge": "🚆 SNCF TER Zou!（往 Ventimiglia 方向）",
        "line_color": "#004b97",
        "gmaps_url": "https://maps.app.goo.gl/Jmj5S49pD76Z6SgLA",
        "alert": None,
        "stops": [
            {"time": "09:45", "name": "Nice-Ville", "coord": [43.70462, 7.26194], "is_start": True},
            {"time": "09:48", "name": "Nice Riquier", "coord": [43.7036, 7.2889]},
            {"time": "09:52", "name": "Villefranche-sur-Mer", "coord": [43.70706, 7.31415], "is_end": True}
        ]
    },
    {
        "id": "route_18",
        "day": "DAY 12",
        "day_badge": "D12 · 費拉角貴族莊園巡禮",
        "title": "尼斯舊港 至 羅斯柴爾德花園別墅",
        "origin_name": "尼斯舊港站（Port Lympia）",
        "origin_addr": "Quai Amiral Infernet / Port Lympia, 06300 Nice, 法國",
        "dest_name": "羅斯柴爾德花園別墅正門（Passable / Rothschild）",
        "dest_addr": "1 Avenue Ephrussi de Rothschild, 06230 Saint-Jean-Cap-Ferrat, 法國",
        "dep_time": "09:30",
        "arr_time": "09:54",
        "duration": "24 分（16 站沿海全景公車）",
        "ticket_title": "通票資訊 · Lignes d'Azur 觀光公車",
        "ticket_sub": "PASS SUD AZUR 南法通票感應卡（涵蓋 15 號海濱公車）",
        "ticket_price": "持 PASS SUD AZUR 通票搭乘（上車感應）",
        "operator": "尼斯都會大眾運輸 Lignes d'Azur",
        "operator_note": "持 PASS SUD AZUR 通票搭乘 15 號公車直達別墅大門口 Passable / Rothschild 站，完全免去徒步爬坡困擾",
        "transit_type": "bus",
        "transit_badge": "🚌 Bus 15（往 Port de Saint-Jean）",
        "line_color": "#0288d1",
        "gmaps_url": "https://maps.app.goo.gl/KsrrBWECHJHFNxME6",
        "alert": "絕景提示：沿著下濱海路行駛，可從高處俯瞰濱海自由城海灣的豪華遊艇！",
        "stops": [
            {"time": "09:30", "name": "Port Lympia（舊港起點站）", "coord": [43.6968, 7.28392], "is_start": True},
            {"time": "09:34", "name": "Saint-Aignan", "coord": [43.6949, 7.2935]},
            {"time": "09:38", "name": "Octroi（自由城觀景點 · 俯瞰自由城海灣）", "coord": [43.7021, 7.3078]},
            {"time": "09:42", "name": "Léopold II（全景高點海濱路）", "coord": [43.7081, 7.3130]},
            {"time": "09:48", "name": "Pont Saint-Jean（費拉角半島入口 · 下車前一站提示）", "coord": [43.7015, 7.3266]},
            {"time": "09:54", "name": "Passable / Rothschild（別墅正門口 · 終點下車）", "coord": [43.69665, 7.32847], "is_end": True}
        ]
    }
]

DAY_DATES = {
    "DAY 01": "10/15（四）",
    "DAY 02": "10/16（五）",
    "DAY 03": "10/17（六）",
    "DAY 04": "10/18（日）",
    "DAY 05": "10/19（一）",
    "DAY 06": "10/20（二）",
    "DAY 07": "10/21（三）",
    "DAY 08": "10/22（四）",
    "DAY 09": "10/23（五）",
    "DAY 10": "10/24（六）",
    "DAY 11": "10/25（日）",
    "DAY 12": "10/26（一）",
    "DAY 13": "10/27（二）",
    "DAY 14": "10/28（三）",
    "DAY 15": "10/29（四）",
}

for r in ROUTES_DATA:
    r["date"] = DAY_DATES.get(r.get("day", ""), "")

ROUTE_PDF_MAPPING = {
    "route_01": "01_D02_MXP_至_米蘭中央車站.pdf",
    "route_02": "02_D03_米蘭中央車站_至_米蘭大教堂.pdf",
    "route_03": "03_D03_斯卡拉大劇院_至_蒙塔內利花園.pdf",
    "route_04": "04_D03_威尼斯門_至_Via_Galvani加爾瓦尼站.pdf",
    "route_05": "05_D04_米蘭中央車站_至_貝爾加莫車站.pdf",
    "route_06": "06_D04_貝爾加莫車站_至_Vittorio_Emanuele47.pdf",
    "route_07": "07_D04_Delle_Mura_San_Giacomo_至_Paleocapa1車站返程.pdf",
    "route_08": "08_D05_米蘭中央車站_至_瓦倫納科莫湖.pdf",
    "route_09": "09_D05_瓦倫納碼頭_至_貝拉焦跨湖渡輪.pdf",
    "route_10": "10_D06_米蘭中央車站_至_熱那亞王子廣場.pdf",
    "route_11": "11_D07_熱那亞王子廣場_至_法拉利廣場地鐵.pdf",
    "route_12": "12_D08_熱那亞王子廣場_至_聖瑪格麗塔.pdf",
    "route_13": "13_D08_聖瑪格麗塔_至_Portofino終點站782公車.pdf",
    "route_14": "14_D09_熱那亞王子廣場_至_文提米利亞邊境.pdf",
    "route_15": "15_D09_文提米利亞_至_尼斯城站TER雙層列車.pdf",
    "route_16": "16_D10_ACHotel_至_Opéra_Vieille_Ville公車12號.pdf",
    "route_17": "17_D11_尼斯城站_至_濱海自由城TER.pdf",
    "route_18": "18_D12_尼斯舊港_至_費拉角別墅15號公車.pdf",
}

def generate_routes_html():
    """Build the interactive, printable routes.html web application."""
    html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>北義 × 南法蔚藍海岸 15 日 · 全程起點到終點路線地圖指引 (Google Maps Transit)</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Noto+Serif+TC:wght@500;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --gold-dark: #8c6a28;
      --gold-mid: #b8862d;
      --gold-light: #f7eed7;
      --navy-dark: #0b1e36;
      --navy-sub: #163259;
      --navy-light: #f0f4f9;
      --text-main: #202124;
      --text-sub: #5f6368;
      --border-line: #dadce0;
      --bg-page: #f8f9fa;
    }}

    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      color: var(--text-main);
      background: var(--bg-page);
      -webkit-font-smoothing: antialiased;
      line-height: 1.5;
    }}

    /* Top App Bar */
    .top-app-header {{
      background: linear-gradient(135deg, var(--navy-dark) 0%, var(--navy-sub) 100%);
      color: #fff;
      padding: 16px 24px;
      position: sticky;
      top: 0;
      z-index: 1000;
      box-shadow: 0 4px 16px rgba(0,0,0,0.18);
    }}
    .header-inner {{
      max-width: 1100px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .brand-title {{
      font-family: 'Cinzel', 'Noto Serif TC', serif;
      font-size: 19px;
      font-weight: 700;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .brand-title span {{
      color: var(--gold-mid);
    }}
    .header-actions {{
      display: flex;
      gap: 10px;
      align-items: center;
    }}
    .nav-btn {{
      padding: 7px 14px;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      cursor: pointer;
    }}
    .nav-btn-gold {{
      background: linear-gradient(135deg, #d4af37 0%, #b8862d 100%);
      color: #0b1e36;
      border: none;
    }}
    .nav-btn-gold:hover {{
      background: #e2be4b;
      box-shadow: 0 2px 8px rgba(212,175,55,0.4);
    }}
    .nav-btn-outline {{
      background: transparent;
      color: #fff;
      border: 1px solid rgba(255,255,255,0.3);
    }}
    .nav-btn-outline:hover {{
      background: rgba(255,255,255,0.1);
      border-color: #fff;
    }}

    /* Filter Bar */
    .filter-bar {{
      background: #fff;
      border-bottom: 1px solid var(--border-line);
      padding: 10px 24px;
      position: sticky;
      top: 64px;
      z-index: 999;
    }}
    .filter-inner {{
      max-width: 1100px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }}
    .filter-group {{
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding-bottom: 2px;
    }}
    .filter-chip {{
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 13px;
      font-weight: 500;
      background: #f1f3f4;
      color: #3c4043;
      border: 1px solid transparent;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.15s ease;
    }}
    .filter-chip.active, .filter-chip:hover {{
      background: var(--navy-dark);
      color: #fff;
      border-color: var(--navy-dark);
    }}
    .global-map-toggle {{
      display: flex;
      align-items: center;
      gap: 4px;
      background: #f1f3f4;
      border: 1px solid #dadce0;
      padding: 3px 6px;
      border-radius: 20px;
    }}
    .toggle-label {{
      font-size: 11px;
      font-weight: 700;
      color: #5f6368;
      padding-left: 6px;
    }}
    .global-mode-btn {{
      border: none;
      background: transparent;
      font-size: 11px;
      font-weight: 600;
      padding: 4px 10px;
      border-radius: 14px;
      cursor: pointer;
      color: #5f6368;
      transition: all 0.15s ease;
    }}
    .global-mode-btn.active {{
      background: #1a73e8;
      color: #fff;
      box-shadow: 0 1px 3px rgba(26,115,232,0.3);
    }}

    /* Main Container */
    .content-container {{
      max-width: 900px;
      margin: 24px auto 60px;
      padding: 0 16px;
    }}

    /* Route Card Styled exactly like 1.pdf & 2.pdf */
    .route-card {{
      background: #fff;
      border: 1px solid var(--border-line);
      border-radius: 12px;
      margin-bottom: 36px;
      padding: 22px 24px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.06);
      page-break-after: always;
      position: relative;
    }}

    .route-header-top {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 16px;
      border-bottom: 1px solid #e8eaed;
      padding-bottom: 12px;
      margin-bottom: 14px;
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
      background: var(--gold-light);
      color: var(--gold-dark);
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
      line-height: 1.3;
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
      margin-top: 4px;
    }}

    /* Map Box & Toolbar */
    .map-toolbar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #f8f9fa;
      border: 1px solid #dadce0;
      border-bottom: none;
      border-top-left-radius: 8px;
      border-top-right-radius: 8px;
      padding: 6px 12px;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .map-tab-group {{
      display: flex;
      gap: 6px;
    }}
    .map-tab-btn {{
      background: #fff;
      border: 1px solid #dadce0;
      color: #5f6368;
      padding: 5px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      transition: all 0.15s ease;
    }}
    .map-tab-btn:hover {{
      background: #f1f3f4;
      color: #202124;
    }}
    .map-tab-btn.active {{
      background: #1a73e8;
      border-color: #1a73e8;
      color: #fff;
      box-shadow: 0 1px 3px rgba(26,115,232,0.3);
    }}
    .map-ext-btn {{
      color: #1a73e8;
      font-weight: 600;
      font-size: 12px;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 4px 8px;
      border-radius: 4px;
      transition: background 0.15s ease;
    }}
    .map-ext-btn:hover {{
      background: #e8f0fe;
      text-decoration: underline;
    }}

    .map-box {{
      width: 100%;
      height: 380px;
      border-bottom-left-radius: 8px;
      border-bottom-right-radius: 8px;
      overflow: hidden;
      border: 1px solid #dadce0;
      margin-bottom: 16px;
      position: relative;
      background: #e8eaed;
    }}
    .gmap-embed-frame {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      border: none;
      z-index: 2;
      display: block;
    }}
    .map-render {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: 1;
    }}
    .map-box.show-osm .gmap-embed-frame {{
      display: none;
    }}
    .map-box.show-osm .map-render {{
      z-index: 3;
    }}
    .map-credit {{
      position: absolute;
      bottom: 8px;
      right: 8px;
      background: rgba(255,255,255,0.92);
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 11px;
      color: #5f6368;
      z-index: 10;
      box-shadow: 0 1px 4px rgba(0,0,0,0.15);
      pointer-events: none;
    }}

    /* Card Details */
    .details-box {{
      border: 1px solid #e8eaed;
      border-radius: 8px;
      padding: 16px 20px;
      background: #fafafa;
    }}
    .fare-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #e8eaed;
      padding-bottom: 12px;
      margin-bottom: 16px;
    }}
    .fare-title {{
      font-size: 14px;
      font-weight: 700;
      color: #202124;
    }}
    .fare-desc {{
      font-size: 12px;
      color: #5f6368;
    }}
    .fare-val {{
      font-size: 15px;
      font-weight: 700;
      color: #188038;
      text-align: right;
    }}

    /* Timeline matching 1.pdf & 2.pdf */
    .transit-timeline {{
      position: relative;
      padding-left: 28px;
      margin-top: 8px;
    }}
    .t-node {{
      position: relative;
      padding-bottom: 16px;
    }}
    .t-node:last-child {{
      padding-bottom: 0;
    }}
    .t-pin {{
      position: absolute;
      left: -28px;
      top: 2px;
      width: 18px;
      height: 18px;
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
      border-color: var(--active-line-color, #d93025);
      background: var(--active-line-color, #d93025);
    }}
    .t-pin.end::after {{
      content: '';
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: #fff;
    }}
    .t-line {{
      position: absolute;
      left: -20px;
      top: 20px;
      bottom: -2px;
      width: 4px;
      background: #dadce0;
    }}
    .t-line.transit-active {{
      background: var(--active-line-color, #d93025);
    }}

    .t-header {{
      display: flex;
      align-items: baseline;
      gap: 10px;
    }}
    .t-time {{
      font-size: 14px;
      font-weight: 700;
      color: #202124;
      min-width: 55px;
    }}
    .t-name {{
      font-size: 14px;
      font-weight: 700;
      color: #202124;
    }}
    .t-addr {{
      font-size: 12px;
      color: #70757a;
      margin-top: 2px;
      margin-left: 65px;
    }}

    .transit-card-inner {{
      margin: 10px 0 10px 65px;
      padding: 12px 16px;
      background: #fff;
      border-radius: 6px;
      border: 1px solid #e8eaed;
      border-left: 4px solid var(--active-line-color, #d93025);
    }}
    .badge-transit {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: var(--active-line-color, #d93025);
      color: #fff;
      padding: 4px 10px;
      border-radius: 4px;
      font-size: 13px;
      font-weight: 700;
    }}
    .transit-meta {{
      font-size: 13px;
      font-weight: 600;
      color: #3c4043;
      margin-top: 6px;
    }}
    .transit-op {{
      font-size: 12px;
      color: #70757a;
      margin-top: 3px;
    }}
    .transit-alert {{
      margin-top: 8px;
      padding: 6px 10px;
      background: #fef7e0;
      border: 1px solid #f9ab00;
      border-radius: 4px;
      font-size: 12px;
      color: #b06000;
      font-weight: 500;
    }}

    /* Intermediate stops */
    .stop-series {{
      margin: 10px 0 0 65px;
      border-left: 2px solid #dadce0;
      padding-left: 14px;
    }}
    .stop-series.two-cols {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 4px 16px;
      padding-left: 12px;
    }}
    .stop-row {{
      font-size: 12px;
      color: #5f6368;
      margin-bottom: 6px;
      display: flex;
      gap: 12px;
      align-items: center;
    }}
    .stop-dot {{
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: #70757a;
    }}
    .stop-t {{
      color: #80868b;
      min-width: 45px;
    }}

    /* Card Actions & Live Link */
    .card-footer-actions {{
      margin-top: 16px;
      padding-top: 12px;
      border-top: 1px solid #e8eaed;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
    }}
    .action-links {{
      display: flex;
      gap: 8px;
    }}
    .btn-gmaps {{
      background: #1a73e8;
      color: #fff;
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: background 0.15s ease;
    }}
    .btn-gmaps:hover {{
      background: #1557b0;
    }}
    .btn-print-one {{
      background: #fff;
      border: 1px solid #dadce0;
      color: #3c4043;
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      text-decoration: none;
    }}
    .btn-print-one:hover {{
      background: #f1f3f4;
    }}

    .official-url {{
      font-size: 11px;
      color: #70757a;
      word-break: break-all;
    }}

    @media (max-width: 680px) {{
      .route-card {{
        padding: 16px 14px;
      }}
      .route-header-top {{
        gap: 12px;
      }}
      .day-hero-num {{
        font-size: 22px;
      }}
      .day-hero-date {{
        font-size: 11px;
        padding: 1px 6px;
      }}
      .route-title-text {{
        font-size: 14px;
      }}
      .route-time-text {{
        font-size: 12px;
      }}
    }}

    /* Print Styles */
    @media print {{
      .top-app-header, .filter-bar, .card-footer-actions, .map-toolbar {{
        display: none !important;
      }}
      body {{
        background: #fff !important;
      }}
      .content-container {{
        max-width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
      }}
      .route-card {{
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin-bottom: 0 !important;
        page-break-after: always !important;
      }}
      .map-box {{
        height: 350px !important;
        border: 1px solid #dadce0 !important;
        border-radius: 8px !important;
      }}
      .gmap-embed-frame {{
        display: none !important;
      }}
      .map-render {{
        position: relative !important;
        height: 350px !important;
        width: 100% !important;
        display: block !important;
        z-index: 10 !important;
        opacity: 1 !important;
        visibility: visible !important;
      }}
      .credit-text-gmap {{
        display: none !important;
      }}
      .credit-text-osm {{
        display: inline !important;
      }}
      @page {{
        size: A4 portrait;
        margin: 12mm 15mm;
      }}
    }}
  </style>
</head>
<body>

  <!-- Top App Bar -->
  <header class="top-app-header">
    <div class="header-inner">
      <div class="brand-title">
        <span>TRAVEL EURO</span> · 全程起點到終點路線地圖指引 (18 條 Transit)
      </div>
      <div class="header-actions">
        <a href="route/all_routes.pdf" download class="nav-btn nav-btn-gold">📥 下載 18 條路線 PDF 合輯</a>
        <a href="print-handbook.html" class="nav-btn nav-btn-outline">📖 隨身手冊</a>
        <a href="index.html" class="nav-btn nav-btn-outline">🌐 首頁</a>
        <button onclick="window.print()" class="nav-btn nav-btn-outline">🖨️ 列印全書</button>
      </div>
    </div>
  </header>

  <!-- Filter Chips & Map Mode -->
  <nav class="filter-bar">
    <div class="filter-inner">
      <div class="filter-group">
        <button class="filter-chip active" onclick="filterRoutes('all', this)">全部 18 條路線</button>
        <button class="filter-chip" onclick="filterRoutes('milan', this)">D02–03 米蘭都會 (4)</button>
        <button class="filter-chip" onclick="filterRoutes('bergamo', this)">D04 貝爾加莫 (3)</button>
        <button class="filter-chip" onclick="filterRoutes('como', this)">D05 科莫湖雙城 (2)</button>
        <button class="filter-chip" onclick="filterRoutes('genova', this)">D06–08 熱那亞與菲諾港 (4)</button>
        <button class="filter-chip" onclick="filterRoutes('nice', this)">D09–12 南法尼斯與蔚藍海岸 (5)</button>
      </div>
      <div class="global-map-toggle">
        <span class="toggle-label">🌐 地圖視角：</span>
        <button class="global-mode-btn active" id="btn_global_gmap" onclick="setGlobalMapMode('gmap')">Google 即時嵌入</button>
        <button class="global-mode-btn" id="btn_global_osm" onclick="setGlobalMapMode('osm')">Google 高清列印版</button>
      </div>
    </div>
  </nav>

  <!-- Main Content Container -->
  <main class="content-container" id="routes-wrapper">
"""

    for r in ROUTES_DATA:
        alert_html = f'<div class="transit-alert">{r["alert"]}</div>' if r.get("alert") else ""
        stops_json = json.dumps(r["stops"], ensure_ascii=False)
        pdf_file = ROUTE_PDF_MAPPING.get(r["id"], f"{r['id']}.pdf")
        
        start_c = r["stops"][0]["coord"]
        end_c = r["stops"][-1]["coord"]
        embed_url = f"https://maps.google.com/maps?saddr={start_c[0]},{start_c[1]}&daddr={end_c[0]},{end_c[1]}&dirflg=r&output=embed"

        # Intermediate stops rows
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
        series_class = "stop-series two-cols" if len(r["stops"]) > 10 else "stop-series"

        # Category for filter
        cat = "milan"
        if "D04" in r["day_badge"]: cat = "bergamo"
        elif "D05" in r["day_badge"]: cat = "como"
        elif "D06" in r["day_badge"] or "D07" in r["day_badge"] or "D08" in r["day_badge"]: cat = "genova"
        elif "D09" in r["day_badge"] or "D10" in r["day_badge"] or "D11" in r["day_badge"] or "D12" in r["day_badge"]: cat = "nice"
        elif "D14" in r["day_badge"]: cat = "airport"

        html_content += f"""
    <!-- Route Card: {r['id']} -->
    <article class="route-card" id="{r['id']}" data-cat="{cat}" style="--active-line-color: {r['line_color']};">
      <div class="route-header-top">
        <div class="day-hero-badge">
          <div class="day-hero-num">{r['day']}</div>
          <div class="day-hero-date">{r['date']}</div>
        </div>
        <div class="route-info-col">
          <span class="route-day-tag">{r['day_badge']}</span>
          <div class="route-title-text">{r['title']}</div>
          <div class="route-addr-text">{r['origin_addr'][:35]}... 至 {r['dest_addr'][:35]}...</div>
          <div class="route-time-text">{r['dep_time']} - {r['arr_time']}（{r['duration']}）</div>
        </div>
      </div>

      <!-- Map Toolbar -->
      <div class="map-toolbar">
        <div class="map-tab-group">
          <button type="button" class="map-tab-btn active" id="tab_gmap_{r['id']}" onclick="toggleMapTab('{r['id']}', 'gmap')">
            <span class="tab-icon">🌐</span> Google Maps 即時互動視圖
          </button>
          <button type="button" class="map-tab-btn" id="tab_osm_{r['id']}" onclick="toggleMapTab('{r['id']}', 'osm')">
            <span class="tab-icon">🗺️</span> Google 地圖高清列印視圖
          </button>
        </div>
        <a href="{r['gmaps_url']}" target="_blank" rel="noopener" class="map-ext-btn">
          <span>↗️ 在 Google Maps App 開啟路線</span>
        </a>
      </div>

      <div class="map-box" id="mapbox_{r['id']}">
        <!-- Google Maps Live Embed (Default Active) -->
        <iframe 
          id="gmap_frame_{r['id']}"
          class="gmap-embed-frame"
          src="{embed_url}"
          loading="lazy"
          allowfullscreen
          referrerpolicy="no-referrer-when-downgrade">
        </iframe>

        <!-- Leaflet Vector Map with Google Maps Tiles (Underneath, ready for print & high-res view) -->
        <div id="map_{r['id']}" class="map-render"></div>

        <div class="map-credit" id="credit_{r['id']}">
          <span class="credit-text-gmap">Google 地圖即時大眾運輸導航指引 · 可縮放拖曳與點選班次</span>
          <span class="credit-text-osm" style="display:none;">地圖底圖 &copy; Google Maps · 高解析度大眾運輸路線</span>
        </div>
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
          <!-- Start Node -->
          <div class="t-node">
            <div class="t-pin start"></div>
            <div class="t-line"></div>
            <div class="t-header">
              <span class="t-time">{r['dep_time']}</span>
              <span class="t-name">{r['origin_name']}</span>
            </div>
            <div class="t-addr">{r['origin_addr']}</div>
          </div>

          <!-- Transit Info Block -->
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

            <!-- Intermediate Stops List -->
            <div class="{series_class}">
              {stops_html}
            </div>
          </div>

          <!-- End Node -->
          <div class="t-node">
            <div class="t-pin end"></div>
            <div class="t-header">
              <span class="t-time">{r['arr_time']}</span>
              <span class="t-name">抵達：{r['dest_name']}</span>
            </div>
            <div class="t-addr">{r['dest_addr']}</div>
          </div>
        </div>

        <div class="card-footer-actions">
          <div class="action-links">
            <a href="{r['gmaps_url']}" target="_blank" rel="noopener" class="btn-gmaps">
              🧭 開啟 Google 地圖即時 GPS 導航
            </a>
            <a href="route/{pdf_file}" download class="btn-print-one">
              📥 下載路線 PDF
            </a>
            <button onclick="printSingleRoute('{r['id']}')" class="btn-print-one">
              🖨️ 列印此路線
            </button>
          </div>
          <div class="official-url">
            直達連結：{r['gmaps_url']}
          </div>
        </div>
      </div>
    </article>
    """

    # Add JavaScript to initialize all Leaflet maps
    maps_init_js = ""
    for r in ROUTES_DATA:
        stops_json = json.dumps([[s["coord"][0], s["coord"][1]] for s in r["stops"]])
        line_color = r["line_color"]
        map_id = f"map_{r['id']}"
        maps_init_js += f"""
    (function() {{
      var stops_{r['id']} = {stops_json};
      var map_{r['id']} = L.map('{map_id}', {{
        zoomControl: false,
        attributionControl: false,
        scrollWheelZoom: false
      }});
      window['leaflet_map_{r['id']}'] = map_{r['id']};
      
      L.tileLayer('https://{{s}}.google.com/vt/lyrs=m&x={{x}}&y={{y}}&z={{z}}', {{
        maxZoom: 20,
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
      }}).addTo(map_{r['id']});

      var poly_{r['id']} = L.polyline(stops_{r['id']}, {{
        color: '{line_color}',
        weight: 6,
        opacity: 0.9,
        lineCap: 'round',
        lineJoin: 'round'
      }}).addTo(map_{r['id']});

      map_{r['id']}.fitBounds(poly_{r['id']}.getBounds(), {{
        padding: [35, 35], maxZoom: 15
      }});

      // Origin Pin
      L.circleMarker(stops_{r['id']}[0], {{
        radius: 8,
        color: '#1a73e8',
        fillColor: '#fff',
        fillOpacity: 1,
        weight: 3
      }}).addTo(map_{r['id']});

      // Destination Pin
      L.circleMarker(stops_{r['id']}[stops_{r['id']}.length - 1], {{
        radius: 8,
        color: '{line_color}',
        fillColor: '{line_color}',
        fillOpacity: 1,
        weight: 3
      }}).addTo(map_{r['id']});

      // Intermediate station dots
      for(var i = 1; i < stops_{r['id']}.length - 1; i++) {{
        L.circleMarker(stops_{r['id']}[i], {{
          radius: 4,
          color: '{line_color}',
          fillColor: '#fff',
          fillOpacity: 1,
          weight: 2
        }}).addTo(map_{r['id']});
      }}
    }})();
"""

    html_content += f"""
  </main>

  <script>
    // Initialize all Leaflet maps
    {maps_init_js}

    // Toggle individual map tab between Google Maps Live Embed and OSM
    function toggleMapTab(routeId, mode) {{
      var mapbox = document.getElementById('mapbox_' + routeId);
      var btnGmap = document.getElementById('tab_gmap_' + routeId);
      var btnOsm = document.getElementById('tab_osm_' + routeId);
      var creditBox = document.getElementById('credit_' + routeId);
      
      if (!mapbox) return;

      if (mode === 'gmap') {{
        mapbox.classList.remove('show-osm');
        if (btnGmap) btnGmap.classList.add('active');
        if (btnOsm) btnOsm.classList.remove('active');
        if (creditBox) {{
          var tg = creditBox.querySelector('.credit-text-gmap');
          var to = creditBox.querySelector('.credit-text-osm');
          if (tg) tg.style.display = 'inline';
          if (to) to.style.display = 'none';
        }}
      }} else {{
        mapbox.classList.add('show-osm');
        if (btnGmap) btnGmap.classList.remove('active');
        if (btnOsm) btnOsm.classList.add('active');
        if (creditBox) {{
          var tg = creditBox.querySelector('.credit-text-gmap');
          var to = creditBox.querySelector('.credit-text-osm');
          if (tg) tg.style.display = 'none';
          if (to) to.style.display = 'inline';
        }}
        if (window['leaflet_map_' + routeId]) {{
          setTimeout(function() {{
            window['leaflet_map_' + routeId].invalidateSize();
          }}, 60);
        }}
      }}
    }}

    // Global toggle for all 18 cards
    function setGlobalMapMode(mode) {{
      var allCards = document.querySelectorAll('.route-card');
      allCards.forEach(function(card) {{
        toggleMapTab(card.id, mode);
      }});
      var btnGlobalGmap = document.getElementById('btn_global_gmap');
      var btnGlobalOsm = document.getElementById('btn_global_osm');
      if (btnGlobalGmap && btnGlobalOsm) {{
        if (mode === 'gmap') {{
          btnGlobalGmap.classList.add('active');
          btnGlobalOsm.classList.remove('active');
        }} else {{
          btnGlobalGmap.classList.remove('active');
          btnGlobalOsm.classList.add('active');
        }}
      }}
    }}

    // Filter cards
    function filterRoutes(category, btn) {{
      var chips = document.querySelectorAll('.filter-chip');
      chips.forEach(function(c) {{ c.classList.remove('active'); }});
      btn.classList.add('active');

      var cards = document.querySelectorAll('.route-card');
      cards.forEach(function(card) {{
        if (category === 'all' || card.getAttribute('data-cat') === category) {{
          card.style.display = 'block';
        }} else {{
          card.style.display = 'none';
        }}
      }});
      // Trigger map resize so tiles render properly when shown
      window.dispatchEvent(new Event('resize'));
    }}

    // Print single route
    function printSingleRoute(cardId) {{
      var cards = document.querySelectorAll('.route-card');
      cards.forEach(function(c) {{
        if (c.id !== cardId) c.style.display = 'none';
        else c.style.display = 'block';
      }});
      window.print();
      // restore after print
      setTimeout(function() {{
        cards.forEach(function(c) {{ c.style.display = 'block'; }});
      }}, 1000);
    }}
  </script>
</body>
</html>
"""

    out_path = "/Users/sher/Documents/trvalpremium/routes.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated {out_path} ({len(html_content)} bytes)")

if __name__ == "__main__":
    generate_routes_html()
