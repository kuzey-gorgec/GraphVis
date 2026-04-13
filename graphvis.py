import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
import json
import math
import random
import graph

ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("blue")  

class Visualizer:
    def __init__(self, backend_graph=None, width=1250, height=800):
        self.lang = "EN"
        
        # --- DİL SÖZLÜĞÜ (Tüm Emojiler Temizlendi) ---
        self.i18n = {
            "EN": {
                "title": "GraphVis",
                "weight": "Weight:",
                "add": "+ Add Edge",
                "update": "Update Edge",
                "remove": "- Remove Edge",
                "directed": "Directed Graph",
                "physics": "Physics Engine",
                "draw_on": "Draw Mode: ON",
                "draw_off": "Draw Mode: OFF",
                "save": "Save",
                "load": "Load",
                "algo": "Algorithm Configuration",
                "start": "Start:",
                "target": "Target:",
                "run": "Run Animation",
                "mst": "Convert to MST",
                "lang_btn": "TR", 
                "help_btn": "Help",
                "t_started": "GraphVis Started successfully.",
                "t_draw_on": "Draw Mode ON. See Help for controls.",
                "t_draw_off": "Draw Mode OFF.",
                "t_dir_upd": "Graph Type Updated: ",
                "t_dir_true": "Directed",
                "t_dir_false": "Undirected",
                "t_saved": "Map saved successfully.",
                "t_loaded": "Map loaded successfully.",
                "t_err_corrupt": "Error: Corrupt File!",
                "t_err_empty": "Error: U or V cannot be empty!",
                "t_added": "Added: ",
                "t_updated": "Updated: ",
                "t_err_noconn": "No connection found to update!",
                "t_removed": "Removed: ",
                "t_mst_conv": "Graph converted to Minimum Spanning Tree.",
                "t_err_start": "Error: Start node is missing in the map!",
                "t_calc": "Calculating: ",
                "t_err_target": "Error: Valid target node required!",
                "t_cost": "Cost: ",
                "t_dist": "Distance: ",
                "t_flow": "Max Flow: ",
                "t_err_rename": "Error: Node name already exists!",
                "algos": ["BFS", "DFS", "Dijkstra", "A* Search", "Prim's MST", "Kruskal's MST", "TSP (Nearest Neighbor)", "TSP (Brute Force)", "Max Flow (Network)"],
                "help_title": "GraphVis - User Manual",
                "help_text": """
Welcome to GraphVis Here is how to use the interactive features:

[ DRAW MODE ]
Turn on 'Draw Mode' from the left panel to edit the map directly on the canvas.
• Add Node: Click on any empty space. (If 'U' input has text, it uses that name).
• Add Edge: Click on a starting node (turns yellow), then click the target node. It will use the value in the 'Weight' input.
• Rename Node: Double-click on any node.
• Delete Node: Right-click on any node.

[ PHYSICS ENGINE ]
Turn on the 'Physics Engine' to let nodes automatically arrange themselves using repulsive and spring forces. You can drag nodes manually at any time.

[ ALGORITHMS ]
• Pathfinding (Dijkstra, A*, BFS, DFS): Requires a 'Start' and 'Target' node.
• MST (Prim, Kruskal): Only requires a 'Start' node.
• Routing (TSP): Only requires a 'Start' node to find a closed loop.
• Max Flow: Make sure 'Directed Graph' is ON. Requires 'Start' (Source) and 'Target' (Sink) nodes.
"""
            },
            "TR": {
                "title": "GraphVis",
                "weight": "Ağırlık Değeri:",
                "add": "+ Kenar Ekle",
                "update": "Güncelle",
                "remove": "- Kenarı Sil",
                "directed": "Yönlü Graf",
                "physics": "Fizik Motoru",
                "draw_on": "Çizim Modu: AÇIK",
                "draw_off": "Çizim Modu: KAPALI",
                "save": "Kaydet",
                "load": "Yükle",
                "algo": "Algoritma Ayarları",
                "start": "Başlangıç:",
                "target": "Hedef:",
                "run": "Simülasyonu Başlat",
                "mst": "MST'ye Dönüştür",
                "lang_btn": "EN",
                "help_btn": "Yardım",
                "t_started": "GraphVis başarıyla başlatıldı.",
                "t_draw_on": "Çizim Modu AÇIK. Kontroller için Yardım'a bakın.",
                "t_draw_off": "Çizim Modu KAPALI.",
                "t_dir_upd": "Graf Tipi Güncellendi: ",
                "t_dir_true": "Yönlü",
                "t_dir_false": "Yönsüz",
                "t_saved": "Harita başarıyla kaydedildi.",
                "t_loaded": "Harita başarıyla yüklendi.",
                "t_err_corrupt": "Hata: Dosya formatı bozuk!",
                "t_err_empty": "Hata: U veya V alanı boş bırakılamaz!",
                "t_added": "Eklendi: ",
                "t_updated": "Güncellendi: ",
                "t_err_noconn": "Hata: Güncellenecek bağlantı bulunamadı!",
                "t_removed": "Silindi: ",
                "t_mst_conv": "Graf başarıyla ağaca (MST) dönüştürüldü.",
                "t_err_start": "Hata: Başlangıç düğümü haritada bulunamadı!",
                "t_calc": "Hesaplanıyor: ",
                "t_err_target": "Hata: Lütfen geçerli bir Hedef düğümü girin!",
                "t_cost": "Maliyet: ",
                "t_dist": "Mesafe: ",
                "t_flow": "Maksimum Akış: ",
                "t_err_rename": "Hata: Bu isimde bir düğüm zaten mevcut!",
                "algos": ["BFS", "DFS", "Dijkstra", "A* Arama", "Prim MST", "Kruskal MST", "TSP (Yakın Komşu)", "TSP (Brute Force)", "Max Flow (Şebeke Akışı)"],
                "help_title": "GraphVis - Kullanım Kılavuzu",
                "help_text": """
GraphVis'e hoş geldiniz! İnteraktif özellikleri kullanmak için rehber:

[ ÇİZİM MODU ]
Sol panelden 'Çizim Modu'nu açarak haritayı fare ile yönetebilirsiniz.
• Düğüm Ekle: Boş bir alana sol tıklayın. (Eğer 'U' kutusu doluysa o ismi kullanır).
• Kenar Çiz: Önce başlangıç düğümüne (sarı yanar), sonra hedef düğüme tıklayın. 'Ağırlık' kutusundaki değeri kullanır.
• İsim Değiştir: Herhangi bir düğüme çift tıklayın.
• Düğüm Sil: Herhangi bir düğüme sağ tıklayın.

[ FİZİK MOTORU ]
Düğümlerin itme ve çekme kuvvetleriyle kendini otomatik düzenlemesi için 'Fizik Motoru'nu açın. Düğümleri fareyle serbestçe sürükleyebilirsiniz.

[ ALGORİTMALAR ]
• Yol Bulma (Dijkstra, A*, BFS, DFS): 'Başlangıç' ve 'Hedef' düğümü gerektirir.
• MST (Prim, Kruskal): Sadece 'Başlangıç' düğümü gerektirir.
• TSP (Gezgin Satıcı): Kapalı döngü bulmak için sadece 'Başlangıç' düğümü gerektirir.
• Max Flow (Akış): Mutlaka 'Yönlü Graf' açık olmalıdır. Kaynak (Başlangıç) ve Hedef düğümü gerektirir.
"""
            }
        }
        
        t = self.i18n[self.lang]
        
        if backend_graph is None:
            self.backend_graph = graph.Graph(is_directed=False)
        else:
            self.backend_graph = backend_graph 
        
        self.root = ctk.CTk()
        self.root.title(t["title"])
        self.root.geometry(f"{width}x{height}")
        self.root.minsize(500, 400) 
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1) 
        
        self.draw_mode = False
        self.selected_draw_node = None 
        self.next_node_id = 1 
        self.sidebar_visible = True 
        
        # --- SOL MENÜ ---
        self.sidebar = ctk.CTkScrollableFrame(self.root, width=300, corner_radius=0, fg_color="#18181f")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        title_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        title_frame.pack(fill="x", pady=(20, 20), padx=15)
        
        ctk.CTkLabel(title_frame, text="GraphVis", font=("Roboto", 22, "bold")).pack(side="left")
        
        # YARDIM VE DİL BUTONLARI (Yan yana, sade)
        self.btn_lang = ctk.CTkButton(title_frame, text=t["lang_btn"], width=40, height=28, fg_color="#34495e", hover_color="#2c3e50", font=("Roboto", 12, "bold"), command=self.switch_language)
        self.btn_lang.pack(side="right", padx=(5, 0))
        
        self.btn_help = ctk.CTkButton(title_frame, text=t["help_btn"], width=50, height=28, fg_color="#7f8fa6", hover_color="#718093", text_color="#2f3640", font=("Roboto", 12, "bold"), command=self.show_help)
        self.btn_help.pack(side="right")
        
        # KART 1: GENEL AYARLAR
        card_settings = ctk.CTkFrame(self.sidebar, fg_color="#23232b", corner_radius=10)
        card_settings.pack(fill="x", padx=15, pady=(0, 15))
        
        self.btn_draw = ctk.CTkSwitch(card_settings, text=t["draw_off"], command=self.toggle_draw_mode, font=("Roboto", 13, "bold"), progress_color="#9b59b6")
        self.btn_draw.pack(fill="x", pady=(15, 10), padx=15)
        
        self.is_dir_var = tk.BooleanVar(value=self.backend_graph.is_directed)
        self.chk_dir = ctk.CTkSwitch(card_settings, text=t["directed"], variable=self.is_dir_var, command=self.toggle_directed, font=("Roboto", 13, "bold"))
        self.chk_dir.pack(fill="x", pady=10, padx=15)

        self.physics_running = False
        self.btn_phys = ctk.CTkSwitch(card_settings, text=t["physics"], command=self.toggle_physics, font=("Roboto", 13, "bold"))
        self.btn_phys.pack(fill="x", pady=(10, 15), padx=15)

        # KART 2: HARİTA DÜZENLEYİCİ
        card_edit = ctk.CTkFrame(self.sidebar, fg_color="#23232b", corner_radius=10)
        card_edit.pack(fill="x", padx=15, pady=15)
        
        uv_frame = ctk.CTkFrame(card_edit, fg_color="transparent")
        uv_frame.pack(fill="x", pady=(15, 5), padx=15)
        uv_frame.grid_columnconfigure(1, weight=1)
        uv_frame.grid_columnconfigure(3, weight=1)
        
        ctk.CTkLabel(uv_frame, text="U:", font=("Roboto", 13, "bold")).grid(row=0, column=0, padx=(0, 5))
        self.entry_u = ctk.CTkEntry(uv_frame, font=("Roboto", 13), height=30, placeholder_text="A")
        self.entry_u.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        
        ctk.CTkLabel(uv_frame, text="V:", font=("Roboto", 13, "bold")).grid(row=0, column=2, padx=(0, 5))
        self.entry_v = ctk.CTkEntry(uv_frame, font=("Roboto", 13), height=30, placeholder_text="B")
        self.entry_v.grid(row=0, column=3, sticky="ew")

        w_frame = ctk.CTkFrame(card_edit, fg_color="transparent")
        w_frame.pack(fill="x", pady=5, padx=15)
        w_frame.grid_columnconfigure(1, weight=1)
        
        self.lbl_w = ctk.CTkLabel(w_frame, text=t["weight"], font=("Roboto", 13, "bold"))
        self.lbl_w.grid(row=0, column=0, padx=(0, 10), sticky="w")
        self.entry_w = ctk.CTkEntry(w_frame, font=("Roboto", 13), height=30)
        self.entry_w.insert(0, "10")
        self.entry_w.grid(row=0, column=1, sticky="ew")

        self.btn_add = ctk.CTkButton(card_edit, text=t["add"], font=("Roboto", 13, "bold"), height=32, command=self.add_new_edge)
        self.btn_add.pack(fill="x", pady=(10, 5), padx=15)
        
        self.btn_upd = ctk.CTkButton(card_edit, text=t["update"], fg_color="#e67e22", hover_color="#d35400", font=("Roboto", 13, "bold"), height=32, command=self.update_existing_edge)
        self.btn_upd.pack(fill="x", pady=5, padx=15)
        
        self.btn_rem = ctk.CTkButton(card_edit, text=t["remove"], fg_color="#e74c3c", hover_color="#c0392b", font=("Roboto", 13, "bold"), height=32, command=self.remove_existing_edge)
        self.btn_rem.pack(fill="x", pady=(5, 15), padx=15)

        # KART 3: ALGORİTMALAR
        card_algo = ctk.CTkFrame(self.sidebar, fg_color="#23232b", corner_radius=10)
        card_algo.pack(fill="x", padx=15, pady=15)
        
        self.lbl_algo = ctk.CTkLabel(card_algo, text=t["algo"], font=("Roboto", 14, "bold"), text_color="#3498db")
        self.lbl_algo.pack(anchor="w", padx=15, pady=(15, 5))
        
        self.algo_var = ctk.StringVar(value=t["algos"][2])
        self.combo_algo = ctk.CTkComboBox(card_algo, variable=self.algo_var, values=t["algos"], font=("Roboto", 13), state="readonly", height=32)
        self.combo_algo.pack(fill="x", padx=15, pady=5)

        st_frame = ctk.CTkFrame(card_algo, fg_color="transparent")
        st_frame.pack(fill="x", pady=5, padx=15)
        st_frame.grid_columnconfigure(1, weight=1)
        st_frame.grid_columnconfigure(3, weight=1)
        
        self.lbl_start = ctk.CTkLabel(st_frame, text=t["start"], font=("Roboto", 12, "bold"))
        self.lbl_start.grid(row=0, column=0, padx=(0, 5))
        self.entry_start = ctk.CTkEntry(st_frame, font=("Roboto", 13), height=30)
        self.entry_start.insert(0, "A")
        self.entry_start.grid(row=0, column=1, sticky="ew", padx=(0, 10))

        self.lbl_target = ctk.CTkLabel(st_frame, text=t["target"], font=("Roboto", 12, "bold"))
        self.lbl_target.grid(row=0, column=2, padx=(0, 5))
        self.entry_target = ctk.CTkEntry(st_frame, font=("Roboto", 13), height=30)
        self.entry_target.insert(0, "F")
        self.entry_target.grid(row=0, column=3, sticky="ew")

        self.btn_run = ctk.CTkButton(card_algo, text=t["run"], fg_color="#27ae60", hover_color="#2ecc71", font=("Roboto", 14, "bold"), height=42, command=self.start_simulation)
        self.btn_run.pack(fill="x", pady=(15, 10), padx=15)
        
        self.btn_mst = ctk.CTkButton(card_algo, text=t["mst"], fg_color="#f39c12", hover_color="#f1c40f", font=("Roboto", 13, "bold"), height=32, state="disabled", command=self.convert_to_mst)
        self.btn_mst.pack(fill="x", pady=(0, 15), padx=15)

        # DOSYA İŞLEMLERİ
        file_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        file_frame.pack(fill="x", padx=15, pady=(5, 20))
        
        self.btn_load = ctk.CTkButton(file_frame, text=t["load"], fg_color="#8e44ad", hover_color="#9b59b6", font=("Roboto", 13, "bold"), height=35, command=self.import_graph_json)
        self.btn_load.pack(side="left", expand=True, padx=(0, 5))
        
        self.btn_save = ctk.CTkButton(file_frame, text=t["save"], fg_color="#2980b9", hover_color="#3498db", font=("Roboto", 13, "bold"), height=35, command=self.export_graph_json)
        self.btn_save.pack(side="right", expand=True, padx=(5, 0))

        # --- ÇİZİM ALANI ---
        self.canvas_frame = ctk.CTkFrame(self.root, corner_radius=0)
        self.canvas_frame.grid(row=0, column=1, sticky="nsew") 
        
        self.canvas_width = width - 300
        self.canvas_height = height
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="#212126", highlightthickness=0) 
        self.canvas.pack(fill="both", expand=True)
        
        self.btn_hamburger = ctk.CTkButton(
            self.canvas_frame, text="✕", width=42, height=42, corner_radius=8, 
            fg_color="#e74c3c", hover_color="#c0392b", font=("Roboto", 22, "bold"), 
            command=self.toggle_sidebar
        )
        self.btn_hamburger.place(x=15, y=15) 

        self.nodes = []
        self.edges = []
        self.edge_weights = {} 
        self.coords = {}
        self.node_ovals = {}
        self.node_texts = {}
        self.edge_lines = {}
        self.edge_texts = {} 
        
        self.path = []
        self.mst_edges = [] 
        self.current_step = 0
        self.dragged_node = None
        self.r = 24 
        
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Button-3>", self.on_right_click)       
        self.canvas.bind("<Double-Button-1>", self.on_double_click) 
        self.canvas.bind("<Configure>", self.on_canvas_resize)
        self.root.bind("<Configure>", self.on_window_resize)

        self.load_from_backend()
        self._simulate_physics()
        self.show_toast(self.t("t_started"), "info")

    # --- YARDIM PENCERESİ (KULLANIM KILAVUZU) ---
    def show_help(self):
        """Ayrı bir pencere açarak seçili dildeki kullanım kılavuzunu gösterir."""
        help_win = ctk.CTkToplevel(self.root)
        help_win.title(self.t("help_title"))
        help_win.geometry("600x450")
        help_win.resizable(False, False)
        
        # Ana pencerenin üzerine odaklansın
        help_win.attributes("-topmost", True)
        
        textbox = ctk.CTkTextbox(help_win, font=("Roboto", 14), wrap="word")
        textbox.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Metni ekle ve yazmayı devre dışı bırak (Read-only)
        textbox.insert("0.0", self.t("help_text"))
        textbox.configure(state="disabled")

    def on_window_resize(self, event):
        if event.widget == self.root:
            current_width = event.width
            if current_width < 950 and self.sidebar_visible:
                self.sidebar.grid_remove()
                self.btn_hamburger.configure(text="☰", fg_color="#34495e", hover_color="#2c3e50")
                self.sidebar_visible = False
            elif current_width >= 950 and not self.sidebar_visible:
                self.sidebar.grid(row=0, column=0, sticky="nsew")
                self.btn_hamburger.configure(text="✕", fg_color="#e74c3c", hover_color="#c0392b")
                self.sidebar_visible = True

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar.grid_remove()
            self.btn_hamburger.configure(text="☰", fg_color="#34495e", hover_color="#2c3e50")
            self.sidebar_visible = False
        else:
            self.sidebar.grid(row=0, column=0, sticky="nsew")
            self.btn_hamburger.configure(text="✕", fg_color="#e74c3c", hover_color="#c0392b")
            self.sidebar_visible = True

    def on_canvas_resize(self, event):
        self.canvas_width = event.width
        self.canvas_height = event.height
        
        if not self.physics_running:
            for u in self.nodes:
                self.coords[u][0] = max(self.r, min(self.canvas_width - self.r, self.coords[u][0]))
                self.coords[u][1] = max(self.r, min(self.canvas_height - self.r, self.coords[u][1]))
            self.update_canvas_positions()

    def t(self, key):
        return self.i18n[self.lang][key]

    def switch_language(self):
        current_algo = self.algo_var.get()
        idx = self.i18n[self.lang]["algos"].index(current_algo)
        
        self.lang = "TR" if self.lang == "EN" else "EN"
        lang_dict = self.i18n[self.lang]
        
        self.root.title(lang_dict["title"])
        self.lbl_w.configure(text=lang_dict["weight"])
        self.btn_add.configure(text=lang_dict["add"])
        self.btn_upd.configure(text=lang_dict["update"])
        self.btn_rem.configure(text=lang_dict["remove"])
        self.chk_dir.configure(text=lang_dict["directed"])
        self.btn_phys.configure(text=lang_dict["physics"])
        self.btn_draw.configure(text=lang_dict["draw_on"] if self.draw_mode else lang_dict["draw_off"])
        self.btn_save.configure(text=lang_dict["save"])
        self.btn_load.configure(text=lang_dict["load"])
        self.btn_lang.configure(text=lang_dict["lang_btn"])
        self.btn_help.configure(text=lang_dict["help_btn"])
        
        self.lbl_algo.configure(text=lang_dict["algo"])
        self.lbl_start.configure(text=lang_dict["start"])
        self.lbl_target.configure(text=lang_dict["target"])
        self.btn_run.configure(text=lang_dict["run"])
        self.btn_mst.configure(text=lang_dict["mst"])
        
        self.combo_algo.configure(values=lang_dict["algos"])
        self.algo_var.set(lang_dict["algos"][idx])

    def show_toast(self, message, level="info"):
        if hasattr(self, 'active_toast') and self.active_toast:
            try: self.active_toast.destroy()
            except: pass

        colors = {"success": "#27ae60", "error": "#c0392b", "warning": "#f39c12", "info": "#2980b9"}
        bg_color = colors.get(level, colors["info"])

        self.active_toast = ctk.CTkFrame(self.canvas_frame, fg_color=bg_color, corner_radius=15)
        self.active_toast.place(relx=0.5, rely=0.92, anchor="center")
        
        lbl = ctk.CTkLabel(self.active_toast, text=message, text_color="white", font=("Roboto", 14, "bold"))
        lbl.pack(padx=30, pady=12)

        self.root.after(3500, self.active_toast.destroy)

    def _parse_val(self, val):
        val = str(val).strip()
        try: return int(val)
        except ValueError: return val.upper()

    def toggle_draw_mode(self):
        self.draw_mode = not self.draw_mode
        if self.draw_mode:
            self.btn_draw.configure(text=self.t("draw_on"))
            self.show_toast(self.t("t_draw_on"), "warning")
        else:
            self.btn_draw.configure(text=self.t("draw_off"))
            self.selected_draw_node = None
            self.load_from_backend() 
            self.show_toast(self.t("t_draw_off"), "info")

    def toggle_directed(self):
        self.backend_graph.is_directed = self.is_dir_var.get()
        self.load_from_backend()
        durum = self.t("t_dir_true") if self.backend_graph.is_directed else self.t("t_dir_false")
        self.show_toast(f"{self.t('t_dir_upd')} {durum}", "info")
        
    def toggle_physics(self):
        self.physics_running = not self.physics_running
        if self.physics_running:
            self._simulate_physics()

    def export_graph_json(self):
        is_dir = getattr(self.backend_graph, 'is_directed', False)
        export_data = {"is_directed": is_dir, "coords": self.coords, "edges": []}
        for (u, v) in self.edges:
            weight = self.edge_weights.get((u, v), 1)
            export_data["edges"].append({"u": u, "v": v, "w": weight})
            
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=4)
            self.show_toast(self.t("t_saved"), "success")

    def import_graph_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    import_data = json.load(f)
                    is_dir = import_data.get("is_directed", False)
                    self.backend_graph = graph.Graph(is_directed=is_dir)
                    
                    if is_dir: self.chk_dir.select()
                    else: self.chk_dir.deselect()
                    
                    for edge in import_data.get("edges", []):
                        self.backend_graph.add_edge(edge["u"], edge["v"], weight=edge.get("w", 1))
                        
                    self.load_from_backend()
                    
                    saved_coords = import_data.get("coords", {})
                    for node, coords in saved_coords.items():
                        parsed_node = self._parse_val(node)
                        if parsed_node in self.coords:
                            self.coords[parsed_node] = coords
                            
                    self.update_canvas_positions()
                    self.show_toast(self.t("t_loaded"), "success")
                except Exception:
                    self.show_toast(self.t("t_err_corrupt"), "error")

    def load_from_backend(self):
        self.canvas.delete("all")
        self.node_ovals.clear()
        self.node_texts.clear()
        self.edge_lines.clear()
        self.edge_texts.clear()
        self.edge_weights.clear()
        
        adjacency_elements = self.backend_graph.adj.get_elements()
        unique_nodes = set()
        self.edges = []
        
        for u, neighbors in adjacency_elements:
            unique_nodes.add(u) 
            for v, w in neighbors:
                unique_nodes.add(v)
                if self.backend_graph.is_directed:
                    edge_tuple = (u, v)
                else:
                    edge_tuple = tuple(sorted((u, v), key=str))
                    
                if edge_tuple not in self.edges:
                    self.edges.append(edge_tuple)
                self.edge_weights[edge_tuple] = w
                
        self.nodes = list(unique_nodes)
        for node in self.nodes:
            if node not in self.coords:
                x = random.randint(100, max(200, self.canvas_width - 100))
                y = random.randint(100, max(200, self.canvas_height - 100))
                self.coords[node] = [x, y, 0.0, 0.0]

        for u, v in self.edges:
            self.edge_lines[(u, v)] = self.canvas.create_line(0, 0, 0, 0, fill="#7f8fa6", width=3, smooth=True)
            w = self.edge_weights.get((u, v), "")
            self.edge_texts[(u, v)] = self.canvas.create_text(0, 0, text=str(w), fill="#ecf0f1", font=("Roboto", 13, "bold"))
            
        for node in self.nodes:
            outline_color = "#f1c40f" if self.draw_mode and node == self.selected_draw_node else "#00a8ff"
            outline_width = 5 if self.draw_mode and node == self.selected_draw_node else 0
            
            self.node_ovals[node] = self.canvas.create_oval(0, 0, 0, 0, fill="#0097e6", outline=outline_color, width=outline_width)
            self.node_texts[node] = self.canvas.create_text(0, 0, text=str(node), font=("Consolas", 15, "bold"), fill="white")

        self.update_canvas_positions()

    def add_new_edge(self):
        u_val, v_val, w_val = self.entry_u.get(), self.entry_v.get(), self.entry_w.get()
        if not u_val or not v_val: 
            self.show_toast(self.t("t_err_empty"), "error")
            return
        u, v = self._parse_val(u_val), self._parse_val(v_val)
        try: w = int(w_val)
        except: w = 1 
        self.backend_graph.add_edge(u, v, weight=w)
        self.load_from_backend()
        self.entry_u.delete(0, tk.END)
        self.entry_v.delete(0, tk.END)
        self.show_toast(f"{self.t('t_added')} {u} -> {v}", "success")

    def update_existing_edge(self):
        u_val, v_val, w_val = self.entry_u.get(), self.entry_v.get(), self.entry_w.get()
        if not u_val or not v_val: return
        u, v = self._parse_val(u_val), self._parse_val(v_val)
        try: w = int(w_val)
        except: w = 1 
        
        is_dir = getattr(self.backend_graph, 'is_directed', False)
        edge_key = (u, v) if is_dir else tuple(sorted((u, v), key=str))
        
        if edge_key in self.edges:
            self.backend_graph.add_edge(u, v, weight=w) 
            self.load_from_backend()
            self.show_toast(f"{self.t('t_updated')} {u} -> {v}", "success")
        else:
            self.show_toast(self.t("t_err_noconn"), "error")
            
        self.entry_u.delete(0, tk.END)
        self.entry_v.delete(0, tk.END)

    def remove_existing_edge(self):
        u_val, v_val = self.entry_u.get(), self.entry_v.get()
        if not u_val or not v_val: return
        u, v = self._parse_val(u_val), self._parse_val(v_val)
        self.backend_graph.remove_edge(u, v)
        self.load_from_backend()
        self.entry_u.delete(0, tk.END)
        self.entry_v.delete(0, tk.END)
        self.show_toast(f"{self.t('t_removed')} {u} - {v}", "warning")

    def convert_to_mst(self):
        if not self.mst_edges: return
        self.backend_graph = graph.Graph(is_directed=False)
        self.is_dir_var.set(False)
        self.chk_dir.deselect() 
        for u, v, w in self.mst_edges:
            self.backend_graph.add_edge(u, v, weight=w)
            
        self.path = []
        self.mst_edges = []
        self.btn_mst.configure(state="disabled") 
        self.load_from_backend() 
        self.show_toast(self.t("t_mst_conv"), "success")

    def start_simulation(self):
        start_node = self._parse_val(self.entry_start.get())
        target_node = self._parse_val(self.entry_target.get())
        current_algo_str = self.algo_var.get()
        
        algo_idx = self.i18n[self.lang]["algos"].index(current_algo_str)
        
        for node in self.nodes:
            self.canvas.itemconfig(self.node_ovals[node], fill="#0097e6", outline="")
        for edge in self.edges:
            self.canvas.itemconfig(self.edge_lines[edge], fill="#7f8fa6", width=3)
            
        self.path = []
        self.mst_edges = []
        self.btn_mst.configure(state="disabled") 
        
        if algo_idx not in [4, 5] and start_node not in self.nodes:
            self.show_toast(self.t("t_err_start"), "error")
            return
            
        self.show_toast(f"{self.t('t_calc')} {current_algo_str}", "info")
        self.root.update() 
            
        if algo_idx == 0: 
            self.path = self.backend_graph.bfs(start_node)
        elif algo_idx == 1: 
            self.path = self.backend_graph.dfs(start_node)
        elif algo_idx == 2: 
            if target_node in self.nodes:
                self.path, cost = self.backend_graph.dijkstra(start_node, target_node)
                self.show_toast(f"Dijkstra {self.t('t_cost')} {cost}", "success")
            else: self.show_toast(self.t("t_err_target"), "error")
        elif algo_idx == 3: 
            if target_node in self.nodes:
                heuristics = {}
                tx, ty = self.coords[target_node][0], self.coords[target_node][1]
                for n in self.nodes:
                    heuristics[n] = math.hypot(tx - self.coords[n][0], ty - self.coords[n][1]) / 20.0 
                self.path, cost = self.backend_graph.a_star(start_node, target_node, heuristics=heuristics)
                self.show_toast(f"A* {self.t('t_cost')} {cost}", "success")
            else: self.show_toast(self.t("t_err_target"), "error")
        elif algo_idx == 4: 
            self.mst_edges, cost = self.backend_graph.prim(start_node)
            self.show_toast(f"Prim {self.t('t_cost')} {cost}", "success")
        elif algo_idx == 5: 
            self.mst_edges, cost = self.backend_graph.kruskal()
            self.show_toast(f"Kruskal {self.t('t_cost')} {cost}", "success")
        elif algo_idx == 6: 
            self.path, cost = self.backend_graph.tsp_nearest_neighbor(start_node)
            self.show_toast(f"TSP {self.t('t_dist')} {cost}", "success")
        elif algo_idx == 7: 
            self.path, cost = self.backend_graph.tsp_brute_force(start_node)
            self.show_toast(f"TSP {self.t('t_dist')} {cost}", "success")
        elif algo_idx == 8: 
            if target_node in self.nodes:
                max_flow, flows = self.backend_graph.ford_fulkerson(start_node, target_node)
                self.show_toast(f"{self.t('t_flow')} {max_flow}", "success")
                for (u, v) in self.edges:
                    cap = self.edge_weights.get((u, v), 1)
                    f1 = flows.get((u, v), 0); f2 = flows.get((v, u), 0)
                    flow = max(0, max(f1, f2))
                    text_id = self.edge_texts.get((u, v)); line_id = self.edge_lines.get((u, v))
                    if text_id: self.canvas.itemconfig(text_id, text=f"{flow} / {cap}", fill="#f1c40f")
                    if line_id:
                        if flow == 0: self.canvas.itemconfig(line_id, fill="#7f8fa6", width=3)
                        elif flow > 0 and flow < cap: self.canvas.itemconfig(line_id, fill="#3498db", width=5)
                        elif flow == cap: self.canvas.itemconfig(line_id, fill="#e74c3c", width=6)
            else: self.show_toast(self.t("t_err_target"), "error")
        
        self.current_step = 0
        if self.path or self.mst_edges:
            self._animate_step()

    def _simulate_physics(self):
        if not self.physics_running: return

        for u in self.nodes:
            for v in self.nodes:
                if u != v:
                    dx, dy = self.coords[u][0] - self.coords[v][0], self.coords[u][1] - self.coords[v][1]
                    dist = math.hypot(dx, dy) or 0.1
                    if dist < 300: 
                        force = 1500 / (dist * dist)
                        self.coords[u][2] += (dx / dist) * force; self.coords[u][3] += (dy / dist) * force

        for u, v in self.edges:
            dx, dy = self.coords[v][0] - self.coords[u][0], self.coords[v][1] - self.coords[u][1]
            dist = math.hypot(dx, dy) or 0.1
            force = 0.05 * (dist - 120) 
            self.coords[u][2] += (dx / dist) * force; self.coords[u][3] += (dy / dist) * force
            self.coords[v][2] -= (dx / dist) * force; self.coords[v][3] -= (dy / dist) * force

        for u in self.nodes:
            if u == self.dragged_node: continue 
            self.coords[u][2] *= 0.70; self.coords[u][3] *= 0.70
            self.coords[u][0] += self.coords[u][2]; self.coords[u][1] += self.coords[u][3]
            self.coords[u][0] = max(self.r, min(self.canvas_width - self.r, self.coords[u][0]))
            self.coords[u][1] = max(self.r, min(self.canvas_height - self.r, self.coords[u][1]))

        self.update_canvas_positions()
        self.root.after(16, self._simulate_physics)

    def update_canvas_positions(self):
        is_dir = getattr(self.backend_graph, 'is_directed', False)
        
        for u, v in self.edges:
            x1, y1 = self.coords[u][0], self.coords[u][1]
            x2, y2 = self.coords[v][0], self.coords[v][1]
            line_id = self.edge_lines[(u, v)]
            text_id = self.edge_texts[(u, v)]
            
            is_bidirectional = is_dir and (v, u) in self.edges
            
            if is_bidirectional:
                dx, dy = x2 - x1, y2 - y1
                dist = math.hypot(dx, dy) or 0.1
                nx, ny = -dy / dist, dx / dist
                offset = 45 
                cx, cy = (x1 + x2) / 2 + nx * offset, (y1 + y2) / 2 + ny * offset
                
                if dist > self.r:
                    ratio = (dist - self.r - 2) / dist
                    x2_arr = x1 + dx * ratio
                    y2_arr = y1 + dy * ratio
                else:
                    x2_arr, y2_arr = x2, y2

                self.canvas.coords(line_id, x1, y1, cx, cy, x2_arr, y2_arr)
                self.canvas.coords(text_id, cx, cy) 
                
            else:
                if is_dir:
                    dx, dy = x2 - x1, y2 - y1
                    dist = math.hypot(dx, dy) or 0.1
                    if dist > self.r:
                        x2 = x2 - (dx / dist) * (self.r + 2)
                        y2 = y2 - (dy / dist) * (self.r + 2)
                
                self.canvas.coords(line_id, x1, y1, x2, y2)
                self.canvas.coords(text_id, (x1 + x2) / 2, (y1 + y2) / 2 - 12)

            if is_dir:
                self.canvas.itemconfig(line_id, arrow=tk.LAST, arrowshape=(16, 20, 6))
            else:
                self.canvas.itemconfig(line_id, arrow="")
            
        for node in self.nodes:
            x, y = self.coords[node][0], self.coords[node][1]
            self.canvas.coords(self.node_ovals[node], x-self.r, y-self.r, x+self.r, y+self.r)
            self.canvas.coords(self.node_texts[node], x, y)

    def on_right_click(self, event):
        if not self.draw_mode: return
        for node in self.nodes:
            if math.hypot(event.x - self.coords[node][0], event.y - self.coords[node][1]) <= self.r:
                if hasattr(self.backend_graph, 'remove_node'):
                    self.backend_graph.remove_node(node)
                    if node in self.coords: del self.coords[node]
                    if self.selected_draw_node == node: self.selected_draw_node = None
                    self.load_from_backend()
                    self.show_toast(f"{self.t('t_removed')}{node}", "info")
                break

    def on_double_click(self, event):
        if not self.draw_mode: return
        for node in self.nodes:
            if math.hypot(event.x - self.coords[node][0], event.y - self.coords[node][1]) <= self.r:
                dialog_title = "Rename" if self.lang == "EN" else "Yeniden Adlandır"
                dialog_msg = f"New name for '{node}':" if self.lang == "EN" else f"'{node}' için yeni isim:"
                
                dialog = ctk.CTkInputDialog(text=dialog_msg, title=dialog_title)
                new_name_raw = dialog.get_input()
                
                if new_name_raw:
                    new_name = self._parse_val(new_name_raw)
                    if new_name in self.nodes and new_name != node:
                        self.show_toast(self.t("t_err_rename"), "error")
                    else:
                        if hasattr(self.backend_graph, 'rename_node'):
                            self.backend_graph.rename_node(node, new_name)
                            if node in self.coords: self.coords[new_name] = self.coords.pop(node)
                            if self.selected_draw_node == node: self.selected_draw_node = new_name
                            self.load_from_backend()
                            self.show_toast(f"{self.t('t_updated')} {node} -> {new_name}", "success")
                break

    def on_press(self, event):
        clicked_node = None
        for node in self.nodes:
            if math.hypot(event.x - self.coords[node][0], event.y - self.coords[node][1]) <= self.r:
                clicked_node = node
                break

        if self.draw_mode:
            if clicked_node is not None:
                if self.selected_draw_node is None:
                    self.selected_draw_node = clicked_node
                    self.load_from_backend() 
                elif self.selected_draw_node == clicked_node:
                    self.selected_draw_node = None
                    self.load_from_backend()
                else:
                    u = self.selected_draw_node
                    v = clicked_node
                    try: w = int(self.entry_w.get())
                    except: w = 1
                    
                    self.backend_graph.add_edge(u, v, weight=w)
                    self.selected_draw_node = None
                    self.load_from_backend()
                    self.show_toast(f"{self.t('t_added')} {u} -> {v}", "success")
            else:
                custom_u = self.entry_u.get().strip()
                if custom_u and self._parse_val(custom_u) not in self.nodes:
                    new_node = self._parse_val(custom_u)
                    self.entry_u.delete(0, tk.END) 
                else:
                    new_node = self._parse_val(str(self.next_node_id))
                    while new_node in self.nodes:
                        self.next_node_id += 1
                        new_node = self._parse_val(str(self.next_node_id))
                        
                if hasattr(self.backend_graph, 'add_node'):
                    self.backend_graph.add_node(new_node)
                else:
                    if self.backend_graph.adj.get(new_node) is None:
                        self.backend_graph.adj.add(new_node, [])
                        
                self.coords[new_node] = [event.x, event.y, 0.0, 0.0]
                self.load_from_backend()
                
        else:
            if clicked_node is not None:
                self.dragged_node = clicked_node
                self.coords[clicked_node][2] = 0
                self.coords[clicked_node][3] = 0

    def on_drag(self, event):
        if not self.draw_mode and self.dragged_node is not None:
            self.coords[self.dragged_node][0], self.coords[self.dragged_node][1] = event.x, event.y
            self.update_canvas_positions()

    def on_release(self, event):
        self.dragged_node = None

    def _animate_step(self):
        if self.path and self.current_step < len(self.path):
            active_node = self.path[self.current_step]
            self.canvas.itemconfig(self.node_ovals[active_node], fill="#ff9f43", outline="#ee5253", width=3) 
            
            if self.current_step > 0:
                prev_node = self.path[self.current_step - 1]
                is_dir = getattr(self.backend_graph, 'is_directed', False)
                edge_key = (prev_node, active_node) if is_dir else tuple(sorted((prev_node, active_node), key=str))
                
                if edge_key not in self.edge_lines and not is_dir:
                    edge_key = tuple(sorted((active_node, prev_node), key=str))

                if edge_key in self.edge_lines:
                    self.canvas.itemconfig(self.edge_lines[edge_key], fill="#ff9f43", width=5)
            
            self.current_step += 1
            self.root.after(800, self._animate_step)
            
        elif self.mst_edges and self.current_step < len(self.mst_edges):
            u, v, w = self.mst_edges[self.current_step]
            edge_key = (u, v) if (u, v) in self.edges else (v, u)
            
            if edge_key in self.edge_lines:
                self.canvas.itemconfig(self.edge_lines[edge_key], fill="#fbc531", width=5) 
                self.canvas.itemconfig(self.node_ovals[u], fill="#ff9f43", outline="#ee5253", width=3)
                self.canvas.itemconfig(self.node_ovals[v], fill="#ff9f43", outline="#ee5253", width=3)
                
            self.current_step += 1
            self.root.after(800, self._animate_step)
            
        else:
            if self.mst_edges:
                self.btn_mst.configure(state="normal")

    def render(self):
        self.root.mainloop()