import cairosvg, io, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages
D="out_v2"
GEN=("General: ISO 2768-mK unless noted. Units mm. Break sharp edges 0.2-0.3. Finish: as machined, NO anodize "
     "(keeps bearing fits). Threads tapped as listed. Model is nominal - fits per table.")
parts=[
("01_housing_pin_ring","6061-T6","1",[
 ("Bearing bore (6812 OD), z 0-10","Ø78 J7","+0.018 / -0.012"),
 ("10x ring-pin pockets Ø6, depth 16, on Ø68 PCD","Ø6 H7","+0.012 / 0"),
 ("Ring-pin PCD position","Ø68 PCD","pos. Ø0.02, coaxial to Ø78 bore"),
 ("Pin-ring bore (disc tip clearance 0.6)","Ø69","±0.05"),
 ("Ring pins sit in pockets (<180° wrap)","-","fit pins with Loctite 638"),
 ("Shoulder face (bearing stop) flatness","-","0.02"),
 ("6x through holes on Ø85 PCD","Ø3.4","clearance M3 x 32, heads on output side")]),
("02_cycloid_disc_x2","7075-T6","2",[
 ("Centre bore (6804 OD)","Ø32 N7","-0.008 / -0.033"),
 ("Cycloid outer profile","per STEP","profile 0.02, ⊥ to faces 0.01"),
 ("6x output holes on Ø46 PCD","Ø8.3","+0.02 / 0, pos. Ø0.02"),
 ("Thickness / parallelism","7","±0.02 / 0.01"),
 ("Both discs identical; Ø1.5 index hole","-","for 180° assembly")]),
("03_output_flange","6061-T6","1",[
 ("Hub (6812 ID), z 0-10","Ø60 k6","+0.021 / +0.002"),
 ("Centre pocket (6800 OD) depth 5","Ø19 H7","+0.021 / 0"),
 ("6x output-pin holes depth 8 on Ø46 PCD","Ø5 H7","+0.012 / 0, pos. Ø0.02 coaxial to Ø60"),
 ("4x holes Ø2.5 depth 8 on Ø28 PCD","M3 thread","tap full depth"),
 ("6x holes Ø4.2 on Ø50 PCD (round output face)","M5 thread","tap, depth 10")]),
("04_bearing_retainer","6061-T6","1",[
 ("Thickness","1.5","±0.05 (laser-cut OK)"),
 ("6x pin clearance holes on Ø46","Ø5.2","+0.05 / 0"),
 ("4x on Ø28 PCD","Ø3.4","clearance M3")]),
("05_eccentric_cam_v2","7075-T6","1",[
 ("Lobe B (z 12.5-19.5), offset +1.5","Ø20 k6","+0.015 / +0.002"),
 ("Lobe A (z 20-27), offset -1.5","Ø20 k6","+0.015 / +0.002"),
 ("Eccentricity both lobes, 180° apart","1.5","±0.01"),
 ("Lower journal (6800 ID)","Ø10 k6","+0.010 / +0.001"),
 ("Rotor spigot (top)","Ø20 h7","0 / -0.021, coaxial to journal Ø0.01"),
 ("Shaft pilot bore, depth 10","Ø10 H7","+0.015 / 0"),
 ("Flange top face","Ø38","⊥ to axis 0.01"),
 ("5x on Ø30 PCD, through flange (4 mm)","M3 thread","tap Ø2.5")]),
("06_motor_can","6061-T6","1",[
 ("Bottom plate centre hole","Ø42","±0.1"),
 ("6x on Ø85 PCD, bottom plate","M3 thread","tap Ø2.5 through (bolts from output side)"),
 ("Wall bore","Ø96.5","±0.05"),
 ("6x on Ø101.2 PCD, top face","M3 thread","tap Ø2.5, depth 8"),
 ("Top face parallel to bottom face","-","0.02")]),
("07_rotor_one_piece_steel","EN8 / C45 steel (magnetic)","1",[
 ("Shaft journals (2x 6000 ID) z 41.5-59.5","Ø10 h6","0 / -0.009, ground or fine-turned"),
 ("Shaft pilot below boss (into cam)","Ø10 h6","0 / -0.009"),
 ("Spigot recess (fits cam Ø20 h7)","Ø20 H7","+0.021 / 0, depth 2"),
 ("Magnet bore (back iron)","Ø87.4 H7","+0.035 / 0, depth 22"),
 ("Outer diameter","Ø93.4","±0.05"),
 ("Bore + OD run-out to shaft axis","-","0.02 (air gap 0.7)"),
 ("5x Ø3.4 on Ø30 PCD, c'bore Ø6.5 x 2.5","M3 clearance","DIN 7984 low-head"),
 ("Finish","-","as machined; light oil / blacken OK, no paint in bore")]),
("10_stator_hub","6061-T6","1",[
 ("Stator seat","Ø51.9","+0 / -0.03 (epoxy)"),
 ("2x 6000 bearing seats, top and bottom","Ø26 J7","+0.012 / -0.009"),
 ("Centre shoulder","Ø22 x 2","±0.05"),
 ("4x on Ø44 PCD, top face","M4 thread","tap Ø3.3, depth 8")]),
("11_back_plate","6061-T6","1",[
 ("6x on Ø101.2 PCD","Ø3.4","clearance M3"),
 ("4x on Ø44 PCD, 90° c'sink Ø8.6 TOP face","Ø4.4","M4 countersunk into stator hub"),
 ("3x on Ø34 PCD","M2.5 thread","encoder PCB standoffs"),
 ("Centre hole / phase-lead slot","Ø14 / 12x5","±0.1"),
 ("Hub seating face flatness","-","0.02")]),
("12_back_cover","6061-T6 or MJF PA12","1",[
 ("6x on Ø101.2 PCD","Ø3.4","clearance M3 (long screws through to can)"),
 ("Cable notch","14 x 6","±0.2")]),
]
with PdfPages(f"{D}/drawings_actuator_v2.pdf") as pdf:
    for name,mat,qty,rows in parts:
        fig=plt.figure(figsize=(11.69,8.27))
        png=cairosvg.svg2png(url=f"{D}/{name}.svg",output_width=900)
        ax=fig.add_axes([0.02,0.12,0.5,0.75]); ax.imshow(mpimg.imread(io.BytesIO(png))); ax.axis("off")
        ax.set_title("Top view (see STEP for 3D)",fontsize=9)
        fig.text(0.02,0.95,f"{name}   |   Material: {mat}   |   Qty: {qty}   |   19 Nm Actuator v2 (flipped motor) — A. Arjun",fontsize=13,weight="bold")
        t=fig.add_axes([0.52,0.15,0.46,0.72]); t.axis("off")
        tb=t.table(cellText=[list(r) for r in rows],colLabels=["Critical feature","Size / fit","Tolerance"],
                   colWidths=[0.55,0.18,0.37],loc="upper center",cellLoc="left")
        tb.auto_set_font_size(False); tb.set_fontsize(8); tb.scale(1,2.2)
        fig.text(0.02,0.04,GEN,fontsize=8,wrap=True)
        pdf.savefig(fig); plt.close(fig)
print("ok")
