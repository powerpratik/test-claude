# Phone Claw – servo button presser for a OnePlus 7 Pro

A 3D‑printable saddle that grips a (case‑less) OnePlus 7 Pro by its two long
edges, the same place your fingers and thumb hold it. Two micro servos press
**Volume +**, **Volume −** and **Power**, driven by a ~$2 **ESP8266 Wemos D1
mini**. You control it from a web page on your phone or PC, an HTTP API, or USB
serial.

![assembly](images/assembly.png)

## How it works

| Side (screen up, top away from you) | Servo | Motion |
|---|---|---|
| Left – volume rocker | SG90 #1 with a double‑ended "rocker" finger | rotate one way presses **Vol +**, the other way presses **Vol −** |
| Right – power key | SG90 #2 with a single finger | rotate in to press **Power** |

A single servo can rock the volume key like a thumb does, so you need only
**two servos for three buttons**. Both servos stand upright in pockets beside
the phone. The printed fingers sit on top of the stock servo horns and hang
down to the button height. At rest each finger is 1 mm away from its button.

The phone slides in from the bottom end until its top edge hits a small stop
post. Lips over the glass edge stop it from lifting. The alert slider has a
cut‑out so sliding the phone in doesn't flip it. The stop post sits on the
right of the top edge, away from the pop‑up selfie camera.

| Volume side | Power side |
|---|---|
| ![](images/closeup_volume.png) | ![](images/closeup_power.png) |

## Which controller is cheapest?

| Option | Typical price | Notes |
|---|---|---|
| **ESP8266 Wemos D1 mini (chosen)** | ~$2–3 | WiFi built in, so no PC needed. Its built‑in `Servo` library needs no extra installs. |
| ESP32‑C3 SuperMini | ~$2–3 | Also works. Needs the `ESP32Servo` library and different pin names. |
| Arduino Nano (clone) | ~$3–4 | No WiFi, so it must stay plugged into a PC to be controlled. |

The D1 mini costs the same or less than a Nano clone and adds WiFi, so it wins.

## Bill of materials (~$7 + filament)

| Qty | Part | ~Price |
|---|---|---|
| 1 | Wemos D1 mini (ESP8266) | $2–3 |
| 2 | SG90 micro servo (comes with horns + screws) | $1–1.5 each |
| 1 | 470–1000 µF ≥10 V electrolytic capacitor | $0.10 |
| – | Dupont jumper wires | $1 |
| 1 | M2×8 screw per servo (the stock horn screw is too short to go through the printed finger) | – |
| – | USB 5 V supply, 1 A or more (any phone charger) | reuse |
| – | ~60–80 g PLA/PETG | – |

## Files

| File | What |
|---|---|
| `phone_claw.scad` | Parametric OpenSCAD source (edit button positions here) |
| `stl/claw_base.stl` | Base / saddle (156 × 95 × 33 mm) |
| `stl/arm_volume.stl` | Double finger for the volume servo (left) |
| `stl/arm_power.stl` | Single finger for the power servo (right) |
| `firmware/phone_claw/phone_claw.ino` | ESP8266 sketch |

## 1. Measure your phone first (important!)

Button positions differ slightly between phones, and the defaults are
estimates. With the phone screen‑up and a ruler, measure **from the top edge
of the phone** to:

- the middle of the **upper half** of the volume rocker → `vol_up_from_top`
- the middle of the **lower half** of the volume rocker → `vol_down_from_top`
- the middle of the **power button** → `power_from_top`
- the middle of the **alert slider** → `alert_from_top`

Then put an SG90 with its horn fitted on the table. Measure from the table to
the **top of the horn** and set that as `horn_top_h` (about 30 mm on most
SG90s). This sets how high the fingers sit.

Edit those values at the top of `phone_claw.scad` and re‑export:

```bash
openscad -D 'part="base"'    -o stl/claw_base.stl  phone_claw.scad
openscad -D 'part="arm_vol"' -o stl/arm_volume.stl phone_claw.scad
openscad -D 'part="arm_pwr"' -o stl/arm_power.stl  phone_claw.scad
```

(If you'd rather not install OpenSCAD, the included STLs use the defaults.
Print one finger first and check it lines up.)

## 2. Print

- PLA or PETG, 0.2 mm layers, 3 walls, 15–20 % infill.
- **Base**: flat on the bed as exported, no supports needed.
- **Arms**: exported upside down (flat side on the bed), no supports needed.
- If the phone is too tight or too loose, change `fit` (default 0.4 mm per side).

## 3. Assemble

1. Center both servos: run the firmware once (it parks the servos at 90° on
   boot), or turn the shafts by hand to the middle of their travel.
2. Push the long **double‑arm horn** onto each servo spline so it lines up
   with the phone's long edge (parallel to the side wall).
3. Drop each servo into its pocket, shaft toward the phone and wire out the
   back slot. Screw the tabs down with the SG90 screws.
4. Press the printed finger onto the horn: the horn fits a recess underneath.
   Fix it with an **M2×8** screw through the center into the shaft, plus a
   drop of super glue or the two small horn screws in the outer holes.
5. Slide the phone in from the bottom until it touches the stop post.

## 4. Wire it

```
 D1 mini            SG90 (brown / red / orange)
 ---------          ---------------------------
 5V  ───────────┬── red   (both servos)
 G   ───────────┼── brown (both servos)
                └── 470-1000 µF cap across 5V/G (+ to 5V)
 D5 (GPIO14) ────── orange  VOLUME servo (left)
 D6 (GPIO12) ────── orange  POWER  servo (right)
```

Power the D1 mini from a USB charger (1 A or more). The servos run from the
5 V pin. The firmware switches the servos off after each press, so they don't
hum or press on the phone constantly.

## 5. Flash and calibrate

1. Arduino IDE → Boards Manager → add
   `https://arduino.esp8266.com/stable/package_esp8266com_index.json` and
   install **esp8266**. Select board **LOLIN(WEMOS) D1 R2 & mini**.
2. Open `firmware/phone_claw/phone_claw.ino`, set `WIFI_SSID` and
   `WIFI_PASS`, then upload.
3. Open the Serial Monitor (115200) to see the IP address, or browse to
   `http://phoneclaw.local/`. If the board can't join your WiFi, it starts its
   own network **PhoneClaw** (password `clawclaw`) at `http://192.168.4.1/`.
4. Expand **Calibrate**. Drag each slider until the finger just clicks the
   button, add 2–3° more, then press **Save**. The angles are kept after a
   reboot.
   - `volRest` / `pwrRest`: fingers clear of the buttons.
   - `volUp` / `volDown`: which direction is which depends on how the horn
     went on. Swap them if Vol + and Vol − are reversed.
   - Don't push much past the click. The servo can push the phone sideways or
     strain itself.

## Control

- **Web page:** Volume +, Volume −, Power, Power (hold 3 s, opens the power
  menu), Screenshot (Power + Vol −).
- **HTTP:** `curl "http://phoneclaw.local/press?b=up"`.
  Valid values are `b=up|down|power|long|shot`. Add `&ms=500` for a custom
  hold time.
- **Serial:** send `u`, `d`, `p`, `P` or `s`.

## Tuning knobs in `phone_claw.scad`

| Parameter | Effect |
|---|---|
| `fit` | grip tightness |
| `gap` | finger‑to‑button distance at rest |
| `deck_h` | phone height above the table (must leave room for the servo under its tabs) |
| `cradle_len` | how far down the phone the saddle reaches |
| `stop_x0/stop_x1` | position of the top‑edge stop (keep it clear of the pop‑up camera) |
| `pwr_reach` | power finger offset from its servo shaft |
