# === Importation des bibliothèques ===
import tkinter as tk                     # Pour créer l'interface graphique
from tkinter import messagebox           # Pour afficher des messages d’erreur ou d'information
import matplotlib.pyplot as plt          # Pour dessiner les résultats avec matplotlib
import matplotlib.patches as patches     # Pour dessiner les rectangles
import time                              # Pour mesurer le temps d'exécution

# === Classe principale pour la gestion du placement de rectangles ===
class PackingManager:
    def __init__(self, container_width, container_height):
        # Initialise la largeur et la hauteur du conteneur
        self.container_width = container_width
        self.container_height = container_height

    def pack_rectangles(self, rectangles):
        # Crée une grille représentant l’espace du conteneur (False = vide, True = occupé)
        grid = [[False] * self.container_width for _ in range(self.container_height)]
        placements = []  # Liste pour enregistrer les positions des rectangles placés

        # Lance l'algorithme de backtracking
        if self.backtrack(0, grid, rectangles, placements):
            return True, placements  # Succès
        return False, []  # Échec

    def can_place(self, x, y, w, h, grid):
        # Vérifie si le rectangle (w x h) peut être placé à la position (x, y)
        if x + w > self.container_width or y + h > self.container_height:
            return False  # Dépasse le conteneur
        return all(not grid[i][j] for i in range(y, y + h) for j in range(x, x + w))

    def place(self, x, y, w, h, grid):
        # Marque les cases de la grille comme occupées par le rectangle
        for i in range(y, y + h):
            for j in range(x, x + w):
                grid[i][j] = True

    def remove(self, x, y, w, h, grid):
        # Libère les cases précédemment occupées (pour backtracking)
        for i in range(y, y + h):
            for j in range(x, x + w):
                grid[i][j] = False

    def backtrack(self, index, grid, rectangles, placements):
        # Algorithme récursif pour essayer de placer tous les rectangles
        if index == len(rectangles):
            return True  # Tous les rectangles ont été placés

        w, h = rectangles[index]
        # Parcourt toutes les positions possibles dans la grille
        for y in range(self.container_height - h + 1):
            for x in range(self.container_width - w + 1):
                if self.can_place(x, y, w, h, grid):
                    self.place(x, y, w, h, grid)
                    placements.append((x, y, w, h))

                    if self.backtrack(index + 1, grid, rectangles, placements):
                        return True  # Succès récursif

                    placements.pop()  # Backtrack
                    self.remove(x, y, w, h, grid)

        return False  # Échec à ce niveau
# === Classe pour l'interface graphique ===
class PackingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Packing Optimal de Carrés")

        # Label pour demander N
        self.label = tk.Label(root, text="Entrez N (1-25) :")
        self.label.pack()

        # Champ de saisie
        self.entry = tk.Entry(root)
        self.entry.pack()

        # Bouton pour lancer l’algorithme
        self.button = tk.Button(root, text="Lancer le packing", command=self.run_packing)
        self.button.pack()

        # Affiche le résultat (succès ou échec)
        self.result = tk.Label(root, text="")
        self.result.pack()
    def run_packing(self):
        try:
            # Récupère et valide la valeur de N
            n = int(self.entry.get())
            if not 1 <= n <= 25:
                raise ValueError
        except ValueError:
            # Affiche une erreur si N est invalide
            messagebox.showerror("Entrée invalide", "Veuillez entrer un entier entre 1 et 25.")
            return

        self.result.config(text="Packing en cours...")
        self.root.update()

        start_time = time.time()  # Début du chronométrage

        # Génère les carrés (NxN, (N-1)x(N-1), ..., 1x1)
        rectangles = [(i, i) for i in range(n, 0, -1)]
        total_area = sum(w * h for w, h in rectangles)

        # On teste différentes tailles de conteneurs (hauteur de plus en plus grande)
        found = False
        for height in range(max(h for _, h in rectangles), total_area + 1):
            width = (total_area + height - 1) // height  # arrondi supérieur
            manager = PackingManager(width, height)
            success, placements = manager.pack_rectangles(rectangles)
            if success:
                found = True
                break  # On arrête à la première solution trouvée

        end_time = time.time()  # Fin du chronométrage

        if found:
            self.result.config(text=f"✅ Packing réussi : {width}x{height} en {end_time - start_time:.2f}s")
            self.visualize(width, height, placements)
        else:
            self.result.config(text="❌ Échec du packing.")
    def visualize(self, width, height, placements):
        # Affiche les rectangles placés avec Matplotlib
        fig, ax = plt.subplots()
        ax.set_xlim(0, width)
        ax.set_ylim(0, height)
        ax.set_aspect('equal')

        for x, y, w, h in placements:
            rect = patches.Rectangle((x, y), w, h, edgecolor='black', facecolor='skyblue')
            ax.add_patch(rect)
            ax.text(x + w / 2, y + h / 2, f"{w}x{h}", fontsize=8, ha='center', va='center')

        plt.gca().invert_yaxis()  # Inverse l’axe Y pour affichage naturel
        plt.title(f"Packing : {width}x{height}")
        plt.show()
# === Point d’entrée du programme ===
if __name__ == '__main__':
    root = tk.Tk()           # Crée la fenêtre principale
    app = PackingApp(root)   # Lance l'application
    root.mainloop()          # Boucle principale de Tkinter
