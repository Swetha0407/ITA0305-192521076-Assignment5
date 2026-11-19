"""
Heritage Trails — Python prototype (Tkinter + SQLite)
Run: python3 app.py
This is a desktop prototype for workflow/state validation, not a native mobile app.
"""
import sqlite3, tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from time import perf_counter

DB = Path(__file__).with_name("heritage_trails.db")
SEED = [
    ("fort", "Old Fort", "Historic fort", "English", "Explore ramparts and courtyards."),
    ("museum", "Maritime Museum", "Museum", "English", "Stories of trade and navigation."),
    ("tower", "Clock Tower", "Landmark", "English", "A central landmark in the old quarter."),
]
class Repository:
    def __init__(self, path=DB):
        self.db = sqlite3.connect(path)
        self.db.execute("""CREATE TABLE IF NOT EXISTS monuments(
            id TEXT PRIMARY KEY, name TEXT, category TEXT, language TEXT, description TEXT)""")
        self.db.execute("""CREATE TABLE IF NOT EXISTS preferences(
            key TEXT PRIMARY KEY, value TEXT)""")
        if self.db.execute("SELECT COUNT(*) FROM monuments").fetchone()[0] == 0:
            self.db.executemany("INSERT INTO monuments VALUES(?,?,?,?,?)", SEED)
        self.db.commit()
    def all(self, query=""):
        if query:
            return self.db.execute("SELECT * FROM monuments WHERE name LIKE ? ORDER BY name",
                                   (f"%{query}%",)).fetchall()
        return self.db.execute("SELECT * FROM monuments ORDER BY name").fetchall()
    def get(self, mid):
        return self.db.execute("SELECT * FROM monuments WHERE id=?", (mid,)).fetchone()
    def close(self): self.db.close()

class GuideApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Heritage Trails — Visitor Guide")
        self.geometry("900x650"); self.minsize(720,560)
        self.repo = Repository(); self.online = True; self.location_allowed = False
        self.container = ttk.Frame(self, padding=18); self.container.pack(fill="both",expand=True)
        self.status = tk.StringVar(value="ONLINE · Content available")
        ttk.Label(self.container,textvariable=self.status,foreground="#216b69").pack(anchor="e")
        self.body = ttk.Frame(self.container); self.body.pack(fill="both",expand=True)
        self.show_home()
        self.protocol("WM_DELETE_WINDOW", self.close)
    def clear(self):
        for w in self.body.winfo_children(): w.destroy()
    def heading(self,title,subtitle):
        ttk.Label(self.body,text=title,font=("Arial",22,"bold")).pack(anchor="w",pady=(12,4))
        ttk.Label(self.body,text=subtitle,wraplength=760).pack(anchor="w",pady=(0,16))
    def nav(self):
        row=ttk.Frame(self.body); row.pack(side="bottom",fill="x",pady=12)
        for label,fn in [("Home",self.show_home),("Explore",self.show_list),
                         ("Preferences",self.show_preferences)]:
            ttk.Button(row,text=label,command=fn).pack(side="left",padx=5)
        ttk.Button(row,text=("Go Offline" if self.online else "Reconnect"),
                   command=self.toggle_network).pack(side="right",padx=5)
    def show_home(self):
        self.clear(); self.heading("Discover the old city","Walking routes, monument stories and e-tickets.")
        ttk.Label(self.body,text="Featured route: Old Fort Heritage Walk · 2.4 km · 70 min").pack(anchor="w",pady=10)
        ttk.Button(self.body,text="Explore monuments",command=self.show_list).pack(anchor="w",pady=6)
        ttk.Button(self.body,text="Language & preferences",command=self.show_preferences).pack(anchor="w",pady=6)
        self.nav()
    def show_list(self):
        start=perf_counter(); self.clear(); self.heading("Explore monuments","Search the locally cached monument catalogue.")
        q=tk.StringVar(); entry=ttk.Entry(self.body,textvariable=q,width=45); entry.pack(anchor="w")
        results=ttk.Frame(self.body); results.pack(fill="both",expand=True,pady=10)
        def render():
            t0=perf_counter()
            for w in results.winfo_children(): w.destroy()
            rows=self.repo.all(q.get())
            if not rows: ttk.Label(results,text="No monuments match this search.").pack(anchor="w")
            for row in rows:
                line=ttk.Frame(results,padding=8); line.pack(fill="x",pady=3)
                ttk.Label(line,text=row[1],font=("Arial",12,"bold")).pack(side="left")
                ttk.Button(line,text="Details",command=lambda mid=row[0]:self.show_detail(mid)).pack(side="right")
            self.last_render_ms=(perf_counter()-t0)*1000
        ttk.Button(self.body,text="Search",command=render).pack(anchor="w",pady=5)
        render(); self.last_transition_ms=(perf_counter()-start)*1000
        self.nav()
    def show_detail(self,mid):
        row=self.repo.get(mid); self.clear(); self.heading(row[1],row[2])
        ttk.Label(self.body,text=row[4],wraplength=740).pack(anchor="w",pady=10)
        ttk.Label(self.body,text=("Cached content available offline" if not self.online else "Content current")).pack(anchor="w")
        ttk.Button(self.body,text="Play narration (demo)",command=lambda:messagebox.showinfo("Media","Narration state: READY (demo)")).pack(anchor="w",pady=5)
        ttk.Button(self.body,text="E-ticket (demo)",command=lambda:messagebox.showinfo("Ticket","Checkout is delegated to a secure provider in production.")).pack(anchor="w",pady=5)
        self.nav()
    def show_preferences(self):
        self.clear(); self.heading("Language & preferences","Permission-aware controls; location is optional.")
        ttk.Label(self.body,text="Display language").pack(anchor="w")
        lang=ttk.Combobox(self.body,values=["English","Tamil","Hindi","French","Spanish"],state="readonly")
        lang.set("English"); lang.pack(anchor="w",pady=5)
        loc=tk.BooleanVar(value=self.location_allowed)
        ttk.Checkbutton(self.body,text="Allow nearby-attraction alerts (simulated permission)",variable=loc).pack(anchor="w",pady=8)
        def save():
            self.location_allowed=loc.get()
            self.status.set("Location enabled" if loc.get() else "Manual browsing · Location not granted")
            messagebox.showinfo("Preferences","Preferences saved.")
        ttk.Button(self.body,text="Save preferences",command=save).pack(anchor="w",pady=8)
        self.nav()
    def toggle_network(self):
        self.online=not self.online
        self.status.set("ONLINE · Sync available" if self.online else "OFFLINE · Local cache active")
        if self.winfo_exists(): self.update_idletasks()
    def close(self):
        self.repo.close(); self.destroy()

if __name__ == "__main__":
    GuideApp().mainloop()
