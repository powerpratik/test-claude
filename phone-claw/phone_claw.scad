// =====================================================================
//  Phone Claw - servo button presser for a OnePlus 7 Pro (bare phone)
// =====================================================================
//  The phone lies screen-up in a saddle that grips both long edges
//  (like your fingers/thumb do). Two SG90 micro servos sit beside it:
//
//    * LEFT  servo  - double-ended "rocker" finger: rotate one way to
//                     press VOLUME UP, the other way to press VOLUME DOWN
//    * RIGHT servo  - single finger that presses POWER
//
//  Coordinates: phone top edge at y = 0, phone extends toward -y.
//  Looking down at the screen with the phone top pointing away from you,
//  volume is on the LEFT (x = 0) and power on the RIGHT (x = inner_w).
//
//  Render one part at a time:  set `part` below, or from the CLI:
//    openscad -D 'part="base"'    -o stl/claw_base.stl    phone_claw.scad
//    openscad -D 'part="arm_vol"' -o stl/arm_volume.stl   phone_claw.scad
//    openscad -D 'part="arm_pwr"' -o stl/arm_power.stl    phone_claw.scad
// =====================================================================

part = "assembly";      // "assembly" | "base" | "arm_vol" | "arm_pwr"

$fn = 48;

// ---------------- Phone (OnePlus 7 Pro, no case) ----------------------
phone_w   = 75.9;       // width
phone_t   = 8.8;        // thickness
phone_l   = 162.6;      // length (only used for the preview)
fit       = 0.4;        // clearance per side. Raise if it is too tight.

// Button press points, measured from the TOP edge of the phone (mm).
// >>> MEASURE YOUR PHONE WITH A RULER AND EDIT THESE <<<
vol_up_from_top   = 50; // centre of the upper half of the volume rocker
vol_down_from_top = 64; // centre of the lower half of the volume rocker
power_from_top    = 62; // centre of the power button
alert_from_top    = 42; // centre of the alert slider (right side), kept clear
alert_len         = 14; // length of the clear zone around the alert slider

// ---------------- SG90 micro servo ------------------------------------
servo_l      = 22.8;    // body length (along x here)
servo_w      = 12.4;    // body width
tab_span     = 32.4;    // tip-to-tip length of the mounting tabs
tab_t        = 2.6;     // tab thickness
tab_z        = 15.9;    // body bottom -> underside of tabs
tab_hole_sp  = 27.5;    // distance between the two tab screw holes
shaft_off    = 5.9;     // body end -> output shaft centre
horn_top_h   = 30.0;    // body bottom -> TOP of the stock horn (measure!)
servo_clr    = 0.4;     // pocket clearance

// Stock double-arm horn (the long straight one that ships with the SG90)
horn_len     = 33;      // tip to tip
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
peg_th    = 3;          // finger thickness (x)
peg_wid   = 6;          // finger width (y)
pad_h     = 4.5;        // height of the contact pad
arm_t     = 4.5;        // thickness of the printed arm
pwr_reach = 10;         // power finger offset from shaft along y

// ---------------- Derived ---------------------------------------------
inner_w   = phone_w + 2*fit;
y_up      = -vol_up_from_top;
y_down    = -vol_down_from_top;
y_pwr     = -power_from_top;
y_alert   = -alert_from_top;

vol_shaft_y = (y_up + y_down)/2;
vol_reach   = abs(y_up - y_down)/2;
pwr_shaft_y = y_pwr - pwr_reach;    // finger at +pwr_reach from the shaft

tab_ledge   = deck_h - tab_t;       // tabs end flush with the deck
servo_bot   = tab_ledge - tab_z;    // z of servo body bottom
arm_z0      = servo_bot + horn_top_h;
btn_z       = deck_h + phone_t/2;   // button centre height
peg_x       = servo_d - gap;        // finger contact face, from shaft

wall_top    = deck_h + phone_t + fit + lip_t;
servo_cx    = -servo_d - servo_l/2 + shaft_off;   // left servo body centre
tower_x0    = servo_cx - tab_span/2 - 4;          // outer face of left tower

echo(str("servo body bottom z=", servo_bot, "  arm bottom z=", arm_z0,
         "  button z=", btn_z, "  finger length=", arm_z0 + arm_t - (btn_z - pad_h/2)));
assert(servo_bot >= 2, "deck_h too low for the servo - raise deck_h");
assert(btn_z - pad_h/2 > deck_h + 0.5, "finger would hit the deck");

// =====================================================================
//  Servo pocket + module, built for the LEFT side; mirrored for right
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
        // tab screw pilot holes (M2 / the screws that come with the SG90)
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

module side_body(window_ranges) {
    difference() {
        union() {
            // rail the phone back rests on
            translate([-wall_t, -cradle_len, 0]) cube([wall_t + rail_w, cradle_len, deck_h]);
            // side wall + lip
            translate([-wall_t, -cradle_len, 0]) cube([wall_t, cradle_len, wall_top]);
            translate([-wall_t, -cradle_len, wall_top - lip_t]) cube([wall_t + lip_w, cradle_len, lip_t]);
        }
        // windows in the wall above the deck where the fingers / slider are
        for (r = window_ranges)
            translate([-wall_t - 1, r[0], deck_h]) cube([wall_t + lip_w + 2, r[1] - r[0], 50]);
    }
}

// ---------------- Base -------------------------------------------------
module base() {
    vol_win  = [[vol_shaft_y - vol_reach - peg_wid/2 - 3, vol_shaft_y + vol_reach + peg_wid/2 + 3]];
    pwr_win  = [[y_pwr - peg_wid/2 - 3, y_pwr + peg_wid/2 + 3],
                [y_alert - alert_len/2, y_alert + alert_len/2]];
    difference() {
        union() {
            // base plate
            translate([tower_x0, -cradle_len, 0])
                cube([inner_w - 2*tower_x0, cradle_len + stop_t, plate_t]);
            // left side
            side_body(vol_win);
            tower_block(vol_shaft_y);
            // right side (mirror)
            translate([inner_w, 0, 0]) mirror([1, 0, 0]) {
                side_body(pwr_win);
                tower_block(pwr_shaft_y);
            }
            // top end stop (a short post on the right part of the top edge)
            translate([stop_x0, 0, 0]) cube([stop_x1 - stop_x0, stop_t, deck_h + 5]);
            translate([inner_w - rail_w, 0, 0]) cube([rail_w + wall_t, stop_t, deck_h]);
        }
        servo_pocket(vol_shaft_y);
        translate([inner_w, 0, 0]) mirror([1, 0, 0]) servo_pocket(pwr_shaft_y);
        // weight-saving / cable slots in the plate
        for (yy = [-cradle_len + 15, -cradle_len/2 + 5])
            translate([rail_w + 6, yy, -1]) cube([inner_w - 2*rail_w - 12, 18, plate_t + 2]);
    }
}

// ---------------- Printed fingers (sit on top of the stock horn) ------
// Local frame: shaft at origin, +x toward the phone, z=0 = arm underside
// (resting on the top of the horn). `tips` = list of finger y-offsets.
module arm(tips) {
    peg_bot = (btn_z - pad_h/2) - arm_z0;      // negative: hangs down
    bar_half = horn_len/2 + 2;
    difference() {
        union() {
            // bar that covers the stock horn
            hull() for (s = [-1, 1]) translate([0, s*bar_half, 0])
                cylinder(d = 8, h = arm_t);
            for (ty = tips) {
                // bridge from bar out to the finger
                hull() {
                    translate([0, ty, 0]) cylinder(d = peg_wid, h = arm_t);
                    translate([peg_x - peg_th, ty - peg_wid/2, 0]) cube([peg_th, peg_wid, arm_t]);
                }
                // finger hanging down to the button
                translate([peg_x - peg_th, ty - peg_wid/2, peg_bot])
                    cube([peg_th, peg_wid, arm_t - peg_bot]);
                // rounded contact pad
                translate([peg_x - pad_h/2, ty, peg_bot + pad_h/2])
                    rotate([90, 0, 0]) cylinder(d = pad_h, h = peg_wid, center = true);
            }
        }
        // recess for the stock double horn (keys the arm against rotation)
        translate([0, 0, -0.01]) linear_extrude(horn_t + 0.2)
            hull() {
                circle(d = horn_w_hub + 0.6);
                for (s = [-1, 1]) translate([0, s*(horn_len/2 - horn_w_tip/2)]) circle(d = horn_w_tip + 0.6);
            }
        // horn screw through the middle + counterbore for its head
        translate([0, 0, -1]) cylinder(d = 2.4, h = 20);
        translate([0, 0, arm_t - 1.4]) cylinder(d = 5, h = 5);
        // pilot holes so the small horn screws can pin the horn's outer holes
        for (s = [-1, 1]) translate([0, s*(horn_len/2 - 3), -1]) cylinder(d = 1.4, h = 20);
    }
}

module arm_vol() { arm([-vol_reach, vol_reach]); }
module arm_pwr() { arm([pwr_reach]); }

// ---------------- Preview helpers -------------------------------------
module sg90_dummy() {
    color("DodgerBlue") {
        translate([-servo_l/2, -servo_w/2, 0]) cube([servo_l, servo_w, 22.7]);
        translate([-tab_span/2, -servo_w/2, tab_z]) cube([tab_span, servo_w, tab_t]);
    }
    color("White") translate([servo_l/2 - shaft_off, 0, 0])
        cylinder(d = 4.8, h = horn_top_h);
}

module assembly() {
    color("Orange") base();
    // phone
    color([0.1, 0.1, 0.12, 0.85])
        translate([fit, -phone_l, deck_h]) cube([phone_w, phone_l, phone_t]);
    // left servo + volume arm
    translate([servo_cx, vol_shaft_y, servo_bot]) sg90_dummy();
    color("Gold") translate([-servo_d, vol_shaft_y, arm_z0]) arm_vol();
    // right servo + power arm
    translate([inner_w, 0, 0]) mirror([1, 0, 0]) {
        translate([servo_cx, pwr_shaft_y, servo_bot]) sg90_dummy();
        color("Gold") translate([-servo_d, pwr_shaft_y, arm_z0]) arm_pwr();
    }
}

// ---------------- Output ----------------------------------------------
if (part == "assembly") assembly();
else if (part == "base") base();
// arms are flipped so their flat top prints on the bed - no supports
else if (part == "arm_vol") rotate([180, 0, 0]) translate([0, 0, -arm_t]) arm_vol();
// the power arm lives on the mirrored (right) side, so print it mirrored
else if (part == "arm_pwr") rotate([180, 0, 0]) translate([0, 0, -arm_t]) mirror([1, 0, 0]) arm_pwr();
