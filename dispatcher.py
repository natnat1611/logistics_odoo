from db import Session
from models import Pallets,Shipments,ShipmentPallet, Groups, Vehicles
from sqlalchemy import asc



def get_group_dimensions(session, group_id):
    pallets = session.query(Pallets).filter(Pallets.group_id == group_id).all()
    total_weight = sum(p.total_weight for p in pallets)
    total_length = sum(p.pallet_length for p in pallets)
    total_width = sum(p.pallet_width for p in pallets)

    return (total_weight,total_length,total_width, len(pallets))

def get_available_vehicles(session):
    trucks = session.query(Vehicles).filter(Vehicles.is_available == True).order_by(Vehicles.max_weight.asc()).all()
    return trucks

def choose_vehicle( vehicles, total_weight, total_length,total_width,n_pallets):
    
    match n_pallets %5:
        case 1:
            mix =0.8 + (n_pallets//5)*2.4
        case 2:
            mix = 1.2 + (n_pallets//5)*2.4
        case 3:
            mix = 1.6 + (n_pallets//5)*2.4
        case 4:
            mix = 2.4 + (n_pallets//5)*2.4
        case 0:
            mix = 2.4 + (n_pallets//5)*2.4
    
    for truck in vehicles:
        if truck.max_width < 1.6 and total_length <= truck.max_length and total_weight <= truck.max_weight:
            return truck
        elif truck.max_width < 2.0 and total_width/2  <= truck.max_length and total_weight <= truck.max_weight:
            return truck
        elif truck.max_width < 2.4 and mix <= truck.max_length and total_weight <= truck.max_weight:
            return truck
        elif truck.max_width >= 2.4 and total_length/2 <= truck.max_length and total_weight <= truck.max_weight:
            return truck
    return None


def create_shipment(session, group_id, vehicle, departure_date, created_by):
    pallets = session.query(Pallets).filter(Pallets.group_id == group_id).all()
    if not pallets:
        return None
    new_shipment = Shipments(
        vehicle_id     = vehicle.id_vehicle,
        geo_zone_id = pallets[0].geo_zone_id,
        departure_date = departure_date,
        status         = 'planned',
        created_by     = created_by
    )
    session.add(new_shipment)
    session.flush()
    load_order = 1
    for pallet in pallets:
        sp = ShipmentPallet(
            shipment_id = new_shipment.id_shipment,
            pallet_id   = pallet.id_pallet,
            load_order  = load_order
        )
        session.add(sp)
        pallet.status = 'loaded'    # palette chargée
        load_order += 1

    group = session.query(Groups).filter(Groups.id_group == group_id).first()
    group.status = 'shipped'
    session.commit()
    return new_shipment


def run_dispatcher(session, created_by, departure_date):
    packed = session.query(Groups).filter(Groups.status == "packed").all()
    for group in packed:
        dimensions = get_group_dimensions(session, group.id_group)
        truck_list = get_available_vehicles(session)
        truck = choose_vehicle(truck_list, dimensions[0], dimensions[1], dimensions[2], dimensions[3])
        if truck is None:
            print(f"Aucun camion disponible pour le groupe {group.id_group}")
            continue
        else:
            create_shipment(session, group.id_group, truck, departure_date, created_by)



if __name__ == '__main__':
    from datetime import date
    run_dispatcher(Session, created_by=1, departure_date=date.today())
    print("Done")

