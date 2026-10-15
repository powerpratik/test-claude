# Phone Claw – servo button presser for a OnePlus 7 Pro

A 3D‑printable saddle that grips a (case‑less) OnePlus 7 Pro by its two long
edges, the same place your fingers and thumb hold it. Three micro servos
press **Volume +**, **Volume −** and **Power**, driven by a ~$2 **ESP8266
Wemos D1 mini**. You control it from a web page on your phone or PC, an HTTP
API, or USB serial.

![assembly](images/assembly.png)

## How it works

Each button has its own SG90 servo standing upright beside the phone. A
printed lever, 15 mm long, sits on the servo horn. A finger hangs down from
its end to button height, 1 mm away from the button. When the servo turns
about 8–12°, the finger's rounded pad pushes the button in. The lever geometry
can push up to ~5.8 mm past the gap, far more than a button needs, and the pad
lands within ~1.5 mm of the button centre.

| Side (screen up, top away from you) | Servo | Pin |
|---|---|---|
| Left – above the volume rocker | Volume + | D5 |
| Left – below the volume rocker | Volume − | D6 |
| Right – below the power key | Power | D7 |

The phone slides in from the bottom end until its top edge hits a small stop
post. Lips over the glass edge stop it from lifting. The alert slider has a
cut‑out so sliding the phone in doesn't flip it. The stop post sits on the
right of the top edge, away from the pop‑up selfie camera.

| Volume side | Power side |
|---|---|
| ![](images/closeup_volume.png) | ![](images/closeup_power.png) |

## Button positions used (measured)

These were measured from a top‑down photo of the phone lying on paper with
pencil marks at its ends and at each button. Two independent ways of reading
the photo agreed to within ~1 mm, and they also match an earlier AR‑ruler
photo. All distances are from the **top edge** of the phone:

| Feature | Span | Press point used |
|---|---|---|
| Volume rocker | 34.0 → 54.5 mm (split at 43.5) | Vol+ 38.75, Vol− 49.0 |
| Power key | 57.5 → 69.0 mm | 63.3 |
| Alert slider | ~41 → 49 mm | kept clear (cut‑out 38–52) |

If your phone differs, edit these at the top of `phone_claw.scad` and
re‑export (see below). The model checks itself: it refuses to render if
parts would collide.

## Which controller is cheapest?

| Option | Typical price | Notes |
|---|---|---|
| **ESP8266 Wemos D1 mini (chosen)** | ~$2–3 | WiFi built in, so no PC needed. Its built‑in `Servo` library needs no extra installs. |
| ESP32‑C3 SuperMini | ~$2–3 | Also works. Needs the `ESP32Servo` library and different pin names. |
| Arduino Nano (clone) | ~$3–4 | No WiFi, so it must stay plugged into a PC to be controlled. |

## Bill of materials (excluding printing)

| Qty | Part | AliExpress | Amazon (multipacks) |
|---|---|---|---|
| 1 | Wemos D1 mini (ESP8266) | $2–3 | ~$10 / 3‑pack |
| 3 | SG90 micro servo (comes with horns + screws) | $1–1.50 each | ~$10 / 4‑pack |
| 1 | 470–1000 µF ≥10 V electrolytic capacitor | ~$0.10 | in a kit |
| – | Dupont jumper wires | ~$1 | ~$6 |
| 3 | M2×8 screws (the stock horn screw is too short to go through the printed lever) | pennies | ~$5 kit |
| – | USB 5 V supply, 1 A or more (any phone charger) | reuse | reuse |
| | **Total** | **≈ $8–10** | **≈ $25–35** (with spares) |

These prices are rough estimates, not checked against current listings.

## Files

| File | What |
|---|---|
| `phone_claw.scad` | Parametric OpenSCAD source |
| `stl/claw_base.stl` | Base / saddle (156 × 95 × 33 mm) |
| `stl/arm_vol_up.stl` | Lever for the Volume + servo |
| `stl/arm_vol_dn.stl` | Lever for the Volume − servo |
| `stl/arm_power.stl` | Lever for the Power servo |
| `firmware/phone_claw/phone_claw.ino` | ESP8266 sketch |

Re‑export after editing:

```bash
openscad -D 'part="base"'    -o stl/claw_base.stl  phone_claw.scad
openscad -D 'part="arm_up"'  -o stl/arm_vol_up.stl phone_claw.scad
openscad -D 'part="arm_dn"'  -o stl/arm_vol_dn.stl phone_claw.scad
openscad -D 'part="arm_pwr"' -o stl/arm_power.stl  phone_claw.scad
```

## 1. Check one servo measurement

Fit a horn on an SG90 and stand the servo on the table. Measure from the
table to the **top of the horn** and set `horn_top_h` (default 30 mm). This
sets the finger height, so it should be within about ±1 mm. The fingers have
a 4.5 mm‑tall pad, so a small error is fine.

## 2. Print

- PLA or PETG, 0.2 mm layers, 3 walls, 15–20 % infill.
- **Base**: flat on the bed as exported, no supports needed.
- **Levers**: exported upside down (flat side on the bed), no supports needed.
- If the phone is too tight or too loose, change `fit` (default 0.4 mm per side).
- Print one lever first and dry‑fit it on a servo in the base with the phone
  in place, to confirm the finger lines up before printing the rest.

## 3. Assemble

1. **Trim the horns.** Use the **single‑arm** horn that comes with each SG90.
   Snip it so it reaches no more than **16 mm** from the centre of the spline
   to its tip. The two volume levers sit close together and need this.
2. Center each servo: run the firmware once (it parks all servos at their
   rest angle on boot), or turn the shafts by hand to mid‑travel.
3. Drop each servo into its pocket, shaft toward the phone and wire out the
   back slot. Screw the tabs down with the SG90 screws.
4. Push a horn onto each spline pointing along the phone edge, toward its
   button. Press the matching printed lever onto it (the horn fits a recess
   underneath). Fix it with an **M2×8** screw through the center into the
   shaft, plus a drop of super glue or a small horn screw in the outer hole.
5. Slide the phone in from the bottom until it touches the stop post.

## 4. Wire it

```
 D1 mini            SG90 (brown / red / orange)
 ---------          ---------------------------
 5V  ───────────┬── red   (all three servos)
 G   ───────────┼── brown (all three servos)
                └── 470-1000 µF cap across 5V/G (+ to 5V)
 D5 (GPIO14) ────── orange  VOLUME UP servo
 D6 (GPIO12) ────── orange  VOLUME DOWN servo
 D7 (GPIO13) ────── orange  POWER servo
```

Power the D1 mini from a USB charger (1 A or more). The firmware switches the
servos off after each press, so they don't hum or press on the phone
constantly. At most two move at once (for a screenshot).

## 5. Flash and calibrate

1. Arduino IDE → Boards Manager → add
   `https://arduino.esp8266.com/stable/package_esp8266com_index.json` and
   install **esp8266**. Select board **LOLIN(WEMOS) D1 R2 & mini**.
2. Open `firmware/phone_claw/phone_claw.ino`, set `WIFI_SSID` and
   `WIFI_PASS`, then upload.
3. Open the Serial Monitor (115200) to see the IP address, or browse to
   `http://phoneclaw.local/`. If the board can't join your WiFi, it starts its
   own network **PhoneClaw** (password `clawclaw`) at `http://192.168.4.1/`.
4. Expand **Calibrate**. For each servo:
   - Set `…Rest` so the finger sits just clear of its button.
   - Drag `…Press` until the button clicks, then add 2–3° more. If the finger
     moves away from the phone, go the other direction from rest.
   - Press **Save**. The angles are kept after a reboot.
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
| `*_from_top` | button positions |
| `fit` | grip tightness |
| `gap` | finger‑to‑button distance at rest |
| `reach` | lever length along the phone edge (longer = more push, more slide) |
| `slide_comp_vol/pwr` | how far past the target the finger starts, to offset the slide while pressing |
| `horn_reach` | how far you trimmed the horn |
| `deck_h` | phone height above the table (must leave room for the servo under its tabs) |
| `stop_x0/stop_x1` | position of the top‑edge stop (keep it clear of the pop‑up camera) |
