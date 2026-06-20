from db import Session
from models import Orders, OrderLines,Pallets,PalletLines, Groups

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
    return pallet.total_weight + order_line.weight_total <= PALLET_MAX_WEIGHT and pallet.pallet_height + order_line.product.height_per_unit * order_line.qty <= PALLET_MAX_HEIGHT


def pack_group(session, group_id):
    group = session.query(Groups).filter(Groups.id_group == group_id).first()
    lines = get_order_lines(session, group_id)
    open_pallets = []
    
    for line in lines:
        for pallet in open_pallets:
            if can_fit(pallet, line):
                new_line = PalletLines(pallet_id = pallet.id_pallet, order_line_id = line.id_order_lines )
                session.add(new_line)
                pallet.total_weight += line.weight_total
                pallet.pallet_height += line.product.height_per_unit * line.qty
                break
        else:
            new_pallet = create_pallet(session, line, group.geo_zone_id)
            open_pallets.append(new_pallet)
            new_line = PalletLines(pallet_id = new_pallet.id_pallet, order_line_id = line.id_order_lines)
            session.add(new_line)
    session.commit()



def run_packer(session):
    groups = session.query(Groups).filter(Groups.status == 'open').all()
    for group in groups:
        pack_group(session, group.id_group)
        group.status = 'packed'  
    session.commit()



if __name__ == '__main__':
    run_packer(Session)
    print('done')