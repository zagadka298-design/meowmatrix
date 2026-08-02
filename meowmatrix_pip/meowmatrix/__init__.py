#!/usr/bin/env python3
import sys, os, time, random, json

COLORS = {
    "red":"1;31","green":"1;32","blue":"1;34","cyan":"1;36",
    "magenta":"1;35","yellow":"1;33","white":"1;37",
    "rainbow":None,"all":None
}

CONFIG_FILE = os.path.expanduser("~/.config/meowmatrix/config.meow")
DEFAULT_CONFIG = {"color":"green","speed":0.05,"density":0.78,"charset":"full","tail_length":15,"bold_head":True}

def load_config():
    try:
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE) as f: cfg = json.load(f)
        for k,v in DEFAULT_CONFIG.items():
            if k not in cfg: cfg[k] = v
        return cfg
    except: return dict(DEFAULT_CONFIG)

def main():
    cfg = load_config()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--init":
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE,"w") as f: json.dump(DEFAULT_CONFIG,f,indent=2)
        print(f"config saved to {CONFIG_FILE}")
        return
    
    # Build color list from ALL args
    selected = []
    for a in sys.argv[1:]:
        if a in COLORS and a not in ("rainbow","all"):
            selected.append(COLORS[a])
        if a in ("rainbow","all"):
            selected = ["1;31","1;32","1;33","1;34","1;35","1;36","1;37"]
    
    if not selected:
        c = cfg.get("color","green")
        if c in ("rainbow","all"):
            selected = ["1;31","1;32","1;33","1;34","1;35","1;36","1;37"]
        else:
            selected = [COLORS.get(c,"1;32")]
    
    speed = float(cfg.get("speed",0.05))
    density = float(cfg.get("density",0.78))
    tail_len = int(cfg.get("tail_length",15))
    charset = cfg.get("charset","full")
    
    chars_map = {
        "full":"ﾊﾐﾋｰｳｼﾅﾓﾆｻﾜﾂｵﾘｱﾎﾃﾏｹﾒｴｶｷﾑﾕﾗｾﾈｽﾀﾇﾍ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "ascii":"abcdefghijklmnopqrstuvwxyz0123456789",
        "hex":"0123456789ABCDEF"
    }
    meow_mode = "meow" in sys.argv
    if meow_mode:
        chars = "🐱😺😸😻😽😼🙀😿😾"
    else:
        chars = chars_map.get(charset, chars_map["full"])
    
    cols = os.get_terminal_size().columns
    rows = os.get_terminal_size().lines
    screen = [[" "]*cols for _ in range(rows)]
    col_colors = [random.choice(selected) for _ in range(cols)]
    drops = [random.randint(-rows,0) for _ in range(cols)]
    lengths = [random.randint(6,tail_len+10) for _ in range(cols)]
    
    sys.stdout.write("\033[2J\033[?25l")
    print(f"  meowmatrix ({len(selected)} color(s)) Ctrl+C to stop")
    
    try:
        while True:
            for i in range(len(drops)):
                if drops[i] < 0:
                    drops[i] += 1
                elif drops[i] == 0 and random.random() > density:
                    drops[i] = 1
                    lengths[i] = random.randint(6,tail_len+10)
                    col_colors[i] = random.choice(selected)
                if drops[i] > 0:
                    if drops[i] <= rows:
                        screen[drops[i]-1][i] = random.choice(chars)
                    if drops[i] > lengths[i] and drops[i]-lengths[i] <= rows:
                        screen[drops[i]-lengths[i]-1][i] = " "
                    drops[i] += 1
                    if drops[i] > rows+lengths[i]:
                        drops[i] = -random.randint(2,15)
                        lengths[i] = random.randint(6,tail_len+10)
                        col_colors[i] = random.choice(selected)
            
            sys.stdout.write("\033[H")
            for y in range(rows):
                row_chars = []
                for x in range(cols):
                    ch = screen[y][x]
                    if ch != " ":
                        c = col_colors[x]
                        if y > 0 and screen[y-1][x] == " ":
                            row_chars.append("\033[1;97m"+ch+"\033[0m")
                        elif y > 1 and screen[y-2][x] == " ":
                            row_chars.append("\033[1;"+c+"m"+ch+"\033[0m")
                        else:
                            row_chars.append("\033[2;"+c+"m"+ch+"\033[0m")
                    else:
                        row_chars.append(" ")
                sys.stdout.write("".join(row_chars)+"\n")
            sys.stdout.flush()
            time.sleep(speed)
    except KeyboardInterrupt:
        sys.stdout.write("\033[2J\033[H\033[?25h")
        print("meow!")

if __name__ == "__main__":
    main()
