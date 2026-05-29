# Cours Pygame — Animation 2D en Python

> **Prérequis :** Python 3.x installé. Niveau débutant accepté.

---

## Table des matières

1. [Installation](#1-installation)
2. [Structure d'un programme Pygame](#2-structure-dun-programme-pygame)
3. [La fenêtre et les couleurs](#3-la-fenêtre-et-les-couleurs)
4. [Dessiner des formes](#4-dessiner-des-formes)
5. [Gérer les entrées clavier et souris](#5-gérer-les-entrées-clavier-et-souris)
6. [Le mouvement — bases de l'animation](#6-le-mouvement--bases-de-lanimation)
7. [Les images (Sprites)](#7-les-images-sprites)
8. [Le texte à l'écran](#8-le-texte-à-lécran)
9. [La détection de collisions](#9-la-détection-de-collisions)
10. [Projet complet — Balle rebondissante interactive](#10-projet-complet--balle-rebondissante-interactive)
11. [Aide-mémoire rapide](#11-aide-mémoire-rapide)

---

## 1. Installation

```bash
pip install pygame
```

Pour vérifier que tout fonctionne :

```python
import pygame
print(pygame.version.ver)  # Ex : 2.5.2
```

---

## 2. Structure d'un programme Pygame

Tout programme Pygame suit **toujours** la même structure en 4 blocs :

```python
import pygame

# ── 1. INITIALISATION ──────────────────────────────────────
pygame.init()
screen = pygame.display.set_mode((800, 600))   # largeur x hauteur
pygame.display.set_caption("Mon jeu")
clock = pygame.time.Clock()

# ── 2. VARIABLES DU JEU ────────────────────────────────────
running = True

# ── 3. BOUCLE PRINCIPALE ───────────────────────────────────
while running:

    # 3a. Événements (clavier, souris, fermeture)
    for event in pygame.event.get():
        if event.zone == pygame.QUIT:
            running = False

    # 3b. Mise à jour de la logique du jeu
    # (déplacements, calculs…)

    # 3c. Dessin
    screen.fill((30, 30, 30))       # efface l'écran
    # … draw ici …
    pygame.display.flip()           # affiche le frame
    clock.tick(60)                  # limite à 60 FPS

# ── 4. FERMETURE ───────────────────────────────────────────
pygame.quit()
```

> **Règle d'or :** `screen.fill()` efface tout, puis on redessine, puis `pygame.display.flip()` envoie le frame à l'écran. Sans ça, les frames s'accumulent et donnent un effet de traînée.

---

## 3. La fenêtre et les couleurs

### Créer la fenêtre

```python
screen = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Titre de la fenêtre")
```

### Le système de coordonnées

```
(0,0) ──────────────► x
  │
  │
  ▼
  y
```

L'axe Y est **inversé** : y augmente vers le **bas**.

### Les couleurs

Les couleurs sont des tuples `(Rouge, Vert, Bleu)` avec des valeurs entre 0 et 255.

```python
NOIR    = (0,   0,   0)
BLANC   = (255, 255, 255)
ROUGE   = (255, 0,   0)
VERT    = (0,   255, 0)
BLEU    = (0,   0,   255)
JAUNE   = (255, 255, 0)
CYAN    = (0,   255, 255)
ORANGE  = (255, 165, 0)
GRIS    = (128, 128, 128)
```

---

## 4. Dessiner des formes

Toutes les fonctions de dessin commencent par `pygame.draw.`.

### Rectangle

```python
# pygame.draw.rect(surface, couleur, (x, y, largeur, hauteur), épaisseur=0)
pygame.draw.rect(screen, BLEU, (100, 50, 200, 100))       # rectangle plein
pygame.draw.rect(screen, BLANC, (100, 50, 200, 100), 3)   # contour de 3px
```

### Cercle

```python
# pygame.draw.circle(surface, couleur, (cx, cy), rayon, épaisseur=0)
pygame.draw.circle(screen, ROUGE, (400, 300), 50)          # cercle plein
pygame.draw.circle(screen, JAUNE, (400, 300), 50, 2)       # contour de 2px
```

### Ligne

```python
# pygame.draw.line(surface, couleur, (x1,y1), (x2,y2), épaisseur=1)
pygame.draw.line(screen, VERT, (0, 0), (800, 600), 2)
```

### Polygone

```python
# pygame.draw.polygon(surface, couleur, [(x1,y1), (x2,y2), …], épaisseur=0)
points = [(400, 100), (500, 300), (300, 300)]
pygame.draw.polygon(screen, CYAN, points)
```

### Ellipse

```python
# pygame.draw.ellipse(surface, couleur, (x, y, largeur, hauteur), épaisseur=0)
pygame.draw.ellipse(screen, ORANGE, (300, 200, 200, 100))
```

---

## 5. Gérer les entrées clavier et souris

### Deux méthodes pour le clavier

**Méthode 1 — Événement KEYDOWN** (une seule fois par appui) :
```python
for event in pygame.event.get():
    if event.zone == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            print("Espace appuyé !")
        if event.key == pygame.K_ESCAPE:
            running = False
        if event.key == pygame.K_i:
            print("I appuyé !")
```

**Méthode 2 — get_pressed()** (continu, tant que la touche est enfoncée) :
```python
keys = pygame.key.get_pressed()
if keys[pygame.K_LEFT]:   x -= 5
if keys[pygame.K_RIGHT]:  x += 5
if keys[pygame.K_UP]:     y -= 5
if keys[pygame.K_DOWN]:   y += 5
```

### Tableau des touches utiles

| Touche          | Constante Pygame        |
|-----------------|------------------------|
| Flèche gauche   | `pygame.K_LEFT`        |
| Flèche droite   | `pygame.K_RIGHT`       |
| Flèche haut     | `pygame.K_UP`          |
| Flèche bas      | `pygame.K_DOWN`        |
| Espace          | `pygame.K_SPACE`       |
| Échap           | `pygame.K_ESCAPE`      |
| Entrée          | `pygame.K_RETURN`      |
| Lettres a–z     | `pygame.K_a` … `pygame.K_z` |
| Chiffres 0–9    | `pygame.K_0` … `pygame.K_9` |

### La souris

```python
for event in pygame.event.get():
    if event.zone == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:                      # clic gauche
            x, y = event.pos                       # position du clic
            print(f"Clic en ({x}, {y})")

# Position en temps réel
mx, my = pygame.mouse.get_pos()

# Boutons enfoncés en continu
boutons = pygame.mouse.get_pressed()
if boutons[0]:    # bouton gauche maintenu
    print("Bouton gauche maintenu")
```

---

## 6. Le mouvement — bases de l'animation

### Déplacer un objet

```python
x, y = 100, 300   # position initiale
vitesse_x = 3     # pixels par frame

while running:
    for event in pygame.event.get():
        if event.zone == pygame.QUIT:
            running = False

    x += vitesse_x          # mise à jour de la position

    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (255, 100, 0), (int(x), int(y)), 30)
    pygame.display.flip()
    clock.tick(60)
```

### Rebondir sur les bords

```python
x, y = 400, 300
vx, vy = 4, 3     # vitesse en x et y
rayon = 30

while running:
    # … events …

    x += vx
    y += vy

    # Rebond gauche / droite
    if x - rayon < 0 or x + rayon > 800:
        vx = -vx

    # Rebond haut / bas
    if y - rayon < 0 or y + rayon > 600:
        vy = -vy

    screen.fill((20, 20, 40))
    pygame.draw.circle(screen, (255, 200, 0), (int(x), int(y)), rayon)
    pygame.display.flip()
    clock.tick(60)
```

### Mouvement basé sur le temps (recommandé)

Utiliser `dt` (delta time) rend le mouvement **indépendant du FPS** :

```python
vitesse = 200    # pixels par seconde

while running:
    dt = clock.tick(60) / 1000.0   # dt en secondes

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        x += vitesse * dt
    if keys[pygame.K_LEFT]:
        x -= vitesse * dt
```

---

## 7. Les images (Sprites)

### Charger et afficher une image

```python
# Charger l'image
image = pygame.image.load("mon_image.png").convert_alpha()
# .convert_alpha() = optimise l'affichage et gère la transparence

# L'afficher à la position (x, y)
screen.blit(image, (x, y))
```

### Redimensionner une image

```python
image = pygame.transform.scale(image, (100, 100))   # 100x100 pixels
```

### Rotation

```python
image_tournee = pygame.transform.rotate(image, angle)   # angle en degrés
```

### Utiliser pygame.Rect pour positionner

`pygame.Rect` est l'outil central pour gérer positions et collisions :

```python
image = pygame.image.load("perso.png").convert_alpha()
rect = image.get_rect()         # récupère le rectangle de l'image
rect.center = (400, 300)        # centre à (400, 300)
# rect.x, rect.y                  coin haut-gauche
# rect.centerx, rect.centery      centre
# rect.topleft, rect.bottomright  coins

screen.blit(image, rect)        # on passe le rect au lieu de (x, y)
```

---

## 8. Le texte à l'écran

```python
# 1. Initialiser une police
font = pygame.font.SysFont("Arial", 36)          # police système
# font = pygame.font.Font("mafont.ttf", 36)      # police personnalisée

# 2. Créer une surface texte
texte_surface = font.render("Hello Pygame !", True, (255, 255, 255))
# Arguments : texte, antialiasing, couleur

# 3. Afficher
screen.blit(texte_surface, (50, 50))

# Centrer le texte
rect_texte = texte_surface.get_rect(center=(400, 300))
screen.blit(texte_surface, rect_texte)
```

### Afficher un score en temps réel

```python
score = 0
font = pygame.font.SysFont("Arial", 28)

while running:
    # … logique du jeu …
    score += 1

    screen.fill((0, 0, 0))
    score_surf = font.render(f"Score : {score}", True, (255, 255, 0))
    screen.blit(score_surf, (10, 10))
    pygame.display.flip()
    clock.tick(60)
```

---

## 9. La détection de collisions

### Collision entre deux rectangles

```python
rect1 = pygame.Rect(100, 100, 50, 50)
rect2 = pygame.Rect(130, 120, 50, 50)

if rect1.colliderect(rect2):
    print("Collision !")
```

### Collision point dans un rectangle

```python
mx, my = pygame.mouse.get_pos()
if rect.collidepoint(mx, my):
    print("La souris est dans le rectangle !")
```

### Collision entre deux cercles (manuelle)

```python
import math

def collision_cercles(x1, y1, r1, x2, y2, r2):
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance < r1 + r2
```

---

## 10. Projet complet — Balle rebondissante interactive

Ce projet synthétise tout le cours :

```python
import pygame
import math

# ── INIT ──────────────────────────────────────────────────
pygame.init()
LARGEUR, HAUTEUR = 800, 600
screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Balle interactive")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# ── COULEURS ──────────────────────────────────────────────
FOND    = (15,  15,  35)
BALLE   = (255, 100,  50)
TEXTE   = (200, 200, 200)

# ── VARIABLES ─────────────────────────────────────────────
bx, by   = 400.0, 300.0   # position
vx, vy   = 200.0, 150.0   # vitesse (pixels/seconde)
rayon    = 25
score    = 0
pause    = False
info     = False

# ── BOUCLE ────────────────────────────────────────────────
running = True
while running:

    dt = clock.tick(60) / 1000.0   # delta time en secondes

    # — ÉVÉNEMENTS ———————————————————————————————————————
    for event in pygame.event.get():
        if event.zone == pygame.QUIT:
            running = False
        if event.zone == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_i:
                info = not info        # afficher/masquer les infos
            if event.key == pygame.K_SPACE:
                pause = not pause      # mettre en pause / reprendre

    # — CONTRÔLE CLAVIER (déplacement manuel) ————————————
    keys = pygame.key.get_pressed()
    if not pause:
        if keys[pygame.K_LEFT]:   bx -= 300 * dt
        if keys[pygame.K_RIGHT]:  bx += 300 * dt
        if keys[pygame.K_UP]:     by -= 300 * dt
        if keys[pygame.K_DOWN]:   by += 300 * dt

    # — PHYSIQUE ——————————————————————————————————————————
    if not pause:
        bx += vx * dt
        by += vy * dt

        if bx - rayon < 0:
            bx = rayon; vx = abs(vx); score += 1
        if bx + rayon > LARGEUR:
            bx = LARGEUR - rayon; vx = -abs(vx); score += 1
        if by - rayon < 0:
            by = rayon; vy = abs(vy); score += 1
        if by + rayon > HAUTEUR:
            by = HAUTEUR - rayon; vy = -abs(vy); score += 1

    # — DESSIN ————————————————————————————————————————————
    screen.fill(FOND)

    # Ombre de la balle
    pygame.draw.circle(screen, (5, 5, 20), (int(bx) + 4, int(by) + 4), rayon)
    # Balle
    pygame.draw.circle(screen, BALLE, (int(bx), int(by)), rayon)
    # Reflet
    pygame.draw.circle(screen, (255, 200, 170), (int(bx) - 7, int(by) - 7), 8)

    # HUD
    screen.blit(font.render(f"Score : {score}", True, TEXTE), (10, 10))

    if pause:
        msg = font.render("PAUSE — ESPACE pour reprendre", True, (255, 220, 50))
        screen.blit(msg, msg.get_rect(center=(LARGEUR // 2, HAUTEUR // 2)))

    if info:
        lignes = [
            f"Position : ({bx:.0f}, {by:.0f})",
            f"Vitesse  : ({vx:.0f}, {vy:.0f})",
            f"FPS      : {clock.get_fps():.0f}",
            "",
            "Flèches  → déplacer",
            "ESPACE   → pause",
            "I        → infos",
            "ÉCHAP    → quitter",
        ]
        for i, ligne in enumerate(lignes):
            surf = font.render(ligne, True, (150, 220, 255))
            screen.blit(surf, (10, 50 + i * 28))

    pygame.display.flip()

pygame.quit()
```

---

## 11. Aide-mémoire rapide

### Fonctions essentielles

| Fonction | Rôle |
|---|---|
| `pygame.init()` | Initialise tous les modules |
| `pygame.display.set_mode((w,h))` | Crée la fenêtre |
| `pygame.display.flip()` | Envoie le frame à l'écran |
| `screen.fill((r,g,b))` | Efface l'écran |
| `clock.tick(fps)` | Limite le FPS, retourne le dt en ms |
| `pygame.event.get()` | Récupère les événements |
| `pygame.key.get_pressed()` | Touches enfoncées en continu |
| `screen.blit(surf, (x,y))` | Dessine une surface |
| `pygame.quit()` | Ferme proprement Pygame |

### Structure minimale en moins de 20 lignes

```python
import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
x = 400

running = True
while running:
    for event in pygame.event.get():
        if event.zone == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:  x -= 4
    if keys[pygame.K_RIGHT]: x += 4
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (255, 80, 0), (x, 300), 30)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

---

> **Prochaines étapes :**
> - Découvrir les **classes** pour organiser les sprites (`class Joueur`)
> - Apprendre `pygame.sprite.Group` pour gérer des groupes d'objets
> - Ajouter du **son** avec `pygame.mixer`
> - Explorer la bibliothèque **Arcade** pour une API encore plus simple