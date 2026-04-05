import time

# Lekal Memory Notebook
memory = {}

def run_command(cmd):
    cmd = cmd.strip()
    if not cmd: return

    # 1. The 'input >>' Rule (e.g., x = input >> "Name?")
    if "=" in cmd and "input >>" in cmd:
        try:
            parts = cmd.split("=")
            var_name = parts[0].strip()
            prompt_text = cmd.split("input >>")[1].replace('"', '').strip()
            user_val = input(prompt_text + " ")
            memory[var_name] = user_val
        except: pass

    # 2. The 'say' Command
    elif cmd.startswith("say"):
        content = cmd.split(">>")[1].strip()
        print(memory.get(content, content.replace('"', '')))
        
    # 3. The 'wait' Command
    elif cmd.startswith("wait"):
        try:
            sec = float(cmd.split(">>")[1].strip())
            time.sleep(sec)
        except: pass

    # 4. The 'calc' Command
    elif cmd.startswith("calc"):
        eq = cmd.split(">>")[1].strip()
        for name, val in memory.items():
            eq = eq.replace(name, str(val))
        try: print(eval(eq))
        except: pass

    # 5. The 'if' Rule
    elif cmd.startswith("if"):
        cond = cmd.split(">>")[1].strip()
        for name, val in memory.items():
            cond = cond.replace(name, str(val))
        try: 
            # We use eval to check the math/logic string
            if eval(cond): return True
            else: return False
        except: pass

while True:
    user_input = input("Lekal >> ")
    
    # A. The 'when touched' Rule (Game Logic)
    # Syntax: when touched lava: say >> "GameOver"
    if user_input.startswith("when touched"):
        try:
            trigger_part = user_input.split(":")[0]
            action_part = user_input.split(":")[1]
            obj_name = trigger_part.replace("when touched", "").strip()
            
            # Logic: In a game app, you'd check a hit-box here. 
            # For now, we simulate the 'touch' to show it works.
            print(f"(System: {obj_name} was touched!)")
            for sub in action_part.split("&"):
                run_command(sub)
        except: pass

    # B. Handle Repeat logic with '&' support
    elif "repeat >>" in user_input:
        try:
            parts = user_input.split("times")
            times_logic = parts[0].replace("repeat >>", "").replace("repeat", "*").strip()
            iterations = int(eval(times_logic))
            action_line = " ".join(parts[1:]).strip()
            for _ in range(iterations):
                for sub in action_line.split("&"):
                    run_command(sub)
        except: pass

    # C. Handle standard chained commands/Input with '&'
    elif "&" in user_input:
        for c in user_input.split("&"):
            run_command(c)
            
    # D. Handle standard single commands or Variables
    else:
        if ">>" in user_input:
            run_command(user_input)
        elif "=" in user_input:
            try:
                parts = user_input.split("=")
                name, value = parts[0].strip(), parts[1].strip()
                if "input >>" not in value:
                    memory[name] = value.replace('"', '')
                else:
                    run_command(user_input)
            except: pass
