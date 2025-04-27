import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import time

from benchmark import get_large_benchmark
from x_first import assign_x_first

# Classe représentant un noeud dans l'arbre binaire
class Node:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.used = False
        self.right = None
        self.down = None

class BinaryTreePacker:
    def __init__(self):
        self.root = None

    def fit(self, blocks):
        if not blocks:
            return
        start = time.time()
        # Initialiser la racine avec le premier bloc
        self.root = Node(0, 0, blocks[0]['w'], blocks[0]['h'])

        for block in blocks:
            node = self.find_node(self.root, block['w'], block['h'])
            if node:
                block['fit'] = self.split_node(node, block['w'], block['h'])
            else:
                block['fit'] = self.grow_node(block['w'], block['h'])
        end = time.time()
        print(f"Temps d'exécution : {end - start:.4f} secondes")
    def find_node(self, root, w, h):
        if root.used:
            return self.find_node(root.right, w, h) or self.find_node(root.down, w, h)
        elif (w <= root.w) and (h <= root.h):
            return root
        else:
            return None

    def split_node(self, node, w, h):
        node.used = True
        node.down = Node(node.x, node.y + h, node.w, node.h - h)
        node.right = Node(node.x + w, node.y, node.w - w, h)
        return node

    def grow_node(self, w, h):
        can_grow_down = (w <= self.root.w)
        can_grow_right = (h <= self.root.h)

        should_grow_right = can_grow_right and (self.root.h >= (self.root.w + w))
        should_grow_down = can_grow_down and (self.root.w >= (self.root.h + h))

        if should_grow_right:
            return self.grow_right(w, h)
        elif should_grow_down:
            return self.grow_down(w, h)
        elif can_grow_right:
            return self.grow_right(w, h)
        elif can_grow_down:
            return self.grow_down(w, h)
        else:
            return None

    def grow_right(self, w, h):
        new_root = Node(0, 0, self.root.w + w, self.root.h)
        new_root.used = True
        new_root.down = self.root
        new_root.right = Node(self.root.w, 0, w, self.root.h)
        self.root = new_root
        node = self.find_node(self.root, w, h)
        if node:
            return self.split_node(node, w, h)

    def grow_down(self, w, h):
        new_root = Node(0, 0, self.root.w, self.root.h + h)
        new_root.used = True
        new_root.right = self.root
        new_root.down = Node(0, self.root.h, self.root.w, h)
        self.root = new_root
        node = self.find_node(self.root, w, h)
        if node:
            return self.split_node(node, w, h)
        
def generate_blocks_random(n=100, max_size=256):
    # Générer des blocs de tailles aléatoires
    blocks = []
    for _ in range(n):
        w = random.randint(1, max_size)
        h = random.randint(1, max_size)
        blocks.append({'w': w, 'h': h})
    return blocks
def generate_blocks_korf(n):
    # Générer des blocs de tailles aléatoires selon la méthode de Korf
    blocks = []
    for i  in range(1,n):
        
        blocks.append({'w': i, 'h': i})
    return blocks
def generate_blocks( base_size=512):
                # Générer des rectangles en divisant chaque rectangle en 4 jusqu'à atteindre une taille minimale
                def divide_rectangle(x, y, w, h, min_size):
                    if w <= min_size or h <= min_size:
                        return [{'x': x, 'y': y, 'w': w, 'h': h}]
                    else:
                        half_w, half_h = w // 2, h // 2
                        return (
                            divide_rectangle(x, y, half_w, half_h, min_size) +
                            divide_rectangle(x + half_w, y, half_w, half_h, min_size)+
                            [{'x': x, 'y': y, 'w': w, 'h': h}]
                            
                        )

                # Créer deux grands rectangles initiaux
                blocks = []
                initial_size = base_size
                min_size = 1

                # Diviser le premier grand rectangle
                blocks += divide_rectangle(0, 0, initial_size, initial_size, min_size)

                # Diviser le deuxième grand rectangle
                blocks += divide_rectangle(initial_size, 0, initial_size, initial_size, min_size)

                return [{'w': block['w'], 'h': block['h']} for block in blocks]

def sort_blocks(blocks):
    # Trier par le côté maximum décroissant pour un meilleur packing
    return sorted(blocks, key=lambda b: max(b['w'], b['h']), reverse=True)

def visualize(blocks, title="Binary Tree Bin Packing"):
    fig, ax = plt.subplots()
    colors = []

    # Déterminer la taille du conteneur final
    width = max(block['fit'].x + block['w'] for block in blocks)
    height = max(block['fit'].y + block['h'] for block in blocks)

    for block in blocks:
        x, y, w, h = block['fit'].x, block['fit'].y, block['w'], block['h']
        color = (random.random(), random.random(), random.random())
        colors.append(color)
        rect = patches.Rectangle((x, y), w, h, edgecolor='black', facecolor=color)
        ax.add_patch(rect)
        # Optionnel : commenter si tu ne veux pas de texte
        # ax.text(x + w/2, y + h/2, f"{w}x{h}", ha='center', va='center', fontsize=7, color='black')

    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_aspect('equal')
    plt.gca().invert_yaxis()
    plt.title(title)
    plt.show()

if __name__ == "__main__":
    n = 100  # Nombre de blocs à générer
    blocks = generate_blocks(256)
    blocks = sort_blocks(blocks)
   
   

    # Visualiser les blocs générés binary
    packer = BinaryTreePacker()
    packer.fit(blocks)

    visualize(blocks, f"Packing {n} blocks")
    

 