from db import Session
from models import GeoZone, Orders, OrderLines,Pallets,PalletLines,Shipments,ShipmentPallet
from datetime import datetime


def get_pending_orders(session):
    pending = session.query(Orders).filter(Orders.status.in_(['validated', 'ready'])).all()
    return pending

def group_orders(session):
    orders = session.query(Orders).filter(Orders.status.in_(['validated', 'ready'])).order_by(Orders.geo_zone_id, Orders.status, Orders.eta).all()
    groups = list()
    for order in orders:
        if groups == []:
                eta_ref = order.eta.replace(hour=8, minute=0, second=0, microsecond=0)
                groups.append({'geo_zone_id':order.geo_zone_id,'eta_ref': eta_ref, 'orders': [order]})
        else:
            if order.status == 'ready':
            
                for group in groups:
                

           
    


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
    group_orders(Session)