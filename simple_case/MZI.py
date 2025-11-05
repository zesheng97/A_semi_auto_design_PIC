import nazca as nd
import nazca.demofab as demo
from nazca.interconnects import Interconnect

# --- Global Parameters ---
Modes = 4
MZI_y_begin = 50
MZI_X_distance = 100
dc_gap = 5
MZI_y_offset = MZI_y_begin - dc_gap/2
DC_middle_length = 50
shallow_DC = 1 
gc_output = 0
wg_width = 0.5 # <-- Target waveguide width 0.5
taper_length = 500


# --- XSections Setup ---
nd.add_layer2xsection(xsection='Wg', layer=1, accuracy=0.001) 
nd.add_xsection(name='Wg') 
nd.add_layer2xsection(xsection='Tp', layer=2, accuracy=0.001) 
nd.add_xsection(name='Tp') 
nd.add_layer2xsection(xsection='Gc', layer=3, accuracy=0.001) 
nd.add_xsection(name='Gc') 

# **Unify Interconnect width**
ic = Interconnect(width=wg_width, radius=30.0)

with nd.Cell(name='gc') as gc:
    # load GDS BB
    gc = nd.load_gds(
        filename='merged_output.gds',
        cellname='MERGED',
        
        
        )
    gc.put()

# --- Arm Drawing Functions with Start Coordinates ---

def draw_upper_arm(start_x, start_y, is_shallow, wg_w, MZI_y0, MZI_X_dist, MZI_y_off, DC_len, ic_obj):
    """
    Draws the upper arm of the directional coupler, starting at (start_x, start_y).
    start_y is the input y-coordinate, the arm will be drawn at y = start_y + MZI_y0.
    """
    y_start_offset = start_y + MZI_y0 # Calculate the actual Y position for the upper arm
    
    if is_shallow == 1:
        # Shallow etched components
        # Put the first element at the calculated starting position
        demo.shallow.sinebend(width = wg_w, distance=MZI_X_dist, offset=-MZI_y_off, xs = 'Wg').put(start_x, y_start_offset)
        demo.shallow.strt(width = wg_w, length=DC_len, xs = 'Wg').put()
        demo.shallow.sinebend(width = wg_w, distance=MZI_X_dist, offset=MZI_y_off, xs = 'Wg').put()
    else:
        # Standard components using Interconnect/demo
        ic_obj.sinebend(distance=MZI_X_dist, offset=-MZI_y_off).put(start_x, y_start_offset)
        demo.strt(width = wg_w, length=DC_len).put()
        demo.sinebend(width = wg_w, distance=MZI_X_dist, offset=MZI_y_off).put()

def draw_lower_arm(start_x, start_y, is_shallow, wg_w, MZI_y0, MZI_X_dist, MZI_y_off, DC_len, ic_obj):
    """
    Draws the lower arm of the directional coupler, starting at (start_x, start_y).
    start_y is the input y-coordinate, the arm will be drawn at y = start_y - MZI_y0.
    """
    y_start_offset = start_y - MZI_y0 # Calculate the actual Y position for the lower arm
    
    if is_shallow == 1:
        # Shallow etched components
        # Put the first element at the calculated starting position
        demo.shallow.sinebend(width = wg_w, distance=MZI_X_dist, offset=MZI_y_off, xs = 'Wg').put(start_x, y_start_offset)
        demo.shallow.strt(width = wg_w, length=DC_len, xs = 'Wg').put()
        demo.shallow.sinebend(width = wg_w, distance=MZI_X_dist, offset=-MZI_y_off, xs = 'Wg').put()
    else:
        # Standard components using Interconnect/demo
        # Note: The 'demo' components in the else block need to be explicitly set to start_x, y_start_offset
        demo.sinebend(width = wg_w, distance=MZI_X_dist, offset=MZI_y_off).put(start_x, y_start_offset)
        demo.strt(width = wg_w, length=DC_len).put()
        demo.sinebend(width = wg_w, distance=MZI_X_dist, offset=-MZI_y_off).put()

# --- Coupler Cell Definition ---
with nd.Cell("Coupler") as coupler:
    
    # **CALL UPPER ARM FUNCTION, starting at (0, 0)**
    # The actual arm starts at (0, MZI_y_begin)
    draw_upper_arm(0, 0, shallow_DC, wg_width, MZI_y_begin, MZI_X_distance, MZI_y_offset, DC_middle_length, ic)

    # **CALL LOWER ARM FUNCTION, starting at (0, 0)**
    # The actual arm starts at (0, -MZI_y_begin)
    draw_lower_arm(0, 0, shallow_DC, wg_width, MZI_y_begin, MZI_X_distance, MZI_y_offset, DC_middle_length, ic)

# --- MZI Building Function ---
X_cas_shift = 2*MZI_X_distance + DC_middle_length
mid_length = 50
def MZI_build(mid_length, x_start, y_start):
    coupler.put(x_start, y_start)
    if shallow_DC == 1:
        # Straight arms of the MZI include width = wg_width
        demo.shallow.strt(width = wg_width, length=mid_length, xs = 'Wg').put(X_cas_shift+x_start, MZI_y_begin+y_start)
        demo.shallow.strt(width = wg_width, length=mid_length, xs = 'Wg').put(X_cas_shift+x_start, -MZI_y_begin+y_start)
    coupler.put(X_cas_shift + mid_length+x_start,y_start)
 
# --- Mesh Generation ---

n1 = int(Modes/2)
n2 = n1-1
x_shift_mesh = 2*X_cas_shift + mid_length
def generate_MZI_mesh(n1, n2):
    x_shift_mesh = 2*X_cas_shift + mid_length
    for i in range(n1):
        for j in range(n1):
            MZI_build(mid_length , + i*2*x_shift_mesh, j*4*MZI_y_begin)
    for i in range(n1):
        for j in range(n2):
            MZI_build(mid_length , + (2*i+1)*x_shift_mesh, (2*j+1)*2*MZI_y_begin)
    for i in range(n1):
        draw_lower_arm((2*i+1)*x_shift_mesh, (2*n2+1)*2*MZI_y_begin, shallow_DC, wg_width, MZI_y_begin, MZI_X_distance, MZI_y_offset, DC_middle_length, ic)
        draw_lower_arm((2*i+1)*x_shift_mesh + X_cas_shift + mid_length, (2*n2+1)*2*MZI_y_begin, shallow_DC, wg_width, MZI_y_begin, MZI_X_distance, MZI_y_offset, DC_middle_length, ic)
        demo.shallow.strt(width = wg_width, length=mid_length, xs = 'Wg').put((2*i+1)*x_shift_mesh + X_cas_shift, (4*n2+1)*MZI_y_begin)
    for i in range(n1):
        draw_upper_arm((2*i+1)*x_shift_mesh, -2*MZI_y_begin, shallow_DC, wg_width, MZI_y_begin, MZI_X_distance, MZI_y_offset, DC_middle_length, ic)
        draw_upper_arm((2*i+1)*x_shift_mesh + X_cas_shift + mid_length, -2*MZI_y_begin, shallow_DC, wg_width, MZI_y_begin, MZI_X_distance, MZI_y_offset, DC_middle_length, ic)
        demo.shallow.strt(width = wg_width, length=mid_length, xs = 'Wg').put((2*i+1)*x_shift_mesh + X_cas_shift, -1*MZI_y_begin)

def generate_input(taper):
    for i in range(n1):
        demo.shallow.taper(width1 = 10, width2 = wg_width, length = taper, xs = 'Tp').put( -taper, (i*4+1)*MZI_y_begin)
        demo.shallow.taper(width1 = 10, width2 = wg_width, length = taper, xs = 'Tp').put( -taper, (i*4-1)*MZI_y_begin)
def generate_output(taper):
    for i in range(n1):
        demo.shallow.taper(width1 = wg_width, width2 = 10, length = taper, xs = 'Tp').put( ((2*n1)*x_shift_mesh ), (i*4+1)*MZI_y_begin)
        demo.shallow.taper(width1 = wg_width, width2 = 10, length = taper, xs = 'Tp').put( ((2*n1)*x_shift_mesh ), (i*4-1)*MZI_y_begin)



    




generate_MZI_mesh(n1, n2)

if gc_output != 1:
    generate_input(taper=500)
    generate_output(taper=500)

def generate_output(gc, taper_shift):
    for i in range(n1):
        gc.put( ((2*n1)*x_shift_mesh + taper_shift), (i*4+1)*MZI_y_begin)
        demo.shallow.strt(width = wg_width, length=taper_shift, xs = 'Gc').put( ((2*n1)*x_shift_mesh), (i*4+1)*MZI_y_begin)
        gc.put( ((2*n1)*x_shift_mesh + taper_shift), (i*4-1)*MZI_y_begin)
        demo.shallow.strt(width = wg_width, length=taper_shift, xs = 'Gc').put( ((2*n1)*x_shift_mesh), (i*4-1)*MZI_y_begin)
        
        
    
if gc_output == 1:
    generate_input(taper=500)
    generate_output(gc, taper_shift=500)

#nd.export_plt()
nd.export_gds(filename = f'{Modes}_modes_MZI.gds')