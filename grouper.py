from db import Session
from models import GeoZone, Orders, OrderLines,Pallets,PalletLines,Shipments,ShipmentPallet
from sqlalchemy import select


def get_pending_orders(session):
    pending = session.query(Orders).filter(Orders.status.in_(['validated', 'ready'])).all()
    return pending

def group_orders(orders):
    groups = dict()
    for order in orders:
        if order.status == "ready": 
            if zone_id not in groups:
                groups[zone_id] = []        
            groups[zone_id].append(order) 

def group_by_eta(orders_by_zone, window_hours):
    #→ pour chaque zone, trie les commandes par ETA
    #→ regroupe celles dont l'écart ETA est <= window_hours
    #→ retourne un dict {geo_zone_id: [[groupe1], [groupe2]]}
    pass

def apply_grouping(session, groups):
    #→ pour chaque groupe formé
    #→ passe les commandes au statut 'grouped'
    #→ commit
    pass

def run_grouping(session, window_hours=48):
    #→ fonction principale appelée par Flask
    #→ appelle les 3 fonctions dans l'ordre
    #→ retourne les groupes pour affichage
    pass
