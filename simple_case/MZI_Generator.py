import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import os
import nazca as nd
import nazca.demofab as demo
from nazca.interconnects import Interconnect
# 尝试导入 Pillow，用于更高级的图片处理
try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

class MZIGeneratorGUI:
    def __init__(self, master):
        self.master = master
        master.title("MZI Generator")
        master.geometry("1000x520")
        master.configure(bg="#f5f5f5")

        # --- Attempt to load company icon (PMC.png / PMC.ico) ---
        script_dir = os.path.dirname(os.path.abspath(__file__))
        png_path = os.path.join(script_dir, "PMC.png")
        ico_path = os.path.join(script_dir, "PMC.ico")

        self.icon_status = tk.StringVar()
        self.icon_status.set("⚠️ PMC icon not found") # 默认状态

        try:
            # Prefer .ico for native Windows titlebar icon
            if os.path.exists(ico_path):
                try:
                    master.iconbitmap(ico_path)
                    self.icon_status.set("✅ PMC.ico loaded as window icon")
                except Exception as e:
                    self.icon_status.set(f"⚠️ Failed to use PMC.ico ({e})")
            
            if os.path.exists(png_path) and HAS_PIL:
                try:
                    img = Image.open(png_path)
                    max_size = (64, 64)
                    img.thumbnail(max_size, Image.LANCZOS)
                    self.icon_image = ImageTk.PhotoImage(img)
                    master.iconphoto(True, self.icon_image)
                    if not self.icon_status.get().startswith("✅"):
                         self.icon_status.set("✅ PMC.png loaded (Pillow)")
                except Exception as e:
                    self.icon_status.set(f"⚠️ Failed to load PMC.png ({e})")
            elif os.path.exists(png_path):
                 try:
                    self.icon_image = tk.PhotoImage(file=png_path)
                    master.iconphoto(True, self.icon_image)
                    if not self.icon_status.get().startswith("✅"):
                         self.icon_status.set("✅ PMC.png loaded (tk.PhotoImage)")
                 except Exception:
                     pass

        except Exception as e:
            self.icon_status.set(f"⚠️ Icon load error ({e})")

        # --- Title Label ---
        ttk.Label(master, text="MZI Array Generator", font=("Arial", 18, "bold")).pack(pady=(20, 5))
        ttk.Label(master, textvariable=self.icon_status, font=("Arial", 10, "italic"), foreground="gray").pack(pady=(0, 10))

        # --- Create main two-column area (left = params, right = image preview) ---
        main_frame = tk.Frame(master, bg="#f5f5f5")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # --- Parameter Frame (left) ---
        param_frame = ttk.LabelFrame(main_frame, text="Global Parameters", padding=15)
        param_frame.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=0)

        # --- Image Preview Frame (right) ---
        image_frame = ttk.LabelFrame(main_frame, text="Preview", padding=10, width=520)
        image_frame.pack(side="right", fill="both", padx=(10, 0), pady=0)

        # --- Input fields ---
        self.entries = {}
        params = [
            ("Modes", 4),
            ("MZI_y_begin", 50),
            ("MZI_X_distance", 100),
            ("dc_gap", 5),
            ("DC_middle_length", 50),
            ("shallow_DC (1=Yes, 0=No)", 1),
            ("gc_output (1=Yes, 0=No)", 0),
            ("wg_width (μm)", 0.5),
            ("taper_length (μm)", 500)
        ]

        for i, (label, default) in enumerate(params):
            ttk.Label(param_frame, text=label, font=("Arial", 11)).grid(row=i, column=0, sticky="w", pady=4)
            entry = ttk.Entry(param_frame, width=15)
            entry.insert(0, str(default))
            entry.grid(row=i, column=1, pady=4, padx=10)
            self.entries[label] = entry

        # --- Buttons ---
        btn_frame = tk.Frame(param_frame, bg="#f5f5f5")
        btn_frame.grid(row=len(params), column=0, columnspan=2, pady=15)

        ttk.Button(btn_frame, text="Generate MZI GDS", command=self.run_generator).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Exit", command=master.quit).grid(row=0, column=1, padx=10)

        # --- Load and show preview image on right ---
        if HAS_PIL and os.path.exists(png_path):
            try:
                img = Image.open(png_path)
                max_size = (520, 520)
                img.thumbnail(max_size, Image.LANCZOS)
                self.preview_image = ImageTk.PhotoImage(img)  # keep reference
                self.preview_label = ttk.Label(image_frame, image=self.preview_image)
                self.preview_label.pack(expand=True)
            except Exception as e:
                 self.preview_label = ttk.Label(image_frame, text=f"加载 PMC.png 失败: {e}", foreground="red")
                 self.preview_label.pack(expand=True)
        else:
            self.preview_label = ttk.Label(image_frame, text="PMC.png 未找到或 Pillow 缺失", foreground="gray")
            self.preview_label.pack(expand=True)

        # --- Status Label ---
        self.status_label = ttk.Label(master, text="Status: Ready", font=("Arial", 10))
        self.status_label.pack(pady=10)

    def run_generator(self):
        try:
            # ✅ 关键修正: 使用 nd.clear_all() 确保 Nazca 状态完全清空
            nd.clear_all() 

            # --- 参数校验和获取 ---
            Modes = int(self.entries["Modes"].get())
            if Modes <= 0 or Modes % 2 != 0:
                 raise ValueError("Modes 必须是正偶数。")
                 
            MZI_y_begin = float(self.entries["MZI_y_begin"].get())
            MZI_X_distance = float(self.entries["MZI_X_distance"].get())
            dc_gap = float(self.entries["dc_gap"].get())
            DC_middle_length = float(self.entries["DC_middle_length"].get())
            shallow_DC = int(self.entries["shallow_DC (1=Yes, 0=No)"].get())
            gc_output = int(self.entries["gc_output (1=Yes, 0=No)"].get()) 
            wg_width = float(self.entries["wg_width (μm)"].get())
            taper_length = float(self.entries["taper_length (μm)"].get())

            MZI_y_offset = MZI_y_begin - dc_gap / 2

            # --- XSection Setup ---
            nd.add_layer2xsection(xsection='Wg', layer=1, accuracy=0.001)
            nd.add_xsection(name='Wg')
            nd.add_layer2xsection(xsection='Tp', layer=2, accuracy=0.001)
            nd.add_xsection(name='Tp')
            nd.add_layer2xsection(xsection='Gc', layer=3, accuracy=0.001)
            nd.add_xsection(name='Gc')

            ic = Interconnect(width=wg_width, radius=30.0)

            # --- GDS 加载和 'gc' Cell 定义 (修正部分) ---
            script_dir = os.path.dirname(os.path.abspath(__file__))
            merged_gds_path = os.path.join(script_dir, "merged_output.gds")
            
            # 创建gc cell（与成功代码相同的方式）
            with nd.Cell(name='gc') as gc_cell:
                if os.path.exists(merged_gds_path):
                    try:
                        # 加载GDS并放置内容（注意保留逗号）
                        loaded_gc = nd.load_gds(
                            filename=merged_gds_path,
                            cellname='MERGED',
                        )
                        loaded_gc.put()  # 关键：这行不能少！
                        print("✅ GDS文件加载成功")
                    except Exception as e:
                        print(f"⚠️ 加载GDS文件失败: {e}")
                else:
                    print("⚠️ merged_output.gds 文件不存在，'gc' Cell内容为空。")
                    
            # --- Drawing logic copied from MZI.py (unchanged) ---
            def draw_upper_arm(start_x, start_y, is_shallow, wg_w, MZI_y0, MZI_X_dist, MZI_y_off, DC_len, ic_obj):
                y_start_offset = start_y + MZI_y0
                if is_shallow == 1:
                    demo.shallow.sinebend(width=wg_w, distance=MZI_X_dist, offset=-MZI_y_off, xs='Wg').put(start_x, y_start_offset)
                    demo.shallow.strt(width=wg_w, length=DC_len, xs='Wg').put()
                    demo.shallow.sinebend(width=wg_w, distance=MZI_X_dist, offset=MZI_y_off, xs='Wg').put()
                else:
                    ic_obj.sinebend(distance=MZI_X_dist, offset=-MZI_y_off).put(start_x, y_start_offset)
                    demo.strt(width=wg_w, length=DC_len).put()
                    demo.sinebend(width=wg_w, distance=MZI_X_dist, offset=MZI_y_off).put()

            def draw_lower_arm(start_x, start_y, is_shallow, wg_w, MZI_y0, MZI_X_dist, MZI_y_off, DC_len, ic_obj):
                y_start_offset = start_y - MZI_y0
                if is_shallow == 1:
                    demo.shallow.sinebend(width=wg_w, distance=MZI_X_dist, offset=MZI_y_off, xs='Wg').put(start_x, y_start_offset)
                    demo.shallow.strt(width=wg_w, length=DC_len, xs='Wg').put()
                    demo.shallow.sinebend(width=wg_w, distance=MZI_X_dist, offset=-MZI_y_off, xs='Wg').put()
                else:
                    demo.sinebend(width=wg_w, distance=MZI_X_dist, offset=MZI_y_off).put(start_x, y_start_offset)
                    demo.strt(width=wg_w, length=DC_len).put()
                    demo.sinebend(width=wg_w, distance=MZI_X_dist, offset=-MZI_y_off).put()

            with nd.Cell("Coupler") as coupler:
                draw_upper_arm(0, 0, shallow_DC, wg_width, MZI_y_begin, MZI_X_distance, MZI_y_offset, DC_middle_length, ic)
                draw_lower_arm(0, 0, shallow_DC, wg_width, MZI_y_begin, MZI_X_distance, MZI_y_offset, DC_middle_length, ic)

            X_cas_shift = 2 * MZI_X_distance + DC_middle_length
            mid_length = 50
            n1 = int(Modes / 2)
            n2 = n1 - 1
            x_shift_mesh = 2 * X_cas_shift + mid_length

            def MZI_build(mid_len, x_start, y_start):
                coupler.put(x_start, y_start)
                if shallow_DC == 1:
                    demo.shallow.strt(width=wg_width, length=mid_len, xs='Wg').put(X_cas_shift + x_start, MZI_y_begin + y_start)
                    demo.shallow.strt(width=wg_width, length=mid_len, xs='Wg').put(X_cas_shift + x_start, -MZI_y_begin + y_start)
                coupler.put(X_cas_shift + mid_len + x_start, y_start)

            def generate_MZI_mesh(n1_local, n2_local):
                for i in range(n1_local):
                    for j in range(n1_local):
                        MZI_build(mid_length, i * 2 * x_shift_mesh, j * 4 * MZI_y_begin)
                for i in range(n1_local):
                    for j in range(n2_local):
                        MZI_build(mid_length, (2 * i + 1) * x_shift_mesh, (2 * j + 1) * 2 * MZI_y_begin)
                
                for i in range(n1_local):
                    draw_lower_arm((2 * i + 1) * x_shift_mesh, (2 * n2_local + 1) * 2 * MZI_y_begin, shallow_DC, wg_width, MZI_y_begin, MZI_X_distance, MZI_y_offset, DC_middle_length, ic)
                    draw_lower_arm((2 * i + 1) * x_shift_mesh + X_cas_shift + mid_length, (2 * n2_local + 1) * 2 * MZI_y_begin, shallow_DC, wg_width, MZI_y_begin, MZI_X_distance, MZI_y_offset, DC_middle_length, ic)
                    demo.shallow.strt(width=wg_width, length=mid_length, xs='Wg').put((2 * i + 1) * x_shift_mesh + X_cas_shift, (4 * n2_local + 1) * MZI_y_begin)
                for i in range(n1_local):
                    draw_upper_arm((2 * i + 1) * x_shift_mesh, -2 * MZI_y_begin, shallow_DC, wg_width, MZI_y_begin, MZI_X_distance, MZI_y_offset, DC_middle_length, ic)
                    draw_upper_arm((2 * i + 1) * x_shift_mesh + X_cas_shift + mid_length, -2 * MZI_y_begin, shallow_DC, wg_width, MZI_y_begin, MZI_X_distance, MZI_y_offset, DC_middle_length, ic)
                    demo.shallow.strt(width=wg_width, length=mid_length, xs='Wg').put((2 * i + 1) * x_shift_mesh + X_cas_shift, -1 * MZI_y_begin)

            def generate_input(taper):
                for i in range(n1):
                    demo.shallow.taper(width1=10, width2=wg_width, length=taper, xs='Tp').put(-taper, (i * 4 + 1) * MZI_y_begin)
                    demo.shallow.taper(width1=10, width2=wg_width, length=taper, xs='Tp').put(-taper, (i * 4 - 1) * MZI_y_begin)

            def generate_output_placeholders(taper):
                for i in range(n1):
                    demo.shallow.taper(width1=wg_width, width2=10, length=taper, xs='Tp').put(((2 * n1) * x_shift_mesh), (i * 4 + 1) * MZI_y_begin)
                    demo.shallow.taper(width1=wg_width, width2=10, length=taper, xs='Tp').put(((2 * n1) * x_shift_mesh), (i * 4 - 1) * MZI_y_begin)

            generate_MZI_mesh(n1, n2)

            if gc_output != 1:
                generate_input(taper=500)
                generate_output_placeholders(taper=500)

            def generate_output_with_gc(gc_cell, taper_shift):
                for i in range(n1):
                    gc_cell.put(((2 * n1) * x_shift_mesh + taper_shift), (i * 4 + 1) * MZI_y_begin)
                    demo.shallow.strt(width=wg_width, length=taper_shift, xs='Gc').put(((2 * n1) * x_shift_mesh), (i * 4 + 1) * MZI_y_begin)
                    gc_cell.put(((2 * n1) * x_shift_mesh + taper_shift), (i * 4 - 1) * MZI_y_begin)
                    demo.shallow.strt(width=wg_width, length=taper_shift, xs='Gc').put(((2 * n1) * x_shift_mesh), (i * 4 - 1) * MZI_y_begin)

            if gc_output == 1:
                # 尝试获取已加载的 'gc' Cell
                try:
                    gc = nd.get_cell('gc')
                    generate_input(taper=500)
                    generate_output_with_gc(gc, taper_shift=500)
                except Exception as e:
                    print(f"⚠️ 无法获取 'gc' Cell ({e})。确保 merged_output.gds 存在且包含 'MERGED' Cell。回退到普通输出。")
                    generate_input(taper=500)
                    generate_output_placeholders(taper=500)

            # --- Export GDS and notify user ---
            gds_filename = f"{Modes}_modes_MZI.gds"
            nd.export_gds(filename=gds_filename)
            self.status_label.config(text=f"✅ GDS exported successfully: {gds_filename}")
            messagebox.showinfo("Success", f"GDS file saved as {gds_filename}")

        except Exception as e:
            self.status_label.config(text=f"❌ Error: {e}")
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = MZIGeneratorGUI(root)
    root.mainloop()