from datetime import date

from flask import Flask, render_template, redirect, url_for, flash, request

from db import Session
from models import (
    Orders, OrderLines, Products, Pallets, PalletLines,
    Shipments, ShipmentPallet, Groups, Vehicles, GeoZone,
)
from grouper import run_grouping
from packer import run_packer
from dispatcher import run_dispatcher

app = Flask(__name__)
app.secret_key = "logistics-dev-key"   # nécessaire pour flash()


# --- Libellés FR pour les statuts (affichage) -------------------------------
ORDER_STATUS_FR = {
    "draft": "Brouillon",
    "validated": "Validée",
    "in_preparation": "En préparation",
    "ready": "Prête",
    "grouped": "Groupée",
    "shipped": "Expédiée",
}
GROUP_STATUS_FR = {"open": "Ouvert", "packed": "Palettisé", "shipped": "Expédié"}
PALLET_STATUS_FR = {"open": "Ouverte", "closed": "Fermée", "loaded": "Chargée"}
SHIPMENT_STATUS_FR = {"planned": "Planifié", "loading": "Chargement", "departed": "Parti"}


@app.teardown_appcontext
def cleanup(exception=None):
    # libère la session du thread à la fin de chaque requête
    Session.remove()


# --- Dashboard --------------------------------------------------------------
@app.route("/")
def dashboard():
    # compteurs pour les cartes du haut
    counts = {
        "orders_pending": Session.query(Orders)
            .filter(Orders.status.in_(["validated", "ready"]))
            .count(),
        "groups_open": Session.query(Groups).filter(Groups.status == "open").count(),
        "groups_packed": Session.query(Groups).filter(Groups.status == "packed").count(),
        "shipments": Session.query(Shipments).count(),
        "vehicles_free": Session.query(Vehicles).filter(Vehicles.is_available == True).count(),
    }

    # on construit une carte zone_id -> nom pour l'affichage
    zones = {z.id_geo_zone: z.zone_name for z in Session.query(GeoZone).all()}

    orders = Session.query(Orders).order_by(Orders.order_number).all()
    groups = Session.query(Groups).order_by(Groups.id_group).all()
    pallets = Session.query(Pallets).order_by(Pallets.id_pallet).all()
    shipments = Session.query(Shipments).order_by(Shipments.id_shipment).all()
    vehicles = Session.query(Vehicles).order_by(Vehicles.id_vehicle).all()

    return render_template(
        "dashboard.html",
        counts=counts,
        zones=zones,
        orders=orders,
        groups=groups,
        pallets=pallets,
        shipments=shipments,
        vehicles=vehicles,
        order_status_fr=ORDER_STATUS_FR,
        group_status_fr=GROUP_STATUS_FR,
        pallet_status_fr=PALLET_STATUS_FR,
        shipment_status_fr=SHIPMENT_STATUS_FR,
    )


# --- Actions (les 3 boutons du moteur) --------------------------------------
@app.route("/run/grouping", methods=["POST"])
def action_grouping():
    window = int(request.form.get("window_hours", 48))
    run_grouping(Session, window_hours=window)
    flash(f"Groupage lancé (fenêtre {window}h).", "ok")
    return redirect(url_for("dashboard"))


@app.route("/run/packing", methods=["POST"])
def action_packing():
    run_packer(Session)
    flash("Palettisation lancée.", "ok")
    return redirect(url_for("dashboard"))


@app.route("/run/dispatch", methods=["POST"])
def action_dispatch():
    run_dispatcher(Session, created_by=1, departure_date=date.today())
    flash("Affectation aux camions lancée.", "ok")
    return redirect(url_for("dashboard"))


# --- Détail d'un shipment (bon de chargement) -------------------------------
@app.route("/shipment/<int:shipment_id>")
def shipment_detail(shipment_id):
    shipment = Session.query(Shipments).filter(Shipments.id_shipment == shipment_id).first()
    if shipment is None:
        flash("Expédition introuvable.", "err")
        return redirect(url_for("dashboard"))

    vehicle = Session.query(Vehicles).filter(Vehicles.id_vehicle == shipment.vehicle_id).first()
    zone = Session.query(GeoZone).filter(GeoZone.id_geo_zone == shipment.geo_zone_id).first()

    # palettes du shipment triées par ordre de chargement
    rows = (
        Session.query(ShipmentPallet, Pallets)
        .join(Pallets, ShipmentPallet.pallet_id == Pallets.id_pallet)
        .filter(ShipmentPallet.shipment_id == shipment_id)
        .order_by(ShipmentPallet.load_order)
        .all()
    )

    total_weight = sum(p.total_weight for _, p in rows)

    return render_template(
        "shipment.html",
        shipment=shipment,
        vehicle=vehicle,
        zone=zone,
        rows=rows,
        total_weight=total_weight,
        shipment_status_fr=SHIPMENT_STATUS_FR,
        pallet_status_fr=PALLET_STATUS_FR,
    )


if __name__ == "__main__":
    app.run(debug=True)