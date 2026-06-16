CREATE SCHEMA IF NOT EXISTS logistics;

CREATE  TABLE logistics.geo_zone ( 
	id_geo_zone          serial  NOT NULL  ,
	post_code            integer  NOT NULL  ,
	zone_name            varchar(100)    ,
	CONSTRAINT pk_geo_zone PRIMARY KEY ( id_geo_zone )
 );

CREATE  TABLE logistics.pallets ( 
	id_pallet            serial  NOT NULL  ,
	geo_zone_id          integer  NOT NULL  ,
	pallet_length        NUMERIC(10,3)  NOT NULL  ,
	pallet_width         NUMERIC(10,3)  NOT NULL  ,
	total_weight         NUMERIC(10,3)  NOT NULL  ,
	pallet_height        NUMERIC(10,3)  NOT NULL  ,
	status               varchar(20)  NOT NULL  CHECK(status IN ('open','closed','loaded')),
	created_at           timestamp DEFAULT CURRENT_TIMESTAMP   ,
	CONSTRAINT pk_pallets PRIMARY KEY ( id_pallet )
 );

CREATE  TABLE logistics.products ( 
	sku                  integer  NOT NULL  ,
	name                 varchar(150)  NOT NULL  ,
	length_per_unit      NUMERIC(10,3)  NOT NULL  ,
	width_per_unit       NUMERIC(10,3)  NOT NULL  ,
	height_per_unit      NUMERIC(10,3)  NOT NULL  ,
	weight_per_unit      NUMERIC(8,3)  NOT NULL  ,
	CONSTRAINT pk_products PRIMARY KEY ( sku )
 );

CREATE  TABLE logistics.users ( 
	id_user              serial  NOT NULL  ,
	name                 varchar(100)  NOT NULL  ,
	user_role            varchar(20)  NOT NULL  CHECK(user_role IN ('dispatcher','preparer','truck_admin')),
	created_at           timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL  ,
	CONSTRAINT pk_users PRIMARY KEY ( id_user )
 );

CREATE  TABLE logistics.vehicles ( 
	id_vehicle           serial  NOT NULL  ,
	plate                varchar(7)  NOT NULL  ,
	max_weight           NUMERIC(10,2)  NOT NULL  ,
	max_length           NUMERIC(10,2)  NOT NULL  ,
	max_width            NUMERIC(10,2)  NOT NULL  ,
	max_height           NUMERIC(10,2)  NOT NULL  ,
	is_available         boolean DEFAULT TRUE NOT NULL  ,
	CONSTRAINT pk_vehicles PRIMARY KEY ( id_vehicle ),
	CONSTRAINT unq_vehicles UNIQUE ( plate ) 
 );

CREATE  TABLE logistics.orders ( 
	order_number         serial  NOT NULL  ,
	customer             varchar(50)  NOT NULL  ,
	address              text  NOT NULL  ,
	postcode             integer  NOT NULL  ,
	city                 varchar(100)  NOT NULL  ,
	status               varchar(20)  NOT NULL  CHECK(status IN('draft','validated','in_preparation','ready','grouped','shipped')),
	geo_zone_id          integer    ,
	validated_by         integer    ,
	validated_at         timestamp    ,
	assigned_to          integer    ,
	created_at           timestamp DEFAULT CURRENT_TIMESTAMP   ,
	CONSTRAINT pk_orders PRIMARY KEY ( order_number )
 );

CREATE  TABLE logistics.shipments ( 
	id_shipment          serial  NOT NULL  ,
	vehicle_id           integer  NOT NULL  ,
	geo_zone_id          integer  NOT NULL  ,
	departure_date       date  NOT NULL  ,
	status               varchar(20)  NOT NULL  CHECK(status IN('planned','loading','departed')),
	total_weight         NUMERIC(10,3)    ,
	created_by           integer  NOT NULL  ,
	departed_at          timestamp,
	length_used          NUMERIC(10,3),
	fill_rate            NUMERIC(10,2),
	CONSTRAINT pk_shipments PRIMARY KEY ( id_shipment )
 );

CREATE  TABLE logistics.order_lines ( 
	id_order_lines       serial  NOT NULL  ,
	order_id             integer  NOT NULL  ,
	product_id           integer  NOT NULL  ,
	qty                  integer  NOT NULL  ,
	weight_total         NUMERIC(10,3)  NOT NULL  ,
	CONSTRAINT pk_order_lines PRIMARY KEY ( id_order_lines )
 );

CREATE  TABLE logistics.pallet_lines ( 
	id_pallet_lines      serial  NOT NULL  ,
	pallet_id            integer  NOT NULL  ,
	order_line_id        integer  NOT NULL  ,
	CONSTRAINT pk_pallet_lines PRIMARY KEY ( id_pallet_lines ),
	CONSTRAINT unq_pallet_lines_pallet_order_line UNIQUE ( pallet_id, order_line_id ) 
 );

CREATE  TABLE logistics.shipment_pallet ( 
	id_shipment_pallet   serial  NOT NULL  ,
	shipment_id          integer  NOT NULL  ,
	pallet_id            integer  NOT NULL  ,
	load_order           integer  NOT NULL  ,
	CONSTRAINT pk_shipment_pallet PRIMARY KEY ( id_shipment_pallet )
 );

CREATE UNIQUE INDEX unq_shipment_pallet ON logistics.shipment_pallet ( shipment_id, pallet_id );

ALTER TABLE logistics.order_lines ADD CONSTRAINT fk_order_lines_order_id FOREIGN KEY ( order_id ) REFERENCES logistics.orders( order_number );

ALTER TABLE logistics.order_lines ADD CONSTRAINT fk_order_lines_product_id FOREIGN KEY ( product_id ) REFERENCES logistics.products( sku );

ALTER TABLE logistics.orders ADD CONSTRAINT fk_validated FOREIGN KEY ( validated_by ) REFERENCES logistics.users( id_user );

ALTER TABLE logistics.orders ADD CONSTRAINT fk_assigned FOREIGN KEY ( assigned_to ) REFERENCES logistics.users( id_user );

ALTER TABLE logistics.orders ADD CONSTRAINT fk_geo_zone FOREIGN KEY ( geo_zone_id ) REFERENCES logistics.geo_zone( id_geo_zone );

ALTER TABLE logistics.pallet_lines ADD CONSTRAINT fk_pallet_lines_pallets FOREIGN KEY ( pallet_id ) REFERENCES logistics.pallets( id_pallet );

ALTER TABLE logistics.pallet_lines ADD CONSTRAINT fk_pallet_lines_order_line FOREIGN KEY ( order_line_id ) REFERENCES logistics.order_lines( id_order_lines );

ALTER TABLE logistics.pallets ADD CONSTRAINT fk_pallets_geo_zone FOREIGN KEY ( geo_zone_id ) REFERENCES logistics.geo_zone( id_geo_zone );

ALTER TABLE logistics.shipment_pallet ADD CONSTRAINT fk_shipment_pallet_shipment_id FOREIGN KEY ( shipment_id ) REFERENCES logistics.shipments( id_shipment );

ALTER TABLE logistics.shipment_pallet ADD CONSTRAINT fk_shipment_pallet_pallet_id FOREIGN KEY ( pallet_id ) REFERENCES logistics.pallets( id_pallet );

ALTER TABLE logistics.shipments ADD CONSTRAINT fk_shipments_vehicles FOREIGN KEY ( vehicle_id ) REFERENCES logistics.vehicles( id_vehicle );

ALTER TABLE logistics.shipments ADD CONSTRAINT fk_shipments_geo_zone FOREIGN KEY ( geo_zone_id ) REFERENCES logistics.geo_zone( id_geo_zone );

ALTER TABLE logistics.shipments ADD CONSTRAINT fk_shipments_creator FOREIGN KEY ( created_by ) REFERENCES logistics.users( id_user );

