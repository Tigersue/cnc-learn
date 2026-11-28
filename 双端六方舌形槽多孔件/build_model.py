"""Build the reference B-Rep STEP model for 双端六方舌形槽多孔件."""

from argparse import ArgumentParser
from math import cos, isclose, radians, sin, sqrt
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image, ImageDraw
from OCP.BRep import BRep_Tool
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.BRepBndLib import BRepBndLib
from OCP.BRepBuilderAPI import (
    BRepBuilderAPI_MakeEdge,
    BRepBuilderAPI_MakeFace,
    BRepBuilderAPI_MakePolygon,
    BRepBuilderAPI_MakeWire,
)
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepGProp import BRepGProp
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.BRepPrimAPI import BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakePrism
from OCP.Bnd import Bnd_Box
from OCP.GCPnts import GCPnts_UniformDeflection
from OCP.GC import GC_MakeArcOfCircle
from OCP.GProp import GProp_GProps
from OCP.IFSelect import IFSelect_RetDone
from OCP.Interface import Interface_Static
from OCP.STEPControl import STEPControl_AsIs, STEPControl_Reader, STEPControl_Writer
from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE, TopAbs_SOLID
from OCP.TopExp import TopExp_Explorer
from OCP.TopLoc import TopLoc_Location
from OCP.TopoDS import TopoDS
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt, gp_Vec

OUTER_DIAMETER = 16.0
OUTER_RADIUS = OUTER_DIAMETER / 2.0
TOTAL_LENGTH = 35.0

LEFT_HEX_AF = 13.86
LEFT_HEX_LENGTH = 5.0

RIGHT_HEX_AF = 13.71
RIGHT_HEX_LENGTH = 5.0

SIDE_THROUGH_RADIUS = 1.50
SIDE_THROUGH_Y = 4.73
SIDE_THROUGH_Z = 13.0

RING_OUTER_RADIUS = 3.00
RING_BOSS_RADIUS = 0.75
RING_DEPTH = 3.00
RING_Z = TOTAL_LENGTH - 19.44  # 15.56

STEP_HOLE_CBORE_RADIUS = 2.50
STEP_HOLE_CBORE_DEPTH = 2.50
STEP_HOLE_BORE_RADIUS = 1.30
STEP_HOLE_BORE_TOTAL_DEPTH = 4.50
STEP_HOLE_Z = 25.00  # Measured from drawing projection (10.00 mm from right end)

RIGHT_SLOT_DEPTH = 3.00  # Estimated
RIGHT_BORE_RADIUS = 1.35
RIGHT_BORE_X = 2.80
RIGHT_BORE_DEPTH = 3.00  # Estimated


def cut(stock, tool):
    """Subtract tool solid from stock solid and simplify result."""
    op = BRepAlgoAPI_Cut(stock, tool)
    assert op.IsDone(), "Boolean cut failed"
    op.SimplifyResult()
    return op.Shape()


def make_cylinder(x, y, z, dx, dy, dz, radius, height):
    """Create a cylinder oriented along (dx, dy, dz)."""
    axis = gp_Ax2(gp_Pnt(x, y, z), gp_Dir(dx, dy, dz))
    return BRepPrimAPI_MakeCylinder(axis, radius, height).Shape()


def make_wire_from_segments(segments):
    """Build a closed face wire from ('line', p1, p2) and ('arc', p1, mid, p2) tuples."""
    wire = BRepBuilderAPI_MakeWire()
    for seg in segments:
        kind = seg[0]
        if kind == "line":
            p1, p2 = seg[1], seg[2]
            edge = BRepBuilderAPI_MakeEdge(gp_Pnt(*p1), gp_Pnt(*p2)).Edge()
        elif kind == "arc":
            p1, pm, p2 = seg[1], seg[2], seg[3]
            arc = GC_MakeArcOfCircle(gp_Pnt(*p1), gp_Pnt(*pm), gp_Pnt(*p2)).Value()
            edge = BRepBuilderAPI_MakeEdge(arc).Edge()
        else:
            raise ValueError(f"Unknown segment type: {kind}")
        wire.Add(edge)
    return wire.Wire()


def cut_hex_flats(body, across_flats, angles_deg, z_start, z_end):
    """Cut 6 outer flat prisms from the cylinder to form a hex end."""
    apothem = across_flats / 2.0
    height = z_end - z_start
    for deg in angles_deg:
        rad = radians(deg)
        nx, ny = cos(rad), sin(rad)
        tx, ty = -ny, nx
        pts = [
            (apothem * nx - 14.0 * tx, apothem * ny - 14.0 * ty),
            (14.0 * nx - 14.0 * tx, 14.0 * ny - 14.0 * ty),
            (14.0 * nx + 14.0 * tx, 14.0 * ny + 14.0 * ty),
            (apothem * nx + 14.0 * tx, apothem * ny + 14.0 * ty),
        ]
        poly = BRepBuilderAPI_MakePolygon()
        for px, py in pts:
            poly.Add(gp_Pnt(px, py, z_start))
        poly.Close()
        face = BRepBuilderAPI_MakeFace(poly.Wire()).Face()
        prism = BRepPrimAPI_MakePrism(face, gp_Vec(0, 0, height)).Shape()
        body = cut(body, prism)
    return body


def build_tongue_slot_cutter():
    """Create cutter for left-end tongue-shaped square pocket (7.20 x 7.20, depth 2.5, R1)."""
    z0 = -1.0
    s2 = sqrt(2.0) / 2.0
    segs = [
        ("line", (-2.60, -3.60, z0), (2.60, -3.60, z0)),
        ("arc", (2.60, -3.60, z0), (2.60 + s2, -2.60 - s2, z0), (3.60, -2.60, z0)),
        ("line", (3.60, -2.60, z0), (3.60, -2.00, z0)),
        ("arc", (3.60, -2.00, z0), (2.60 + s2, -2.00 + s2, z0), (2.60, -1.00, z0)),
        ("line", (2.60, -1.00, z0), (0.00, -1.00, z0)),
        ("arc", (0.00, -1.00, z0), (-1.00, 0.00, z0), (0.00, 1.00, z0)),
        ("line", (0.00, 1.00, z0), (2.60, 1.00, z0)),
        ("arc", (2.60, 1.00, z0), (2.60 + s2, 2.00 - s2, z0), (3.60, 2.00, z0)),
        ("line", (3.60, 2.00, z0), (3.60, 2.60, z0)),
        ("arc", (3.60, 2.60, z0), (2.60 + s2, 2.60 + s2, z0), (2.60, 3.60, z0)),
        ("line", (2.60, 3.60, z0), (-2.60, 3.60, z0)),
        ("arc", (-2.60, 3.60, z0), (-2.60 - s2, 2.60 + s2, z0), (-3.60, 2.60, z0)),
        ("line", (-3.60, 2.60, z0), (-3.60, -2.60, z0)),
        ("arc", (-3.60, -2.60, z0), (-2.60 - s2, -2.60 - s2, z0), (-2.60, -3.60, z0)),
    ]
    face = BRepBuilderAPI_MakeFace(make_wire_from_segments(segs)).Face()
    return BRepPrimAPI_MakePrism(face, gp_Vec(0, 0, 3.50)).Shape()


def build_right_slot_cutter():
    """Create cutter for right-end eccentric rounded-rectangle slot (3.80 x 6.10, R1.50)."""
    z0 = TOTAL_LENGTH - RIGHT_SLOT_DEPTH  # 32.0
    r = 1.50
    d = r * sqrt(2.0) / 2.0
    x_min, x_max = -4.00, -0.20
    y_min, y_max = -1.93, 4.17
    cx0, cx1 = x_min + r, x_max - r  # -2.50, -1.70
    cy0, cy1 = y_min + r, y_max - r  # -0.43, 2.67
    segs = [
        ("line", (cx0, y_min, z0), (cx1, y_min, z0)),
        ("arc", (cx1, y_min, z0), (cx1 + d, cy0 - d, z0), (x_max, cy0, z0)),
        ("line", (x_max, cy0, z0), (x_max, cy1, z0)),
        ("arc", (x_max, cy1, z0), (cx1 + d, cy1 + d, z0), (cx1, y_max, z0)),
        ("line", (cx1, y_max, z0), (cx0, y_max, z0)),
        ("arc", (cx0, y_max, z0), (cx0 - d, cy1 + d, z0), (x_min, cy1, z0)),
        ("line", (x_min, cy1, z0), (x_min, cy0, z0)),
        ("arc", (x_min, cy0, z0), (cx0 - d, cy0 - d, z0), (cx0, y_min, z0)),
    ]
    face = BRepBuilderAPI_MakeFace(make_wire_from_segments(segs)).Face()
    return BRepPrimAPI_MakePrism(face, gp_Vec(0, 0, RIGHT_SLOT_DEPTH + 1.0)).Shape()


def verify_shape(shape):
    """Verify B-Rep validity, single solid, exact bounding box, and return volume."""
    assert BRepCheck_Analyzer(shape).IsValid(), "Invalid B-Rep geometry"
    solids = TopExp_Explorer(shape, TopAbs_SOLID)
    assert solids.More(), "No solid found"
    solids.Next()
    assert not solids.More(), "Expected exactly 1 solid"

    bbox = Bnd_Box()
    BRepBndLib.AddOptimal_s(shape, bbox)
    lo, hi = bbox.CornerMin(), bbox.CornerMax()
    limits = (lo.X(), lo.Y(), lo.Z(), hi.X(), hi.Y(), hi.Z())
    targets = (-OUTER_RADIUS, -OUTER_RADIUS, 0.0, OUTER_RADIUS, OUTER_RADIUS, TOTAL_LENGTH)
    for actual, target in zip(limits, targets):
        assert isclose(actual, target, abs_tol=1e-5), f"BBox mismatch: {limits} vs {targets}"

    props = GProp_GProps()
    BRepGProp.VolumeProperties_s(shape, props)
    return props.Mass(), limits


def render_verification_views(shape, out_path):
    """Render 6 orthographic/isometric wireframe + shaded views for visual inspection."""
    BRepMesh_IncrementalMesh(shape, 0.05, False, 0.2, True)

    # Collect edge polylines
    polylines = []
    exp = TopExp_Explorer(shape, TopAbs_EDGE)
    while exp.More():
        edge = TopoDS.Edge(exp.Current())
        curve = BRepAdaptor_Curve(edge)
        algo = GCPnts_UniformDeflection(curve, 0.03)
        if algo.IsDone() and algo.NbPoints() >= 2:
            pts = []
            for i in range(1, algo.NbPoints() + 1):
                p = algo.Value(i)
                pts.append((p.X(), p.Y(), p.Z()))
            polylines.append(pts)
        exp.Next()

    # Collect face triangles for shaded iso
    tris = []
    fexp = TopExp_Explorer(shape, TopAbs_FACE)
    while fexp.More():
        face = TopoDS.Face(fexp.Current())
        loc = TopLoc_Location()
        tri = BRep_Tool.Triangulation_s(face, loc)
        if tri is not None:
            trsf = loc.Transformation()
            for i in range(1, tri.NbTriangles() + 1):
                t = tri.Triangle(i)
                n1, n2, n3 = t.Get()
                p1 = tri.Node(n1).Transformed(trsf)
                p2 = tri.Node(n2).Transformed(trsf)
                p3 = tri.Node(n3).Transformed(trsf)
                tris.append((
                    (p1.X(), p1.Y(), p1.Z()),
                    (p2.X(), p2.Y(), p2.Z()),
                    (p3.X(), p3.Y(), p3.Z()),
                ))
        fexp.Next()

    # Projection functions matching drawing first-angle views
    def proj_front(x, y, z):
        return (z, -y, -x)  # +z right, +y up, -x toward viewer

    def proj_top(x, y, z):
        return (z, -x, y)  # looking from +y: +z right, +x down

    def proj_bottom(x, y, z):
        return (z, x, -y)  # looking from -y: +z right, -x down

    def proj_left_end(x, y, z):
        return (-x, -y, -z)  # looking at Z=0 from -Z: -X right, +Y up

    def proj_right_end(x, y, z):
        return (x, -y, z)  # looking at Z=35 from +Z: +X right, +Y up

    def proj_iso(x, y, z):
        # View from (-X, +Y, -Z) side to show left hex + tongue slot + side holes
        a, b = radians(35), radians(25)
        u = z * cos(a) + x * sin(a)
        v_raw = -z * sin(a) + x * cos(a)
        v = -y * cos(b) + v_raw * sin(b)
        depth = y * sin(b) + v_raw * cos(b)
        return (u, v, -depth)

    panels = [
        ("Front View (look from -X)", proj_front, 18.0, 0.0, 12.0, False),
        ("Top View (look from +Y: Ø5/Ø2.60)", proj_top, 18.0, 0.0, 12.0, False),
        ("Bottom View (look from -Y: Ø6/Ø1.50)", proj_bottom, 18.0, 0.0, 12.0, False),
        ("Left End (Z=0, H13.86 + Tongue)", proj_left_end, 0.0, 0.0, 18.0, False),
        ("Right End (Z=35, H13.71 + Slot+Hole)", proj_right_end, 0.0, 0.0, 18.0, False),
        ("3D Isometric (Shaded)", proj_iso, 16.0, 0.0, 11.0, True),
    ]

    pw, ph = 420, 320
    img = Image.new("RGB", (pw * 3, ph * 2), (248, 250, 252))
    draw = ImageDraw.Draw(img)

    for idx, (title, proj, cx_ref, cy_ref, scale, shaded) in enumerate(panels):
        ox = (idx % 3) * pw + pw // 2
        oy = (idx // 3) * ph + ph // 2 + 10
        x_box0, y_box0 = (idx % 3) * pw, (idx // 3) * ph
        draw.rectangle([x_box0 + 4, y_box0 + 4, x_box0 + pw - 5, y_box0 + ph - 5], outline=(210, 215, 222))
        draw.text((x_box0 + 14, y_box0 + 10), title, fill=(25, 35, 50))

        def to_px(pt):
            u, v, _ = proj(*pt)
            if idx < 3:
                return (ox + (u - 17.5) * scale, oy + v * scale)
            elif idx in (3, 4):
                return (ox + u * scale, oy + v * scale)
            else:
                return (ox + (u - 14.0) * scale, oy + v * scale)

        if shaded:
            rendered = []
            for p1, p2, p3 in tris:
                q1, q2, q3 = proj(*p1), proj(*p2), proj(*p3)
                # Backface / lighting
                ux, uy, uz = q2[0] - q1[0], q2[1] - q1[1], q2[2] - q1[2]
                vx, vy, vz = q3[0] - q1[0], q3[1] - q1[1], q3[2] - q1[2]
                nx = uy * vz - uz * vy
                ny = uz * vx - ux * vz
                nz = ux * vy - uy * vx
                norm = sqrt(nx * nx + ny * ny + nz * nz) + 1e-12
                light = abs((0.35 * nx - 0.55 * ny + 0.75 * nz) / norm)
                shade = int(75 + 145 * min(1.0, light))
                col = (int(shade * 0.92), int(shade * 0.65), int(shade * 0.35))
                avg_d = (q1[2] + q2[2] + q3[2]) / 3.0
                rendered.append((avg_d, [to_px(p1), to_px(p2), to_px(p3)], col))
            rendered.sort(key=lambda item: item[0])
            for _, pts2d, col in rendered:
                draw.polygon(pts2d, fill=col)

        for pts in polylines:
            pts2d = [to_px(p) for p in pts]
            draw.line(pts2d, fill=(20, 30, 45), width=1)

    img.save(out_path)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--views", type=Path, help="Optional path for the six-view PNG")
    args = parser.parse_args()

    # 1. Base cylinder Ø16.0 x 35.0
    body = make_cylinder(0.0, 0.0, 0.0, 0.0, 0.0, 1.0, OUTER_RADIUS, TOTAL_LENGTH)

    # 2. Left end hex H13.86 (Z = 0..5)
    body = cut_hex_flats(body, LEFT_HEX_AF, [30, 90, 150, 210, 270, 330], -1.0, LEFT_HEX_LENGTH)

    # 3. Right end hex H13.71 (Z = 30..35, 30 deg phase shift)
    body = cut_hex_flats(body, RIGHT_HEX_AF, [0, 60, 120, 180, 240, 300], TOTAL_LENGTH - RIGHT_HEX_LENGTH, TOTAL_LENGTH + 1.0)

    # 4. Left end tongue-shaped square pocket (7.20 x 7.20, depth 2.5)
    body = cut(body, build_tongue_slot_cutter())

    # 5. Side eccentric through-hole (Ø3.00 at Y=+4.73, Z=13.0)
    body = cut(body, make_cylinder(-10.0, SIDE_THROUGH_Y, SIDE_THROUGH_Z, 1.0, 0.0, 0.0, SIDE_THROUGH_RADIUS, 20.0))

    # 6. Side annular pocket with Ø1.50 central boss (-Y side, Z=15.56, Ø6 depth 3.0)
    ring_outer = make_cylinder(0.0, -10.0, RING_Z, 0.0, 1.0, 0.0, RING_OUTER_RADIUS, 2.0 + RING_DEPTH)
    ring_inner = make_cylinder(0.0, -11.0, RING_Z, 0.0, 1.0, 0.0, RING_BOSS_RADIUS, 7.0)
    ring_cutter = cut(ring_outer, ring_inner)
    body = cut(body, ring_cutter)

    # 7. Opposite stepped flat-bottom hole (+Y side, Z=25.00, Ø5 depth 2.5 + Ø2.60 depth 4.5)
    cbore = make_cylinder(0.0, 10.0, STEP_HOLE_Z, 0.0, -1.0, 0.0, STEP_HOLE_CBORE_RADIUS, 2.0 + STEP_HOLE_CBORE_DEPTH)
    inner_bore = make_cylinder(0.0, 10.0, STEP_HOLE_Z, 0.0, -1.0, 0.0, STEP_HOLE_BORE_RADIUS, 2.0 + STEP_HOLE_BORE_TOTAL_DEPTH)
    body = cut(body, cbore)
    body = cut(body, inner_bore)

    # 8. Right end eccentric rounded-rectangle slot (3.80 x 6.10, R1.50, depth 3.0)
    body = cut(body, build_right_slot_cutter())

    # 9. Right end eccentric blind hole (Ø2.70 at X=+2.80, Y=0, depth 3.0)
    right_bore = make_cylinder(RIGHT_BORE_X, 0.0, TOTAL_LENGTH - RIGHT_BORE_DEPTH, 0.0, 0.0, 1.0, RIGHT_BORE_RADIUS, RIGHT_BORE_DEPTH + 1.0)
    body = cut(body, right_bore)

    volume, limits = verify_shape(body)

    step_path = args.output_dir / "双端六方舌形槽多孔件.step"
    with TemporaryDirectory() as temp_dir:
        # Keep the exported filename ASCII for the STEP reader/writer.
        tmp_step = Path(temp_dir) / "DoubleHexTongueSlot.step"
        writer = STEPControl_Writer()
        Interface_Static.SetCVal_s("write.step.schema", "AP214IS")
        assert writer.Transfer(body, STEPControl_AsIs) == IFSelect_RetDone
        assert writer.Write(str(tmp_step)) == IFSelect_RetDone

        reader = STEPControl_Reader()
        assert reader.ReadFile(str(tmp_step)) == IFSelect_RetDone
        assert reader.TransferRoots() == 1
        reloaded_vol, _ = verify_shape(reader.OneShape())
        assert isclose(reloaded_vol, volume, abs_tol=1e-4)

        args.output_dir.mkdir(parents=True, exist_ok=True)
        step_path.write_bytes(tmp_step.read_bytes())

    if args.views is not None:
        args.views.parent.mkdir(parents=True, exist_ok=True)
        render_verification_views(body, args.views)
    print(f"OK! Volume = {volume:.4f} mm^3, BBox = {tuple(round(v, 4) for v in limits)}")
    print(f"STEP written to {step_path}")


if __name__ == "__main__":
    main()
