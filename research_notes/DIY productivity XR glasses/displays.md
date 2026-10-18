# Displays and driver boards for DIY productivity XR glasses (2025–2026)

> Method note (researcher): the research environment blocked direct page fetches (WebFetch DNS failures; curl CONNECT returned 403), so all findings below come from search-engine result summaries of the cited pages, not full page reads. Prices are as shown in those listings when searched (Oct 2026) and may be stale or vary by option. Treat each price as indicative and confirm on the live listing.

## 1. Sony micro-OLED panels (ECX335 / ECX339 / ECX344 / newer) — availability to individuals, prices, driver boards

### Takeaway
Hobbyists can buy older Sony micro-OLED panels through resellers (Tindie "Display Components", Panox, Youritech, Spiritbing, Gesight) with HDMI driver boards. Examples are the 0.71" 1920x1080 ECX335 family and the 0.5" 1600x1200 ECX339A. A panel plus HDMI board costs about $240–$400 per eye, and ready-made dual-eye HDMI kits exist (~$528). Sony's 4K-class 1.3" ECX344A (3552x3840) was not found for sale with a hobbyist driver board.

### Cited Findings
- **ECX335 (0.71", 1920x1080):** Display Components (Tindie) sells the Sony ECX335S panel for $238. It also sells an HDMI driver board for the ECX335A/ECX335S for $95 (37.5x16.5 mm, 3.5–5 V, brightness adjustment) and a dual-eye HDMI version for $528. The kit is sold as display + optional HDMI board + optional optics. — [Tindie HDMI board](https://www.tindie.com/products/oled-modules/hdmi-driver-board-for-071-inch-micro-oled-display/); [Tindie ECX335S](https://www.tindie.com/products/oled-modules/sony-ecx335s-micro-071-oled-display-1920x1080/)
- Gesight sells a 0.71" micro-OLED 1920x1080 LVDS HDMI controller board for $135. It is designed for the ECX335AF, measures 40x25 mm, and has a single HDMI input with USB power. — [Gesight](https://gesight.com/product/071microoled200/)
- Spiritbing sells Sony ECX335BG modules bundled with a driver board for $342.99–$399.99. It states the board is not made by Sony but is "verified compatible." — [Spiritbing](https://www.spiritbing.com/detail/Sony-Ecx335bg-Oled-Microdisplay-Module-With-Driver-Board_zr19dc99c78baa9.html)
- Panox Display sells ECX335AF/ECX335B/ECX335SN panels. It says the 3 models share an interface (LVDS) and can be driven by the same HDMI-to-LVDS board. The page is roughly 5 years old (flag: older data). — [Panox](https://www.panoxdisplay.com/micro-display/sony-0-71-inch-1920x1080-micro-oled-lvds.html)
- A Global Sources listing (Shenzhen Control Electronic) offers the ECX335S with a controller board from $98 (wholesale, MOQ unclear). — [Global Sources](https://www.globalsources.com/product/head-up-display_1208736760f.htm)
- Tek Gear sells the O8 driver board (two mini-HDMI connectors, supports the ECX335 series). Tek Gear says the OLEDs must be bought directly from Sony. No price was listed. — [Tek Gear O8](https://www.tekgear.com/o8.html)
- **ECX339A (0.5", 1600x1200, Sub-LVDS):** A reseller lists it at $153.05. An Alibaba listing shows $20 (likely a placeholder), and other distributors quote on request. — [Youritech online](https://youritech-online.com/products/et339a-0-5-inch-si-oled-amoled-display1600-1200-display-hmd-vr-ar-display); [Alibaba](https://www.alibaba.com/product-detail/SONY-ECX339A-0-5-inch-High_1600993893219.html); [lcds-display](https://www.lcds-display.com/products/ECX339A_SONY.html)
- Display Components sells HDMI boards for Sony microdisplays at $99.50 and $109.92. The listing text targets the 0.5" 1280x960 panel and the ECX337A/ECX337RF, and no listing explicitly confirms the 1600x1200 ECX339A. Store boards range from about $95 to $346. — [Tindie HDMI controller 0.5"](https://www.tindie.com/products/oled-modules/hdmi-controller-board-for-05-arvr-microdisplay/); [Tindie HDMI board Sony](https://www.tindie.com/products/oled-modules/hdmi-driver-board-for-the-sony-microdisplays/)
- **ECX344A (1.3-type, 3552x3840):** Sony announced it in Aug 2023 for VR/AR HMDs. It runs at 90 fps, covers up to 96% DCI-P3, and offers normal/upscale/foveated scan modes. The sample price was ¥150,000 (excl. tax), with sample shipments planned for Nov 2023. — [Sony news release](https://www.sony-semicon.com/en/news/2023/2023082401.html); [PR Newswire](https://www.prnewswire.com/news-releases/sony-semiconductor-solutions-to-release-large-size-high-definition-1-3-type-4k-oled-microdisplay-that-reproduces-realistic-spaces-enhancing-the-experiential-value-of-vr-and-ar-head-mounted-displays-301908652.html)
- Per a search summary of Sony's product page, the ECX344A input is **MIPI D-PHY with DSC**. OLED-Info reported the ¥150,000 price (~$1,000+) and estimated Apple paid ~$350/panel (2023). — [Sony OLED lineup](https://www.sony-semicon.com/en/products/microdisplay/oled.html); [OLED-Info](https://www.oled-info.com/sony-officially-launches-its-13-4k-oled-microdisplay-product)
- A Panox supplier article gives ECX344A brightness of up to 1,000 cd/m² (20% duty) and contrast of ≥100,000:1. The same article also wrongly calls it "Full HD," so treat its figures with caution. Reports that Vision Pro uses this panel come from secondary sources. — [Panox ECX344A article](https://www.panoxdisplay.com/knowledge/sony-ecx344a-game-changer-micro-oled.html)
- Sony demonstrated a professional MR headset built on its 1.3" 4K OLED. — [OLED-Info](https://www.oled-info.com/sony-demonstrates-professional-mr-headset-based-its-13-inch-4k-oled)
- **Newer Sony parts (supplier-reported only, not verified against Sony):**
  - ECX350F: 0.44" 1920x1080, 5.1 µm pixel, 10,000 nits peak.
  - ECX348E: 0.55" 1920x1080, 5,000 nits.
  - ECX334E (per Sony lineup summary): 0.39" XGA 1024x768.
  - Source: [Panox](https://www.panoxdisplay.com/solution/what-makes-sony-micro-oled-displays-stand-out/); [Sony OLED lineup](https://www.sony-semicon.com/en/products/microdisplay/oled.html)

### Inferences
- The ECX335 ecosystem (0.71" 1080p, LVDS) is the most mature hobbyist Sony path. Single-HDMI boards cost $95–$135, so a full dual-eye 1080p kit runs ~$530–$800.
- A hobbyist ECX344A build is unrealistic. It needs a DSC-capable MIPI source (no off-the-shelf HDMI/DP→MIPI+DSC hobby board was found), and the ~$1,000+ sample price means ~$2,000+ for panels alone.
- The ECX348E (0.55") is probably the class of panel in the XREAL One Pro (0.55" Sony), but I found no hobbyist listing with a driver board.

### Gaps
- No confirmed hobbyist listing (AliExpress/Taobao) for the ECX344A, ECX348E, or ECX350F with a driver board, and no prices for them.
- I did not verify the "ECX343" part number. No Sony source in the results mentioned it. Sony's 4K part is the **ECX344A**.
- ECX339A-specific HDMI board compatibility is unconfirmed.
- Refresh/brightness specs for the ECX335/ECX339 could not be read from datasheets because fetches were blocked.

## 2. BOE / SeeYA / Olightek micro-OLED panels (0.39"–1.35")

### Takeaway
Chinese micro-OLEDs (mostly SeeYA, plus BOE) are the most accessible hobbyist panels in 2025–26. All are MIPI with HDMI or Type-C driver boards, at MOQ 1:

| Size and resolution | Price range |
|---|---|
| 0.39" 1920x1080 | ~$70–$290 with board |
| 0.49" 1920x1080 | ~$54–$300 |
| 0.6" 1920x1080 120 Hz | ~$299 panel, $799 binocular kit |
| 0.68" 1920x1200 | ~$435 with HDMI board |
| 1.03" 2560x2560 (90 Hz) | ~$342 with single HDMI board; binocular boards available |

### Cited Findings
- **0.39" 1920x1080 (BOE/SeeYA-style):**
  - AliExpress panel + HDMI board bundles range ~$71 (sale, from $88.85) to ~$231 (sale, from $289.36). — [AliExpress 1](https://www.aliexpress.com/i/1005011653696669.html); [AliExpress 2](https://www.aliexpress.com/item/1005002019892277.html)
  - The Wisecoco listing (Type-C→MIPI board) is $285. A bare panel on Alibaba is $78 with MOQ 2. — [Wisecoco](https://www.wisecocodisplay.com/product/0-39-inch-1920x1080-micro-oled-display/); [Alibaba](https://www.alibaba.com/product-detail/1600247234926_1600247234926.html)
  - DisplayModule sells the bare panel for $139 and a separate HDMI micro driver board for $199. It warns that the ESP32-P4 cannot drive the panel. — [DisplayModule 0.39](https://www.displaymodule.com/products/0-39-inch-micro-oled-display-1920x1080-with-mipi-i2c); [DisplayModule HDMI board](https://www.displaymodule.com/products/dmrxhrb-hdmi-micro-driver-board-typec-oled-amoled-evaluation-demo)
  - The Alibaba listing gives 1200 cd/m² and 10000:1 contrast. — [Alibaba](https://www.alibaba.com/product-detail/1600247234926_1600247234926.html)
- **SeeYA 0.49" 1920x1080 (SY049WDM02):**
  - Alibaba listings show $54–134 with MOQ 1. Brightness variants are listed at 1500, 1800, 3000, and 20,000 nits. — [Alibaba 1800nits](https://www.alibaba.com/product-detail/SeeYA-SY049WDM02-0-49-inch-Micro_1600430057971.html); [Alibaba 3000nits](https://www.alibaba.com/product-detail/SeeYA-SY049WDM02-0-49-inch-Micro_1601386042046.html); [Alibaba 20000nits](https://www.alibaba.com/product-detail/SeeYA-0-49-inch-1920-1080_1600922351560.html)
  - DisplayModule sells the 0.49" for $149, or $299 with an HDMI-MIPI adapter. — [DisplayModule 0.49](https://www.displaymodule.com/products/0-49-inch-micro-oled-display-1920x1080-with-mipi)
  - A SeeYA 0.49" binocular birdbath optical module (SY049WDG09 / BY049WA060) also exists. — [Alibaba birdbath module](https://www.alibaba.com/product-detail/SeeYA-BY049WA060-0-49-inch-FHD_1600509361610.html)
- **0.6" 1920x1080, 120 Hz, 6000 nits:**
  - Sold on Tindie (Display Components). — [Tindie 0.6](https://www.tindie.com/products/oled-modules/06-micro-oled-display-1920x1080-120hz-6000nits/)
  - DisplayModule lists the screen only at $299 and a binocular screen + adapter at $799. — [DisplayModule 0.6](https://www.displaymodule.com/products/0-6-micro-oledos-display-1920x1080-120hz-6000nits-mipi-1006)
- **0.68" 1920x1200, 3000 nits:** Tindie lists it at $435 with an HDMI controller board. Amazon also lists 0.68" 1920x1200 modules with an HDMI adapter board (price not captured). — [Tindie 0.68](https://www.tindie.com/products/oled-modules/068micro-oled-display-1920x1200-3000nits-for-ar/); [Amazon](https://www.amazon.com/1920x1200-Silicon-Based-Brightness-Microdisplay-Viewfinder/dp/B0H377WG8Z)
- **1.03" 2560x2560 (SeeYA):**
  - Tindie (Display Components) lists it at $342.00. Specs: 1800 cd/m² typical, MIPI, 60–90 Hz. HDMI single and double (binocular) board options are available. Some listings say 1000 nits, so check the datasheet. — [Tindie 1.03 AR](https://www.tindie.com/products/oled-module/2k-micro-oled-103-inch-2560x2560-1800nits-for-ar/); [Tindie 1.03](https://www.tindie.com/products/oled-modules/103-inch-2k-micro-oled-display-2560x2560-1800nits/)
  - A pancake lens AR optical module for the 1.03" is also sold. — [Tindie pancake module](https://www.tindie.com/products/oled-modules/103micro-oled-pancake-lenses-ar-optical-module/)
  - Alibaba (SeeYA) offers a binocular driver board 5B0103T03-1 and a "2×1.03 inch display + 1×driver board" option. A 3000-nit variant is also listed. — [Alibaba SeeYA 1.03](https://www.alibaba.com/product-detail/Seeya-4K-Micro-OLED-Display-1_1601482424691.html); [Alibaba pancake](https://www.alibaba.com/product-detail/SeeYA-3D-Pancake-VR-lens-1_1601285726834.html)
  - Interface: MIPI 1-port or 2-port D-PHY. Vendors offer HDMI and Type-C boards, monocular or binocular. — [DisplayModule 1.03](https://www.displaymodule.com/products/1-03-inch-micro-oled-display-2560x2560-with-mipi); [iFan](https://ifan-display.com/product/1-03-inch-micro-oled-2560x2560/); [transparentoleddisplay](https://transparentoleddisplay.com/product/1-03inch-microdisplay-25602560-oled-mipi-ar-vr-dual-amoled-typec-hdmi-driver-board/); [Panox 1.03](https://www.panoxdisplay.com/micro-display/1inch-microoled2560x2560.html); [Jeke 90Hz](https://www.jekedisplay.com/Micro-OLED-2560X2560-Micro-Display-for-AR-glasses-p.html); [YX 3000nits](https://www.yxmicrodisplay.com/products/micro-oled-1-03-inch-micro-oledos-display-2560x2560-3000nits-mipi)
  - Hicenda also sells a 1.03" 2560x2560 panel on Tindie with a Type-C driver option. — [Tindie Hicenda](https://www.tindie.com/products/hicenda/micro-oled-display-103-fhd-2560rgbx2560/)
- **BOE:** BOE says its VR/AR micro-OLED modules span 0.39"–5.5". Panox offers custom HDMI→MIPI and Type-C→MIPI boards for BOE panels. Its listed compatibility is a 0.39" BOE panel, and other panels are custom. — [BOE VR/AR](https://www.boe.com/en/Enterprise/VR_AR); [Panox driver boards](https://www.panoxdisplay.com/ad-driving-board/)

### Inferences
- For a productivity build, the strongest hobbyist micro-OLED options are:
  - **1.03" 2560x2560 (~$342/eye with board; ~$700–$900 for a binocular set)** with pancake optics, for VR-style wide FOV.
  - **0.68" 1920x1200 or 0.6" 1920x1080 120 Hz**, for birdbath AR glasses similar to XREAL or Viture.
- Driver boards for 1.03" panels are HDMI or Type-C (DP Alt-mode), not full-size DisplayPort. Binocular 2560x2560 at 90 Hz over one HDMI input would need ~5120x2560@90, which exceeds HDMI 2.0 bandwidth without compression. Actual achievable refresh on the binocular board is unverified, and 60 Hz is likely.

### Gaps
- No Olightek-specific listings or prices were found.
- No hobbyist-available listing was found for a BOE 1.35" 2560x2560 (or 1.35" in general).
- The input resolution/refresh of the SeeYA binocular board 5B0103T03-1 is unverified.

## 3. Fast-switch LCD VR panels and dual-panel kits

### Takeaway
VR fast-LCD panels with HDMI/DP→MIPI boards are cheap and widely available:
- 2.9" 2160x2160 at 90 Hz: ~$140–$205 per eye with an HDMI board.
- 2.9" 1440x1440 dual-panel 120 Hz kit with a DP→MIPI board: ~$219.

No hobby board with DSC support was confirmed. DIY builders report trouble reaching 90 Hz at full resolution on cheap boards.

### Cited Findings
- **2.9" 2160x2160 (LS029B3SX06, Sharp-pattern part number):**
  - 1054–1058 PPI, 90 Hz, MIPI 2-channel 4-lane, 51-pin FPC, active area 51.84x51.84 mm. — [Wisecoco via AliRadar ($121.83)](https://en.aliradar.com/item/4001155589878-Wisecoco-2.9-Inch-2160*2160-LCD-Screen-1058PPI-Display-MIPI-51-Pins-FPC-for-VR-Glasses-Watch); [Wisecoco product page](https://www.wisecocodisplay.com/product/2-9-inch-21602160-high-resolution-square-tft-lcd-module/)
  - Panox lists the driver IC as Synaptics R63455, offers an SSD2828 demo kit and an HDMI controller board, and suggests its online store for small quantities. — [Panox 2.9 2160](https://www.panoxdisplay.com/tft-lcd/2-9-inch-lcd-2160x2160-vr-90-hz.html)
  - eBay lists the panel with an HDMI control board at $142.45, plus $62.88 shipping (≈$205 total). — [eBay](https://www.ebay.com/itm/178079258296)
  - Per a search summary, AliExpress lists the driver board at ~$141.61 and a bare LS029B3SX06 panel at ~$40.96. — [AliExpress search](https://www.aliexpress.us/w/wholesale-2160-lcd-vr.html)
- **2.56"/2.6" 2160x2160:**
  - DisplayModule sells a 2.56" 2160x2160 LTPS panel at 1192 PPI. Its interface is **MIPI C-PHY with DSC**, which needs a DSC-capable source/bridge. — [DisplayModule 2.56](https://www.displaymodule.com/products/2-56-inch-2160x2160-ltps-tft-display-mipi-dmhxt0256z2na)
  - iFan sells a 2.6" fast LCD 2160x2160 at 90 Hz (MIPI DSI) with customizable boards. — [iFan 2.6](https://ifan-display.com/product/2-6-inch-vr-fast-lcd-2160x2160/)
- **2.9" 1440x1440:**
  - An AliExpress listing offers a 120 Hz dual-panel SLS029B3SX02 2.9" 1440x1440 kit with a DP→MIPI board at $219.02 (from $547.55). — [AliExpress](https://www.aliexpress.us/item/2251832788969355.html?gatewayAdapt=jpn2usa4itemAdapt)
  - eBay lists a 2.9" 1440x1440 dual LCD + HDMI driver DIY kit. — [eBay](https://www.ebay.com/itm/176644569329)
  - eBay lists a 2.1" 1600x1600 panel with an HDMI controller DIY kit. — [eBay](https://www.ebay.com/itm/405247831975)
- Wisecoco sells a 5.5" 3840x2160 4K LCD with a MIPI controller board (single panel, split-screen style). — [Wisecoco 5.5 4K](https://www.wisecocodisplay.com/product/5-5-inch-38402160-4k-lcd-panel-touch-screen-display/)
- AliExpress also sells 90 Hz dual 3.81" 1080p OLED + HDMI→MIPI kits (older). — [AliTools](https://alitools.io/en/showcase/diy-vr-screen-with-90hz-dual-3-81-inch-1080p-oled-display-with-hdmi-to-mipi-driver-board-for-projector-hmd-vr-glass-vr-headset-32977594942)
- **Known issues:** The CNCDan DIY_VR headset (dual 1440x1440 LCDs) creator reports the LCDs would not run at 90 Hz at full resolution. — [GitHub DIY_VR](https://github.com/dmcke5/DIY_VR)

### Inferences
- The 2.9" 2160x2160 at 90 Hz is the best-value high-resolution LCD for a VR-style productivity headset, at ~$140–$205 per eye with board.
- Because these are LCDs, expect lower contrast than OLED, backlight bleed, and possible mura.
- Panels marked "with DSC" (e.g., 2.56" C-PHY) are a trap for hobbyists unless the vendor supplies a matching board.

### Gaps
- No specific reports on mura or persistence for these hobby panels were found.
- The maximum dual-panel refresh achievable on the 2160x2160 HDMI board (60 vs 90 Hz) is unverified.
- No 2560x2560 LCD dual kit at MOQ 1 was found.

## 4. 4K-class micro-OLED (Sony 1.3" 3552x3840, BOE 1.35" 2560x2560) — purchasable by hobbyists?

### Takeaway
Effectively no. The Sony ECX344A has a published sample price (~¥150,000, ~$1,000+) but needs MIPI D-PHY with DSC, and no hobbyist driver board or reseller listing was found. No BOE 1.35" panel was found for retail sale. The closest purchasable "high-end" micro-OLED is the 1.03" 2560x2560 SeeYA class (~$342 per eye with HDMI board).

### Cited Findings
- ECX344A: ¥150,000 sample price, 90 fps, 3552x3840. — [Sony news release](https://www.sony-semicon.com/en/news/2023/2023082401.html)
- ECX344A: MIPI D-PHY with DSC; ~$1,000 price; estimated ~$350 Apple cost. — [OLED-Info](https://www.oled-info.com/sony-officially-launches-its-13-4k-oled-microdisplay-product); [Sony lineup](https://www.sony-semicon.com/en/products/microdisplay/oled.html)
- No BOE 1.35" 2560x2560 hobby listing was found. Panox and Youritech offer custom quotes only. — [Panox](https://www.panoxdisplay.com/ad-driving-board/); [Youritech micro OLED](https://www.youritech.com/products/micro-oled/)
- The 1.03" 2560x2560 at $342 with a board is available on Tindie. — [Tindie](https://www.tindie.com/products/oled-module/2k-micro-oled-103-inch-2560x2560-1800nits-for-ar/)

### Inferences
- Through a distributor, a hobbyist might obtain ECX344A samples, but driving them requires a custom FPGA/SoC with a DSC encoder. That is a project in itself, not a purchase.

### Gaps
- No Taobao/AliExpress ECX344A listings were found (search did not cover Taobao).
- No pricing was found for any BOE 1.35" panel.

## 5. Driver boards / bridge chips (TC358870, LT6911, LT7911, ANX7530) and DSC

### Takeaway
Hobby-available boards use HDMI- or DP-to-MIPI bridges. Examples:
- Toshiba TC358870 (dual MIPI, max 3840x2160 at 30 Hz per vendor).
- Analogix ANX7530 (Project North Star board).
- Generic DP/Type-C adapters (DisplayModule DM-ADTTR-020, $189, up to 2880x1440).

No hobby board was found that advertises DSC output for 2160x2160@90 Hz+ per eye.

### Cited Findings
- The DisplayModule HDMI→dual MIPI DSI adapter uses the Toshiba TC358870XGB, max 3840x2160@30 Hz. The vendor advises confirming dual-display behavior and panel timing. — [DisplayModule adapter](https://www.displaymodule.com/products/display-adapter-driver-board-for-hdmi-to-mipi-dsi-single-screen-or-dual-screen)
- DisplayModule's AR/VR DP/Type-C→MIPI adapter (DM-ADTTR-020) is $189, max 2880x1440. The bridge chipset is disclosed only on engineering request. — [DisplayModule DP adapter](https://www.displaymodule.com/products/ar-vr-display-adapter-driver-board-for-dp-type-c-to-mipi)
- The Project North Star display driver board (Smart Prototyping) uses the Analogix ANX7530. It has no HDCP key, so SteamVR Direct Mode does not work on recent GPU drivers. — [Smart Prototyping](https://www.smart-prototyping.com/Project-North-Star-Display-Driver-Board)
- Digital View's MIP-1000 is a commercial HDMI-input MIPI DSI controller. — [Digital View](https://www.digitalview.com/controller-mip-1000)
- Generic HDMI→MIPI boards are sold on AliExpress and Alibaba. — [AliExpress](https://www.aliexpress.com/w/wholesale-hdmi-mipi-driver-board.html); [Rjoytek](https://rjoytek.com/product/universal-lcd-display-control-board-hdmi-to-mipi-controller-board-kit/)
- Hackaday.io GPXR proposes an SBC with two 4K60 MIPI outputs for panels like the 2160x2160 LCD. It is a project, not a product. — [Hackaday.io GPXR](https://hackaday.io/project/194899-gpxr-general-purpose-vr-ar-mr-xr)

### Inferences
- **Bandwidth check (arithmetic, not sourced):**
  - 2160x2160x90 Hz x 24 bpp ≈ 10 Gbps per eye before blanking, ≈ 20 Gbps for two eyes.
  - That exceeds HDMI 2.0 (14.4 Gbps effective) and approaches DP 1.4 HBR3 (25.9 Gbps).
  - A single-input dual-eye board at 90 Hz therefore needs DP 1.4 or HDMI 2.1, or must drop to 60 Hz or lower resolution.
- **HDCP gotcha:** Boards without HDCP keys (e.g., the ANX7530 North Star board) may fail SteamVR Direct Mode. For productivity use as an extended desktop monitor this matters less.

### Gaps
- No sourced info on hobby boards with the Lontium LT6911/LT7911 (common on AliExpress boards, but unverified here).
- No board found with confirmed DSC output.
- Exact chips on the Wisecoco/Panox 2160x2160 HDMI boards are unverified.

## 6. Pixels-per-degree (PPD) implications for text

### Takeaway
Rough averages (horizontal pixels ÷ horizontal FOV):
- Birdbath AR at ~50–58° diagonal with 1920-wide panels: ~39–44 PPD. Good for text.
- 2560x2560 behind ~90–100° pancake optics: ~26–28 PPD. Usable for text with large virtual monitors.
- 2160x2160 at ~100°: ~22 PPD. Marginal.
- 1440x1440 at ~100°: ~14 PPD. Poor for text.

Bigscreen Beyond 2 (2560x2560 micro-OLED) claims 32 peak PPD.

### Cited Findings
- Bigscreen Beyond 2: 5120x2560 total (2560x2560 per eye) micro-OLED, manufacturer-claimed peak 32 PPD. — [Bigscreen](https://bigscreenvr.com/); [Sim Racing Cockpit](https://simracingcockpit.gg/bigscreen-beyond-2-review/)
- Original Beyond: ~28 PPD cited by Panox (supplier). Panox guessed 1.03" 2560x2560 micro-OLED; that is not confirmed. — [Panox application](https://www.panoxdisplay.com/application/micro-oled-application-bigscreen-beyond.html)

### Inferences (arithmetic; averages ignore lens distortion, so center PPD is higher)
- 1920x1080 at 50° diagonal (16:9 → ~43.6° horizontal): **~44 PPD**. This matches XREAL One-class optics.
- 1920x1080 at 57° diagonal (~49.7° horizontal): **~39 PPD**. This matches XREAL One Pro-class optics.
- 1920x1200 at 58° diagonal (16:10 → ~49° horizontal): **~39 PPD**. This matches Viture Beast-class optics.
- 2560 wide at 90° / 100° horizontal: **~28 / ~26 PPD**.
- 2160 wide at 90° / 100°: **~24 / ~22 PPD**.
- 1440 wide at 90° / 100°: **~16 / ~14 PPD**.
- 3552 wide (ECX344A) at 100°: **~36 PPD**.
- Rule of thumb (not sourced here): ~60 PPD ≈ 20/20 "retina"; ≥~30–35 PPD is comfortable for normal-size text; ~20–25 PPD needs enlarged fonts or a large, close virtual screen.
- **Design trade-off:** for a productivity-first DIY build, a narrow-FOV birdbath with a 1920x1080/1200 micro-OLED delivers the highest PPD per dollar. A wide-FOV VR build needs ≥2560 px per eye to match it.

### Gaps
- No sourced measured PPD for DIY combos. Birdbath/pancake optic part availability and FOV are outside this scope.

## 7. Benchmark: displays inside commercial glasses/headsets

### Takeaway
Current consumer AR glasses use Sony micro-OLEDs:
- XREAL One: 0.68" 1080p, 50°.
- XREAL One Pro: 0.55" 1080p, 57°, 120 Hz.
- Viture Beast: Sony 1920x1200, 58°, ~1250 nits.
- Rokid Max 2: Sony, 50°, 600 nits.
- RayNeo Air 3s: 1080p, 120 Hz, 1200 nits; panel maker unconfirmed. The Air 3s Pro is reportedly a Sony 0.6" tandem.
- Bigscreen Beyond 2: 2560x2560 per-eye micro-OLED; panel maker not officially disclosed.

### Cited Findings
- XREAL One Pro: 0.55" Sony micro-OLED, 57° FOV, X1 chip, X-Prism optics. — [XREAL One Pro](https://www.xreal.com/one-pro); [XREAL shop](https://us.shop.xreal.com/products/xreal-one-pro)
- XREAL One: 0.68" Sony micro-OLED, 50° FOV, 1080p, 120 Hz. — [XREAL One Pro page comparison](https://www.xreal.com/one-pro); [Amazon](https://www.amazon.com/clp/B0DNFFXG65)
- One Pro brightness reports conflict: ~700 nits (Tom's Guide) vs 1200 nits for the "One Pro Plus" variant. A Notebookcheck figure of 5000 nits likely refers to panel brightness, not output. — [Tom's Guide](https://www.tomsguide.com/computing/smart-glasses/xreal-one-pro-vs-viture-beast); [Tom's Guide Pro Plus](https://www.tomsguide.com/computing/smart-glasses/xreal-one-pro-plus-vs-viture-beast-round-2-can-a-refresh-even-the-stakes); [Notebookcheck](https://www.notebookcheck.net/Xreal-One-Pro-AR-glasses-launch-with-virtual-171-inch-display-Bose-audio-and-optional-12MP-camera.928200.0.html)
- Viture Beast: Sony micro-OLED, 1920x1200 per eye, 58° FOV, 120 Hz, ~1250 nits, $549. Weight is reported as 98 g or 88 g depending on source. — [Tom's Guide](https://www.tomsguide.com/computing/smart-glasses/xreal-one-pro-vs-viture-beast); [AR Compare](https://www.arcompare.com/compare/viture-beast-vs-xreal-one-pro/); [Viture blog](https://www.viture.com/blog/how-the-beast-stands-apart-from-other-xr-ar-glasses)
- Rokid Max 2: "Sony's latest Micro-OLED," 50° FOV, 600 nits. — [Android Central](https://www.androidcentral.com/gaming/virtual-reality/rokid-max-2-review); [Amazon](https://www.amazon.com/clp/B0DKX1WSQ3)
- RayNeo Air 3s: 1080p per eye, 120 Hz, 98% DCI-P3, 200,000:1 contrast, 1200 nits; panel supplier not named. AR Compare lists the Air 3s **Pro** as a Sony 0.6" tandem micro-OLED (HueView 2.0). — [RayNeo](https://www.rayneo.com/products/rayneo-air-3s-xr-glasses); [Amazon](https://www.amazon.com/clp/B0FWC5BVTJ); [AR Compare RayNeo](https://www.arcompare.com/brands/rayneo/)
- Bigscreen Beyond 2: 2560x2560 per eye micro-OLED, 32 PPD claimed. The official teardown covers optics, IPD adjustment, and the eye-tracking sensor; the summarized results did not name the panel maker. — [Bigscreen teardown blog](https://store.bigscreenvr.com/blogs/beyond/inside-bigscreen-beyond-2-the-teardown); [Notebookcheck](https://www.notebookcheck.net/Bigscreen-Beyond-2-Very-light-VR-headset-features-micro-OLED-displays.999151.0.html)

### Inferences
- A DIY build with the 0.68" 1920x1200 or 0.6" 1920x1080 120 Hz panels sold on Tindie or DisplayModule is roughly equivalent in panel class to the XREAL One and Viture Beast. The commercial products' value-add is the optics (birdbath/X-Prism), the SoC, and the 3DoF tracking.
- Commercial glasses (~$400–$600) are cheaper than a DIY binocular micro-OLED kit plus optics (~$800+). DIY makes sense mainly for custom FOV/optics or wide-FOV VR-style productivity.

### Gaps
- Panel diagonal for the Viture Beast and Rokid Max 2 is unconfirmed.
- RayNeo Air 3s base-model panel supplier is unconfirmed.
- No Karl Guttag or iFixit teardown confirming exact panel part numbers (e.g., ECX348E in the One Pro) was found.
- The Bigscreen Beyond 2 panel maker is unconfirmed; it is often said to be BOE or SeeYA, but no source was found.
