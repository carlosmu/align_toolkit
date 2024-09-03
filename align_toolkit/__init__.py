# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

####################################
# IMPORT MODULES
####################################

from . import ot_alignator_3d
from . import ot_distributor_3d
from . import ui_pt_alignator_3d
from . import ui_icons
from . import ui_user_prefs

bl_info = {
    "name": "Align Toolkit",
    "author": "Carlos Mu <carlos.damian.munoz@gmail.com>",
    "blender": (3, 6, 0),
    "version": (1, 1, 1),
    "category": "Modeling",
    "location": "3D View Sidebar > Item Tab",
    "description": "Align and distribute selected objects",
    "warning": "",
    "doc_url": "https://blendermarket.com/products/align-toolkit",
    "tracker_url": "https://blendermarket.com/creators/carlosmu",
}

####################################
# REGISTER/UNREGISTER
####################################
def register():
    ui_icons.load_icons()
    ot_alignator_3d.register()
    ot_distributor_3d.register()
    ui_pt_alignator_3d.register()
    ui_user_prefs.register()

def unregister():
    ui_icons.unload_icons()
    ot_alignator_3d.unregister()
    ot_distributor_3d.unregister()
    ui_pt_alignator_3d.unregister()
    ui_user_prefs.unregister()