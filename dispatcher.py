from db import Session
from models import GeoZone, Orders, OrderLines,Pallets,PalletLines,Shipments,ShipmentPallet, Groups, Vehicles
from sqlalchemy import asc



def get_group_dimensions(session, group_id):
    pallets = session.query(Pallets).filter(Pallets.group_id == group_id).all()
    total_weight = sum(p.total_weight for p in pallets)
    total_length = sum(p.pallet_length for p in pallets)
    total_width = sum(p.pallet_width for p in pallets)

    return (total_length,total_width,total_weight)

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
            return truck.id_vehicle
        elif truck.max_width < 2.0 and total_width/2  <= truck.max_length and total_weight <= truck.max_weight:
            return truck.id_vehicle
        elif truck.max_width < 2.4 and mix <= truck.max_length and total_weight <= truck.max_weight:
            return truck.id_vehicle
        elif truck.max_width >= 2.4 and total_length/2 <= truck.max_length and total_weight <= truck.max_weight:
            return truck.id_vehicle
    return None

