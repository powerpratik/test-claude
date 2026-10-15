/*
  Phone Claw firmware - ESP8266 (Wemos D1 mini)

  Two SG90 servos press the OnePlus 7 Pro buttons:
    VOL servo (left side, D5)  : rocks one way for VOL UP, the other for VOL DOWN
    PWR servo (right side, D6) : presses POWER

  Control it from:
    * a web page   -> open http://phoneclaw.local/ (or the IP printed on Serial)
    * HTTP API     -> /press?b=up|down|power|shot&ms=150
    * Serial 115200-> u = vol up, d = vol down, p = power, P = long power,
                      s = screenshot (power + vol down), ? = help

  Calibrate once from the web page (jog sliders, then "Save"); the angles are
  stored in flash so they survive reboots.

  Board: "LOLIN(WEMOS) D1 R2 & mini" (ESP8266 core). No extra libraries needed.
*/

#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <EEPROM.h>
#include <Servo.h>

// ---------- WiFi ----------------------------------------------------------
// Fill in your home WiFi. If it can't connect within 15 s the board starts its
// own access point "PhoneClaw" (password below) - connect and open 192.168.4.1
const char* WIFI_SSID = "YOUR_WIFI";
const char* WIFI_PASS = "YOUR_PASSWORD";
const char* AP_SSID   = "PhoneClaw";
const char* AP_PASS   = "clawclaw";   // at least 8 characters

// ---------- Pins ----------------------------------------------------------
const uint8_t PIN_VOL = D5;   // GPIO14
const uint8_t PIN_PWR = D6;   // GPIO12

// ---------- Timing --------------------------------------------------------
const uint16_t TRAVEL_MS     = 180;   // time for the servo to reach the button
const uint16_t TAP_MS        = 150;   // default press duration
const uint16_t LONG_PRESS_MS = 3000;  // long power press (power menu)
const uint16_t SHOT_MS       = 900;   // power + vol down (screenshot)

// ---------- Calibration (stored in EEPROM) -------------------------------
struct Cal {
  uint32_t magic;
  uint8_t volRest, volUp, volDown;
  uint8_t pwrRest, pwrPress;
};
const uint32_t CAL_MAGIC = 0xC1A70001;
// Safe defaults: finger centred, +/-25 deg to press. Tune with the web page.
Cal cal = {CAL_MAGIC, 90, 65, 115, 90, 115};

Servo volServo, pwrServo;
ESP8266WebServer server(80);

void loadCal() {
  EEPROM.begin(sizeof(Cal));
  Cal c;
  EEPROM.get(0, c);
  if (c.magic == CAL_MAGIC) cal = c;
}

void saveCal() {
  EEPROM.put(0, cal);
  EEPROM.commit();
}

// Move a servo and leave it powered (used for jogging during calibration).
void moveTo(Servo& s, uint8_t pin, uint8_t angle) {
  if (!s.attached()) s.attach(pin, 500, 2400);
  s.write(constrain(angle, 0, 180));
}

// Release both servos so they don't hum or keep pushing on the phone.
void relax() {
  delay(TRAVEL_MS + 100);
  volServo.detach();
  pwrServo.detach();
}

void restAll() {
  moveTo(volServo, PIN_VOL, cal.volRest);
  moveTo(pwrServo, PIN_PWR, cal.pwrRest);
}

// Press one or both buttons for `holdMs`, then return to rest.
void press(bool vol, uint8_t volAngle, bool pwr, uint16_t holdMs) {
  if (vol) moveTo(volServo, PIN_VOL, volAngle);
  if (pwr) moveTo(pwrServo, PIN_PWR, cal.pwrPress);
  delay(TRAVEL_MS + holdMs);
  if (vol) moveTo(volServo, PIN_VOL, cal.volRest);
  if (pwr) moveTo(pwrServo, PIN_PWR, cal.pwrRest);
  relax();
}

// Returns false for an unknown button name.
bool doButton(const String& b, uint16_t ms) {
  if (b == "up")         press(true, cal.volUp, false, ms ? ms : TAP_MS);
  else if (b == "down")  press(true, cal.volDown, false, ms ? ms : TAP_MS);
  else if (b == "power") press(false, 0, true, ms ? ms : TAP_MS);
  else if (b == "long")  press(false, 0, true, ms ? ms : LONG_PRESS_MS);
  else if (b == "shot")  press(true, cal.volDown, true, ms ? ms : SHOT_MS);
  else return false;
  return true;
}

// ---------- Web UI --------------------------------------------------------
const char PAGE[] PROGMEM = R"HTML(<!doctype html><html><head>
<meta name=viewport content="width=device-width,initial-scale=1"><title>Phone Claw</title>
<style>
body{font-family:system-ui,sans-serif;max-width:420px;margin:auto;padding:16px;background:#111;color:#eee}
button{width:100%;padding:18px;margin:6px 0;font-size:20px;border:0;border-radius:10px;background:#2a6df4;color:#fff}
button.alt{background:#444}.row{display:flex;gap:8px}.row button{flex:1}
label{display:block;margin-top:10px}input[type=range]{width:100%}details{margin-top:20px}
</style></head><body>
<h2>Phone Claw</h2>
<button onclick="p('up')">Volume +</button>
<button onclick="p('down')">Volume &minus;</button>
<button onclick="p('power')">Power</button>
<div class=row><button class=alt onclick="p('long')">Power (hold)</button>
<button class=alt onclick="p('shot')">Screenshot</button></div>
<details><summary>Calibrate</summary>
<p>Drag a slider: the servo moves live. Find the angle where the finger just
clicks the button (plus 2-3&deg; more), then press Save.</p>
<div id=cal></div>
<button class=alt onclick="fetch('/rest')">Go to rest</button>
<button onclick="save()">Save</button></details>
<p id=st></p>
<script>
const F=['volRest','volUp','volDown','pwrRest','pwrPress'];
function st(t){document.getElementById('st').textContent=t}
function p(b){st('...');fetch('/press?b='+b).then(r=>r.text()).then(st)}
fetch('/cal').then(r=>r.json()).then(c=>{let h='';for(const k of F)h+=
`<label>${k}: <b id=v_${k}>${c[k]}</b><input type=range min=0 max=180 value=${c[k]} id=${k}
 oninput="v_${k}.textContent=this.value;fetch('/jog?k=${k}&a='+this.value)"></label>`;
document.getElementById('cal').innerHTML=h});
function save(){fetch('/save?'+F.map(k=>k+'='+document.getElementById(k).value).join('&'))
 .then(r=>r.text()).then(st)}
</script></body></html>)HTML";

String calJson() {
  return String("{\"volRest\":") + cal.volRest + ",\"volUp\":" + cal.volUp +
         ",\"volDown\":" + cal.volDown + ",\"pwrRest\":" + cal.pwrRest +
         ",\"pwrPress\":" + cal.pwrPress + "}";
}

uint8_t* calField(const String& k) {
  if (k == "volRest") return &cal.volRest;
  if (k == "volUp") return &cal.volUp;
  if (k == "volDown") return &cal.volDown;
  if (k == "pwrRest") return &cal.pwrRest;
  if (k == "pwrPress") return &cal.pwrPress;
  return nullptr;
}

void setupWeb() {
  server.on("/", [] { server.send_P(200, "text/html", PAGE); });

  server.on("/press", [] {
    String b = server.arg("b");
    uint16_t ms = server.arg("ms").toInt();
    if (doButton(b, ms)) server.send(200, "text/plain", "pressed " + b);
    else server.send(400, "text/plain", "use b=up|down|power|long|shot");
  });

  server.on("/cal", [] { server.send(200, "application/json", calJson()); });

  // Live jog for calibration - does not save.
  server.on("/jog", [] {
    String k = server.arg("k");
    uint8_t a = constrain(server.arg("a").toInt(), 0, 180);
    if (k.startsWith("vol")) moveTo(volServo, PIN_VOL, a);
    else if (k.startsWith("pwr")) moveTo(pwrServo, PIN_PWR, a);
    server.send(200, "text/plain", "ok");
  });

  server.on("/save", [] {
    const char* keys[] = {"volRest", "volUp", "volDown", "pwrRest", "pwrPress"};
    for (const char* k : keys)
      if (server.hasArg(k)) *calField(k) = constrain(server.arg(k).toInt(), 0, 180);
    saveCal();
    restAll();
    relax();
    server.send(200, "text/plain", "saved " + calJson());
  });

  server.on("/rest", [] { restAll(); relax(); server.send(200, "text/plain", "rest"); });

  server.begin();
}

void setupWifi() {
  WiFi.mode(WIFI_STA);
  WiFi.hostname("phoneclaw");
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("Connecting to WiFi");
  for (int i = 0; i < 30 && WiFi.status() != WL_CONNECTED; i++) {
    delay(500);
    Serial.print('.');
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.printf("\nOpen http://%s/  or  http://phoneclaw.local/\n",
                  WiFi.localIP().toString().c_str());
  } else {
    WiFi.mode(WIFI_AP);
    WiFi.softAP(AP_SSID, AP_PASS);
    Serial.printf("\nNo WiFi - join \"%s\" (pw %s) and open http://%s/\n", AP_SSID,
                  AP_PASS, WiFi.softAPIP().toString().c_str());
  }
  MDNS.begin("phoneclaw");
}

void handleSerial() {
  if (!Serial.available()) return;
  char c = Serial.read();
  switch (c) {
    case 'u': doButton("up", 0); Serial.println("vol up"); break;
    case 'd': doButton("down", 0); Serial.println("vol down"); break;
    case 'p': doButton("power", 0); Serial.println("power"); break;
    case 'P': doButton("long", 0); Serial.println("power (long)"); break;
    case 's': doButton("shot", 0); Serial.println("screenshot"); break;
    case '?': Serial.println("u=vol up d=vol down p=power P=long power s=screenshot"); break;
  }
}

void setup() {
  Serial.begin(115200);
  delay(100);
  loadCal();
  restAll();   // park the fingers away from the buttons on boot
  relax();
  setupWifi();
  setupWeb();
}

void loop() {
  server.handleClient();
  MDNS.update();
  handleSerial();
}
