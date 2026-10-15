// =====================================================================
//  Phone Claw - servo button presser for a OnePlus 7 Pro (bare phone)
// =====================================================================
//  The phone lies screen-up in a saddle that grips both long edges
//  (like your fingers/thumb do). Three SG90 micro servos sit beside it,
//  one per button, each swinging a 15 mm lever whose finger pushes the
//  button sideways:
//
//    * LEFT  side - VOLUME UP servo (above the rocker) and
//                   VOLUME DOWN servo (below the rocker)
//    * RIGHT side - POWER servo (below the power key)
//
//  Coordinates: phone top edge at y = 0, phone extends toward -y.
//  Looking down at the screen with the phone top pointing away from you,
//  volume is on the LEFT (x = 0) and power on the RIGHT (x = inner_w).
//
//  Render one part at a time:  set `part` below, or from the CLI:
//    openscad -D 'part="base"'    -o stl/claw_base.stl   phone_claw.scad
//    openscad -D 'part="arm_up"'  -o stl/arm_vol_up.stl  phone_claw.scad
//    openscad -D 'part="arm_dn"'  -o stl/arm_vol_dn.stl  phone_claw.scad
//    openscad -D 'part="arm_pwr"' -o stl/arm_power.stl   phone_claw.scad
// =====================================================================

part = "assembly";      // "assembly" | "base" | "arm_up" | "arm_dn" | "arm_pwr"

$fn = 48;

// ---------------- Phone (OnePlus 7 Pro, no case) ----------------------
phone_w   = 75.9;       // width
phone_t   = 8.8;        // thickness
phone_l   = 162.6;      // length (only used for the preview)
fit       = 0.4;        // clearance per side. Raise if it is too tight.

// Button positions, measured from the TOP edge of the phone (mm).
// Taken from the owner's pencil-mark photo (two methods agreed to ~1 mm):
//   volume rocker 34.0 -> 54.5 (split at 43.5)
//   power key     57.5 -> 69.0
//   alert slider  41   -> 49
vol_up_from_top   = 38.75;  // centre of the upper half of the rocker
vol_down_from_top = 49.0;   // centre of the lower half of the rocker
power_from_top    = 63.3;   // centre of the power key
alert_from_top    = 45;     // centre of the alert slider (kept clear)
alert_len         = 14;     // length of the clear zone around it

// ---------------- SG90 micro servo ------------------------------------
servo_l      = 22.8;    // body length (along x here)
servo_w      = 12.4;    // body width
tab_span     = 32.4;    // tip-to-tip length of the mounting tabs
tab_t        = 2.6;     // tab thickness
tab_z        = 15.9;    // body bottom -> underside of tabs
tab_hole_sp  = 27.5;    // distance between the two tab screw holes
shaft_off    = 5.9;     // body end -> output shaft centre
horn_top_h   = 30.0;    // body bottom -> TOP of the fitted horn (measure!)
servo_clr    = 0.4;     // pocket clearance

// Stock SINGLE-arm horn. Trim it with side cutters so it reaches no more
// than horn_reach from the centre of the spline to its tip.
horn_reach   = 16;
horn_w_hub   = 7;
horn_w_tip   = 4;
horn_t       = 1.8;     // thickness of the flat arm part

// ---------------- Frame -----------------------------------------------
deck_h    = 22;         // height of the surface the phone lies on
plate_t   = 3;          // base plate thickness
wall_t    = 3;          // side wall thickness
lip_w     = 1.6;        // lip that hooks over the edge of the glass
lip_t     = 1.6;
rail_w    = 13;         // width of the rails the phone back rests on
cradle_len= 92;         // how far down the phone the cradle reaches
stop_t    = 3;          // top-edge end stop
stop_x0   = 52;         // stop sits on the RIGHT part of the top edge so
stop_x1   = 66;         //   the pop-up selfie camera (left of centre) is clear

// ---------------- Fingers ---------------------------------------------
servo_d   = 14;         // distance: shaft centre -> phone side face
gap       = 1.0;        // finger-to-button gap at rest
reach     = 15;         // lever length along the phone edge (y)
// The tip slides ~1-3 mm toward its shaft while it presses, so it starts
// this far beyond the target. Volume uses less so the two volume fingers
// keep a 3 mm gap between them.
slide_comp_vol = 1;
slide_comp_pwr = 2;
peg_th    = 3;          // finger thickness (x)
peg_wid   = 5;          // finger width (y)
pad_d     = 5;          // rounded contact pad diameter
pad_h     = 4.5;        // height of the contact pad
arm_t     = 4.5;        // thickness of the printed arm

// ---------------- Derived ---------------------------------------------
inner_w   = phone_w + 2*fit;

// dir = +1: servo shaft above the button (toward the phone top)
//       -1: servo shaft below the button
function shaft_y(from_top, dir, comp) = -from_top + dir*(reach - comp);

UP_DIR  = +1;  DN_DIR = -1;  PWR_DIR = -1;
up_sy   = shaft_y(vol_up_from_top,   UP_DIR,  slide_comp_vol);
dn_sy   = shaft_y(vol_down_from_top, DN_DIR,  slide_comp_vol);
pwr_sy  = shaft_y(power_from_top,    PWR_DIR, slide_comp_pwr);

tab_ledge   = deck_h - tab_t;       // tabs end flush with the deck
servo_bot   = tab_ledge - tab_z;    // z of servo body bottom
arm_z0      = servo_bot + horn_top_h;
btn_z       = deck_h + phone_t/2;   // button centre height
peg_x       = servo_d - gap;        // finger contact face, from shaft

wall_top    = deck_h + phone_t + fit + lip_t;
servo_cx    = -servo_d - servo_l/2 + shaft_off;   // left servo body centre
tower_x0    = servo_cx - tab_span/2 - 4;          // outer face of left tower

echo(str("shafts from top: vol-up ", -up_sy, "  vol-down ", -dn_sy, "  power ", -pwr_sy));
echo(str("max push past the gap: ",
         sqrt(peg_x*peg_x + reach*reach) - peg_x - gap, " mm"));
assert(servo_bot >= 2, "deck_h too low for the servo - raise deck_h");
assert(btn_z - pad_h/2 > deck_h + 0.5, "finger would hit the deck");
// lever bars reach horn_reach + 2 from their shafts; fingers are peg_wid wide
assert((up_sy - horn_reach - 2) - (dn_sy + horn_reach + 2) >= 1.5,
       "volume levers would collide - trim horns shorter or move buttons");
assert((up_sy - reach) - (dn_sy + reach) - peg_wid >= 2,
       "volume fingers would collide");
assert(-pwr_sy + servo_w/2 + 5 <= cradle_len, "power servo off the end of the cradle");

// =====================================================================
//  Servo pocket + tower, built for the LEFT side; mirrored for the right
// =====================================================================
module servo_pocket(sy) {
    c = servo_clr;
    translate([servo_cx, sy, 0]) {
        // body
        translate([-servo_l/2 - c, -servo_w/2 - c, servo_bot - 0.3])
            cube([servo_l + 2*c, servo_w + 2*c, 100]);
        // tabs
        translate([-tab_span/2 - c, -servo_w/2 - c, tab_ledge])
            cube([tab_span + 2*c, servo_w + 2*c, 100]);
        // tab screw pilot holes (the screws that come with the SG90)
        for (sx = [-1, 1]) translate([sx*tab_hole_sp/2, 0, tab_ledge - 8])
            cylinder(d = 1.8, h = 10);
        // wire exit on the outer end
        translate([-servo_l/2 - 20, -2.5, servo_bot + 1])
            cube([20.5, 5, 100]);
    }
}

module tower_block(sy) {
    translate([tower_x0, sy - servo_w/2 - 5, 0])
        cube([-tower_x0 + 0.01, servo_w + 10, deck_h]);
}

// windows: list of [y_from, y_to] where the wall above the deck is removed
module side_body(windows) {
    difference() {
        union() {
            // rail the phone back rests on
            translate([-wall_t, -cradle_len, 0]) cube([wall_t + rail_w, cradle_len, deck_h]);
            // side wall + lip
            translate([-wall_t, -cradle_len, 0]) cube([wall_t, cradle_len, wall_top]);
            translate([-wall_t, -cradle_len, wall_top - lip_t]) cube([wall_t + lip_w, cradle_len, lip_t]);
        }
        for (r = windows)
            translate([-wall_t - 1, r[0], deck_h]) cube([wall_t + lip_w + 2, r[1] - r[0], 50]);
    }
}

// ---------------- Base -------------------------------------------------
module base() {
    vol_win = [[-vol_down_from_top - 9, -vol_up_from_top + 9]];
    pwr_win = [[-power_from_top - 8, -power_from_top + 8],
               [-alert_from_top - alert_len/2, -alert_from_top + alert_len/2]];
    difference() {
        union() {
            // base plate
            translate([tower_x0, -cradle_len, 0])
                cube([inner_w - 2*tower_x0, cradle_len + stop_t, plate_t]);
            // left side: volume up + volume down
            side_body(vol_win);
            tower_block(up_sy);
            tower_block(dn_sy);
            // right side (mirror): power
            translate([inner_w, 0, 0]) mirror([1, 0, 0]) {
                side_body(pwr_win);
                tower_block(pwr_sy);
            }
            // top end stop (a short post on the right part of the top edge)
            translate([stop_x0, 0, 0]) cube([stop_x1 - stop_x0, stop_t, deck_h + 5]);
            translate([inner_w - rail_w, 0, 0]) cube([rail_w + wall_t, stop_t, deck_h]);
        }
        servo_pocket(up_sy);
        servo_pocket(dn_sy);
        translate([inner_w, 0, 0]) mirror([1, 0, 0]) servo_pocket(pwr_sy);
        // weight-saving / cable slots in the plate
        for (yy = [-cradle_len + 15, -cradle_len/2 + 5])
            translate([rail_w + 6, yy, -1]) cube([inner_w - 2*rail_w - 12, 18, plate_t + 2]);
    }
}

// ---------------- Printed finger (sits on top of the stock horn) ------
// Local frame: shaft at origin, +x toward the phone, z=0 = arm underside
// (resting on top of the horn). dir as in shaft_y(): the finger is at
// y = -dir*reach, i.e. on the button side of the shaft.
module arm(dir) {
    ty = -dir*reach;
    hy = -dir*(horn_reach - horn_w_tip/2);       // horn tip centre
    peg_bot = (btn_z - pad_h/2) - arm_z0;        // negative: hangs down
    body_x  = peg_x - pad_d/2;                   // finger body front face
    difference() {
        union() {
            // bar that covers the horn
            hull() {
                cylinder(d = 10, h = arm_t);
                translate([0, hy, 0]) cylinder(d = horn_w_tip + 4, h = arm_t);
            }
            // bridge from the bar out to the finger
            hull() {
                translate([0, ty, 0]) cylinder(d = peg_wid, h = arm_t);
                translate([body_x - peg_th, ty - peg_wid/2, 0]) cube([peg_th, peg_wid, arm_t]);
            }
            // finger hanging down to the button (set back so only the pad touches)
            translate([body_x - peg_th, ty - peg_wid/2, peg_bot])
                cube([peg_th, peg_wid, arm_t - peg_bot]);
            // rounded contact pad: its front is exactly at peg_x
            translate([body_x, ty, peg_bot]) cylinder(d = pad_d, h = pad_h);
        }
        // recess for the single-arm horn (keys the finger against rotation)
        translate([0, 0, -0.01]) linear_extrude(horn_t + 0.2)
            hull() {
                circle(d = horn_w_hub + 0.6);
                translate([0, hy]) circle(d = horn_w_tip + 0.6);
            }
        // horn screw through the middle + counterbore for its head
        translate([0, 0, -1]) cylinder(d = 2.4, h = 20);
        translate([0, 0, arm_t - 1.4]) cylinder(d = 5, h = 5);
        // pilot hole so a small horn screw can pin the horn's outer hole
        translate([0, -dir*(horn_reach - 4), -1]) cylinder(d = 1.4, h = 20);
    }
}

// ---------------- Preview helpers -------------------------------------
module sg90_dummy() {
    color("DodgerBlue") {
        translate([-servo_l/2, -servo_w/2, 0]) cube([servo_l, servo_w, 22.7]);
        translate([-tab_span/2, -servo_w/2, tab_z]) cube([tab_span, servo_w, tab_t]);
    }
    color("White") translate([servo_l/2 - shaft_off, 0, 0])
        cylinder(d = 4.8, h = horn_top_h);
}

module servo_and_arm(sy, dir) {
    translate([servo_cx, sy, servo_bot]) sg90_dummy();
    color("Gold") translate([-servo_d, sy, arm_z0]) arm(dir);
}

module assembly() {
    color("Orange") base();
    color([0.1, 0.1, 0.12, 0.85])
        translate([fit, -phone_l, deck_h]) cube([phone_w, phone_l, phone_t]);
    // button markers on the phone edges (red = target press points)
    color("Red") {
        for (y = [vol_up_from_top, vol_down_from_top])
            translate([fit - 0.5, -y, btn_z]) sphere(d = 2);
        translate([inner_w - fit + 0.5, -power_from_top, btn_z]) sphere(d = 2);
    }
    servo_and_arm(up_sy, UP_DIR);
    servo_and_arm(dn_sy, DN_DIR);
    translate([inner_w, 0, 0]) mirror([1, 0, 0]) servo_and_arm(pwr_sy, PWR_DIR);
}

// ---------------- Output ----------------------------------------------
// Arms are flipped so their flat top prints on the bed - no supports.
module flip() rotate([180, 0, 0]) translate([0, 0, -arm_t]) children();

if (part == "assembly") assembly();
else if (part == "base") base();
else if (part == "arm_up")  flip() arm(UP_DIR);
else if (part == "arm_dn")  flip() arm(DN_DIR);
// the power arm lives on the mirrored (right) side, so print it mirrored
else if (part == "arm_pwr") flip() mirror([1, 0, 0]) arm(PWR_DIR);
