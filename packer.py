CONSTANTES
    PALETTE_STD_LENGTH = 1.2
    PALETTE_STD_WIDTH  = 0.8
    PALETTE_MAX_HEIGHT = 2.0
    PALETTE_MAX_WEIGHT = 1500.0

def get_order_lines(session, group)
    → pour chaque order du groupe
    → récupère toutes les order_lines avec les produits associés
    → retourne une liste de order_lines

def create_palette(order_line)
    → crée une nouvelle palette
    → dimensions : max(standard, dimensions du produit)
    → retourne un dict palette vide

def can_fit(palette, order_line)
    → vérifie si order_line rentre dans la palette
    → check poids : palette['weight'] + order_line.weight_total <= 1500
    → check hauteur : palette['height'] + product.height_per_unit <= 2.0
    → retourne True/False

def pack_group(session, group)
    → appelle get_order_lines()
    → pour chaque order_line :
        → chercher une palette ouverte où ça rentre (can_fit)
        → si trouvée → ajouter la ligne
        → si pas trouvée → créer nouvelle palette
    → retourne liste de palettes

def run_packer(session, groups)
    → pour chaque groupe
    → appelle pack_group()
    → retourne toutes les palettes formées