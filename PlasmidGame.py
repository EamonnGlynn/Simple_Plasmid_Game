import tkinter as tk
import random
import math
import time


class Bacteria:
    def __init__(self, canvas, x, y, size, speed, energy):
        self.canvas = canvas
        self.id = canvas.create_oval(x, y, x + size, y + size, fill='green')
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.energy = energy
        self.dx = 0
        self.dy = 0
        self.consumption = 0.1
        self.canvas.bind_all('<KeyPress>', self.on_key_press)
        self.canvas.bind_all('<KeyRelease>', self.on_key_release)
        self.plasmid = "NONE"
        self.level = 1
        self.xp = 0
        self.lvl_text = canvas.create_text(self.x + self.size / 2, self.y - self.size / 2,
                                             text=("lvl. " + str(self.level)), font=("Arial", 12))



    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.canvas.move(self.id, self.dx, self.dy)
        self.canvas.coords(self.lvl_text, self.x + self.size / 2, self.y - 10)
        self.check_boundaries()

    def check_boundaries(self):
        if self.x < 0:
            self.x = 0
        if self.x > 700 - self.size:
            self.x = 700 - self.size
        if self.y < 0:
            self.y = 0
        if self.y > 700 - self.size:
            self.y = 700 - self.size

    def on_key_press(self, event):
        if event.keysym == 'Left':
            self.dx = -self.speed
        elif event.keysym == 'Right':
            self.dx = self.speed
        elif event.keysym == 'Up':
            self.dy = -self.speed
        elif event.keysym == 'Down':
            self.dy = self.speed

    def on_key_release(self, event):
        if event.keysym in ['Left', 'Right']:
            self.dx = 0
        elif event.keysym in ['Up', 'Down']:
            self.dy = 0

    def decrease_energy(self, amount=0.0):
        if amount == 0:
            self.energy -= self.consumption
        else:
            self.energy -= amount
        if self.energy < 0:
            self.energy = 0


    def is_alive(self):
        return self.energy > 0

    def is_touching(self, white_blood_cell):
        bacteria_pos = self.canvas.coords(self.id)
        white_blood_cell_pos = self.canvas.coords(white_blood_cell.id)
        # check if the two cells' rectangles intersect
        return not (bacteria_pos[2] < white_blood_cell_pos[0] or
                    bacteria_pos[3] < white_blood_cell_pos[1] or
                    bacteria_pos[0] > white_blood_cell_pos[2] or
                    bacteria_pos[1] > white_blood_cell_pos[3])

    def fight(self, enemy):
        if (enemy.id == 0):
            return
        bacteria_pos = self.canvas.coords(self.id)
        enemy_list = self.canvas.coords(enemy.id)
        # check if the two cells' rectangles intersect
        value = not (bacteria_pos[2] < enemy_list[0] or
                    bacteria_pos[3] < enemy_list[1] or
                    bacteria_pos[0] > enemy_list[2] or
                    bacteria_pos[1] > enemy_list[3])
        if value:
            if self.level > enemy.level:
                enemy.canvas.delete(enemy.id)
                enemy.canvas.delete(enemy.lvl_label)
                enemy.id = 0
                bacteria.energy += 75
                bacteria.xp += 30
                if enemy.plasmid not in bacteria.plasmid:
                    bacteria.plasmid += enemy.plasmid
                    bacteria.consumption += .2
            if self.level < enemy.level:
                self.energy = 0

class Enemy:
    def __init__(self, canvas, x, y, size, type, level):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.x_speed = random.randint(-3, 3)
        self.y_speed = random.randint(-3, 3)
        self.type = type
        self.level = level
        self.lvl_label = canvas.create_text(x, y ,text="lvl. " + str(level), font=("Arial", 12))
        if type == "Lactose":
            self.id = canvas.create_oval(x, y, x + size, y + size, fill='blue')
            self.plasmid = "Lactose"
        if type == "Arabinose":
            self.id = canvas.create_oval(x, y, x+size, y+size, fill='yellow')
            self.plasmid = "Arabinose"

    def move(self):
        if self.id == 0:
            return
        else:
            self.x += self.x_speed
            self.y += self.x_speed
            self.canvas.move(self.id, self.x_speed, self.y_speed)
            pos = self.canvas.coords(self.id)
            self.canvas.coords(self.lvl_label, pos[2] - self.size/2, pos[3] + self.size/2)
            if pos[0] <= 0 or pos[2] >= 700:
                self.x_speed = -self.x_speed
            if pos[1] <= 0 or pos[3] >= 700:
                self.y_speed = -self.y_speed

    def is_touching(self, white_blood_cell):
        if self.id == 0:
            return
        bacteria_pos = self.canvas.coords(self.id)
        white_blood_cell_pos = self.canvas.coords(white_blood_cell.id)
        # check if the two cells' rectangles intersect
        test =  (bacteria_pos[2] < white_blood_cell_pos[0] or
                    bacteria_pos[3] < white_blood_cell_pos[1] or
                    bacteria_pos[0] > white_blood_cell_pos[2] or
                    bacteria_pos[1] > white_blood_cell_pos[3])
        if not test:
            self.canvas.delete(self.id)
            self.canvas.delete(self.lvl_label)
            self.id = 0


class WhiteBloodCell:
    def __init__(self, canvas):
        self.canvas = canvas
        self.id = canvas.create_oval(10, 10, 50, 50, fill="gray")
        self.x = random.randint(0, 400)
        self.y = random.randint(0, 400)
        self.canvas.move(self.id, self.x, self.y)
        self.x_speed = random.randint(-5, 5)
        self.y_speed = random.randint(-5, 5)
        self.canvas_width = 700
        self.canvas_height = 700

    def move(self):
        self.canvas.move(self.id, self.x_speed, self.y_speed)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0 or pos[2] >= self.canvas_width:
            self.x_speed = -self.x_speed
        if pos[1] <= 0 or pos[3] >= self.canvas_height:
            self.y_speed = -self.y_speed

class Sugar:
    def __init__(self, canvas, type):
        self.canvas = canvas
        self.size = 10  # size of the hexagon
        self.center_x = random.randint(30, 650)  # center x-coordinate of the hexagon
        self.center_y = random.randint(30, 650)  # center y-coordinate of the hexagon
        self.type = type

        # calculate the coordinates of the six vertices of the hexagon
        self.vertices = []
        for i in range(6):
            angle_deg = 60 * i - 30
            angle_rad = math.pi / 180 * angle_deg
            vertex_x = self.center_x + self.size * math.cos(angle_rad)
            vertex_y = self.center_y + self.size * math.sin(angle_rad)
            self.vertices.append((vertex_x, vertex_y))

        # draw the hexagon on the canvas
        if (type == "Glucose"):
            self.hexagon = self.canvas.create_polygon(self.vertices, fill='brown', outline='black')
        if (type == "Lactose"):
            self.hexagon = self.canvas.create_polygon(self.vertices, fill='blue', outline='black')
        if (type == "Arabinose"):
            self.hexagon = self.canvas.create_polygon(self.vertices, fill='yellow', outline='black')

def is_touching_hexagon(bacteria, sugar_list):
    if not sugar_list:
        return False
    if bacteria.id == 0:
        return False
    bacteria_pos = canvas.coords(bacteria.id)
    for sugar in sugar_list:
        hexagon_points = canvas.coords(sugar.hexagon)
        if (sugar.type not in bacteria.plasmid and (sugar.type != "Glucose")):
            return False
        for i in range(0, len(hexagon_points), 2):
            x, y = hexagon_points[i], hexagon_points[i + 1]
            if bacteria_pos[2] >= x and bacteria_pos[0] <= x and bacteria_pos[3] >= y and bacteria_pos[1] <= y:
                canvas.delete(sugar.hexagon)
                sugar_list.remove(sugar)
                return True
    return False



def energy_update():
    energy_label.config(text="Energy: " + str(round((bacteria.energy), 3)))


# create tkinter window
window = tk.Tk()
window.title('Bacteria Game')

# create canvas
canvas = tk.Canvas(window, width=700, height=700, bg='white')
canvas.pack()

# create bacteria
bacteria = Bacteria(canvas, 0, 30, 30, 2, 200)
white_blood = WhiteBloodCell(canvas)
g1 = Sugar(canvas, "Glucose")
g2 = Sugar(canvas, "Glucose")
g3 = Sugar(canvas, "Glucose")
g4 = Sugar(canvas, "Glucose")
g_list = [g1, g2, g3, g4]

l1 = Sugar(canvas, "Lactose")
l2 = Sugar(canvas, "Lactose")
l_list = [l1, l2]

a1 = Sugar(canvas, "Arabinose")
a2 = Sugar(canvas, "Arabinose")
a_list = [a1, a2]

enemy1 = Enemy(canvas, 200, 200, 30, "Lactose", 1)
enemy2 = Enemy(canvas, 340, 600, 30, "Arabinose", 1)

energy_label = tk.Label(canvas, text="Energy: " + str(bacteria.energy), font=("Arial", 12))
energy_label.place(x=10, y=680)
level_label = tk.Label(canvas, text="lvl. " + str(bacteria.level), font=("Arial", 12))
level_label.place(x=660, y=680)

sugars_list = [g_list, l_list, a_list]
enemy_list = [enemy1, enemy2]
enemy_count = 2
white_blood_list = [white_blood]
check_time = time.time()
# game loop
while bacteria.is_alive():
    current_time = time.time()
    if current_time - check_time > 20:
        for i in range(3):
            enemy_type = random.choice(['Lactose', 'Arabinose'])
            if bacteria.level == 1:
                enemy_level = random.randint(bacteria.level, bacteria.level+ 1)
            else:
                enemy_level = random.randint(bacteria.level - 1 , bacteria.level+ 1)
            if bacteria.x >= 350:
                enemy_x = random.randint(50, 190)
            else:
                enemy_x = random.randint(510, 680)
            if bacteria.y >= 350:
                enemy_y = random.randint(50, 190)
            else:
                enemy_y = random.randint(510,680)
            enemy = Enemy(canvas, enemy_x, enemy_y, 30, enemy_type, enemy_level)
            enemy_list.append(enemy)
            enemy_count += 1

        for i in range(5):
            sugar_type = random.choice(["Lactose", "Arabinose", "Glucose"])
            shuga = Sugar(canvas, sugar_type)
            if (sugar_type == "Lactose"):
                l_list.append(shuga)
            if (sugar_type == "Arabinose"):
                a_list.append(shuga)
            if(sugar_type == "Glucose"):
                g_list.append(shuga)
        check_time = time.time()
    bacteria.decrease_energy()
    bacteria.update()
    white_blood.move()
    for en in enemy_list:
        en.move()
        en.is_touching(white_blood)
        bacteria.fight(en)
        for su in sugars_list:
            is_touching_hexagon(en, su)

    if bacteria.is_touching(white_blood):
        bacteria.energy = 0
    if is_touching_hexagon(bacteria, g_list):
        bacteria.energy += 50
        bacteria.xp += 20
        if (bacteria.xp != 0) and (bacteria.xp >= 40):
            bacteria.xp -= 40
            bacteria.level += 1
            level_label.config(text="lvl. " + str(bacteria.level))
            bacteria.canvas.delete(bacteria.lvl_text)
            bacteria.lvl_text = canvas.create_text(bacteria.x + bacteria.size / 2, bacteria.y - bacteria.size / 2,
                                             text=("lvl. " + str(bacteria.level)), font=("Arial", 12))

    if is_touching_hexagon(bacteria, l_list):
        bacteria.energy += 50
        bacteria.xp += 20
        if (bacteria.xp != 0) and (bacteria.xp >= 40):
            bacteria.xp -= 40
            bacteria.level += 1
            level_label.config(text="lvl. " + str(bacteria.level))
            bacteria.canvas.delete(bacteria.lvl_text)
            bacteria.lvl_text = canvas.create_text(bacteria.x + bacteria.size / 2, bacteria.y - bacteria.size / 2,
                                             text=("lvl. " + str(bacteria.level)), font=("Arial", 12))

    if is_touching_hexagon(bacteria, a_list):
        bacteria.energy += 50
        bacteria.xp += 20
        if (bacteria.xp != 0) and (bacteria.xp >= 40):
            bacteria.xp -= 40
            bacteria.level += 1
            level_label.config(text="lvl. " + str(bacteria.level))
            bacteria.canvas.delete(bacteria.lvl_text)
            bacteria.lvl_text = canvas.create_text(bacteria.x + bacteria.size / 2, bacteria.y - bacteria.size / 2,
                                             text=("lvl. " + str(bacteria.level)), font=("Arial", 12))


    energy_update()
    canvas.update()

    # delay to make the movement smoother
    canvas.after(10)

# game over
canvas.create_text(250, 250, text='Game Over', fill='red', font=('Arial', 24, 'bold'))

# start the tkinter event loop
window.mainloop()