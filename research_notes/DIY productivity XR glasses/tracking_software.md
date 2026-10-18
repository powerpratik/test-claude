# Head Tracking and the Software Stack for DIY XR Productivity Glasses (2025-2026)

Research note: several primary sites (monado.freedesktop.org, gitlab.freedesktop.org, docs.slimevr.dev, fosdem.org, gamingonlinux.com) failed DNS resolution from the research environment, so some findings come from search-result summaries of those pages rather than full-page reads. Items marked "background knowledge" in Inferences come from the researcher's training data and were not verified against a source this session.

## 1. 3DoF IMU head tracking: IMUs, MCUs, fusion, drift, rates, firmware

### Takeaway
Two practical routes: (a) a BNO085/BNO086, which does its own fusion and outputs a quaternion (rotation vector up to 400 Hz; a magnetometer-free "game" vector at about 0.5°/min yaw drift), or (b) a raw 6-axis IMU (ICM-45686, LSM6DSV, ICM-42688, BMI270) with fusion running on the MCU, as SlimeVR firmware does. SlimeVR now ranks ICM-45686 and LSM6DSV above BNO085. The closest existing open firmware for a head tracker is Azimuth (ESP32-C3 + BNO08x, OpenTrack UDP / Hatire over USB) and dlktdr's HeadTracker.

### Cited Findings
- BNO08x report rates: the rotation vector and the game rotation vector are each exposed at up to 400 Hz. The raw gyroscope reaches 1000 Hz. The ARVR-stabilized rotation vector variants are capped at 100 Hz — [Luxonis BNO08x docs](https://docs.luxonis.com/hardware/platform/sensors/imu/bno08x.md)
- The BNO08x game rotation vector deliberately leaves out the magnetometer, "as specified by Google," for smoothness, and "long term the output will likely drift in yaw." The standard rotation vector uses the magnetometer to correct yaw, at the cost of jumps and responsiveness — [Luxonis BNO08x docs](https://docs.luxonis.com/hardware/platform/sensors/imu/bno08x.md)
- SparkFun's BNO086 VR IMU breakout spec gives game rotation vector dynamic heading drift of 0.5°/min — [SparkFun BNO086](https://www.sparkfun.com/products/14618)
- ARVR stabilization smooths magnetometer-correction "jumps" based on sensor velocity. It does not remove drift. One forum user saw no difference (anecdotal) — [SparkFun community](https://community.sparkfun.com/t/bno086-explanation-and-detailed-info-for-readings-please/66713)
- An ESP-IDF component drives the BNO085 over I2C using CEVA's SH2 sensor-hub protocol — [Espressif component registry](https://components.espressif.com/components/rinku404/bno085/versions/1.1.1/readme)
- ICM-42688-P: 6-axis gyro and accelerometer, I3C/I2C/SPI, 2 kB FIFO — [TDK InvenSense datasheet page](https://invensense.tdk.com/?p=9240). An Arduino driver exists — [DFRobot_ICM42688](https://github.com/DFRobot/DFRobot_ICM42688)
- SlimeVR's IMU comparison ranks ICM-45686 first with current firmware (the recommended IMU) and says LSM6DSV performs about as well as BNO085 at lower cost. Both are often out of stock — [SlimeVR IMU comparison](https://docs.slimevr.dev/diy/imu-comparison.html) (search summary; the page could not be fetched)
- SlimeVR tracker firmware supports BMI270, ICM-42688, LSM6DS3TR-C, LSM6DSV, LSM6DSO, LSM6DSR and MPU-6050 through a shared software-fusion path, with gyro offset and 6-side accelerometer calibration. BMI270 gets extra gyro-sensitivity auto-calibration. Magnetometer support is not implemented for these IMUs — [SlimeVR-Tracker-ESP fork README](https://github.com/sojifes/SlimeVR-Tracker-ESP)
- A Sept 2024 community post (anecdotal) says the LSM6DSV beta firmware lacked temperature calibration, so trackers needed a warm-up — [r/pandaslimevr mirror](https://lr.us.psf.lt/r/pandaslimevr)
- Azimuth: DIY head tracker for flight sims. Hardware is a Seeed XIAO ESP32-C3 with a BNO08x over SPI, or a custom PCB with an ESP32-C3 and BNO086. Fusion runs on the IMU ("external fusion IMU"). Outputs are OpenTrack UDP over Wi-Fi or USB Hatire (one at a time). The README does not mention USB HID. It is the successor to Nano33_PC_Head_Tracker — [Azimuth GitHub](https://github.com/FugLong/Azimuth)
- dlktdr HeadTracker: Arduino Nano 33 BLE Rev2 (nRF52840) on PlatformIO/Zephyr, with GUI and firmware included. It is aimed at RC camera pan/tilt but usable elsewhere — [Arduino Project Hub](https://projecthub.arduino.cc/dlktdr/head-tracker-2127da). The predecessor project used Madgwick fusion — [gitter-badger/headtracker](https://github.com/gitter-badger/headtracker)
- Relativty uses an Arduino Due with an MPU-6050 for 3DoF tracking — [Arduino blog](https://blog.arduino.cc/?p=20549)
- For the USB HID side, an RP2040 firmware built on the pico-examples dev_hid_composite plus a TinyUSB CDC debug port is a usable template (a trackball, not an IMU) — [xythobuz Trackball firmware](https://git.xythobuz.de/thomas/Trackball/src/commit/44da7888a4b32958ca955fc8b3704b9242bdb182/firmware)

### Inferences
- For keeping virtual monitors still, yaw drift is the main 3DoF problem. 0.5°/min on a BNO08x game vector means about 30° per hour without a recenter, so magnetometer fusion (rotation vector) or a recenter gesture/hotkey is required. Breezy offers multi-tap recentering (section 3). Indoor magnetometers are disturbed by laptops, monitors and steel desks, so many builders prefer gyro-only yaw plus a manual recenter.
- Background knowledge (unverified): ESP32-S3 and RP2040 both have native USB and can enumerate as HID or CDC through TinyUSB. ESP32-C3 has only USB-Serial/JTAG (no custom HID class). For a USB HID head tracker, an RP2040 or ESP32-S3 is therefore a better fit than an ESP32-C3. STM32 parts with USB FS are also used. A 6-axis IMU sampled at 1 kHz with Madgwick/Mahony or a VQF filter on the MCU, sending quaternions at 500-1000 Hz, is achievable. USB full-speed HID interrupt endpoints poll at 1 ms (1000 Hz) at most.
- A tracker should report orientation through an interface that the chosen desktop software can actually read (section 3). XRLinuxDriver only reads specific commercial glasses, so a DIY IMU needs either OpenTrack (UDP) or a custom Monado driver.

### Gaps
- No ready-made open firmware was found that outputs a 1 kHz quaternion over USB HID specifically for XR virtual-desktop software. Existing trackers target OpenTrack (flight sims) or SlimeVR (body tracking).
- No published drift or latency benchmarks comparing ICM-45686, LSM6DSV and BNO085 for head use were found. The SlimeVR page could not be fetched in full.
- LSM6DSV16X's onboard sensor fusion (SFLP) behaviour and rates were not verified.

## 2. 6DoF inside-out tracking for hobbyists

### Takeaway
The RealSense T265, once the standard hobbyist 6DoF tracker, was discontinued (last order date 28 Feb 2022). The current open path is a camera+IMU device, such as a Luxonis OAK-D (depthai driver) or a RealSense D435i/D455, running Monado's Basalt fork. Collabora says (FOSDEM 2026) that Basalt is CPU-heavy and does not yet match commercial tracking quality. Expect usable but not rock-solid world-locking.

### Cited Findings
- Intel discontinued the LiDAR and Tracking families, including the T265. The last order date was 28 Feb 2022 — [RealSense support](https://support.realsenseai.com/hc/en-us/articles/10705277802643-Are-the-Intel-RealSense-LiDAR-and-Tracking-Product-Families-Being-Discontinued)
- Intel staff suggested the D455/D435i (which have IMUs) as replacements. These require third-party SLAM, such as SLAMCORE — [RealSense support](https://support.realsenseai.com/hc/en-us/articles/10705277802643)
- PX4 docs still list the T265 as discontinued and note it is sensitive to high-frequency vibration — [PX4 docs](https://docs.px4.io/main/en/camera/camera_intel_realsense_t265_vio)
- Monado added initial visual-inertial tracking in April 2022, integrating Kimera-VIO, ORB-SLAM3 and Basalt — [Collabora blog 2022-04](https://www.collabora.com/news-and-blog/blog/2022/04/05/visual-inertial-tracking-support-for-monado-openxr/)
- In December 2022 Monado had a "depthai" (Luxonis OAK) driver tested with a North Star HMD, plus a RealSense driver — [Collabora blog 2022-12](https://www.collabora.com/news-and-blog/blog/2022/12/20/state-of-monado-visual-inertial-tracking)
- Monado's main inside-out tracker is a fork of Basalt. The Monado SLAM datasets were released in Sept 2023 under CC-BY 4.0 — [Hugging Face dataset](https://huggingface.co/datasets/collabora/monado-slam-datasets/blob/d9f2c2c679e3bc1735bb4ba7eb76e2bb759f9c0c/README.md); [Collabora news](https://collabora.com/news-and-blog/news-and-events/monado-slam-datasets-now-available.html)
- A Monado MR fixes Basalt VIO and hand tracking on a Luxonis OAK-D Pro with a simulated North Star HMD (crash fix, IMU handling, axis orientation) — [Monado MR 2228](https://gitlab.freedesktop.org/monado/monado/-/merge_requests/2228)
- FOSDEM 2026 Collabora slides say Basalt is CPU-heavy and its tracking quality does not yet match commercial systems — [FOSDEM 2026 "Monado and beyond" slides](https://fosdem.org/2026/events/attachments/T38AKM-monado-and-beyond/slides/266219/monado_an_tfzl8ak.pdf) (search summary; the PDF could not be fetched)
- Monado's hardware list shows North Star with 6DoF via T265 on-device tracking or via Monado Basalt (experimental), Linux only — [Monado site](https://monado.freedesktop.org/) (search summary)
- Breezy Desktop Pro ($2/mo, $20/yr or $50 lifetime) adds 6DoF position tracking. This applies to supported commercial glasses that have it — [breezy-desktop README](https://github.com/wheaney/breezy-desktop)

### Inferences
- For virtual monitors, rotation stability (low latency, low yaw drift) matters far more than position. 6DoF mainly adds parallax and lets you lean in toward a screen. A 3DoF IMU plus recenter is the pragmatic DIY baseline. Add 6DoF (OAK-D + Basalt on a PC) only if leaning in or walking around matters.
- Background knowledge (unverified prices): an OAK-D Lite is roughly $150 and an OAK-D Pro roughly $300-400. A RealSense D435i is roughly $300+. Running Basalt on a Raspberry Pi is likely too slow (Basalt is CPU-heavy per Collabora). A Jetson or the host PC is the realistic compute.
- OpenVINS is a common research VIO alternative, but no evidence was found of a maintained Monado integration.

### Gaps
- No quantitative jitter or drift figures for Basalt on OAK-D in a desk/HMD use case were found.
- Current OAK-D pricing and any 2025-2026 hobbyist VIO projects on Jetson or Pi were not verified.

## 3. Virtual-monitor software: which can drive a custom/generic HMD?

### Takeaway
On Linux, Breezy Desktop (GPL-3.0) is the most complete multi-monitor XR desktop. It only reads commercial glasses through XRLinuxDriver (VITURE, XREAL, RayNeo, Rokid), so a DIY tracker needs code added to XRLinuxDriver or another route. For a truly custom HMD, Monado (open OpenXR runtime, Boost license) plus an OpenXR desktop app (xrdesktop, Simula, StereoKit-based apps) is the open path. Vendor apps (XREAL Nebula, VITURE SpaceWalker) are brand-locked. Windows and macOS have no mature open-source equivalent.

### Cited Findings
- **Breezy Desktop:** supports KDE Plasma 6 and GNOME 45-51 on Linux. It offers multiple virtual displays alongside physical monitors, plus Virtual Display, VR-Lite mouse/joystick and Follow modes. Smooth Follow, auto-recenter and side-by-side are Supporter-tier features, with multi-tap recenter/recalibrate gestures. License GPL-3.0. Productivity Basic is $10/yr or $25 lifetime, Pro (6DoF) $2/mo, $20/yr or $50 lifetime, with a 2-month trial and free Basic for qualifying non-commercial users. A separate "Breezy Box" for Windows, macOS or Android is described as in progress — [breezy-desktop README](https://github.com/wheaney/breezy-desktop)
- Breezy's GNOME version was released in June 2024. Its roadmap listed multiple virtual monitors, KWin effects for KDE and Monado support — [ecosyste.ms sponsors page for wheaney](https://sponsors.ecosyste.ms/accounts/wheaney)
- **XRLinuxDriver** (GPL-3.0): a Linux service that turns supported glasses' head movement into mouse/joystick input and an external broadcast. It does not do virtual displays itself (that is Breezy's job). Supported: VITURE (One through Beast; Beast uses the official SDK with custom fusion and more drift), RayNeo, Rokid (official closed-source SDKs), and XREAL Air through One Pro (unofficial open SDK; XREAL is "unwilling to collaborate"). Runs on x86_64 and aarch64. The README describes no generic or custom device path — [XRLinuxDriver README](https://github.com/wheaney/XRLinuxDriver)
- **Monado:** an open OpenXR runtime with drivers for North Star (Linux; 3D and 2D/polynomial distortion), Vive/Pro/Index, OSVR HDK, Rift S and XREAL Air 2 Pro, and more headsets via OpenHMD. "Most of the included VR hardware drivers are limited to Linux" — [Monado site](https://monado.freedesktop.org/) (search summary)
- Monado has shipped a SteamVR driver since 21.0 that exposes any Monado HMD or controller driver inside SteamVR. Monado 21.0 was officially OpenXR-conformant and included work toward a Windows port — [Phoronix](https://www.phoronix.com/news/Monado-21.0-Released); [Collabora](https://test.www.collabora.com/news-and-blog/news-and-events/monado-2100-officially-conformant-openxr-implementation.html)
- Monado v25.0.0 was the first stable release of 2025, with driver improvements for SteamVR Lighthouse, WMR, Ultraleap and Cardboard. 25.1.0 followed in December 2025 (reliability, infrastructure, hardware compatibility) — [Khronos news mirror](https://www.khronos.org/news/archives/September%202014%20Community%20Meeting%20Position%20Paper%20Guidelines/openmax/Upcoming%20OpenCL%20Programming%20Webinars%20in%20May/www.khronos.org/conformance/Another%20Milestone%20for%20ASTC%20Texture%20Compression/P120); [GamingOnLinux Dec 2025](https://www.gamingonlinux.com/2025/12/open-source-xr-runtime-monado-25-1-0-released-with-expanded-hardware-support/comment_id=286929)
- A June 2026 feature article claims Monado runs on Linux, Windows and Android. This is a secondary source and not confirmed by release notes — [VR.org](https://vr.org/articles/monado-open-source-openxr-runtime-powering-xr-industry-2026)
- **xrdesktop** (Collabora, Valve-funded) mirrors kwin or gnome-shell windows into XR. Version 0.14 (2020) added OpenXR support, allowing a fully open stack on Monado — [Collabora xrdesktop 0.14](https://www.collabora.com/news-and-blog/news-and-events/xrdesktop-014-with-openxr-support-released.html). FOSDEM 2026 slides describe it as "currently not really active" and list Simula with a question mark — [FOSDEM 2026 slides](https://fosdem.org/2026/events/attachments/T38AKM-monado-and-beyond/slides/266219/monado_an_tfzl8ak.pdf)
- **SimulaVR:** a Godot-based VR window manager for Linux. It officially supports SteamVR headsets with Linux drivers and experimentally supports Monado OpenXR headsets (North Star, OSVR HDK, PSVR). This description is older — [ecosyste.ms listing](https://awesome.ecosyste.ms/projects/69806)
- **StereoKit:** an open-source mixed-reality library with Linux support, listed among open XR dev tools in the FOSDEM 2026 deck — [GamingOnLinux](https://www.gamingonlinux.com/articles/16621/)
- **VITURE SpaceWalker Desktop:** projects multiple virtual screens with several layouts and adjustable refresh. It has a Mac download, and a Windows (PC) page exists. A reseller says there are free apps for Windows, macOS, iOS and Android with 3DoF, multiple displays and ultrawide — [VITURE academy](https://www.viture.com/en-US/academy/spacewalker/desktop); [reseller](https://yespress.io/products/viture-luma-ultra-xr-glasses.md)
- **XREAL Nebula for Windows** beta (Dec 2023): up to 3 virtual screens or an ultrawide curved screen, 3DoF, up to 90 Hz. This is older info — [r/Xreal team post](https://nyc1.lr.ggtyler.dev/r/Xreal/comments/18lykaq/new_nebula_for_windows/krdfs8h/?context=3)
- **AirDesktop:** an unofficial Mac virtual-screen app for XR glasses (private beta), positioned as a Nebula-for-Mac alternative — [airdesktop.notion.site](https://airdesktop.notion.site)

### Inferences
- **Custom-HMD compatibility:** Nebula, SpaceWalker and AirDesktop are tied to vendor glasses. Breezy is tied to XRLinuxDriver's device list. Because it is GPL, a DIY builder could add a device driver to XRLinuxDriver that reads their own IMU. This is the lowest-effort route to Breezy-quality multi-monitor on Linux, but the README shows no supported path for it. Monado's driver framework is designed for new HMDs, and its SteamVR driver can expose them to SteamVR.
- Background knowledge (unverified this session): Immersed and Virtual Desktop (Guy Godin) target Quest, Vision Pro and PC VR headsets through their own clients or SteamVR/OpenXR. Neither supports arbitrary DIY glasses natively, though a DIY HMD exposed as a SteamVR/OpenXR headset could run PC-VR desktop apps such as SteamVR's built-in desktop view or OVR Toolkit / Desktop+ (Windows). Lightspace and ShapesXR are 3D-design/collaboration apps, not virtual-monitor tools. On Linux, WlxOverlay-S and Stardust XR are active OpenXR desktop/overlay projects on Monado/WiVRn.
- On Windows, the most practical open route for a custom HMD is a SteamVR driver (the OpenVR driver API, or Monado's SteamVR driver if its Windows build works) plus Desktop+ or OVR Toolkit for multiple desktop panels. On macOS there is no open OpenXR runtime with HMD output, so a custom app that captures displays and renders SBS is required.

### Gaps
- Breezy Box / Breezy on Windows and macOS: only "in progress"; no release date was found.
- Official Monado Windows support status in 25.x was not confirmed from primary release notes.
- Immersed, Virtual Desktop and Lightspace generic-HMD support was not verified from 2025-2026 sources.

## 4. Virtual display drivers and screen capture APIs

### Takeaway
Windows: VirtualDrivers/Virtual-Display-Driver (MIT, IddCx-based, Win10/11, custom resolutions, refresh rates, EDID and HDR) creates headless monitors for an XR app to capture. macOS: BetterDisplay virtual/dummy screens (basic dummies free; custom virtual screens Pro). Linux: Breezy creates virtual displays inside the compositor itself.

### Cited Findings
- Virtual Display Driver: a fork of ge9/IddSampleDriver (Microsoft IddCx sample). It creates virtual monitors that behave like physical ones (streaming, VR, recording, headless), with custom EDIDs, custom and fractional refresh rates and resolutions "beyond hardware limitations," SDR 8/10-bit and HDR 10/12-bit (HDR needs Win11 23H2+). Windows 10/11, MIT license. Max monitor count is not stated on the README — [VirtualDrivers/Virtual-Display-Driver](https://github.com/VirtualDrivers/Virtual-Display-Driver)
- BetterDisplay (macOS): dummy display creation is free. Custom virtual screens (custom resolution, orientation, naming) and virtual screens matched to a real display are Pro — [BetterDisplay README snapshot](https://github.com/waydabber/BetterDisplay/blob/5751d6813fee46b1b74cac5aaab8ab21588d8712/README.md); [Wayback copy](https://webcf.waybackmachine.org/web/20231226205257/https://github.com/waydabber/BetterDisplay)
- Breezy Desktop supports multiple virtual displays alongside physical monitors on GNOME/KDE — [breezy-desktop README](https://github.com/wheaney/breezy-desktop)

### Inferences
- Background knowledge (unverified): Windows capture uses the DXGI Desktop Duplication API or Windows.Graphics.Capture, which keep frames on the GPU as D3D11 textures and suit low-latency XR compositing. Linux Wayland capture uses xdg-desktop-portal ScreenCast through PipeWire (DMA-BUF zero-copy). X11 can create extra outputs with xrandr --setmonitor/VIRTUAL outputs or EVDI (DisplayLink's open kernel module). Wayland compositors offer headless outputs (wlroots `create_output`, KWin virtual outputs, GNOME Mutter virtual monitors via remote-desktop/screencast APIs). macOS uses ScreenCaptureKit, plus CGVirtualDisplay (the private API used by BetterDisplay and Deskpad) for virtual screens.

### Gaps
- No primary-source 2025-2026 notes were gathered on PipeWire or Desktop Duplication latency figures, or on EVDI's current state.

## 5. Presenting the custom HMD to the PC; distortion, timewarp, latency

### Takeaway
There are two architectures. (1) Glasses as an ordinary extended monitor, with an app such as Breezy rendering the virtual screens full-screen or SBS on that display using IMU pose. This is simple and works with birdbath glasses, which need no lens distortion. (2) A full OpenXR runtime (Monado) with a custom driver, which gives direct mode, distortion meshes and timewarp. Keep motion-to-photon latency under about 20 ms. Rotational timewarp/late-latching is what keeps world-locked text stable.

### Cited Findings
- Below about 20 ms motion-to-photon latency is the commonly cited threshold for presence/comfort — [USPTO patent 9858637](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9858637); [Unity glossary](https://unity.com/ja/glossary/motion-to-photon-latency)
- Timewarp warps the rendered image just before scan-out to correct for head motion after rendering — [USPTO 11127195](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11127195). Extrapolation can make objects appear to drift side to side during rotation — [USPTO 10699472](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10699472)
- Monado's North Star driver supports both 3D and 2D/polynomial distortion correction — [Monado site](https://monado.freedesktop.org/) (search summary)
- Breezy offers modes including Virtual Display, Follow and Smooth Follow, plus SBS support — [breezy-desktop README](https://github.com/wheaney/breezy-desktop)
- Monado's SteamVR driver can expose a Monado-driven HMD to SteamVR — [Phoronix](https://www.phoronix.com/news/Monado-21.0-Released)

### Inferences
- Background knowledge (unverified): commercial birdbath glasses (XREAL, VITURE) appear as plain 1920x1080 DisplayPort-alt-mode monitors, with 3840x1080 SBS mode for 3D. Software such as Breezy treats them as monitors and does pose-based reprojection in the compositor. A DIY build using a birdbath or flat-combiner optic can copy this "extended monitor" model and skip direct mode. Lens-based (VR-style) or North Star reflector optics need per-eye distortion meshes and chromatic correction, which Monado provides.
- Latency budget for a DIY 3DoF stack: IMU at 1 kHz (~1 ms), USB HID poll (1 ms), fusion (<1 ms), compositor render plus late pose sampling, then display scan-out (~8-16 ms at 60-120 Hz). Rendering with a pose predicted to scan-out time and re-sampling just before present (a cheap rotational timewarp) is what keeps text from swimming. Higher display refresh helps most.

### Gaps
- No published motion-to-photon measurements were found for Breezy Desktop or for DIY 3DoF trackers.

## 6. Practical DIY results (Relativty, North Star, OpenHMD, etc.)

### Takeaway
DIY headset projects have mostly targeted gaming (SteamVR) rather than productivity. Relativty is 3DoF, SteamVR-only and dated. North Star + Monado is the best-documented open stack with 6DoF and distortion, but on Linux only. No well-documented DIY headset + multi-monitor productivity project was found.

### Cited Findings
- Relativty: 3DoF, no built-in controllers, designed for SteamVR. It recommends HadesVR for 6DoF. Built with a soldering iron and a 3D printer — [Relativty README](https://cdn.jsdelivr.net/gh/relativty/relativty@master/README.md). Cost is about $100 per Arduino coverage — [Arduino blog](https://blog.arduino.cc/?p=20549), or about 20,000 yen — [Gigazine](https://gigazine.net/gsc_news/en/20200911-diy-vr-headset-relativty). The sources conflict on refresh rate (60 Hz vs the README's 120 FPS claim). These sources are 2020-era.
- North Star is natively supported in Monado with T265 or Basalt 6DoF and full distortion correction (Linux) — [Monado site](https://monado.freedesktop.org/); depthai driver tested with North Star — [Collabora 2022-12](https://www.collabora.com/news-and-blog/blog/2022/12/20/state-of-monado-visual-inertial-tracking)
- Users report Monado quirks with some hardware, such as a PS camera headset showing as "Dummy HMD" and a Vive not released on shutdown — [Monado issue 133](https://gitlab.freedesktop.org/monado/monado/-/issues/133); [Monado issue 195](https://gitlab.freedesktop.org/monado/monado/-/issues/195)
- A 2024 user write-up describes running Monado on openSUSE with a Valve Index instead of SteamVR — [arnavion.dev](https://arnavion.dev/blog/2024-06-29-monado-opensuse-valve-index)

### Inferences
- The most reliable DIY productivity setup today is likely a birdbath display module (or a commercial glasses display) plus Breezy on Linux. The pragmatic DIY twist is a custom IMU integrated into XRLinuxDriver, or buying glasses with a supported IMU. A fully custom optics/HMD build pushes you to Monado plus xrdesktop/Simula/Stardust, which are less polished for multi-monitor work.

### Gaps
- No 2024-2026 Hackaday or GitHub project was found that documents a DIY headset used daily with virtual monitors. Esky (North Star's Unity software) and OpenHMD status in 2025-2026 were not verified.

## 7. Text rendering quality: PPD, distance, supersampling, curvature

### Takeaway
About 60 PPD matches 20/20 acuity, and today's VR sits at roughly 20-30 PPD, where text is legible but soft. A 1080p birdbath glasses display with a ~45-50° FOV gives roughly 40-45 PPD, which is why such glasses are viable for text. Choose the virtual screen size and distance so a 1080p virtual monitor spans about the same angle as the glasses' FOV (≈1:1 pixel mapping), and use supersampled, mipmapped or anisotropic filtering.

### Cited Findings
- About 60 PPD corresponds to the 20/20 line. Meta's Butterscotch prototype reached 55 PPD. Quest 2 is 20 PPD and Quest Pro 22 PPD — [Meta blog](https://www.meta.com/en-gb/blog/vr-display-optics-pancake-lenses-ppd/)
- Meta research says current VR is about 20-30 PPD. Text needs roughly 20-60 PPD depending on spatial frequency. In a test, 56 PPD text was clearly preferred, though all variants were legible — [Meta Reality Labs EI system MTF paper](https://research.facebook.com/file/797036571843537/20230103-EI-system-MTF-JerryJia-v4_noSupportMat.pdf)
- Rotating content reduced effective PPD for English text from 22.5 to 20.8, so effective sharpness depends on the lens, display and content alignment — [Meta EI System MTF slides](https://research.facebook.com/file/764762761804389/EI-System-MTF-v4-JerryJia.pdf)
- A VR text patent sizes fonts from headset PPD, eye PPD (60) and viewing distance — [USPTO 11394947](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11394947)
- Detail degrades away from the lens centre, and fixed 2D HUDs work poorly; content should live in world space — [nDreams dev blog](https://www.ndreams.com/blog/2016/coding-the-assembly-lets-get-technical/) (2016)

### Inferences
- PPD ≈ horizontal pixels / horizontal FOV, so 1920 px over ~46° gives about 42 PPD (calculation; FOV figure is background knowledge). Any virtual monitor larger than the FOV, or placed at a slant or curve, is resampled below 1:1, so text loses sharpness. Remedies: render virtual screens to textures at native resolution, sample with mipmaps or anisotropic filtering (or 1.5-2× supersampling of the eye buffer), keep the main screen dead-centre and near 1:1, use curved screens so the edges stay perpendicular to the gaze, and raise OS scaling (125-150%) on the virtual monitors.
- Sub-pixel judder from IMU noise makes text shimmer. A small dead-band or low-pass on the pose when the head is still, with Breezy-style "smooth follow" as the alternative, helps text stability at the cost of a little lag.

### Gaps
- No measured, glasses-specific (birdbath) PPD and legibility study was found. Figures here come from VR headset research.
