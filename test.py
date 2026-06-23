from db import Session
from packer import get_order_lines
from models import Groups

group = Session.query(Groups).first()
print(f"group_id: {group.id_group}, status: {group.status}")
lines = get_order_lines(Session, group.id_group)
print(f"lines trouvées: {len(lines)}")