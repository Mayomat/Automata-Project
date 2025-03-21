import turtle
import math
from Automata import *

def visualize_automaton(automaton):
    """
    Affiche graphiquement un automate fini en utilisant la bibliothèque Turtle.

    :param automaton: Un objet de la classe Automata à visualiser
    """
    # Configuration de la fenêtre
    screen = turtle.Screen()
    screen.title("Visualisation d'Automate")
    screen.setup(800, 600)
    screen.bgcolor("white")
    screen.tracer(0)  # Désactive l'animation pour accélérer le rendu

    # Configuration du stylo
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.pensize(2)
    pen.speed(0)

    # Calcul des positions des états en cercle
    radius = min(300, 100 + 30 * automaton.nb_states)  # Dynamically adjust radius
    state_positions = {}
    angle_step = 2 * math.pi / automaton.nb_states

    for i, state in enumerate(automaton.states):
        angle = i * angle_step
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        state_positions[state.num] = (x, y)

    # Dessiner les états
    for state in automaton.states:
        x, y = state_positions[state.num]

        # Dessiner le cercle de l'état
        pen.penup()
        pen.goto(x, y - 25)  # Décalage pour dessiner le cercle
        pen.pendown()
        pen.circle(25)

        # État terminal avec une flèche sortante
        if state.terminal:
            # Dessiner une flèche sortante pour l'état terminal
            arrow_angle = (state.num * angle_step + math.pi / 4) % (2 * math.pi)
            arrow_x = x + 25 * math.cos(arrow_angle)
            arrow_y = y + 25 * math.sin(arrow_angle)

            pen.penup()
            pen.goto(arrow_x, arrow_y)
            pen.pendown()
            pen.setheading(math.degrees(arrow_angle))
            pen.forward(25)
            pen.left(150)
            pen.forward(10)
            pen.backward(10)
            pen.right(300)
            pen.forward(10)
            pen.backward(10)

        # Étiquette de l'état
        pen.penup()
        pen.goto(x, y)
        pen.pendown()
        pen.write(f"q{state.num}", align="center", font=("Arial", 12, "normal"))

        # Marquer les états initiaux avec une flèche entrante
        if state.initial:
            entry_angle = (state.num * angle_step + math.pi) % (2 * math.pi)
            entry_x = x + 50 * math.cos(entry_angle)
            entry_y = y + 50 * math.sin(entry_angle)

            pen.penup()
            pen.goto(entry_x, entry_y)
            pen.pendown()
            pen.setheading(math.degrees(entry_angle) - 180)  # Pointe vers l'état
            pen.forward(25)
            pen.left(150)
            pen.forward(10)
            pen.backward(10)
            pen.right(300)
            pen.forward(10)
            pen.backward(10)

    # Dessiner les transitions
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    for state in automaton.states:
        for i in range(automaton.nb_alphabet):
            for target in state.transitions[i]:
                draw_transition(pen, state_positions[state.num], state_positions[target],
                                alphabet[i], state.num == target)

    # Mettre à jour l'écran
    screen.update()

    # Attendre le clic de l'utilisateur pour fermer
    screen.exitonclick()


def draw_transition(pen, start_pos, end_pos, label, is_loop):
    """
    Dessine une transition (flèche) entre deux états ou une boucle sur un état.

    :param pen: Le stylo Turtle à utiliser
    :param start_pos: Position du premier état (x, y)
    :param end_pos: Position du deuxième état (x, y)
    :param label: Étiquette de la transition (lettre de l'alphabet)
    :param is_loop: Indique si c'est une boucle sur un même état
    """
    start_x, start_y = start_pos
    end_x, end_y = end_pos

    if is_loop:
        # Dessiner une boucle
        pen.penup()
        pen.goto(start_x, start_y + 25)
        pen.pendown()
        pen.setheading(60)
        pen.circle(20, 270)

        # Dessiner la pointe de flèche
        pen.left(30)
        pen.forward(10)
        pen.backward(10)
        pen.right(60)
        pen.forward(10)
        pen.backward(10)

        # Écrire l'étiquette
        pen.penup()
        pen.goto(start_x, start_y + 60)
        pen.pendown()
        pen.write(label, align="center", font=("Arial", 10, "normal"))
    else:
        # Calculer l'angle et la distance entre les états
        dx = end_x - start_x
        dy = end_y - start_y
        distance = math.sqrt(dx * dx + dy * dy)
        angle = math.atan2(dy, dx)

        # Ajuster les points de départ et d'arrivée pour qu'ils soient sur le bord des cercles
        start_x_adj = start_x + 25 * math.cos(angle)
        start_y_adj = start_y + 25 * math.sin(angle)
        end_x_adj = end_x - 25 * math.cos(angle)
        end_y_adj = end_y - 25 * math.sin(angle)

        # Dessiner la flèche
        pen.penup()
        pen.goto(start_x_adj, start_y_adj)
        pen.pendown()
        pen.setheading(math.degrees(angle))

        # Calculer le point de contrôle pour une légère courbe
        # (facilite la visibilité lorsqu'il y a plusieurs transitions entre mêmes états)
        curve_intensity = 0.2 * distance
        control_x = (start_x_adj + end_x_adj) / 2 + curve_intensity * math.sin(angle)
        control_y = (start_y_adj + end_y_adj) / 2 - curve_intensity * math.cos(angle)

        # Dessiner une courbe de Bézier simple
        t = 0
        steps = 20
        last_x, last_y = start_x_adj, start_y_adj

        while t <= 1:
            # Formule quadratique de Bézier
            x = (1 - t) ** 2 * start_x_adj + 2 * (1 - t) * t * control_x + t ** 2 * end_x_adj
            y = (1 - t) ** 2 * start_y_adj + 2 * (1 - t) * t * control_y + t ** 2 * end_y_adj

            pen.goto(x, y)
            pen.pendown()

            last_x, last_y = x, y
            t += 1 / steps

        # Dessiner la pointe de flèche
        pen.setheading(math.degrees(angle))
        pen.left(150)
        pen.forward(10)
        pen.backward(10)
        pen.right(300)
        pen.forward(10)

        # Écrire l'étiquette
        label_x = control_x + 10
        label_y = control_y + 10
        pen.penup()
        pen.goto(label_x, label_y)
        pen.pendown()
        pen.write(label, align="center", font=("Arial", 10, "normal"))

# Exemple d'utilisation:
automaton = Automata()
automaton.create_automaton_from_file("Finite_Automata_files/6.txt")
visualize_automaton(automaton)