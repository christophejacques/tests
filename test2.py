import pygame

# Initialiser PyGame
pygame.init()

# Définir la police et la taille du texte
font = pygame.font.SysFont("segoeui-symbol", 16, bold=False, italic=False)
screen = pygame.display.set_mode((600, 400))

# Définir le texte et le symbole
texte = " Afficher plus d'options : "
symbole = u"\u27A2"  # Flèche vers la droite 
symbole = u"\u27A4"  # Flèche vers la droite 
symbole = u"\u2771"  # Flèche vers la droite 
symbole = u"\u276F"  # Flèche vers la droite 
# symbole = u"\u276D"  # Flèche vers la droite 

# Définir la taille du carré
carre_taille = 20

# Rendu du texte et du symbole
texte_surface = font.render(texte, True, (0, 0, 0))
symbole_surface = font.render(symbole, True, (0, 0, 0))

# Définir la position du texte, du symbole et du carré
texte_rect = texte_surface.get_rect()
symbole_rect = symbole_surface.get_rect()
symbole_rect.x = texte_rect.x + texte_rect.width + 5
carre_rect = pygame.Rect(symbole_rect.x + symbole_rect.width + 5, 0, carre_taille, carre_taille)

# Dessiner le carré, le texte et le symbole sur la surface
surface = pygame.Surface((carre_rect.x + carre_rect.width, texte_rect.height))
surface.fill((255, 255, 255))  # Couleur de fond blanc
# pygame.draw.rect(surface, (0, 0, 0), carre_rect)  # Dessiner le carré
surface.blit(texte_surface, (0, 0))
surface.blit(symbole_surface, symbole_rect)

# Afficher la surface sur l'écran
screen.fill((200, 200, 200))
screen.blit(surface, (0, 0))


def main():
    # Afficher la surface
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                return


main()
pygame.quit()
