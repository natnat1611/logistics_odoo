
from typing import Optional
import datetime
import decimal
 
from sqlalchemy import create_engine, Boolean, CheckConstraint, Date, DateTime, ForeignKeyConstraint, Index, Integer, Numeric, PrimaryKeyConstraint, String, Text, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
 
 
 
class Base(DeclarativeBase):
    pass
 
 
class GeoZone(Base):
    __tablename__ = 'geo_zone'
    __table_args__ = (
        PrimaryKeyConstraint('id_geo_zone', name='pk_geo_zone'),
        {'schema': 'logistics'}
    )
 
    id_geo_zone: Mapped[int] = mapped_column(Integer, primary_key=True)
    post_code: Mapped[int] = mapped_column(Integer, nullable=False)
    zone_name: Mapped[Optional[str]] = mapped_column(String(100))
 
    orders: Mapped[list['Orders']] = relationship('Orders', back_populates='geo_zone')
    pallets: Mapped[list['Pallets']] = relationship('Pallets', back_populates='geo_zone')
    shipments: Mapped[list['Shipments']] = relationship('Shipments', back_populates='geo_zone')
    groups: Mapped[list['Groups']] = relationship('Groups', back_populates='geo_zone')
 
class Products(Base):
    __tablename__ = 'products'
    __table_args__ = (
        PrimaryKeyConstraint('sku', name='pk_products'),
        {'schema': 'logistics'}
    )
 
    sku: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    length_per_unit: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 3), nullable=False)
    width_per_unit: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 3), nullable=False)
    height_per_unit: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 3), nullable=False)
    weight_per_unit: Mapped[decimal.Decimal] = mapped_column(Numeric(8, 3), nullable=False)
 
    order_lines: Mapped[list['OrderLines']] = relationship('OrderLines', back_populates='product')
 
 
class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        CheckConstraint("user_role::text = ANY (ARRAY['dispatcher'::character varying, 'preparer'::character varying, 'truck_admin'::character varying]::text[])", name='users_user_role_check'),
        PrimaryKeyConstraint('id_user', name='pk_users'),
        {'schema': 'logistics'}
    )
 
    id_user: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    user_role: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
 
    orders_assigned_to: Mapped[list['Orders']] = relationship('Orders', foreign_keys='[Orders.assigned_to]', back_populates='users')
    orders_validated_by: Mapped[list['Orders']] = relationship('Orders', foreign_keys='[Orders.validated_by]', back_populates='users_')
    shipments: Mapped[list['Shipments']] = relationship('Shipments', back_populates='users')
 
 
class Vehicles(Base):
    __tablename__ = 'vehicles'
    __table_args__ = (
        PrimaryKeyConstraint('id_vehicle', name='pk_vehicles'),
        UniqueConstraint('plate', name='unq_vehicles'),
        {'schema': 'logistics'}
    )
 
    id_vehicle: Mapped[int] = mapped_column(Integer, primary_key=True)
    plate: Mapped[str] = mapped_column(String(7), nullable=False)
    max_weight: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    max_length: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    max_width: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    max_height: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('true'))
 
    shipments: Mapped[list['Shipments']] = relationship('Shipments', back_populates='vehicle')
 
 
class Orders(Base):
    __tablename__ = 'orders'
    __table_args__ = (
        CheckConstraint("status::text = ANY (ARRAY['draft'::character varying, 'validated'::character varying, 'in_preparation'::character varying, 'ready'::character varying, 'grouped'::character varying, 'shipped'::character varying]::text[])", name='orders_status_check'),
        ForeignKeyConstraint(['assigned_to'], ['logistics.users.id_user'], name='fk_assigned'),
        ForeignKeyConstraint(['geo_zone_id'], ['logistics.geo_zone.id_geo_zone'], name='fk_geo_zone'),
        ForeignKeyConstraint(['validated_by'], ['logistics.users.id_user'], name='fk_validated'),
        ForeignKeyConstraint(['group_id'], ['logistics.groups.id_group'], name='fk_orders_group'),
        PrimaryKeyConstraint('order_number', name='pk_orders'),
        {'schema': 'logistics'}
    )
 
    order_number: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer: Mapped[str] = mapped_column(String(50), nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    postcode: Mapped[int] = mapped_column(Integer, nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    geo_zone_id: Mapped[Optional[int]] = mapped_column(Integer)
    validated_by: Mapped[Optional[int]] = mapped_column(Integer)
    validated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    assigned_to: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    eta: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    group_id: Mapped[Optional[int]] = mapped_column(Integer)
 
    users: Mapped[Optional['Users']] = relationship('Users', foreign_keys=[assigned_to], back_populates='orders_assigned_to')
    geo_zone: Mapped[Optional['GeoZone']] = relationship('GeoZone', back_populates='orders')
    users_: Mapped[Optional['Users']] = relationship('Users', foreign_keys=[validated_by], back_populates='orders_validated_by')
    order_lines: Mapped[list['OrderLines']] = relationship('OrderLines', back_populates='order')
 
    group: Mapped[Optional['Groups']] = relationship('Groups', back_populates='orders')
 
    def __repr__(self):
        return f"Order({self.order_number}, {self.customer}, {self.status}, {self.geo_zone_id}, {self.eta})"
 
class Pallets(Base):
    __tablename__ = 'pallets'
    __table_args__ = (
        CheckConstraint("status::text = ANY (ARRAY['open'::character varying, 'closed'::character varying, 'loaded'::character varying]::text[])", name='pallets_status_check'),
        ForeignKeyConstraint(['geo_zone_id'], ['logistics.geo_zone.id_geo_zone'], name='fk_pallets_geo_zone'),
        ForeignKeyConstraint(['group_id'], ['logistics.groups.id_group'], name='fk_pallets_group'),
        PrimaryKeyConstraint('id_pallet', name='pk_pallets'),
        {'schema': 'logistics'}
    )
 
    id_pallet: Mapped[int] = mapped_column(Integer, primary_key=True)
    geo_zone_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pallet_length: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 3), nullable=False)
    pallet_width: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 3), nullable=False)
    total_weight: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 3), nullable=False)
    pallet_height: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 3), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    group_id: Mapped[Optional[int]] = mapped_column(Integer)
 
    geo_zone: Mapped['GeoZone'] = relationship('GeoZone', back_populates='pallets')
    group: Mapped[Optional['Groups']] = relationship('Groups', back_populates='pallets')
    shipment_pallet: Mapped[list['ShipmentPallet']] = relationship('ShipmentPallet', back_populates='pallet')
    pallet_lines: Mapped[list['PalletLines']] = relationship('PalletLines', back_populates='pallet')
 
 
class Shipments(Base):
    __tablename__ = 'shipments'
    __table_args__ = (
        CheckConstraint("status::text = ANY (ARRAY['planned'::character varying, 'loading'::character varying, 'departed'::character varying]::text[])", name='shipments_status_check'),
        ForeignKeyConstraint(['created_by'], ['logistics.users.id_user'], name='fk_shipments_creator'),
        ForeignKeyConstraint(['geo_zone_id'], ['logistics.geo_zone.id_geo_zone'], name='fk_shipments_geo_zone'),
        ForeignKeyConstraint(['vehicle_id'], ['logistics.vehicles.id_vehicle'], name='fk_shipments_vehicles'),
        PrimaryKeyConstraint('id_shipment', name='pk_shipments'),
        {'schema': 'logistics'}
    )
 
    id_shipment: Mapped[int] = mapped_column(Integer, primary_key=True)
    vehicle_id: Mapped[int] = mapped_column(Integer, nullable=False)
    geo_zone_id: Mapped[int] = mapped_column(Integer, nullable=False)
    departure_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    created_by: Mapped[int] = mapped_column(Integer, nullable=False)
    total_weight: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 3))
    departed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    length_used: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 3))
    fill_rate: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
 
    users: Mapped['Users'] = relationship('Users', back_populates='shipments')
    geo_zone: Mapped['GeoZone'] = relationship('GeoZone', back_populates='shipments')
    vehicle: Mapped['Vehicles'] = relationship('Vehicles', back_populates='shipments')
    shipment_pallet: Mapped[list['ShipmentPallet']] = relationship('ShipmentPallet', back_populates='shipment')
 
 
class OrderLines(Base):
    __tablename__ = 'order_lines'
    __table_args__ = (
        ForeignKeyConstraint(['order_id'], ['logistics.orders.order_number'], name='fk_order_lines_order_id'),
        ForeignKeyConstraint(['product_id'], ['logistics.products.sku'], name='fk_order_lines_product_id'),
        PrimaryKeyConstraint('id_order_lines', name='pk_order_lines'),
        {'schema': 'logistics'}
    )
 
    id_order_lines: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(Integer, nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)
    qty: Mapped[int] = mapped_column(Integer, nullable=False)
    weight_total: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 3), nullable=False)
 
    order: Mapped['Orders'] = relationship('Orders', back_populates='order_lines')
    product: Mapped['Products'] = relationship('Products', back_populates='order_lines')
    pallet_lines: Mapped[list['PalletLines']] = relationship('PalletLines', back_populates='order_line')
 
 
class ShipmentPallet(Base):
    __tablename__ = 'shipment_pallet'
    __table_args__ = (
        ForeignKeyConstraint(['pallet_id'], ['logistics.pallets.id_pallet'], name='fk_shipment_pallet_pallet_id'),
        ForeignKeyConstraint(['shipment_id'], ['logistics.shipments.id_shipment'], name='fk_shipment_pallet_shipment_id'),
        PrimaryKeyConstraint('id_shipment_pallet', name='pk_shipment_pallet'),
        Index('unq_shipment_pallet', 'shipment_id', 'pallet_id', unique=True),
        {'schema': 'logistics'}
    )
 
    id_shipment_pallet: Mapped[int] = mapped_column(Integer, primary_key=True)
    shipment_id: Mapped[int] = mapped_column(Integer, nullable=False)
    pallet_id: Mapped[int] = mapped_column(Integer, nullable=False)
    load_order: Mapped[int] = mapped_column(Integer, nullable=False)
 
    pallet: Mapped['Pallets'] = relationship('Pallets', back_populates='shipment_pallet')
    shipment: Mapped['Shipments'] = relationship('Shipments', back_populates='shipment_pallet')
 
 
class PalletLines(Base):
    __tablename__ = 'pallet_lines'
    __table_args__ = (
        ForeignKeyConstraint(['order_line_id'], ['logistics.order_lines.id_order_lines'], name='fk_pallet_lines_order_line'),
        ForeignKeyConstraint(['pallet_id'], ['logistics.pallets.id_pallet'], name='fk_pallet_lines_pallets'),
        PrimaryKeyConstraint('id_pallet_lines', name='pk_pallet_lines'),
        UniqueConstraint('pallet_id', 'order_line_id', name='unq_pallet_lines_pallet_order_line'),
        {'schema': 'logistics'}
    )
 
    id_pallet_lines: Mapped[int] = mapped_column(Integer, primary_key=True)
    pallet_id: Mapped[int] = mapped_column(Integer, nullable=False)
    order_line_id: Mapped[int] = mapped_column(Integer, nullable=False)
 
    order_line: Mapped['OrderLines'] = relationship('OrderLines', back_populates='pallet_lines')
    pallet: Mapped['Pallets'] = relationship('Pallets', back_populates='pallet_lines')
 
 
class Groups(Base):
    __tablename__ = 'groups'
    __table_args__ = (
        CheckConstraint("status::text = ANY (ARRAY['open'::character varying, 'packed'::character varying, 'shipped'::character varying]::text[])", name='groups_status_check'),
        ForeignKeyConstraint(['geo_zone_id'], ['logistics.geo_zone.id_geo_zone'], name='fk_groups_geo_zone'),
        PrimaryKeyConstraint('id_group', name='pk_groups'),
        {'schema': 'logistics'}
    )
 
    id_group: Mapped[int] = mapped_column(Integer, primary_key=True)
    geo_zone_id: Mapped[int] = mapped_column(Integer, nullable=False)
    eta_ref: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
 
    geo_zone: Mapped['GeoZone'] = relationship('GeoZone', back_populates='groups')
    orders: Mapped[list['Orders']] = relationship('Orders', back_populates='group')
    pallets: Mapped[list['Pallets']] = relationship('Pallets', back_populates='group')