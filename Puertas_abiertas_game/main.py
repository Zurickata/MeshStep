import pygame
import sys
import time
import json
import os
import random
import math

# --- Configuración ---
WIDTH, HEIGHT = 600, 600
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BORDER_COLOR = (86, 219, 130)  # #56db82
MAX_DEPTH = 4

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego Quadtree!")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 28)
BIG_FONT = pygame.font.SysFont(None, 72)

# --- Cargar imágenes de niveles ---
levels = ["level1.png", "level2.png"]
level_images = []
for img in levels:
    if os.path.exists(img):
        bg = pygame.image.load(img).convert_alpha()  # <-- cambio aquí
        bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
        level_images.append(bg)
    else:
        level_images.append(None)

# --- Cargar fondo del menú ---
menu_background = None
if os.path.exists("menu_bg.png"):
    menu_background = pygame.image.load("menu_bg.png").convert()
    menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))

# --- Cargar fondo nivel secreto ---
secret_bg_img = None
if os.path.exists("secret_level.png"):
    secret_bg_img = pygame.image.load("secret_level.png").convert_alpha()
    secret_bg_img = pygame.transform.scale(secret_bg_img, (WIDTH, HEIGHT))

# --- Clase Quadtree ---
class Quad:
    def __init__(self, x, y, size, depth=0, parent=None):
        self.x, self.y, self.size = x, y, size
        self.depth = depth
        self.parent = parent
        self.color = None
        self.children = []

    def is_leaf(self):
        return len(self.children) == 0

    def subdivide(self):
        if self.depth >= MAX_DEPTH or not self.is_leaf():
            return
        half = self.size // 2
        self.children = [
            Quad(self.x, self.y, half, self.depth+1, self),
            Quad(self.x+half, self.y, half, self.depth+1, self),
            Quad(self.x, self.y+half, half, self.depth+1, self),
            Quad(self.x+half, self.y+half, half, self.depth+1, self)
        ]
        self.color = None

    def collapse(self):
        self.children = []

    def draw(self, surf, highlight=False):
        if self.is_leaf():
            if self.color:
                s = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
                s.fill((*self.color, 150))
                surf.blit(s, (self.x, self.y))
            pygame.draw.rect(surf, BORDER_COLOR, (self.x, self.y, self.size, self.size), 2)
            if highlight:
                pygame.draw.rect(surf, YELLOW, (self.x, self.y, self.size, self.size), 3)
        else:
            for ch in self.children:
                ch.draw(surf, highlight)

    def get_leaf_at(self, mx, my):
        if not (self.x <= mx < self.x+self.size and self.y <= my < self.y+self.size):
            return None
        if self.is_leaf():
            return self
        for ch in self.children:
            found = ch.get_leaf_at(mx, my)
            if found:
                return found
        return None

    def to_dict(self):
        return {
            "x": self.x, "y": self.y, "size": self.size, "depth": self.depth,
            "color": list(self.color) if self.color else None,
            "children": [c.to_dict() for c in self.children]
        }

def dict_to_quad(data, parent=None):
    q = Quad(data["x"], data["y"], data["size"], data.get("depth",0), parent)
    q.color = tuple(data["color"]) if data.get("color") else None
    for child in data.get("children",[]):
        q.children.append(dict_to_quad(child, q))
    return q

# --- Guardar historial de intentos ---
def log_attempt(level, root, results_display, start_time):
    """
    Guarda un intento completo para KPIs
    - level: número de nivel
    - root: objeto Quad del intento
    - results_display: lista de resultados evaluados
    - start_time: timestamp de inicio del intento
    """
    path = "attempts.json"
    data = {}
    if os.path.exists(path):
        with open(path,"r") as f:
            try:
                data = json.load(f)
            except:
                data = {}

    # Determinar mejor resultado
    if results_display:
        best = max(results_display, key=lambda r: r["score"])
        best_score = best["score"]
        solution_name = best["solution"]
    else:
        best_score = 0
        solution_name = None

    # contar hojas pintadas
    def flatten_colored_leaves(q):
        leaves = []
        if q.get("children"):
            for c in q["children"]:
                leaves.extend(flatten_colored_leaves(c))
        else:
            if q.get("color"):
                leaves.append(q)
        return leaves

    colored_leaves = flatten_colored_leaves(root.to_dict())
    total_leaves = sum_leaf_area(root.to_dict())  # área total
    colored_area = sum(l["size"]**2 for l in colored_leaves)
    percentage_colored = int((colored_area / total_leaves) * 100) if total_leaves > 0 else 0

    attempt_record = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "level": level,
        "score": best_score,
        "solution_name": solution_name,
        "time_elapsed": round(time.time() - start_time, 2),
        "cells_colored": len(colored_leaves),
        "total_area": total_leaves,
        "colored_area": colored_area,
        "percentage_colored": percentage_colored
    }

    if str(level) not in data:
        data[str(level)] = []
    data[str(level)].append(attempt_record)

    with open(path,"w") as f:
        json.dump(data,f,indent=4)

    print(f"Intento registrado: Nivel {level}, Score {best_score}, Tiempo {attempt_record['time_elapsed']}s")


# --- Guardar soluciones ---
def save_solution(level, name, root):
    sol = {}
    path = "solutions.json"
    if os.path.exists(path):
        with open(path,"r") as f:
            sol = json.load(f)
    if str(level) not in sol:
        sol[str(level)] = {}
    sol[str(level)][name] = root.to_dict()
    with open(path,"w") as f:
        json.dump(sol,f,indent=4)
    print(f"Solución '{name}' guardada para nivel {level}")

# --- Comparación con peso por área ---
def compare_quads(q1, q2):
    if q1.get("children") and q2.get("children"):
        acc = 0.0
        weights = [c["size"]**2 for c in q2["children"]]
        total_area = sum(weights)
        for c1, c2 in zip(q1.get("children",[]), q2.get("children",[])):
            acc += compare_quads(c1,c2) * (c2["size"]**2/total_area)
        return acc
    elif not q1.get("children") and not q2.get("children"):
        if q1.get("color")==q2.get("color") and q1.get("color") is not None:
            return q2["size"]**2
        else:
            return 0
    else:
        return 0

def sum_leaf_area(q):
    if q.get("children"):
        return sum(sum_leaf_area(c) for c in q["children"])
    else:
        return q["size"]**2

def evaluate_attempt(level, root):
    path = "solutions.json"
    if not os.path.exists(path):
        return []

    with open(path,"r") as f:
        sol = json.load(f)

    results=[]
    if str(level) not in sol:
        return results

    def flatten_colored_leaves(q):
        """Devuelve lista de hojas coloreadas: (x, y, size, color)"""
        leaves = []
        if q.get("children"):
            for c in q["children"]:
                leaves.extend(flatten_colored_leaves(c))
        else:
            if q.get("color"):
                leaves.append((q["x"], q["y"], q["size"], tuple(q["color"])))
        return leaves

    root_leaves = flatten_colored_leaves(root.to_dict())

    for name, sol_tree in sol[str(level)].items():
        sol_leaves = flatten_colored_leaves(sol_tree)

        matched_area = 0
        total_area = sum(s[2]**2 for s in sol_leaves)

        for sx, sy, ssize, scolor in sol_leaves:
            for rx, ry, rsize, rcolor in root_leaves:
                if rx == sx and ry == sy and rsize == ssize and rcolor == scolor:
                    matched_area += rsize**2
                    break  # coincidencia encontrada

        score = int((matched_area / total_area) * 100)
        results.append({"solution": name, "score": score})

    return results



# --- Confetti ---
class ConfettiParticle:
    def __init__(self):
        self.reset()
    def reset(self):
        self.x=random.randint(0,WIDTH)
        self.y=random.randint(-HEIGHT,-10)
        self.size=random.randint(4,9)
        self.color=random.choice([(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255)])
        self.speed=random.uniform(1.5,4.0)
        self.angle=random.uniform(-0.3,0.3)
    def update(self):
        self.y+=self.speed
        self.x+=self.angle*2
        if self.y>HEIGHT+50:
            self.reset()
    def draw(self,surf):
        pygame.draw.rect(surf,self.color,(int(self.x),int(self.y),self.size,self.size))

# --- Fondo estilo espacio para nivel secreto ---
class Star:
    def __init__(self):
        self.reset()
    def reset(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.randint(1, 3)
        self.brightness = random.randint(100, 255)
        self.speed = random.uniform(0.5, 1.3)
    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.reset()
            self.y = 0
    def draw(self, surf):
        color = (self.brightness, self.brightness, self.brightness)
        pygame.draw.circle(surf, color, (int(self.x), int(self.y)), self.size)


# --- Estado inicial ---
current_level=None
root=None
started=False
attempt_finished=False
results_display=[]
highlighted=None
start_time=None
animating_score=False
anim_start_time=None
score_to_reach=0
current_score=0
confetti_active=False
confetti_particles=[]
solution_view_mode=False
solutions_list=[]
solution_index=0
root_backup=None
show_tutorial = False
RETRY_RECT=pygame.Rect(200,400,200,40)
EVAL_RECT=pygame.Rect(200,460,200,40)
num_stars = 200
stars = [Star() for _ in range(num_stars)]


# --- Reset ---
def reset_game():
    global current_level, root, started, attempt_finished, results_display
    global highlighted, start_time, animating_score, current_score
    global confetti_active, confetti_particles, solution_view_mode, solutions_list, root_backup
    current_level=None
    root=None
    started=False
    attempt_finished=False
    results_display=[]
    highlighted=None
    start_time=None
    animating_score=False
    current_score=0
    confetti_active=False
    confetti_particles=[]
    solution_view_mode=False
    solutions_list=[]
    root_backup=None

reset_game()

# --- Loop principal ---
running = True
# --- Fondo del menú ---
menu_background = None
if os.path.exists("menu_bg.png"):
    menu_background = pygame.image.load("menu_bg.png")
    menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))


while running:
    mx, my = pygame.mouse.get_pos()
    screen.fill(WHITE)


    keys = pygame.key.get_pressed()

    # --- Pantalla de tutorial ---
    if show_tutorial:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show_tutorial = False

        # Fondo base del tutorial
        if menu_background:
            screen.blit(menu_background, (0, 0))
        else:
            screen.fill((230, 250, 230))

        # --- Bloque sólido encima del fondo ---
        overlay = pygame.Surface((WIDTH - 100, HEIGHT - 150), pygame.SRCALPHA)
        rect_color = (245, 255, 250)
        border_color = (86, 219, 130)
        pygame.draw.rect(overlay, rect_color, overlay.get_rect(), border_radius=20)
        pygame.draw.rect(overlay, border_color, overlay.get_rect(), 6, border_radius=20)
        screen.blit(overlay, (50, 75))

        # Título y texto
        title = BIG_FONT.render("Tutorial", True, (20, 40, 20))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        lines = [
            "Clic izquierdo: subdividir cuadrado",
            "Clic derecho: colapsar subdivisión",
            "Q: borrar color    |   E: pintar verde",
            "Enter: terminar intento",
            "R: reiniciar",
            #"F10: guardar solución   |   F9: ver soluciones",
            "ESC: salir del tutorial"
        ]
        for i, text in enumerate(lines):
            txt = FONT.render(text, True, (0, 0, 0))
            screen.blit(txt, (100, 180 + i * 55))

        pygame.display.flip()
        clock.tick(30)
        continue

    # --- MENÚ PRINCIPAL ---
    if not started:
        if menu_background:
            screen.blit(menu_background, (0, 0))
        else:
            screen.fill((240, 240, 240))

        level_names = ["Mario", "Minecraft", "Castillo final"]
        for i, bg in enumerate(level_images):
            rect = pygame.Rect(200, 200 + i * 100, 200, 50)
            pygame.draw.rect(screen, (200, 200, 200), rect)
            txt = FONT.render(level_names[i], True, (0, 0, 0))
            screen.blit(txt, (rect.centerx - txt.get_width() // 2,
                              rect.centery - txt.get_height() // 2))

        # --- Nivel secreto si se mantiene S ---
        if keys[pygame.K_s]:
            secret_rect = pygame.Rect(200, 200 + len(level_images)*100, 200, 50)
            pygame.draw.rect(screen, (255, 215, 0), secret_rect)
            secret_txt = FONT.render("Nivel Secreto", True, (0, 0, 0))
            screen.blit(secret_txt, (secret_rect.centerx - secret_txt.get_width() // 2,
                                     secret_rect.centery - secret_txt.get_height() // 2))

    else:
        # --- Niveles normales ---
        screen.fill(WHITE)
        # Fondo del nivel
        if current_level < len(level_images) and level_images[current_level]:
            screen.blit(level_images[current_level], (0, 0))
        # Nivel secreto
        elif current_level == len(level_images):
            # Fondo estilo espacio
            screen.fill((5, 5, 30))  # fondo negro
            for star in stars:
                star.update()
                star.draw(screen)
            # Dibujar personaje secreto encima
            if secret_bg_img:
                screen.blit(secret_bg_img, (0, 0))

        # Dibujar quadtree
        if root:
            highlighted = root.get_leaf_at(mx, my)
            root.draw(screen, highlight=bool(highlighted))
        else:
            highlighted = None

        # Score y confetti
        if attempt_finished and animating_score:
            elapsed = time.time() - anim_start_time
            duration = 2.0
            t = min(elapsed / duration, 1.0)
            eased_t = 1 - (1-t)**3
            current_score = int(score_to_reach * eased_t)
            color = (0, 200, 0)
            size = 72
            display_score = current_score
            if score_to_reach > 94:
                display_score = 100
                size = 72 + int(20*abs(math.sin(time.time()*5)))
                color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
            score_text = BIG_FONT.render(f"Nota: {display_score}", True, color)
            screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
            if t >= 1.0:
                animating_score = False
                if score_to_reach >= 60:
                    confetti_active = True
                    confetti_particles = [ConfettiParticle() for _ in range(200)]

        if confetti_active:
            for p in confetti_particles:
                p.update()
                p.draw(screen)

    # --- Botones ---
    if started and attempt_finished:
        pygame.draw.rect(screen, (200, 200, 200), RETRY_RECT)
        screen.blit(FONT.render("Reintentar", True, (0,0,0)),
                    (RETRY_RECT.centerx - FONT.size("Reintentar")[0]//2,
                     RETRY_RECT.centery - FONT.size("Reintentar")[1]//2))
        pygame.draw.rect(screen, (200, 200, 200), EVAL_RECT)
        screen.blit(FONT.render("Evaluar", True, (0,0,0)),
                    (EVAL_RECT.centerx - FONT.size("Evaluar")[0]//2,
                     EVAL_RECT.centery - FONT.size("Evaluar")[1]//2))
        if results_display:
            y = 520
            for r in results_display:
                s = FONT.render(f"{r['solution']}: {r['score']}%", True, (0,0,0))
                screen.blit(s, (10, y))
                y += 26

    # --- Eventos ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Tutorial con W en cualquier momento
            if event.key == pygame.K_w:
                show_tutorial = True
            # ESC sale del tutorial
            if show_tutorial and event.key == pygame.K_ESCAPE:
                show_tutorial = False
            if event.key == pygame.K_r:
                reset_game()
            if event.key == pygame.K_F10 and started and not solution_view_mode:
                name = time.strftime("sol_%Y%m%d_%H%M%S")
                save_solution(current_level, name, root)
            if event.key == pygame.K_F9 and started:
                # Manejo de soluciones
                path="solutions.json"
                if not solution_view_mode and os.path.exists(path):
                    with open(path,"r") as f:
                        sol = json.load(f)
                    if str(current_level) in sol and sol[str(current_level)]:
                        solutions_list = list(sol[str(current_level)].items())
                        solution_index = 0
                        root_backup = root.to_dict()
                        root = dict_to_quad(solutions_list[solution_index][1])
                        solution_view_mode = True
                        print(f"Mostrando solución {solutions_list[solution_index][0]}")
                elif solution_view_mode:
                    if solutions_list:
                        solution_index = (solution_index + 1) % len(solutions_list)
                        root = dict_to_quad(solutions_list[solution_index][1])
                        print(f"Mostrando solución {solutions_list[solution_index][0]}")
            if event.key == pygame.K_ESCAPE and solution_view_mode:
                if root_backup:
                    root = dict_to_quad(root_backup)
                solution_view_mode = False
                solutions_list = []
                root_backup = None
            if started and not solution_view_mode and highlighted:
                if event.key == pygame.K_e:
                    highlighted.color = (0,200,0)
                elif event.key == pygame.K_q:
                    highlighted.color = None
            if event.key == pygame.K_RETURN and started and not attempt_finished:
                attempt_finished = True
                confetti_active = False
                confetti_particles = []
                results_display = []

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button in (1,3):
            mx, my = event.pos
            # --- Selección de nivel ---
            if not started:
                for i in range(len(level_images)):
                    r = pygame.Rect(200, 200 + i*100, 200, 50)
                    if r.collidepoint(mx, my):
                        current_level = i
                        root = Quad(0,0,WIDTH)
                        started = True
                        attempt_finished = False
                        start_time = time.time()
                        results_display = []
                        confetti_active = False
                        confetti_particles = []
                        solution_view_mode = False
                        print(f"Nivel {i} seleccionado")
                        break
                # Nivel secreto
                if keys[pygame.K_s]:
                    secret_rect = pygame.Rect(200, 200 + len(level_images)*100, 200, 50)
                    if secret_rect.collidepoint(mx, my):
                        current_level = len(level_images)
                        root = Quad(0,0,WIDTH)
                        started = True
                        attempt_finished = False
                        start_time = time.time()
                        results_display = []
                        confetti_active = False
                        confetti_particles = []
                        solution_view_mode = False
                        print("¡Nivel Secreto seleccionado!")
            else:
                if attempt_finished:
                    if RETRY_RECT.collidepoint(mx, my):
                        root = Quad(0,0,WIDTH)
                        attempt_finished = False
                        animating_score = False
                        current_score = 0
                        results_display = []
                        confetti_active = False
                        confetti_particles = []
                        print("Reintentar")
                    elif EVAL_RECT.collidepoint(mx, my):
                        results_display = evaluate_attempt(current_level, root)
                        if results_display:
                            print("=== Resultados ===")
                            for r in results_display:
                                print(r)
                            score_to_reach = max(r["score"] for r in results_display)
                            anim_start_time = time.time()
                            animating_score = True
                            log_attempt(current_level, root, results_display, start_time)
                        else:
                            print("No hay soluciones guardadas")
                else:
                    if highlighted:
                        if event.button == 1:
                            highlighted.subdivide()
                        elif event.button == 3:
                            if highlighted.parent:
                                highlighted.parent.collapse()

    pygame.display.flip()
    clock.tick(30)


pygame.quit()
sys.exit()
