import sys
import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, Pango

class ZeroWasm(Gtk.Window):
    def __init__(self):
        super().__init__(title="Zero Wasm - Ultimate Studio")
        self.set_default_size(1100, 750)
        
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.header.props.title = ""
        self.header.get_style_context().add_class("hidden-header")
        self.set_titlebar(self.header)
        
        self.setup_css()
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.add(main_box)
        
        # ================= SIDEBAR =================
        self.sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.sidebar.set_size_request(280, -1)
        self.sidebar.get_style_context().add_class("sidebar")
        main_box.pack_start(self.sidebar, False, False, 0)
        
        logo = Gtk.Label(label="Z E R O W A S M")
        logo.get_style_context().add_class("sidebar-logo")
        logo.set_margin_top(20)
        logo.set_margin_bottom(20)
        self.sidebar.pack_start(logo, False, False, 0)
        
        btn_deploy = Gtk.Button(label="🚀 Deploy Module")
        btn_deploy.get_style_context().add_class("action-btn")
        self.sidebar.pack_start(btn_deploy, False, False, 10)
        
        lbl_mods = Gtk.Label(label="RUNNING MODULES")
        lbl_mods.get_style_context().add_class("section-label")
        lbl_mods.set_halign(Gtk.Align.START)
        lbl_mods.set_margin_start(20)
        lbl_mods.set_margin_top(15)
        self.sidebar.pack_start(lbl_mods, False, False, 10)
        
        modules = [
            ("Video Encoder", "🟢 14MB"),
            ("Rust Physics Engine", "🟢 2.3MB"),
            ("Data Parser", "🟢 0.8MB"),
            ("Crypto Miner", "🔴 Stopped")
        ]
        
        for name, mem in modules:
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            box.set_margin_start(20)
            box.set_margin_end(20)
            box.set_margin_bottom(12)
            
            ln = Gtk.Label(label=name)
            ln.get_style_context().add_class("mod-name")
            lp = Gtk.Label(label=mem)
            lp.get_style_context().add_class("mod-mem")
            
            box.pack_start(ln, True, True, 0)
            box.pack_end(lp, False, False, 0)
            self.sidebar.pack_start(box, False, False, 0)
            
        # ================= WORKSPACE =================
        self.workspace = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.workspace.get_style_context().add_class("workspace")
        main_box.pack_start(self.workspace, True, True, 0)
        
        top_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        top_bar.set_margin_start(30)
        top_bar.set_margin_end(30)
        top_bar.set_margin_top(20)
        
        title = Gtk.Label(label="Runtime Telemetry")
        title.get_style_context().add_class("dash-title")
        top_bar.pack_start(title, False, False, 0)
        self.workspace.pack_start(top_bar, False, False, 20)
        
        grid = Gtk.Grid(column_spacing=20, row_spacing=20)
        grid.set_margin_start(30)
        grid.set_margin_end(30)
        self.workspace.pack_start(grid, False, False, 0)
        
        grid.attach(self.make_stat_card("CPU Usage", "4.2%"), 0, 0, 1, 1)
        grid.attach(self.make_stat_card("Memory Allocation", "17.1 MB"), 1, 0, 1, 1)
        
        # Terminal Console
        console_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        console_box.get_style_context().add_class("console-box")
        console_box.set_margin_start(30)
        console_box.set_margin_end(30)
        console_box.set_margin_top(20)
        console_box.set_margin_bottom(30)
        
        c_title = Gtk.Label(label="WASM VM LOGS")
        c_title.get_style_context().add_class("console-title")
        c_title.set_halign(Gtk.Align.START)
        c_title.set_margin_start(20)
        c_title.set_margin_top(15)
        
        c_text = Gtk.TextView()
        c_text.get_style_context().add_class("console-text")
        c_text.set_margin_start(20)
        c_text.set_margin_end(20)
        c_text.set_margin_top(10)
        c_text.set_margin_bottom(20)
        c_text.set_editable(False)
        c_text.get_buffer().set_text(
            "[INFO] Initializing WebAssembly V8 Engine... OK\n"
            "[INFO] Sandbox memory allocated: 1024 MB\n"
            "[INFO] Module 'Video Encoder' loaded successfully.\n"
            "[WARN] 'Crypto Miner' hit execution timeout, aborting thread.\n"
            "[INFO] Waiting for RPC calls..."
        )
        
        console_box.pack_start(c_title, False, False, 0)
        console_box.pack_start(c_text, True, True, 0)
        self.workspace.pack_start(console_box, True, True, 0)
        
    def make_stat_card(self, title, val):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.get_style_context().add_class("stat-card")
        box.set_size_request(380, 150)
        
        lt = Gtk.Label(label=title)
        lt.get_style_context().add_class("stat-title")
        lt.set_margin_top(20)
        
        lv = Gtk.Label(label=val)
        lv.get_style_context().add_class("stat-val")
        lv.set_margin_top(15)
        
        box.pack_start(lt, False, False, 0)
        box.pack_start(lv, False, False, 0)
        return box
        
    def setup_css(self):
        css = b'''
            window { background-color: #030305; }
            .hidden-header { background: #030305; min-height: 0px; padding: 0px; border: none; box-shadow: none; }
            .sidebar { background-color: rgba(6, 8, 12, 0.98); border-right: 1px solid rgba(255, 255, 255, 0.05); }
            .sidebar-logo { color: #FFFFFF; font-size: 22px; font-weight: 900; letter-spacing: 5px; text-shadow: 0 0 15px rgba(255, 51, 0, 0.6); }
            .action-btn { background: linear-gradient(45deg, #FF3300, #FF6600); color: #FFFFFF; border-radius: 12px; font-weight: bold; padding: 15px; margin: 0 20px; border: none; box-shadow: 0 5px 20px rgba(255, 51, 0, 0.3); transition: all 0.3s; }
            .action-btn:hover { box-shadow: 0 8px 30px rgba(255, 51, 0, 0.5); transform: scale(1.02); }
            .section-label { color: #4A5568; font-size: 11px; font-weight: 900; letter-spacing: 2px; }
            .mod-name { color: #FFFFFF; font-weight: bold; font-size: 14px; }
            .mod-mem { color: #8B94A5; font-size: 14px; }
            .workspace { background: radial-gradient(circle at bottom, #1A0A0A, #030305); }
            .dash-title { color: #FFFFFF; font-size: 32px; font-weight: bold; }
            .stat-card { background: rgba(255,255,255,0.02); border: 1px solid rgba(255, 51, 0, 0.2); border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); transition: all 0.3s ease; }
            .stat-card:hover { border: 1px solid #FF3300; box-shadow: 0 15px 40px rgba(255, 51, 0, 0.2); transform: translateY(-3px); }
            .stat-title { color: #8B94A5; font-size: 16px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }
            .stat-val { color: #FF3300; font-size: 48px; font-weight: 200; text-shadow: 0 0 20px rgba(255, 51, 0, 0.4); }
            .console-box { background: rgba(0,0,0,0.8); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; }
            .console-title { color: #4A5568; font-size: 12px; font-weight: bold; letter-spacing: 2px; }
            .console-text { background: transparent; color: #FF6600; font-family: monospace; font-size: 14px; line-height: 1.5; }
            .console-text text { background: transparent; }
        '''
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

if __name__ == "__main__":
    win = ZeroWasm()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
