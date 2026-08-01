#!/usr/bin/env python3
"""
MeowMatrix - A better cmatrix with cat vibes.
Usage: python3 meowmatrix.py [color]
Config: ~/.config/meowmatrix/config.meow
"""

import sys, os, time, random, json

COLORS = {
    "mew":"35","nya":"36","purr":"32","hiss":"31","angry":"33","trill":"34",
    "red":"31","green":"32","blue":"34","cyan":"36","magenta":"35","yellow":"33","white":"37",
    "rainbow":None,"all":None
}

CONFIG_FILE = os.path.expanduser("~/.config/meowmatrix/config.meow")
DEFAULT_CONFIG = {
    "color": "green",
    "speed": 0.05,
    "density": 0.78,
    "charset": "full",
    "tail_length": 15,
    "bold_head": True,
    "fps": 20
}

def load_config():
    try:
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE) as f:
            cfg = json.load(f)
        for k, v in DEFAULT_CONFIG.items():
            if k not in cfg:
                cfg[k] = v
        return cfg
    except:
        return dict(DEFAULT_CONFIG)

def save_default_config():
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(DEFAULT_CONFIG, f, indent=2)
    print(f"  config saved to {CONFIG_FILE}")

def main():
    cfg = load_config()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--init":
        save_default_config()
        return
    
    if len(sys.argv) > 1 and sys.argv[1] in COLORS:
        cfg["color"] = sys.argv[1]
    
    color = "32"
    rainbow_mode = False
    if cfg["color"] in COLORS:
        if cfg["color"] in ("rainbow", "all"):
            rainbow_mode = True
        else:
            color = COLORS[cfg["color"]]
    
    speed = float(cfg.get("speed", 0.05))
    density = float(cfg.get("density", 0.78))
    tail_len = int(cfg.get("tail_length", 15))
    bold_head = cfg.get("bold_head", True)
    
    charset_full = "ﾊﾐﾋｰｳｼﾅﾓﾆｻﾜﾂｵﾘｱﾎﾃﾏｹﾒｴｶｷﾑﾕﾗｾﾈｽﾀﾇﾍ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    charset_ascii = "abcdefghijklmnopqrstuvwxyz0123456789"
    charset_hex = "0123456789ABCDEF"
    charsets = {"full": charset_full, "ascii": charset_ascii, "hex": charset_hex}
    chars = charsets.get(cfg.get("charset", "full"), charset_full)
    
    cols = os.get_terminal_size().columns
    rows = os.get_terminal_size().lines
    screen = [[" "] * cols for _ in range(rows)]
    col_colors = [random.choice(["31","32","33","34","35","36"]) for _ in range(cols)]
    drops = [random.randint(-rows, 0) for _ in range(cols)]
    lengths = [random.randint(6, tail_len + 10) for _ in range(cols)]
    
    sys.stdout.write("\033[2J\033[?25l")
    print(f"  🐱 meowmatrix {cfg['color']} (Ctrl+C to stop)")
    
    try:
        while True:
            for i in range(len(drops)):
                if drops[i] < 0:
                    drops[i] += 1
                elif drops[i] == 0 and random.random() > density:
                    drops[i] = 1
                    lengths[i] = random.randint(6, tail_len + 10)
                    if rainbow_mode:
                        col_colors[i] = random.choice(["31","32","33","34","35","36"])
                if drops[i] > 0:
                    if drops[i] <= rows:
                        screen[drops[i]-1][i] = random.choice(chars)
                    if drops[i] > lengths[i] and drops[i] - lengths[i] <= rows:
                        screen[drops[i]-lengths[i]-1][i] = " "
                    drops[i] += 1
                    if drops[i] > rows + lengths[i]:
                        drops[i] = -random.randint(2, 15)
                        lengths[i] = random.randint(6, tail_len + 10)
                        if rainbow_mode:
                            col_colors[i] = random.choice(["31","32","33","34","35","36"])
            
            sys.stdout.write("\033[H")
            for y in range(rows):
                row_chars = []
                for x in range(cols):
                    ch = screen[y][x]
                    if ch != " ":
                        c = col_colors[x] if rainbow_mode else color
                        if bold_head and y > 0 and screen[y-1][x] == " ":
                            row_chars.append("\033[1;37m\033[1;" + c + "m" + ch + "\033[0m")
                        elif bold_head and y > 1 and screen[y-2][x] == " ":
                            row_chars.append("\033[1;" + c + "m" + ch + "\033[0m")
                        else:
                            row_chars.append("\033[2;" + c + "m" + ch + "\033[0m")
                    else:
                        row_chars.append(" ")
                sys.stdout.write("".join(row_chars) + "\n")
            sys.stdout.flush()
            time.sleep(speed)
    except KeyboardInterrupt:
        sys.stdout.write("\033[2J\033[H\033[?25h")
        print("🐱 meow!")

if __name__ == "__main__":
    main()
