from . import views

urls = {
    '/v1/equipment/<int:equipment_id>': views.EquipmentView.as_view('equipment'),
    '/v1/equipment': views.EquipmentView.as_view('add_equipment'),
}