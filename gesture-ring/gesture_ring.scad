// =====================================================================
//  Gesture Ring v1 - BLE mouse / macro ring housing
// =====================================================================
//  Worn on the INDEX finger (proximal segment). A top "pod" holds a
//  Seeed XIAO nRF52840 Sense (BLE + 6-axis IMU + LiPo charger) stacked
//  over a small LiPo cell. A side "lobe" facing the thumb holds two tiny
//  tactile switches the thumb presses while the hand rests on a desk.
//
//  Coordinates: finger axis = Y (+Y toward the fingertip), Z = back of
//  the hand (up), -X = thumb side for a RIGHT hand.
//
//  Parts (set `part`, or from the CLI):
//    openscad -D 'part="ring"'  -o stl/ring.stl   gesture_ring.scad
//    openscad -D 'part="lid"'   -o stl/lid.stl    gesture_ring.scad
//    openscad -D 'part="sizer"' -o stl/sizer.stl  gesture_ring.scad
// =====================================================================

part = "assembly";      // "assembly" | "worn" | "ring" | "lid" | "sizer" | "section"
hand = "right";         // "right" or "left" (mirrors the thumb lobe)

$fn = 96;

// ---------------- Fit --------------------------------------------------
// US ring size of the finger you will wear it on (measure with the
// printed sizer first). Inner diameter = 11.63 + 0.8128 * size.
ring_size_us = 9;
size_fudge   = 0.2;     // extra inner diameter for printing tolerance
band_t       = 1.8;     // band wall thickness
band_w       = 10;      // band width along the finger
comfort_ch   = 0.7;     // rounded-off inner edges

// ---------------- Electronics -----------------------------------------
// Seeed XIAO nRF52840 Sense
xiao_l   = 21.0;        // along the finger (USB-C end toward fingertip)
xiao_w   = 17.8;
xiao_pcb = 1.0;         // PCB thickness
usb_h    = 3.2;         // USB-C height above the PCB (tallest part) - measure
usb_w    = 9.0;
// LiPo cell under the board (default "401012": 4.0 x 10 x 12 mm, ~50 mAh).
// Length includes the little protection board on the end of the cell.
bat_t    = 4.0;
bat_w    = 10.5;
bat_l    = 15.0;
wire_gap = 0.5;         // room for the battery leads under the board

// Tactile switches on the thumb lobe ("3x6x2.5 mm" type)
sw_n     = 2;
sw_len   = 8.4;         // pocket length incl. the solder legs
sw_wid   = 3.4;         // pocket height
sw_depth = 1.9;         // pocket depth -> the stem sticks out ~0.6-0.8 mm
sw_gap   = 1.6;         // web between pockets

// ---------------- Housing ---------------------------------------------
clr      = 0.25;        // clearance around the board
wall     = 1.4;
floor_t  = 1.0;
lift     = 0.6;         // pod floor height above the finger surface
ledge    = 1.3;         // ledges the board rests on
lid_t    = 1.2;
lid_plug = 1.0;         // locating rim under the lid
corner_r = 2.2;
lobe_out = 3.0;         // how far the thumb lobe stands off the band
lobe_z0  = -1.5;
lobe_z1  = 9.5;

// ---------------- Derived ---------------------------------------------
inner_d  = 11.63 + 0.8128*ring_size_us + size_fudge;
r_in     = inner_d/2;
r_out    = r_in + band_t;

cav_w    = xiao_w + 2*clr;
cav_l    = xiao_l + 2*clr;
pod_w    = cav_w + 2*wall;
pod_l    = cav_l + 2*wall;

pod_bot  = r_in + lift;
cav_bot  = pod_bot + floor_t;
board_z  = cav_bot + bat_t + wire_gap;            // underside of the PCB
wall_top = board_z + xiao_pcb + usb_h + 0.3;      // lid sits here
pod_top  = wall_top + lid_t;

lobe_len = sw_n*sw_len + (sw_n - 1)*sw_gap + 2*wall;
lobe_x   = -(r_out + lobe_out);                   // outer face of the lobe
sw_z     = (lobe_z0 + lobe_z1)/2;

echo(str("inner diameter ", inner_d, " mm; pod ", pod_w, " x ", pod_l,
         " mm; top of pod is ", pod_top - r_in, " mm above the finger"));
assert(bat_w <= cav_w - 2*ledge, "battery too wide for the space under the board");
assert(bat_l <= cav_l, "battery too long");
assert(lobe_len <= pod_l + 2, "too many switches for the lobe");

// ---------------- Helpers ---------------------------------------------
module rrect(w, l, h, r = corner_r) {           // rounded box, centred in x/y
    hull() for (sx = [-1, 1], sy = [-1, 1])
        translate([sx*(w/2 - r), sy*(l/2 - r), 0]) cylinder(r = r, h = h);
}
module ycyl(r, l) rotate([90, 0, 0]) cylinder(r = r, h = l, center = true);

// ---------------- Ring body --------------------------------------------
module pod_block() translate([0, 0, pod_bot]) rrect(pod_w, pod_l, wall_top - pod_bot);

module band_top() intersection() {
    ycyl(r_out, band_w);
    translate([-50, -50, 0]) cube(100);
}

module lobe_block() {
    r = 1.6;
    hull() for (y = [-1, 1], z = [lobe_z0 + r, lobe_z1 - r])
        translate([lobe_x, y*(lobe_len/2 - r), z]) rotate([0, 90, 0])
            cylinder(r = r, h = lobe_x*-1 - (r_out - 3));
}

module ring_solid() {
    union() {
        ycyl(r_out, band_w);
        hull() { pod_block(); band_top(); }
        hull() {
            lobe_block();
            translate([-pod_w/2, 0, pod_bot]) rrect(0.01 + 2*corner_r, pod_l, 0.01);
        }
    }
}

// switch y-centres along the lobe
function sw_y(i) = -lobe_len/2 + wall + sw_len/2 + i*(sw_len + sw_gap);

module cavities() {
    // finger hole + extra clearance where the pod overhangs the band
    ycyl(r_in, 200);
    difference() { ycyl(r_in + lift, 200); ycyl(50, band_w); }
    // comfort chamfers on the inner edges of the band
    for (s = [-1, 1]) translate([0, s*band_w/2, 0]) rotate([s*90, 0, 0])
        cylinder(r1 = r_in + comfort_ch, r2 = r_in - 0.01, h = comfort_ch + 0.01);
    // board bay (open top, closed by the lid)
    translate([0, 0, board_z]) rrect(cav_w, cav_l, 50, 1);
    // battery bay under the board, narrower -> leaves ledges for the board
    translate([0, 0, cav_bot]) rrect(cav_w - 2*ledge, cav_l, board_z - cav_bot + 0.01, 1);
    // USB-C opening at the fingertip end
    translate([-(usb_w + 3)/2, cav_l/2 - 1, board_z + xiao_pcb - 0.4])
        cube([usb_w + 3, wall + 2, 50]);
    // switch pockets on the thumb side + wire channels into the battery bay
    for (i = [0 : sw_n - 1]) {
        y = sw_y(i);
        translate([lobe_x - 1, y - sw_len/2, sw_z - sw_wid/2])
            cube([sw_depth + 1, sw_len, sw_wid]);
        hull() {
            translate([lobe_x + sw_depth - 0.2, y, sw_z]) sphere(r = 0.85, $fn = 16);
            translate([lobe_x + sw_depth + 0.4, y*0.6, lobe_z1 - 1.2]) sphere(r = 0.85, $fn = 16);
        }
        hull() {
            translate([lobe_x + sw_depth + 0.4, y*0.6, lobe_z1 - 1.2]) sphere(r = 0.85, $fn = 16);
            translate([-(cav_w/2 - ledge) + 1, y*0.4, cav_bot + 1]) sphere(r = 0.85, $fn = 16);
        }
    }
}

module ring() {
    m = hand == "left" ? 1 : 0;
    mirror([m, 0, 0]) difference() { ring_solid(); cavities(); }
}

// ---------------- Lid --------------------------------------------------
// Print the lid in translucent filament so the board's LEDs show through.
module lid() {
    rrect(pod_w, pod_l, lid_t);
    translate([0, 0, -lid_plug]) difference() {
        rrect(cav_w - 0.3, cav_l - 0.3, lid_plug + 0.01, 0.9);
        translate([0, 0, -1]) rrect(cav_w - 0.3 - 1.6, cav_l - 0.3 - 1.6, lid_plug + 2, 0.5);
        // clear the USB-C connector at the fingertip end
        translate([-(usb_w + 1)/2, cav_l/2 - 4, -1]) cube([usb_w + 1, 5, lid_plug + 2]);
    }
}

// ---------------- Sizer (plain band, same inner diameter) ---------------
module sizer() difference() {
    ycyl(r_out, 8);
    ycyl(r_in, 20);
    for (s = [-1, 1]) translate([0, s*4, 0]) rotate([s*90, 0, 0])
        cylinder(r1 = r_in + comfort_ch, r2 = r_in - 0.01, h = comfort_ch + 0.01);
}

// ---------------- Preview dummies --------------------------------------
module electronics() {
    m = hand == "left" ? 1 : 0;
    mirror([m, 0, 0]) {
        color("SteelBlue") translate([-xiao_w/2, -xiao_l/2, board_z]) cube([xiao_w, xiao_l, xiao_pcb]);
        color("Silver") translate([-usb_w/2, xiao_l/2 - 7.5, board_z + xiao_pcb]) cube([usb_w, 7.5, usb_h]);
        color("DimGray") translate([-3.5, -4, board_z + xiao_pcb]) cube([7, 7, 0.9]);
        color("Gold") translate([-bat_w/2, -bat_l/2, cav_bot]) cube([bat_w, bat_l, bat_t]);
        for (i = [0 : sw_n - 1]) color("Black")
            translate([lobe_x - 0.7, sw_y(i) - 3, sw_z - 1.5]) cube([2.5, 6, 3]);
    }
}

// ---------------- Output ----------------------------------------------
if (part == "assembly") {
    color("WhiteSmoke") ring();
    electronics();
    color([1, 1, 1, 0.45]) translate([0, 0, wall_top + 8]) lid();
    color([0.95, 0.8, 0.7, 0.35]) ycyl(r_in - 0.3, 60);      // finger
}
else if (part == "worn") {      // ring + parts as worn, no finger/lid
    color("WhiteSmoke") ring();
    electronics();
}
else if (part == "section") {   // cut through the middle of one switch
    intersection() {
        union() { color("WhiteSmoke") ring(); electronics(); }
        translate([-50, sw_y(0) - 0.5 - 50, -50]) cube([100, 50, 100]);
    }
}
// print the ring pod-opening-down: flat face on the bed, no supports
else if (part == "ring")  translate([0, 0, wall_top]) rotate([180, 0, 0]) ring();
else if (part == "lid")   translate([0, 0, lid_t]) rotate([180, 0, 0]) lid();
else if (part == "sizer") translate([0, 0, 4]) rotate([90, 0, 0]) sizer();
