# Optical Systems for DIY Productivity XR/AR/VR Glasses (2025-2026)

Research method note: WebFetch failed with DNS errors on every page this session (kguttag.com, tindie.com, displaymodule.com, yankodesign.com). All findings below come from search-engine result summaries and snippets, not full-page reads. Treat prices as asking prices seen in listings (retrieved Oct 2026, most listings undated). Verify them before relying on them.

## Birdbath optics (XREAL Air/One, Viture, Rokid, RayNeo): how they work, FOV, efficiency, buyable modules

### Takeaway
Birdbath is the most practical see-through architecture for a hobbyist building productivity glasses. Complete 1080p micro-OLED birdbath modules (39-50° FOV) are sold one at a time on Tindie, AliExpress and Alibaba for about $170-$575, with HDMI or MIPI driver boards. The costs are low light efficiency (about 10-15% of display nits reach the eye) and a dim view of the real world (about 25% of ambient light passes).

### Cited Findings
- **How it works.** A beam splitter sends light from the display to a curved partial mirror (the "birdbath") and back through to the eye. With a plain 50/50 non-polarizing splitter, 50% × 50% = 25% gets through. A polarizing design with a quarter-wave plate has only one nominal 50% polarization loss — [Guttag, Nreal Teardown Pt 1 (2021, older)](https://kguttag.com/2021/06/01/nreal-teardown-part-1-clones-and-birdbath-basics/); [Guttag 2017 pros/cons (older)](https://kguttag.com/2017/03/03/near-eye-bird-bath-optics-pros-and-cons-and-immys-different-approach/)
- **Efficiency:** "Birdbath optics typically deliver 10 to 15 percent of the display's nits to the eye." From a 1,000-nit OLED, about 120 nits reach the eye. Diffractive waveguides deliver about 0.1% — [Guttag, SID Information Display 2023](https://sid.onlinelibrary.wiley.com/doi/10.1002/msid.1379)
- Nreal's partial mirror is 40% reflective and 60% transmissive, which gives about 27% to the eye. Changing it to 20% reflective and 80% transmissive would only raise that to about 35%. Guttag elsewhere cites about 10% for see-through AR and about 20% when the front mirror is fully reflective (VR) — [Guttag, Nreal Teardown Pt 2 (2021)](https://kguttag.com/2021/06/04/nreal-teardown-part-2-detailed-look-inside/)
- **See-through:** XREAL birdbaths block about 75% of real-world light (25% transmissive). The One Pro blocks about 78% (22% transmissive with its dimmer at its clearest setting) — [Guttag, XREAL One Pro optics (Feb 2025)](https://kguttag.com/2025/02/24/xreal-one-pro-optics-and-its-connections-to-ant-reality-and-google/)
- **Newer variant:** The XREAL One Pro moved from birdbath to a "flat prism" (X-Prism). The optics are much thinner, so the eyes sit closer — [Guttag Feb 2025](https://kguttag.com/2025/02/24/xreal-one-pro-optics-and-its-connections-to-ant-reality-and-google/). FOV went from 50° (One) to 57° (One Pro) — [ITmedia, Jul 2025](https://www.itmedia.co.jp/mobile/spv/2507/02/news079.html). XREAL claims reflections are cut by more than 90% (Japanese materials) or by 99%. These vendor figures conflict — [Witchdoctor](https://www.witchdoctor.co.nz/?p=88864); [ITmedia](https://www.itmedia.co.jp/mobile/articles/2507/02/news099.html)
- **Typical specs:** The XREAL Air, Air 2 and Air 2 Pro all have a 46° FOV. The Air 2 uses 0.55" Sony micro-OLED (down from 0.68" on the original Air) and is rated 49 PPD and up to 500 nits (Air: 400 nits) — [GSMArena Air 2 review](https://www.gsmarena.com/xreal_air_2_review-news-60451.php); [XREAL docs](https://docs.xreal.com/XREALDevices/XREAL%20Glasses)
- **Hobbyist-buyable modules (asking prices, undated listings, seen Oct 2026):**
  - Tindie (Display Components, Hong Kong): 0.71" micro-OLED 1920×1080 birdbath, 50° FOV, optional HDMI driver board, about $574. A 0.49" 1920×1080 module (FOV >39.8°) is about $170. Prices on the store pages run from about $75 to $569 — [Tindie 0.71" FOV50](https://tindie.com/products/oled-modules/bird-bath-lenses-ar-glasses-optical-module-fov50); [Tindie 0.49"](https://tindie.com/products/oled-module/049-micro-oled-display-birdbath-optics-module); [Tindie binocular FOV39](https://www.tindie.com/products/oled-module/binocular-birdbath-fov-39-ar-optics-glasses-module/); [Tindie 50° optical module](https://www.tindie.com/products/oled-module/ar-birdbath-optics-19201080-50-fov-optical-modul/)
  - AliExpress: binocular 0.71" 1080p birdbath with HDMI input, about $370-$378 — [AliExpress search](https://www.aliexpress.com/w/wholesale-heads-up-display-glasses-diy.html)
  - Alibaba (SeeYA, a Chinese micro-OLED maker): 0.49" FHD birdbath binocular module, $225-$325. A 1920×1080 dual Si-OLED module with driver board (MIPI), 41° FOV, 0 to −5 D adjustable diopter, $210-$310. An "1800 nits" binocular prototyping module is also listed — [Alibaba SeeYA 0.49"](https://www.alibaba.com/product-detail/SeeYA-BY049WA060-0-49-inch-FHD_1600509361610.html); [Alibaba 41° w/ diopter](https://www.alibaba.com/product-detail/SeeYA-Birdbath-Ar-Glasses-Binocular-Optical_1601450089571.html); [Alibaba 1800 nits](https://www.alibaba.com/product-detail/SeeYA-birdbath-binocular-AR-optical-module_1600584928461.html)
  - DisplayModule.com: binocular 1080p 47° FOV LVDS module at $999, specced with a 14×8 mm eyebox, 20-40% see-through transmittance and a 136" image at 4 m. A 42° single-panel version is $1,499. Custom modules take a 6-month development cycle — [DisplayModule 47°](https://displaymodule.com/products/binocular-araugmented-reality-glasses-birdbath-1920-1080-47-fov-optical-module-with-lvds); [DisplayModule 42°](https://www.displaymodule.com/products/birdbath-1920rgb-x-1080-araugmented-reality-optical-module-fov-42-degree-lvds); [DisplayModule dev kit](https://www.displaymodule.com/products/ar-binocular-development-kit-module-with-birdbath-optical-module-type-c)
  - Bulk example: a 0.71" module at $616.80 with a 200-piece MOQ; a Shenzhen Solskin module at $485 with an MOQ of 1 — [Accio](https://www.accio.ai/find-product/birdbath-ar)

### Inferences
- The cheapest route to birdbath optics is usually a complete consumer pair, such as a used XREAL Air/Air 2 or a Viture/Rokid/RayNeo. These typically sell well under the $370-$575 module prices, based on general market knowledge rather than a sourced listing. They also come with a working DisplayPort-alt-mode driver. Bare OEM modules make sense mainly when you need custom mechanics, a different driver interface, or adjustable diopter.
- About 25% see-through makes these glasses work like sunglasses. Indoor pass-through is dim but usable, and the "monitor" content dominates the view. That suits productivity work, where the virtual screen is the point.
- A 14×8 mm eyebox (DisplayModule spec) is small. Placing the eye and matching IPD both matter, so a DIY frame needs an adjustable nose pad and a fixed, rigid binocular alignment between the two modules.

### Gaps
- No sourced prices for used XREAL/Viture/Rokid glasses or salvaged optics on eBay. No teardown guide for reusing their optics in a custom frame.
- No measured MTF, chromatic aberration or ghosting data for the generic AliExpress/Tindie modules versus XREAL. The only ghosting data is XREAL's own reflection-reduction claims.
- Full page contents (shipping, driver board compatibility, warranty) could not be fetched.

## Pancake lenses (Quest 3, Bigscreen Beyond, Vision Pro): hobbyist availability, panel pairing, efficiency, cost

### Takeaway
Pancake optics are buyable as small-volume modules, mainly a 1.03" 2560×2560 micro-OLED plus pancake lens from Tindie with HDMI or USB-C driver options. Generic 2.1-2.56" fast-LCD pancake sets also exist on Alibaba. Taking pancakes out of a Quest 3 is not a supported path. Efficiency is capped at 25% for polarized light (12.5% for unpolarized), so you need very bright panels. The result is fully occluded VR, so pass-through requires cameras.

### Cited Findings
- **Theoretical ceiling:** 25% maximum efficiency because of the half-mirror. Total light efficiency is limited to 12.5% for an unpolarized display source and 25% for a polarized one. Peak brightness of pancake headsets is usually lower than conventional ones — [OEA journal 2024](https://www.oejournal.org/oea/article/doi/10.29026/oea.2024.230178); [MDPI Crystals](https://www.mdpi.com/2073-4352/11/2/107/xml)
- **Real-world loss:** More than 75% of the light is lost before reaching the eye in the Quest 3. It is rated at about 100 nits at the eye — [Display Training Center, Quest 3 teardown (Nov 2025)](https://displaytrainingcenter.com/2025/11/13/meta-quest-3-teardown-optical-analysis/). Other sources give 10-25% transmission — [propelrc 2026 comparison (secondary)](https://www.propelrc.com/esnel-vs-pancake-lenses-vr/)
- **Stack:** A pancake lens combines reflective polarizer film and a quarter-wave plate — [Avantier via Vision Systems Design](https://www.vision-systems.com/directory/lenses/product/55300228/avantier-inc-pancake-lenses-for-vr-optical-systems)
- **Hobbyist modules:**
  - Tindie (Display Components): "3D pancake VR lenses with 1.03" 2.5K micro display" (2560×2560). It ships with the screen and lens, with HDMI or USB-C adapter options — [Tindie](https://www.tindie.com/products/oled-module/3d-pancake-vr-lenses-with-103-25k-micro-display/); [Tindie 1.03" pancake AR module](https://tindie.com/products/oled-modules/103micro-oled-pancake-lenses-ar-optical-module). The price was not retrieved because the page fetch failed.
  - A shared design on r/augmentedreality (Apr 2023, older) paired a pancake lens with a 2.48" fast-LCD and a driver PCB, with a 1P/2P option for diopter adjustment — [Reddit r/augmentedreality](https://redlib.ssps.io/r/augmentedreality/comments/12jjibv/pancake_lense_module)
  - DisplayModule sells a 2.1" 1600×1600 fast-switch LCD "myopia VR" module with MIPI and HX8379-C driver IC. It is the kind of panel used with generic pancakes — [DisplayModule](https://displaymodule.com/products/2-1-myopia-vr-display-module-mipi)
  - Alibaba carries generic "pancake lens VR" listings — [Alibaba](https://electronics.alibaba.com/product/pancake-lens-vr)
  - DIY pancake attempt: WalkerDev built a homebrew "pancake" by stacking two off-the-shelf Fresnel lenses in a 3D-printed housing. The project is experimental and still in development — [Hackaday](https://hackaday.com/blog/page/1453/?cat=Brazil)
- **Quest 3 lenses:** Meta forum replies say the pancake lenses cannot be replaced. A user thread asking about building a DIY headset with Quest 3 lenses had no replies — [Meta forum](https://communityforums.atmeta.com/discussions/OtherTroubleshooting/scratched-lenses/1339543); [Meta forum DIY thread](https://communityforums.atmeta.com/discussions/dev-general/diy-headset-with-quest-3-lenses/1320235)
- **Reference point, Bigscreen Beyond 2:** dual 1" 2560×2560 micro-OLED with pancakes, 116° diagonal FOV (original: 102°), 90 Hz. PPD is reported as 32 by Notebookcheck. The original was quoted at 28 PPD, later 32 with revised optics. Sources conflict on which unit the 32 refers to — [Road to VR](https://roadtovr.com/pc-vr-bigscreen-beyond-2-fov-boost-release-date-price/); [Notebookcheck](https://www.notebookcheck.net/Bigscreen-Beyond-2-Very-light-VR-headset-features-micro-OLED-displays.999151.0.html); [UploadVR](https://www.uploadvr.com/bigscreen-beyond-lens-improvements-field-of-view/)

### Inferences
- For productivity, a 1.03" 2560×2560 micro-OLED pancake module is the strongest DIY option for sharpness. At around 90-100° FOV it gives about 25-28 PPD; narrowing FOV raises PPD. That is borderline for small text, though better than Fresnel/LCD builds.
- A pancake build is opaque VR. "See-through" needs camera pass-through, which adds latency and complexity for one person.
- Pancakes are sensitive to polarization stack alignment and to the eye-to-lens distance. Expect ghosting if the polarizer stack is misaligned. This is general optics knowledge; no hobbyist-specific source was found.

### Gaps
- Prices for the Tindie 1.03" pancake module and for generic Alibaba/AliExpress 2.1"/2.56" pancake sets were not retrievable.
- No sourced information on Hypervision or Bradley Lynch pancake analyses (searches returned none).
- No measured ghosting or chromatic data for hobbyist pancake modules.

## Aspheric and Fresnel VR lenses (Cardboard-style, replacement lenses, 40-50 mm)

### Takeaway
The cheapest optics are Fresnel or biconvex/aspheric lenses at a few dollars on AliExpress, paired with 2.9" 1440×1440 LCDs. They power the best-known DIY VR headsets of 2025-2026 (CNCDan, about $150 total; Persephone 3 Lite). They give wide FOV but low PPD (roughly 15 by my estimate), and Fresnels add godrays on white-on-black text. That makes them poor for reading text, though good for learning.

### Cited Findings
- **CNCDan's open-source headset (PC Gamer, ~2025):** 2880×1440 total from two 2.9" LCDs, adjustable screen positions, Fresnel lenses, an IMU and an Arduino Pro, all from AliExpress, for a little over $150. The displays are advertised as 90 Hz but reach only 60 Hz at full resolution — [PC Gamer](https://www.pcgamer.com/hardware/vr-hardware/a-youtuber-has-built-his-own-vr-headset-for-a-little-over-usd150-and-made-the-whole-project-open-source-so-anyone-can-give-it-a-go/); [Yanko Design](https://www.yankodesign.com/?p=583960)
- **Persephone 3 Lite (Hackaday, Feb 2026):** two 2.9" square 1440×1440 displays at up to 90 Hz, with "cheap Fresnel lenses sourced from AliExpress for a few dollars." Files are on Patreon — [Hackaday Feb 2026](https://hackaday.com/2026/02/01/a-diy-headset-for-steamvr/)
- Waterloo Reality Labs uses 1440×1440 90 Hz LCDs with 50 mm biconvex glass lenses, and recommends Fresnel for DIY — [GitHub uwrealitylabs](https://github.com/uwrealitylabs)
- Relativty is an open-source SteamVR headset for about $200 (older project) — [GitHub Relativty](https://github.com/relativty/Relativty)
- **Godrays:** streaks radiating from the lens center, most visible on high-contrast content like white text on black. They are caused by scattering at the Fresnel grooves and can "hardly be avoided physically." Fresnels have a small sweet spot, and slight eye movement blurs or color-fringes the image. Aspherics have no grooves, give a consistently sharp image without godrays, and are heavier — [heise (2025)](https://heise.de/-10503349); [Pimax aspheric vs pancake vs Fresnel (vendor)](https://pimax.com/aspheric-vs-pancake-vr-lenses-and-why-glass/); [Pimax godrays (vendor)](https://pimax.com/what-are-glare-god-rays-and-distortion-in-vr/)
- Hybrid Fresnel (central smooth zone plus peripheral ridges) is patented by Facebook. Sony patented light-absorbing coatings on non-optical Fresnel facets — [Road to VR](https://roadtovr.com/?p=168426); [Road to VR](https://roadtovr.com/?p=106440)

### Inferences
- **PPD estimate:** about 1440 px across roughly 90-100° per eye is about 14-16 PPD. A virtual 1080p monitor would need to fill most of the view to be legible, which defeats "multiple monitors."
- For a text-focused VR build with cheap glass, a smooth aspheric gives better edge-to-edge clarity. With a narrower FOV, say 60-70°, a 1440-2160 px panel reaches about 20-30 PPD. That is a deliberate tradeoff that favors productivity.

### Gaps
- No sourced Surplus Shed, Edmund or Thorlabs pricing for 40-50 mm aspherics was retrieved.
- No sourced listings for replacement Quest 2, Vive or Index lenses.

## Freeform prisms and "bug-eye" reflectors (Project North Star)

### Takeaway
Project North Star is still the most accessible wide-FOV see-through AR optic. Smart Prototyping (CombineReality) lists combiner sets for $15-$39.90 (in stock as of the listing) and full kits around $399. It has a huge FOV (about 95°×70° per eye, 100°+ combined) but only about 1600×1440 per eye, so PPD is around 17, too low for small text.

### Cited Findings
- **Optics:** ellipsoidal reflectors of optical-grade acrylic with thin silver coatings that reflect 50% and pass the rest. Dual 1600×1440 120 Hz LCDs, with about 95° tall × 75° wide per eye and 65% overlap, give more than 100° horizontal FOV. The design was open-sourced in 2018 (older info) — [Analogix/Leap Motion coverage](https://analogix.com/en/node/2216); [Tom's Hardware](https://www.tomshardware.com/uk/news/leap-motion-augmented-reality-headset,36849.html); [21stcentech](https://www.21stcentech.com/gizmos-gadgets-leap-motions-north-star-advances-human-computer-interface/)
- **Current availability (Smart Prototyping listings, undated, seen Oct 2026):** Single-Piece Combiner Set v3.1SPC, $15, in stock. North Star Optical Combiner Set, $39.90, in stock, polycarbonate with AR coatings. Kit A (no printed parts) $299 and Kit C (assembled and calibrated) $499 are both marked discontinued. Kit B (all parts) is $399. A 3D-printed parts kit is also listed. Shenzhenlab's "North Star Combiner v4" at $25 is sold out — [Smart Prototyping combiner set](https://www.smart-prototyping.com/Project-North-Star-Lenses-Single-Piece-Set-v3_1-SPC); [SPC replacement](https://www.smart-prototyping.com/Project-North-Star-Single-Piece-Combiner-Set-v3_1SPC-Bad-Lens-Replacement); [Kit A](https://www.smart-prototyping.com/Project-North-Star-Kit); [Kit C](https://www.smart-prototyping.com/AR-VR-MR-XR/AR-VR-Kits-Bundles/Project-North-Star-Kit-C); [3D printed parts](https://www.smart-prototyping.com/Project-North-Star-3D-Printed-Parts-Kit); [Shenzhenlab](https://shop.shenzhenlab.com/)
- Polaris AR (Noah Zerkin / NOA Labs) was created to supply North Star modules, kits and assembled headsets — [Leap Motion blog](https://www.leapmotiontechnology.com/blog-sub/north-star-workshop-augmented-reality-for-everyone); [Smart Prototyping blog](https://www.smart-prototyping.com/blog/Polaris-AR-releases-Project-North-Star-Kit-for-the-masses)
- CombineReality's CR Deck Mk.1 is a North Star derivative (older) — [UploadVR](https://uploadvr.com/cr-deck-mk-1-open-source-ar-headset-project-north-star/)
- Other DIY reflector and freeform builds: "Less than $100, high FOV, mobile AR glasses" on Hackaday.io (older) uses a phone and an imported reflector frame of about $30 — [Hackaday.io](https://hackaday.io/project/163805-less-than-100-high-fov-mobile-ar-glasses). Leon Furze describes a developer's "Zero" glasses that use telescope-eyepiece optics and a resin-cast lens (Nov 2024) — [Leon Furze](https://leonfurze.com/2024/11/06/hacking-the-future-a-developers-diy-approach-to-ar-glasses/)

### Inferences
- North Star reflectors need calibration of the display-to-reflector geometry, and distortion correction is done in software. The North Star community provides tooling for this, though it is not sourced here. The headset is bulky compared with glasses.
- For text, North Star's wide FOV spreads few pixels across a lot of angle. Pairing it with higher-resolution 2.9"/3.1" 2K-4K fast LCDs could raise PPD, but no sourced build doing this was found.

### Gaps
- Current North Star GitHub documentation was not fetched. Polaris AR's own storefront, current stock and see-through transmission figures were not retrieved.

## Waveguides (diffractive/reflective): obtainable by individuals?

### Takeaway
Waveguide modules can be bought one at a time from Chinese OEMs (about $119-$2,100) but are a poor fit for productivity DIY. Most have small FOV (26-30°, some 50°), low resolution (640×400 to 1280×720) and very low efficiency (about 0.1% for diffractive). Some vendors list 1080p-class micro-OLED waveguide modules at around 50° FOV for about $900-$1,100. Realistic as a curiosity; inferior to birdbath for multi-monitor text.

### Cited Findings
- **DisplayModule waveguide modules:** 1280×720, 30° FOV, "from $149" in one listing and $999 in another (single lens, lens with driver, or binocular dev kit). A 0.68" micro-OLED waveguide with 50° FOV at $899-$1,099. A 0.23" micro-OLED with 26° FOV from $119 — [DisplayModule ARM-101](https://www.displaymodule.com/products/ar-module-arm-101); [DisplayModule AR/VR collection](https://www.displaymodule.com/collections/ar-vr)
- **Global Sources:** 1024×768 OLED waveguide module, $450, MOQ 1 — [Global Sources](https://www.globalsources.com/product/optical-waveguide_1207509327f.htm). Alibaba listings range from $450-$850 up to $1,599-$2,099 for a 640×400 module — [Alibaba showroom](https://www.alibaba.com/showroom/waveguide-display.html)
- Diffractive waveguides deliver about 0.1% of display nits to the eye — [Guttag SID 2023](https://sid.onlinelibrary.wiley.com/doi/10.1002/msid.1379)
- A low-cost liquid optical waveguide for AR is a 2025 research paper, not a product — [Nature Comms Eng 2025](https://www.nature.com/articles/s44172-025-00469-4)

### Inferences
- HoloLens, Magic Leap and Even Realities waveguides are not sold as parts. Salvaging them from used devices means you also need their proprietary projectors and drivers, which is unrealistic. Generic OEM modules are the only path.
- 1280×720 over 30° is about 49 PPD, sharp but tiny: one small virtual monitor. Monochrome or green microLED waveguides (Even Realities-style) are for notifications, not monitors.

### Gaps
- No hobbyist build logs using generic waveguide modules were found. Specific HoloLens, Magic Leap and Even Realities part availability was not searched in depth.

## Pixels-per-degree math for comfortable text

### Takeaway
Aim for about 30 PPD minimum for readable UI text, 40+ PPD for comfortable long sessions and about 60 PPD as "retina." Only birdbath/flat-prism 1080p glasses (about 38-49 PPD) and narrow-FOV micro-OLED setups reach 40+. Wide-FOV VR (Fresnel/LCD at about 15 PPD, Beyond-class pancake micro-OLED at about 28-32) does not.

### Cited Findings
- One AR maker says 30 PPD is the threshold for "just being able to read documents and system UI," and users report no eye strain at 40+ PPD — [Unseen Reality, What is PPD](https://www.unseen-reality.com/blog/what-is-ppd)
- A buyer's guide puts the floor at 20 PPD and says pixels stop being noticeable at 30-40 PPD (secondary, less reliable) — [Dymesty guide](https://dymesty.com/blogs/articles/smart-glasses-display-quality-guide)
- 60 PPD is treated as the human-eye limit. More than 60 PPD "causes a waste" — [USPTO patent 11394947](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11394947); [BMJ Paeds Open](https://bmjpaedsopen.bmj.com/node/5362)
- Typical VR is about 20-30 PPD. A desktop monitor viewed at about 50 cm is 30-75 PPD — [Meta Reality Labs MTF paper](https://research.facebook.com/file/764762761804389/EI-System-MTF-v4-JerryJia.pdf)
- A 2026 arXiv study links resolution deficits to simulator sickness and reduced reading performance in VR. PPD alone ignores optical aberrations and render resolution — [arXiv 2601.02829](https://arxiv.org/html/2601.02829v1)
- XREAL Air 2 is 49 PPD at a 46° diagonal with 1080p — [GSMArena](https://www.gsmarena.com/xreal_air_2_review-news-60451.php). Bigscreen Beyond is 28-32 PPD — [UploadVR](https://www.uploadvr.com/bigscreen-beyond-lens-improvements-field-of-view/)

### Inferences (my arithmetic; horizontal FOV for a 16:9 diagonal ≈ diag × 0.87)
- 1920 px at 46° diagonal (about 40° H) gives about 48 PPD, consistent with XREAL's 49.
- 1920 px at 50° diagonal (about 43.6° H) gives about 44 PPD.
- 1920 px at 57° diagonal (about 49.7° H, the One Pro) gives about 39 PPD.
- 2560 px at about 90-100° (pancake micro-OLED) gives about 26-28 PPD.
- 1440 px at about 95° (North Star, Fresnel 2.9") gives about 15-17 PPD.
- **Multi-monitor implication:** to show a 1920-px-wide virtual monitor at 1:1 pixel mapping, you need 1920/PPD degrees: about 64° at 30 PPD, about 48° at 40 PPD, about 32° at 60 PPD. Several monitors therefore need head-tracked virtual screens, with the glasses' FOV acting as a window. At 40-49 PPD with birdbath, one virtual monitor at about 1:1 roughly fills the FOV. Extra monitors are reached by turning your head, which needs a 3DoF IMU plus software.
- Text sharpness also depends on aberrations: birdbath edges soften, and Fresnels have a small sweet spot. Effective PPD at the edge is lower than these nominal figures.

### Gaps
- No controlled studies of reading speed versus PPD in AR glasses were found beyond the arXiv paper's general finding.

## Practical DIY results and lessons (alignment, IPD, focus, diopter)

### Takeaway
Documented hobbyist builds from 2025-2026 are mostly VR: CNCDan's ~$150 build and Persephone 3 Lite, both with AliExpress Fresnels and 2.9" LCDs. North Star kits remain the main see-through DIY path. No well-documented hobbyist build using bare birdbath modules was found. Recurring lessons are adjustable lens/screen spacing for IPD and focus, refresh-rate limits of cheap panels, and the need for diopter adjustment, which some OEM modules include (0 to −5 D).

### Cited Findings
- CNCDan lets the user manually adjust screen positions (for IPD/focus). His panels reach only 60 Hz at full resolution despite 90 Hz advertising — [PC Gamer](https://www.pcgamer.com/hardware/vr-hardware/a-youtuber-has-built-his-own-vr-headset-for-a-little-over-usd150-and-made-the-whole-project-open-source-so-anyone-can-give-it-a-go/)
- Persephone 3 Lite: 2.9" 1440×1440 at 90 Hz with cheap Fresnels, plus SteamVR integration — [Hackaday Feb 2026](https://hackaday.com/2026/02/01/a-diy-headset-for-steamvr/)
- A DIY VR headset GitHub repo is still in early planning (target <$250, printable enclosure) — [GitHub damien-john-knowles](https://github.com/damien-john-knowles/diy-vr-headset)
- Diopter: a SeeYA birdbath module offers 0 to −5 D adjustable diopter — [Alibaba](https://www.alibaba.com/product-detail/SeeYA-Birdbath-Ar-Glasses-Binocular-Optical_1601450089571.html). The Reddit pancake module concept offered 1P/2P diopter options — [Reddit](https://redlib.ssps.io/r/augmentedreality/comments/12jjibv/pancake_lense_module)
- Bare modules need your own driver board (HDMI/LVDS/MIPI), frame, power and head tracking. LVDS modules need a matching controller — [DisplayModule listings via search](https://displaymodule.com/pages/ar-birdbath-optical-module)
- A generic guide suggests salvaging optics from discontinued dev kits or smart glasses as the most practical start (low-quality SEO source) — [inairspace](https://inairspace.com/blogs/learn-with-inair/homemade-ar-glasses-a-comprehensive-guide-to-building-your-own-augmented-reality)

### Inferences
- **Practical recommendation for a productivity build, ranked by realism:**
  1. Use off-the-shelf birdbath or flat-prism glasses (or a $170-$575 Tindie/AliExpress birdbath module with HDMI board) in a custom 3D-printed frame, adding an IMU and virtual-desktop software. About 44-49 PPD, about 25% see-through.
  2. Use a 1.03" 2560×2560 micro-OLED pancake module for opaque VR productivity at about 26-28 PPD (higher if FOV is narrowed).
  3. North Star for wide see-through AR, but at about 17 PPD it is poor for text.
  4. Fresnel/2.9" LCD for learning or gaming, at about 15 PPD.
  5. Generic waveguides: small FOV, dim, expensive.
- Birdbath module eyeboxes (around 14×8 mm) mean IPD alignment between two separate modules must be precise. A rigid, printed binocular bridge with a slide adjustment is advisable. Vertical misalignment between eyes causes eyestrain; this is general binocular-display knowledge and is not sourced here.

### Gaps
- No Hackaday, Reddit or YouTube build log of a hobbyist assembling bare birdbath modules into a custom productivity headset was found.
- No r/Xreal or r/VITURE DIY mod threads (for example re-framing or prescription mods) were retrieved.
- The page-fetch outage prevented reading full build logs for specific alignment and calibration lessons.
