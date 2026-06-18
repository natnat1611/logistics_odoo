CREATE TABLE logistics.groups (
    id_group    SERIAL NOT NULL,
    geo_zone_id INTEGER NOT NULL,
    eta_ref     TIMESTAMP NOT NULL,
    status      VARCHAR(20) NOT NULL CHECK(status IN ('open', 'packed', 'shipped')),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_groups PRIMARY KEY (id_group),
    CONSTRAINT fk_groups_geo_zone FOREIGN KEY (geo_zone_id) REFERENCES logistics.geo_zone(id_geo_zone)
);

ALTER TABLE logistics.orders ADD COLUMN group_id INTEGER;
ALTER TABLE logistics.orders ADD CONSTRAINT fk_orders_group FOREIGN KEY (group_id) REFERENCES logistics.groups(id_group);