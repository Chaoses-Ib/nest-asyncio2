# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "nest-asyncio2",
#     "pytest",
#     "pyvista[jupyter]",
# ]
#
# [tool.uv.sources]
# nest-asyncio2 = { path = "../", editable = true }
# pyvista = { git = "https://github.com/pyvista/pyvista", branch = "testing/python3.14" }
# ///
from __future__ import annotations

import pytest

import pyvista as pv

has_trame = True
try:
    from trame.app import get_server

    from pyvista.trame.jupyter import Widget
    from pyvista.trame.jupyter import build_url
    from pyvista.trame.jupyter import elegantly_launch
    from pyvista.trame.ui import get_viewer
    from pyvista.trame.ui import plotter_ui
    from pyvista.trame.ui.vuetify2 import divider as vue2_divider
    from pyvista.trame.ui.vuetify2 import select as vue2_select
    from pyvista.trame.ui.vuetify2 import slider as vue2_slider
    from pyvista.trame.ui.vuetify2 import text_field as vue2_text_field
    from pyvista.trame.ui.vuetify3 import divider as vue3_divider
    from pyvista.trame.ui.vuetify3 import select as vue3_select
    from pyvista.trame.ui.vuetify3 import slider as vue3_slider
    from pyvista.trame.ui.vuetify3 import text_field as vue3_text_field
    from pyvista.trame.views import _BasePyVistaView
except ImportError:
    has_trame = False

pytestmark = [
    pytest.mark.skipif(not has_trame, reason='Requires trame'),
    pytest.mark.filterwarnings(
        r'ignore:It is recommended to use web\.AppKey instances for '
        r'keys:aiohttp.web_exceptions.NotAppKeyWarning'
    ),
    pytest.mark.filterwarnings(
        r'ignore:Call to deprecated method GetData\. '
        r'\(Use ExportLegacyFormat, or GetOffsetsArray/GetConnectivityArray instead\.\)'
        ':DeprecationWarning:trame_vtk'
    ),
]


def test_trame_server_launch():
    pv.set_jupyter_backend('trame')
    name = pv.global_theme.trame.jupyter_server_name
    elegantly_launch(name)
    server = get_server(name=name)
    assert server.running


@pytest.mark.parametrize('client_type', ['vue2', 'vue3'])
@pytest.mark.filterwarnings(
    'ignore:Suppress rendering on the plotter is changed to .*:UserWarning'
)
def test_trame_plotter_ui(client_type):
    # give different names for servers so different instances are created
    name = f'{pv.global_theme.trame.jupyter_server_name}-{client_type}'
    pv.set_jupyter_backend('trame')
    elegantly_launch(name, client_type=client_type)
    server = get_server(name=name)
    assert server.running

    pl = pv.Plotter(notebook=True)

    for mode in ['trame', 'client', 'server']:
        ui = plotter_ui(pl, mode=mode, server=server)
        assert isinstance(ui, _BasePyVistaView)

    # Test invalid mode
    mode = 'invalid'
    with pytest.raises(ValueError, match=f'`{mode}` is not a valid mode choice. Use one of: (.*)'):
        ui = plotter_ui(pl, mode=mode, server=server)

    # Test when mode and server are None
    ui = plotter_ui(pl)
    assert isinstance(ui, _BasePyVistaView)


@pytest.mark.parametrize('client_type', ['vue2', 'vue3'])
def test_trame(client_type):
    # give different names for servers so different instances are created
    name = f'{pv.global_theme.trame.jupyter_server_name}-{client_type}'
    pv.set_jupyter_backend('trame')
    elegantly_launch(name, client_type=client_type)
    server = get_server(name=name)
    assert server.running

    pl = pv.Plotter(notebook=True)
    actor = pl.add_mesh(pv.Cone())
    widget = pl.show(return_viewer=True)
    assert isinstance(widget, Widget)

    if pv.global_theme.trame.server_proxy_enabled:
        assert pv.global_theme.trame.server_proxy_prefix in widget.src
    else:
        assert 'http://' in widget.src

    viewer = get_viewer(pl)

    for cp in ['xy', 'xz', 'yz', 'isometric']:
        exec(f'viewer.view_{cp}()')
        cpos = list(pl.camera_position)
        pl.camera_position = cp[:3]
        assert cpos == pl.camera_position

    orig_value = actor.prop.show_edges
    server.state[viewer.EDGES] = not orig_value
    viewer.on_edge_visibility_change(**server.state.to_dict())
    assert actor.prop.show_edges != orig_value

    server.state[viewer.GRID] = True
    assert len(pl.actors) == 1
    viewer.on_grid_visibility_change(**server.state.to_dict())
    assert len(pl.actors) == 2
    server.state[viewer.GRID] = False
    viewer.on_grid_visibility_change(**server.state.to_dict())
    assert len(pl.actors) == 1

    server.state[viewer.OUTLINE] = True
    assert len(pl.actors) == 1
    viewer.on_outline_visibility_change(**server.state.to_dict())
    assert len(pl.actors) == 2
    server.state[viewer.OUTLINE] = False
    viewer.on_outline_visibility_change(**server.state.to_dict())
    assert len(pl.actors) == 1

    server.state[viewer.AXIS] = True
    assert pl.renderer.axes_actor is None
    viewer.on_axis_visibility_change(**server.state.to_dict())
    assert pl.renderer.axes_actor is not None
    server.state[viewer.AXIS] = False
    viewer.on_axis_visibility_change(**server.state.to_dict())

    server.state[viewer.SERVER_RENDERING] = False
    viewer.on_rendering_mode_change(**server.state.to_dict())
    server.state[viewer.SERVER_RENDERING] = True
    viewer.on_rendering_mode_change(**server.state.to_dict())

    assert viewer.actors == pl.actors

    # Test update methods
    viewer.update_image()
    viewer.reset_camera()
    viewer.push_camera()
    assert len(viewer.views) == 1

    viewer.export()

    assert isinstance(viewer.screenshot(), memoryview)


@pytest.mark.parametrize('client_type', ['vue2', 'vue3'])
def test_trame_custom_menu_items(client_type):
    # give different names for servers so different instances are created
    name = f'{pv.global_theme.trame.jupyter_server_name}-{client_type}'
    pv.set_jupyter_backend('trame')
    elegantly_launch(name, client_type=client_type)
    server = get_server(name=name)
    assert server.running

    pl = pv.Plotter(notebook=True)
    algo = pv.ConeSource()
    mesh_actor = pl.add_mesh(algo)

    viewer = get_viewer(pl, server=server)

    # setup vuetify items
    slider = vue2_slider if client_type == 'vue2' else vue3_slider
    text_field = vue2_text_field if client_type == 'vue2' else vue3_text_field
    select = vue2_select if client_type == 'vue2' else vue3_select
    divider = vue2_divider if client_type == 'vue2' else vue3_divider

    # vuetify items to pass as argument
    def custom_tools():
        divider(vertical=True, classes='mx-1')
        slider(
            ('resolution', 3),
            'Resolution slider',
            min=3,
            max=20,
            step=1,
        )
        text_field(('resolution', 3), 'Resolution value', type='number')
        divider(vertical=True, classes='mx-1')
        select(
            model=('visibility', 'Show'),
            tooltip='Toggle visibility',
            items=['Visibility', ['Hide', 'Show']],
        )

    with viewer.make_layout(server, template_name=pl._id_name):
        viewer.ui(
            mode='trame',
            default_server_rendering=True,
            collapse_menu=False,
            add_menu_items=custom_tools,
        )

    src = build_url(server, ui=pl._id_name, host='localhost', protocol='http')
    widget = Widget(viewer, src, '99%', '600px')

    state, ctrl = server.state, server.controller
    ctrl.view_update = widget.viewer.update

    @state.change('resolution')
    def update_resolution(resolution, **kwargs):  # noqa: ARG001
        algo.resolution = resolution
        ctrl.view_update()

    @state.change('visibility')
    def set_visibility(visibility, **kwargs):  # noqa: ARG001
        toggle = {'Hide': 0, 'Show': 1}
        mesh_actor.visibility = toggle[visibility]
        ctrl.view_update()

    # assert server.state['resolution'] == 3
    server.state.update({'resolution': 5, 'visibility': 'Hide'})
    server.state.flush()
    # assert algo.resolution == 5
    # assert not mesh_actor.visibility


retcode = pytest.main(['312_pyvista.py'])
