import pygame
import random
import os

# Initialisation de Pygame
pygame.init()

# Initialisation du mixer pour la musique
pygame.mixer.init()

# Charger et jouer la musique d'ambiance (assurez-vous que le fichier musique.mp3 est dans le bon répertoire)
pygame.mixer.music.load('musique/musique_ambiance.mp3') # Utilisez le chemin correct de votre fichier audio MP3
pygame.mixer.music.play(-1) # -1 permet de répéter la musique en boucle

# Dimensions de la fenêtre
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jeu de Tri Sélectif")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Charger une image de fond pour le menu
def load_image(filename):
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"Erreur : le fichier {filename} est introuvable.")
    return pygame.image.load(filename)

menu_background = pygame.transform.scale(load_image("images/menu_background.png"), (screen_width, screen_height))
bouton_image = pygame.transform.scale(load_image("images/bouton_commencer.png"), (400, 200)) # Augmenter la hauteur du bouton

# Charger les autres images
background = load_image("images/nature_background.png")
poubelle_plastique = load_image("images/poubelle_plastique.png")
poubelle_papier = load_image("images/poubelle_papier.png")
poubelle_verre = load_image("images/poubelle_verre.png")

dechet_plastique = load_image("images/dechet_plastique.png")
dechet_papier = load_image("images/dechet_papier.png")
dechet_verre = load_image("images/dechet_verre.png")

# Redimensionner les images
background = pygame.transform.scale(background, (screen_width, screen_height))
poubelle_plastique = pygame.transform.scale(poubelle_plastique, (200, 300)) # Poubelles plus grandes
poubelle_papier = pygame.transform.scale(poubelle_papier, (200, 300))
poubelle_verre = pygame.transform.scale(poubelle_verre, (200, 300))
dechet_plastique = pygame.transform.scale(dechet_plastique, (100, 100)) # Déchets plus grands
dechet_papier = pygame.transform.scale(dechet_papier, (100, 100))
dechet_verre = pygame.transform.scale(dechet_verre, (100, 100))

# Polices et textes
font = pygame.font.SysFont(None, 60)
small_font = pygame.font.SysFont(None, 36)

# Score du joueur
score = 0

# Déchets : positions aléatoires
dechets = [
    {"type": "plastique", "image": dechet_plastique, "rect": pygame.Rect(random.randint(100, 1000), random.randint(50, 400), 100, 100)},
    {"type": "papier", "image": dechet_papier, "rect": pygame.Rect(random.randint(100, 1000), random.randint(50, 400), 100, 100)},
    {"type": "verre", "image": dechet_verre, "rect": pygame.Rect(random.randint(100, 1000), random.randint(50, 400), 100, 100)},
]

current_dechet = None
dragging = False
offset_x = 0
offset_y = 0
dechets_a_supprimer = []

# Ajouter un nouveau déchet
def ajouter_nouveau_dechet():
    nouveau_type = random.choice(["plastique", "papier", "verre"])
    if nouveau_type == "plastique":
        image = dechet_plastique
    elif nouveau_type == "papier":
        image = dechet_papier
    else:
        image = dechet_verre
    return {"type": nouveau_type, "image": image, "rect": pygame.Rect(random.randint(100, 1000), random.randint(50, 400), 100, 100)}

# Dessiner du texte
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Bouton image avec gestion des clics
def draw_image_button(image, x, y, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    screen.blit(image, (x, y))

    if x + image.get_width() > mouse[0] > x and y + image.get_height() > mouse[1] > y:
        if click[0] == 1 and action is not None:
            action()

# Menu principal
def menu_principal():
    while True:
        screen.blit(menu_background, (0, 0))

        draw_text("Jeu de Tri Sélectif", font, BLACK, screen, screen_width // 2, screen_height // 4)
        draw_image_button(bouton_image, screen_width // 2 - 200, screen_height // 2, jeu)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

# Boucle principale du jeu
def jeu():
    global score, current_dechet, dragging, offset_x, offset_y

    running = True
    while running:
        screen.blit(background, (0, 0))

        # Afficher les poubelles
        screen.blit(poubelle_plastique, (50, 500))
        screen.blit(poubelle_papier, (500, 500))
        screen.blit(poubelle_verre, (950, 500))

        # Définir les rectangles de collision des poubelles
        plastique_rect = pygame.Rect(50, 500, 200, 300)
        papier_rect = pygame.Rect(500, 500, 200, 300)
        verre_rect = pygame.Rect(950, 500, 200, 300)

        # Afficher le score
        score_text = small_font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Dessiner les déchets
        for dechet in dechets:
            screen.blit(dechet["image"], dechet["rect"].topleft)

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for dechet in dechets:
                    if dechet["rect"].collidepoint(event.pos):
                        current_dechet = dechet
                        dragging = True
                        offset_x = current_dechet["rect"].x - event.pos[0]
                        offset_y = current_dechet["rect"].y - event.pos[1]
                        break

            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging:
                    # Vérifier si le déchet est déposé dans la bonne poubelle
                    if current_dechet["rect"].colliderect(plastique_rect) and current_dechet["type"] == "plastique":
                        score += 1
                        dechets_a_supprimer.append(current_dechet)
                    elif current_dechet["rect"].colliderect(papier_rect) and current_dechet["type"] == "papier":
                        score += 1
                        dechets_a_supprimer.append(current_dechet)
                    elif current_dechet["rect"].colliderect(verre_rect) and current_dechet["type"] == "verre":
                        score += 1
                        dechets_a_supprimer.append(current_dechet)
                    else:
                        score -= 1

                    dragging = False
                    current_dechet = None

            elif event.type == pygame.MOUSEMOTION and dragging:
                if current_dechet:
                    current_dechet["rect"].x = event.pos[0] + offset_x
                    current_dechet["rect"].y = event.pos[1] + offset_y

        # Supprimer les déchets après l'itération de la boucle principale
        for dechet in dechets_a_supprimer:
            dechets.remove(dechet)
            dechets.append(ajouter_nouveau_dechet())
        dechets_a_supprimer.clear()

        # Rafraîchir l'écran
        pygame.display.flip()

# Lancer le menu principal
menu_principal()

# Quitter Pygame
pygame.quit()