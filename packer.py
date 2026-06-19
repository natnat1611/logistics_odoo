from db import Session
from models import GeoZone, Orders, OrderLines,Pallets,PalletLines,Shipments,ShipmentPallet, Groups

#CONST
PALLET_STD_LENGTH = 1.2
PALLET_STD_WIDTH  = 0.8
PALLET_MAX_HEIGHT = 2.0
PALLET_MAX_WEIGHT = 1500.0

def get_order_lines(session, group_id):
    return session.query(OrderLines)\
        .join(Orders, OrderLines.order_id == Orders.order_number)\
        .filter(Orders.group_id == group_id)\
        .all()



def create_pallet(session, order_line, geo_zone_id):
    product = order_line.product
    
    is_oversized = (product.length_per_unit > PALLET_STD_LENGTH or 
                    product.width_per_unit > PALLET_STD_WIDTH)
    
    new_pallet = Pallets(
        geo_zone_id   = geo_zone_id,
        pallet_length = max(PALLET_STD_LENGTH, product.length_per_unit),
        pallet_width  = max(PALLET_STD_WIDTH, product.width_per_unit),
        pallet_height = product.height_per_unit * order_line.qty,
        total_weight  = order_line.weight_total,
        status        = 'closed' if is_oversized else 'open'
    )
    session.add(new_pallet)
    session.flush()
    return new_pallet

def can_fit(pallet, order_line):
    return pallet.total_weight + order_line.weight_total <= PALLET_MAX_WEIGHT and pallet.pallet_height + order_line.product.height_per_unit * order_line.qty <= PALLET_MAX_HEIGHT:


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