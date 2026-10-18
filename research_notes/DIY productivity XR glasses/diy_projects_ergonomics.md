# DIY/Open-Source XR Headset Projects & Ergonomics for Productivity Headsets (2025-2026 research notes)

Research note: Several primary docs sites (docs.projectnorthstar.org, project-north-star.gitbook.io, mdpi.com, notebookcheck.net, tech.yahoo.com) failed DNS from the research environment, so some findings rely on search-result snippets/secondary coverage. These are flagged where relevant. About 20 tool calls were used.

## (a) Survey of DIY / open-source headset projects

### Takeaway
DIY headsets come in three families. (1) **Relativty-style PC-tethered VR**: an off-the-shelf 2K–2.9K LCD with its driver board, Fresnel/aspheric lenses, an Arduino-class MCU and IMU, and a SteamVR driver. These give 3DoF only and cost about $100–200. (2) **Project North Star reflective AR**: open-source since 2018, wide FOV, but it needs custom reflectors, driver boards and hand-tracking modules, and most coverage is 2018–2023. (3) **Commercial micro-OLED + pancake modules** (2560×2560 at 1.03"), now sold as hobbyist modules on Tindie. I found little documentation of full DIY builds with them. The recurring lessons: tracking (3DoF→6DoF), display fragility and power, driver and window-placement quirks, and custom optics are the hard parts. The 3D-printed housing is not.

### Cited Findings

**Relativty (relativty/Relativty, GPL-3.0)**
- Pitched as "An open source VR headset with SteamVR supports for $200." The maintainers stress it is "NOT A CONSUMER PRODUCT." — [GitHub relativty/Relativty](https://github.com/relativty/Relativty)
- Current guide is labelled "As of May 2023": an ATmega32U4 USB-HID board (Arduino Pro Micro) plus any IMU the FastIMU library supports. The legacy build used an Arduino Due or custom SAM3X8E board with an MPU-6050/MPU-9250. — [GitHub](https://github.com/relativty/Relativty)
- Display: a small 2K 120 FPS PC display with driver board, ideally bought as a matched bundle, about $150–190. Lenses are 40 mm diameter, 50 mm focal length. The housing is 3D-printed or a modified phone VR shell. The strap and facial interface are HTC Vive replacement parts. The bare PCB costs about $4. — [GitHub](https://github.com/relativty/Relativty)
- Tracking is 3DoF (rotation only) with no controllers. There is experimental webcam/neural-net body tracking (needs an NVIDIA CUDA GPU, PyTorch 1.6). The README points to HadesVR for 6DoF and controllers. — [GitHub](https://github.com/relativty/Relativty)
- Software: a SteamVR driver configured via `default.vrsettings` (VID/PID, window position, resolution, distortion, IPD). — [GitHub](https://github.com/relativty/Relativty)
- Known issues: the VR window disappears after clicking (restart vrcompositor); the display won't power on if the USB cable is too long or the port is underpowered (use a powered hub); a wrong window origin/size crashes the driver; mirrored mode steals keyboard and mouse input; IMU drift (calibration helps); the small high-performance displays are fragile. — [GitHub](https://github.com/relativty/Relativty)
- Earlier version ("Relativ", c. 2018): about $100 using an Arduino Due, MPU-6050, a 2560×1440 LCD and two 80 mm Fresnel lenses (older info). — [Arduino Project Hub](https://create.arduino.cc/projecthub/relativty/relativ-build-your-own-vr-headset-for-100-57adba); [Hackster](https://hackster.io/138706/relativty-is-a-low-cost-vr-headset-you-can-build-yourself-fa6e7d)
- c. 2020 cost breakdown: controller-board parts about $25, 2K screens about €170 on AliExpress. — [Xataka](https://www.xataka.com/realidad-virtual-aumentada/relativty-proyecto-open-source-que-puedes-montarte-tus-propias-gafas-realidad-virtual-unos-200-dolares)

**CNCDan's open-source DIY headset (2025, Relativty-derived)**
- Two 2.9" displays totalling 2880×1440, adjustable IPD, IMU on an Arduino. Costs about $150 excluding printed parts. Uses the Relativty software. Files are on his GitHub. — [Notebookcheck](https://www.notebookcheck.net/DIY-YouTuber-builds-cheap-VR-headset-and-makes-it-open-source.1137242.0.html) (snippet via search; page not fetchable)
- Limitations: only 60 Hz at full resolution; 3DoF only (enough for his sim racing). — [Notebookcheck](https://www.notebookcheck.net/DIY-YouTuber-builds-cheap-VR-headset-and-makes-it-open-source.1137242.0.html); [Yahoo Tech](https://tech.yahoo.com/ar-vr/articles/meet-150-open-source-diy-110000300.html)
- November 2025 follow-up: he added 6DoF and wireless controllers. At that time the upgrade files were not yet on GitHub. — [Notebookcheck IT](https://www.notebookcheck.it/Il-costruttore-fai-da-te-aggiorna-il-setup-VR-stampato-in-3D-open-source-con-6-DoF-e-controller.1163527.0.html)

**Project North Star (Leap Motion/Ultraleap, Apache 2.0)**
- Released in 2018 with mechanical/electronic designs on GitHub. At launch the software and electronics schematics were incomplete (older info). — [Road to VR](https://www.roadtovr.com/leap-motion-reveals-project-north-star-an-open-source-wide-fov-ar-headset-dev-kit/); [Tom's Hardware](https://www.tomshardware.com/uk/news/project-north-star-open-source-documents,37222.html)
- Original optics: two 120 fps 1600×1440 displays with reflective combiners, "over a hundred degrees combined" FOV. Other reports give 105°×75° per eye in early revisions and a 95°×70° sweet spot after the FOV was reduced. No source confirmed a "110°" figure. — [Leap Motion blog](https://www.leapmotiontechnology.com/blog-sub/north-star-open-source); [Gigazine](https://gigazine.net/news/20180410-leap-motion-project-north-star)
- Leap's targets were a BOM under $100 and retail under $200 at scale. The custom reflectors, display driver board and hand-tracking module are expensive in single units. — [Gigazine](https://gigazine.net/news/20180410-leap-motion-project-north-star); [TechRadar](https://www.techradar.com/news/leap-motion-reveals-a-weird-looking-ultra-affordable-augmented-reality-headset)
- Release 3 improved comfort and focal-distance adjustment, and it can be worn over prescription glasses. — [Next Reality](https://next.reality.news/news/leap-motion-update-improves-design-project-north-star-augmented-reality-headset-0193018/)
- Smart Prototyping sold NS-compatible reflective lenses and offered frame 3D models (no price found). Before that, the only option was CNC machining the lenses and paying for a custom reflective coating. — [Hackaday](https://hackaday.com/tag/reflective-lens/)
- Polaris AR (Noah Zerkin / NOA Labs) sells modules, kits and assembled, calibrated headsets. A Sunnyvale workshop had 20+ people build headsets in 48 h. — [Leap Motion/Ultraleap blog](https://www.leapmotiontechnology.com/blog-sub/north-star-workshop-augmented-reality-for-everyone)
- Combine Reality's CR Deck Mk.1 is an injection-moulded NS derivative with 1440×1600 per eye at up to 120 Hz and Ultraleap hand tracking. A Kickstarter was planned. — [UploadVR](https://uploadvr.com/cr-deck-mk-1-open-source-ar-headset-project-north-star/)
- Repo state: about 1.8k stars, 279 forks, 55 commits on master, 25 open issues. Community docs are at project-north-star.gitbook.io, plus a Discord (discord.gg/NghjdX7) and r/ProjectNorthStar. — [GitHub leapmotion/ProjectNorthStar](https://github.com/leapmotion/ProjectNorthStar)

**Micro-OLED + pancake parts for hobbyists**
- Tindie sellers offer a 1.03" 2560×2560 micro-OLED with 90° pancake optics, with HDMI or Type-C driver-board options. — [Tindie](https://www.tindie.com/products/oled-module/3d-pancake-vr-lenses-with-103-25k-micro-display/); [Tindie AR module](https://tindie.com/products/oled-modules/103micro-oled-pancake-lenses-ar-optical-module)
- Pancake optics fold light through polarization, which costs optical efficiency. Vision Pro's perceived brightness is only about 100 nits from roughly 5000-nit panels, because of pancake losses and duty cycle. — [Vision Systems](https://www.vision-systems.com/directory/lenses/product/55300228/avantier-inc-pancake-lenses-for-vr-optical-systems); [PhoneArena citing UploadVR](https://www.phonearena.com/news/lg-unveils-10000-nit-micro-oled-displays_id158480)
- WalkerDev built a homebrew "pancake-like" lens by stacking two Fresnels in a printed housing (work in progress when reported). — [Hackaday](https://hackaday.com/blog/page/1499/?cat=LUX)
- Commercial reference: Bigscreen Beyond (2560×2560 micro-OLED per eye). Pimax launched a micro-OLED + pancake line (Dream Air / Air SE / Crystal Super) in September 2025. — [Wikipedia Bigscreen Beyond](https://en.wikipedia.org/wiki/Bigscreen_Beyond); [PR Newswire](https://tools.prnewswire.com/en-us/live/20823/release/20250919EN77857)

**DIY birdbath / AR glasses**
- Hackaday.io project 163805: the hard parts were making birdbath combiners cheaply (dental vacuum-forming was considered) and laser-cutting a frame. Software included Unity demos and a vertex-warping distortion shader. — [Hackaday.io log](https://hackaday.io/project/163805/log/159267)
- Hack Club "Glare" builder: waveguides are "super expensive and not DIY-friendly", and birdbath reduces imperfections "by a lot" but is bulky and harder to get right. Prism optics are the fallback. — [Hack Club Glare](https://hardware.hackclub.com/projects/rr-creator/glare)
- A birdbath combines a spherical part-mirror combiner with a beam splitter. — [DisplayModule](https://www.displaymodule.com/blogs/knowledge/optical-see-through-birdbath)
- University of Eastern Finland's OpenAR 1.0: educational DIY AR glasses built from available components, with a 3D-printed variant. — [OpenAR 1.0](https://sites.uef.fi/openar/openar10/)

### Inferences
- For a productivity build, the cheapest viable path is probably **buying a commercial birdbath glasses optical engine or a Tindie micro-OLED + pancake module**, then designing the printed housing, strap and electronics around it. Making the optics yourself is where every project above struggled.
- Relativty-class builds (3DoF, 60–120 Hz LCD with Fresnels) are fine as a fixed virtual monitor for desk work, which doesn't need 6DoF. Text clarity and weight (big LCD panels) would be the weak points.
- Software path: a SteamVR driver (Relativty) for Windows, or the open-source OpenXR runtime Monado for Linux. I found no sourced 2025–2026 DIY builds using Monado (see Gaps).

### Gaps
- No sources found for: specific Wisecoco 2560×2560 + pancake hobbyist builds; PiXR/Raspberry Pi headsets; ESP32 display glasses; "DIY Apple Vision Pro" projects; OpenHMD/Monado-driven DIY HMDs; Bigscreen-Beyond-like DIY builds. Searches did not surface them, and Reddit was not reachable.
- I could not confirm current (2025–2026) North Star kit availability or prices (Smart Prototyping, Polaris), or the Esky/Monado integration status. The docs site failed DNS.
- No measured weights or achieved FOV figures for any of the DIY builds above.

## (b1) Weight, balance, fit, nose/face pressure, thermal

### Takeaway
Comfort depends on both mass and how far the center of mass sits in front of the neck pivot (neck torque). Every extra ~33 g measurably shortens comfortable wear time. Reference points: about 63–77 g display glasses (Viture), 107–127 g for the Beyond (without straps), about 625 g for Vision Pro, which drew widespread complaints until a top strap was added. A multi-hour productivity device should aim for the glasses class, or a sub-150 g front with the weight carried by a halo or top strap. Face-contact surfaces should stay well below 43 °C.

### Cited Findings
- Zhang et al. 2025 (*Ergonomics*): 88 participants, 1,860 trial sets. HMD weight and COM position significantly affected comfort, and head length also mattered. The authors give an SVR model with weight-range references for HMD design. — [PubMed 39772983](https://pubmed.ncbi.nlm.nih.gov/39772983/)
- Chihara & Seo 2018: masses of 0.8/1.2/1.6 kg and COM offsets of −7/0/+7 cm. Neck torque rose with mass in all postures, and the torque-minimising COM varied by posture. — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S000368701730265X)
- Ito et al. 2019 (Rift CV1): weight affects fatigue, and the size of the effect depends on COM. Neck-joint torque tracks the physical load. — [ResearchGate](https://www.researchgate.net/publication/334337366_Effects_of_Weight_and_Balance_of_Head_Mounted_Display_on_Physical_Load)
- An average of 33 g added weight reduced "comfortable wear time" by 11 minutes (16-person study). — [ResearchGate](https://www.researchgate.net/publication/373974445_The_effects_of_head_mounted_weight_on_comfort_for_helmets_and_headsets_with_a_definition_of_comfortable_wear_time)
- A claim that 500–600 g headsets are comfortable for no more than about 2 h is repeated in a review, but I could not trace it to a primary source. Treat it as unverified. — [MDPI Electronics review 2026](https://www.mdpi.com/2079-9292/15/16/3755) (snippet only)
- Bigscreen Beyond 2 weighs 107 g without straps or face pad, versus 127 g for Beyond 1. It needs an iPhone face scan for its custom face pad. A planned Halo Mount allows a universal face pad or no face pad. — [Road to VR](https://roadtovr.com/pc-vr-bigscreen-beyond-2-fov-boost-release-date-price/); [UploadVR](https://www.uploadvr.com/bigscreen-beyond-2-and-beyond-2e-announced/)
- Vision Pro weighs about 625 g with the default strap and face pad. Reviewers reported pain within minutes (Engadget) and brow pressure/headache (The Verge) with the Solo Knit Band, which has no top strap. The Dual Loop band's top strap improved weight distribution (Engadget, WSJ). Users also stacked two Solo Knit bands. — [Road to VR](https://roadtovr.com/?p=121035); [UploadVR](https://uploadvr.com/apple-vision-pro-has-a-comfort-problem); [Cult of Mac](https://www.cultofmac.com/843690/apple-vision-pro-weight/); [BGR](https://bgr.com/tech/someone-made-the-vision-pro-way-more-comfortable-with-one-simple-tweak/)
- Viture Pro XR weighs 77 g; Viture Pro 2 weighs 63 g. — [Viture Academy Pro/One](https://www.viture.com/en-US/academy/xr-glasses/pro-one-series); [Viture Pro 2](https://www.viture.com/academy/xr-glasses/pro-2)
- Thermal: IEC 62368-1 touch-temperature limits are about 43–48 °C depending on contact, and a smart-glasses paper says this "does not meet the comfort requirements for glasses". 43 °C is described as the damage threshold for steady contact longer than 10 minutes. The limits derive from ISO 13732-1, and the standards have limited applicability to long exposures. — [arXiv 2512.16045](https://arxiv.org/pdf/2512.16045); [COMSOL blog](https://www.comsol.com/blogs/design-safe-wearable-technology-with-heat-transfer-modeling/); [UL tech brief](https://japan.ul.com/wp-content/uploads/sites/27/2014/06/1_techbrief_touchtemp.pdf); [InCompliance](https://incompliancemag.com/contact-burn-injuries-part-2/)
- Long-duration VR work: Biener et al. 2022 (16 participants, a week in VR versus a week in a physical office) found VR significantly worse on task load, frustration, anxiety, eye strain, usability, flow, productivity and simulator sickness. Some measures improved over the 5 days. Press reports give about +48% eye strain, +35% perceived workload and −16% self-rated productivity. Verify these against the paper. — [arXiv 2206.03189](https://arxiv.org/pdf/2206.03189); [Fortune](https://fortune.com/2022/06/21/study-working-in-metaverse-low-productivity-high-anxiety); [Gigazine](https://gigazine.net/gsc_news/en/20220617-working-vr-stressful-lessens-productivity)
- In the same dataset, headset-adjusting actions fell 46% over the 5 days, which suggests fit is learned. Adjusting the headset was a frequent behaviour. — [arXiv 2401.14920](https://arxiv.org/pdf/2401.14920)

### Inferences
- Design targets I derived (not from a standard):
  - Glasses-form device: about 80 g or less on the nose and ears.
  - Headset-form device: front module 150 g or less, with the battery or compute moved to the rear as a counterweight, or off-head on a tethered puck.
  - Use a halo or top strap so the load sits on the forehead and crown rather than the cheeks and nose.
  - Keep face-contact surfaces under about 40 °C and put heat sources (driver boards) away from the face or at the temples, with vents.
- Moving the COM rearward toward the neck pivot matters as much as cutting grams.

### Gaps
- No sourced numeric nose-pad pressure limits (kPa) or face-gasket material comparisons. The MDPI review likely has them but could not be fetched.
- No primary source for the "≤2 h for 500–600 g" figure, or for the "70–90 g ideal glasses" target.
- No face-specific thermal limit beyond the general IEC/ISO touch limits.
- No cable-management studies found.

## (b2) IPD

### Takeaway
Adult IPD averages about 62–64 mm (SD about 3.8–4 mm) and spans roughly 52–78 mm. A 54–74 mm adjustment range covers the large majority of people. Commercial practice is moving from fixed sizes to per-lens mechanical adjustment (Beyond 2).

### Cited Findings
- ANSUR (US Army, n=3,976, ages 17–51) as cited via Dodgson: mean 63.36 mm, SD 3.832 mm, range 52–78 mm; male 64.7 mm, female 62.3 mm. This is a secondary source, a patent. — [USPTO patent 10429648](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10429648); [PMC5497600](https://pmc.ncbi.nlm.nih.gov/articles/PMC5497600)
- Turkish adults: 62.5 ± 4.1 mm (range 49–76). — [Dovepress](https://www.dovepress.com/evaluation-of-interpupillary-distance-in-the-turkish-population-peer-reviewed-fulltext-article-OPTH)
- Iranian adults: women 61.1 ± 3.5 mm, men 63.6 ± 3.9 mm. 96.2% of adults fall in 55–70 mm. — [PMC3520592](https://pmc.ncbi.nlm.nih.gov/articles/PMC3520592); [SID](https://sid.ir/paper/26459/en)
- A systematic review of 243 studies found IPD varies by ethnicity: larger in Western Africa, South India, East Asia, among Latinos and among Native/African Americans; smaller in Europe, North Africa and the Middle East. — [Dovepress Clin Ophthalmol 2026](https://www.dovepress.com/the-interpupillary-distance-differs-between-ethnicities-and-associates-peer-reviewed-fulltext-article-OPTH)
- Bigscreen Beyond 1 came in 18 fixed IPD sizes. Beyond 2 adjusts each lens separately with markings, but the user must enter the IPD in software manually because there is no sensor. — [Road to VR](https://roadtovr.com/pc-vr-bigscreen-beyond-2-fov-boost-release-date-price/)
- Relativty and CNCDan expose IPD as a software setting in `default.vrsettings`, and CNCDan's build adds mechanical IPD adjustment. — [GitHub Relativty](https://github.com/relativty/Relativty); [Notebookcheck](https://www.notebookcheck.net/DIY-YouTuber-builds-cheap-VR-headset-and-makes-it-open-source.1137242.0.html)

### Inferences
- For a DIY build, design two independent lens/display carriages on a printed rail, with mm markings and a 54–74 mm range. Software IPD only shifts the image and can't move the eyebox, so mechanical adjustment is needed whenever the optics' eyebox is small (pancake/micro-OLED).

### Gaps
- No sourced eyebox dimensions or misalignment tolerance for birdbath versus pancake optics.

## (b3) Prescription correction

### Takeaway
Display glasses handle myopia with built-in diopter dials (Viture: 0 to −5.0 D per eye). These do not correct astigmatism or prism, or myopia beyond about −5 D. Headsets use custom insert lenses (Bigscreen). North Star allows wearing glasses underneath. A DIY build should provide insert mounts, magnetic or clip-in, plus room for glasses or a focus adjustment.

### Cited Findings
- Viture Pro XR has myopia adjustment up to −5.0 D through dials above the lenses. — [Viture Academy](https://www.viture.com/en-US/academy/xr-glasses/pro-one-series)
- Viture Pro 2 has per-eye 0 to −5.0 D dials. — [Viture Pro 2](https://www.viture.com/academy/xr-glasses/pro-2)
- Diopter dials do not replace a full prescription: astigmatism, prism and stronger myopia need custom lenses. — [Dymesty review](https://dymesty.com/blogs/articles/viture-pro-2-review) (secondary)
- Bigscreen: prescription inserts made from 2025 onward fit Beyond 1, 2 and 2e. Pre-2025 inserts fit Beyond 1 and 2 but not 2e. — [UploadVR](https://www.uploadvr.com/bigscreen-beyond-2-and-beyond-2e-announced/)
- North Star Release 3 accommodates prescription glasses and adjustable focal distance. — [Next Reality](https://next.reality.news/news/leap-motion-update-improves-design-project-north-star-augmented-reality-headset-0193018/)

### Inferences
- In a DIY build, the simplest way to get diopter adjustment is to make the display-to-lens distance adjustable, on a screw or slider. This also sets the virtual image distance.

### Gaps
- No sourced specs for magnetic prescription-insert designs (e.g., third-party insert vendors) or how DIY builds have mounted them.

## (b4) Focal distance and vergence–accommodation conflict (VAC)

### Takeaway
With fixed-focus optics, focus stays at the virtual-image distance while vergence follows the content, and the dioptric mismatch drives discomfort. Shibata et al.'s "zone of comfort" shows that tolerance depends on distance and on the sign of the conflict. For office work, the virtual screen and the focal plane should sit at the same distance, roughly 1–2 m (0.5–1 D). Content should be rendered near that plane, and rapid depth changes avoided.

### Cited Findings
- On fixed-focus displays, focal distance is fixed while vergence varies with simulated depth. Diopters = 1/m. Example: a 2 m virtual image (0.5 D) viewing an object at 30 cm (3.33 D) gives a 2.83 D conflict (illustrative; "citation needed" on Wikipedia). — [Wikipedia VAC](https://en.wikipedia.org/wiki/Vergence%E2%80%93accommodation_conflict)
- Shibata et al.: the zone of comfort sits inside the zone of clear single binocular vision. A given dioptric conflict was slightly less comfortable at far distances than near. Negative conflicts (content behind the screen) are worse at far distances; positive conflicts (content in front) are worse at near distances. — [PMC3369815](https://pmc.ncbi.nlm.nih.gov/articles/PMC3369815); [PhilArchive](https://dc2.philarchive.org/rec/SHITZO)
- Symptoms are more serious when the conflict changes rapidly. — [PMC3824256](https://pmc.ncbi.nlm.nih.gov/articles/PMC3824256)
- Varifocal displays plus eye tracking are the main mitigation, and they require accurate gaze-based focus estimation. — [Dunn 2019, UNC](https://telepresence.web.unc.edu/wp-content/uploads/sites/11620/2019/03/Dunn_2019_RequiredAccuracyOfGazeTrackingForVarifocalDisplays.pdf)
- A patent suggests that for a computing platform with content at a 0.5 m (arm's-reach) vergence distance, the focal distance should be under 1 m (a patent's framing, not a standard). — [USPTO 10088673](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10088673)
- Viture claims its semi-transparent birdbath optics "naturally break the fixed focal distance" (marketing claim). — [Viture Pro 2](https://www.viture.com/academy/xr-glasses/pro-2)

### Inferences
- For a "virtual monitor" use case, set the optics' virtual image distance to about 1–2 m and render the virtual screen at that same distance. That reduces the conflict to near zero for the main content. A desk-reach virtual screen (0.6–1 m) would argue for a closer focal plane, about 1–1.5 D.

### Gaps
- No sourced virtual image distances for commercial display glasses (Viture, XREAL) and no sourced optometry consensus on the best distance for office work.

## (b5) 3D-printing considerations for the housing

### Takeaway
Avoid PLA near displays and the face because it softens at low heat deflection temperatures. PETG is an easy default; ASA offers more heat and UV resistance but warps and needs an enclosure and ventilation. TPU, resin and nylon specifics, and optical alignment tolerances, were not well sourced.

### Cited Findings
- PLA's low heat deflection and glass-transition temperatures make it warp in summer heat. ABS/ASA outperform it. — [Maker Forums](https://forum.makerforums.info/t/man-do-i-love-this-inland-petg-from-micro-center-rebranded-esun-i-believe/3781); [Van's Air Force](https://vansairforce.net/goto/post?id=1789314)
- PETG prints about as easily as PLA, with higher heat deflection. ASA is the most heat-resistant of the three but warps on cooling and needs drying, an enclosure and ventilation (it emits VOCs). Brims and enclosures reduce warping. — [QIDI](https://qidi3d.com/fr/blogs/news/stop-warping-abs-asa-prints); [Wevolver](https://www.wevolver.com/article/3d-print-warping)
- Relativty uses printed housings with HTC Vive replacement strap and face cushions rather than printed cushions. — [GitHub Relativty](https://github.com/relativty/Relativty)
- Leap designed North Star around off-the-shelf parts and 3D-printed parts where possible. The CR Deck moved to injection moulding to remove the printing step. — [Leap Motion blog](https://www.leapmotiontechnology.com/blog-sub/north-star-workshop-augmented-reality-for-everyone); [UploadVR](https://uploadvr.com/cr-deck-mk-1-open-source-ar-headset-project-north-star/)

### Inferences
- Suggested approach (not sourced as a standard):
  - Print the shell in PETG, or ASA/PC-blend if it will be hot. Avoid PLA.
  - Put matte black interior surfaces and a light seal around the optics.
  - Put adjustment slots for focus and IPD in the printed design rather than relying on print accuracy for optical alignment.
  - Use off-the-shelf replacement foam or PU face cushions, or a soft TPU (about 85A) printed interface with a fabric cover, rather than a hard printed face edge.
  - Lightweight the shell with thin walls and ribs, and keep driver boards away from the face.

### Gaps
- No sourced data on printed-part tolerances for optics alignment, TPU face-cushion hardness or comfort, resin (SLA) versus FDM for optical mounts, nylon, or light-sealing methods.
