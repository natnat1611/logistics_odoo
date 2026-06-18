from db import Session
from models import GeoZone, Orders, OrderLines,Pallets,PalletLines,Shipments,ShipmentPallet
from datetime import datetime


def get_pending_orders(session):
    pending = session.query(Orders).filter(Orders.status.in_(['validated', 'ready'])).all()
    return pending


def group_orders(session, window_hours=48):
    orders = session.query(Orders)\
        .filter(Orders.status.in_(['validated', 'ready']))\
        .order_by(Orders.geo_zone_id, Orders.status, Orders.eta)\
        .all()
    
    groups = []
    
    for order in orders:
        if order.status == 'ready':
            for group in groups:
                if group['geo_zone_id'] == order.geo_zone_id:
                    group['orders'].append(order)
                    break
            else:
                eta_ref = order.eta.replace(hour=8, minute=0, second=0, microsecond=0)
                groups.append({'geo_zone_id': order.geo_zone_id, 'eta_ref': eta_ref, 'orders': [order]})
        
        else:  # validated
            for group in groups:
                if group['geo_zone_id'] == order.geo_zone_id:
                    ecart = abs((order.eta - group['eta_ref']).total_seconds()) / 3600
                    if ecart <= window_hours:
                        group['orders'].append(order)
                        break
            else:
                eta_ref = order.eta.replace(hour=8, minute=0, second=0, microsecond=0)
                groups.append({'geo_zone_id': order.geo_zone_id, 'eta_ref': eta_ref, 'orders': [order]})
    
    return groups
           
    


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


if __name__ == '__main__':
    groups =  group_orders(Session)

    for group in groups:
        print(f"Zone {group['geo_zone_id']} - ETA ref {group['eta_ref']} - {len(group['orders'])} orders")