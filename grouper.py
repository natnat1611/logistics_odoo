from db import Session
from models import GeoZone, Orders, OrderLines,Pallets,PalletLines,Shipments,ShipmentPallet, Groups
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

    for group in groups:
        new_group =  Groups(
        geo_zone_id = group['geo_zone_id'],
        eta_ref     = group['eta_ref'],
        status      = 'open'
)
        session.add(new_group)
        session.flush()
        for order in group['orders']:
            order.group_id = new_group.id_group  

    session.commit()              
    

def run_grouping(session, window_hours=48):
    groups = group_orders(session)
    apply_grouping(session, groups)



if __name__ == '__main__':
    run_grouping(Session)