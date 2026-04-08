import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
from repositorio import Repositorio

# ── Paleta F1
F1_RED      = "#E21A00"
F1_DARK_RED = "#E21A00"
F1_BLACK    = "#111111"
F1_WHITE    = "#F5F5F5"
F1_GRAY     = "#3B3939"
F1_SILVER   = "#A4A4A4"
F1_ACCENT   = "#FFD700"


class F1App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.repo = Repositorio()

        self.title("🏎  F1 Manager — Pilotos")
        self.geometry("900x580")
        """self.resizable(False, False)"""
        self.configure(bg=F1_BLACK)

        self._build_title_bar()
        self._build_body()
        self._refresh_table()

    # ── Barra de título
    def _build_title_bar(self):
        bar = tk.Frame(self, bg=F1_RED, height=54)
        bar.pack(fill="x", side="top")
        bar.pack_propagate(False)

        stripe_frame = tk.Frame(bar, bg=F1_RED)
        stripe_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        for i in range(12):
            c = F1_RED if i % 2 == 0 else F1_BLACK
            tk.Frame(stripe_frame, bg=c, width=18).pack(side="left", fill="y")

        overlay = tk.Frame(bar, bg=F1_RED, bd=0)
        overlay.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.8)

        tk.Label(
            overlay, text="⚑  F1 MANAGER",
            font=("Impact", 22, "bold"),
            fg=F1_WHITE, bg=F1_RED, padx=12
        ).pack(side="left")

        tk.Label(
            overlay, text="FORMULA 1  ●  PILOTOS",
            font=("Courier New", 10, "bold"),
            fg=F1_ACCENT, bg=F1_RED
        ).pack(side="left", padx=8)

    # ── painel principal
    def _build_body(self):
        body = tk.Frame(self, bg=F1_RED, padx=6, pady=6)
        body.pack(fill="both", expand=True)

        self._build_sidebar(body)
        self._build_main_panel(body)
        self._build_right_panel(body)

    # ── barra esquerda
    def _build_sidebar(self, parent):
        side = tk.Frame(parent, bg=F1_BLACK, width=160, padx=8, pady=10)
        side.pack(side="left", fill="y", padx=(0, 6))
        side.pack_propagate(False)

        tk.Label(
            side, text="AÇÕES", font=("Impact", 13),
            fg=F1_ACCENT, bg=F1_BLACK
        ).pack(pady=(0, 10))

        actions = [
            ("CADASTRO",    self._on_cadastro),
            ("ATUALIZAR",   self._on_atualizar),
            ("REMOVER",     self._on_remover),
            ("LISTAR",      self._on_listar),
            ("ORDENAR",     self._on_ordenar),
            ("IMPORTAR API",self._on_importar_api),
        ]
        for label, cmd in actions:
            self._make_btn(side, label, cmd)

    def _make_btn(self, parent, text, cmd, accent=False):
        bg  = F1_ACCENT if accent else F1_RED
        fg  = F1_BLACK  if accent else F1_WHITE
        btn = tk.Button(
            parent, text=text, command=cmd,
            font=("Impact", 12),
            bg=bg, fg=fg, activebackground=F1_DARK_RED,
            activeforeground=F1_WHITE,
            relief="flat", bd=0, cursor="hand2",
            width=14, height=2
        )
        btn.pack(pady=4, fill="x")
        btn.bind("<Enter>", lambda e, b=btn, a=accent: b.config(
            bg=F1_ACCENT if not a else F1_WHITE))
        btn.bind("<Leave>", lambda e, b=btn, a=accent: b.config(bg=bg))
        return btn

    # ── Painel central
    def _build_main_panel(self, parent):
        main = tk.Frame(parent, bg=F1_GRAY, padx=2, pady=2)
        main.pack(side="left", fill="both", expand=True)

        header = tk.Frame(main, bg=F1_BLACK, height=32)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header, text="  🏁  LISTA DE PILOTOS",
            font=("Courier New", 11, "bold"),
            fg=F1_WHITE, bg=F1_BLACK
        ).pack(side="left", padx=6, pady=4)

        search_frame = tk.Frame(main, bg=F1_SILVER, pady=4)
        search_frame.pack(fill="x")

        tk.Label(
            search_frame, text="🔍 Buscar:",
            font=("Courier New", 10), bg=F1_SILVER, fg=F1_BLACK
        ).pack(side="left", padx=8)

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._filter_table)
        entry = tk.Entry(
            search_frame, textvariable=self.search_var,
            font=("Courier New", 10), relief="flat",
            bg=F1_WHITE, fg=F1_BLACK, insertbackground=F1_RED,
            width=28
        )
        entry.pack(side="left", ipady=4, padx=4)

        # Colunas alinhadas com repositório: numero, nome, sigla, equipe, pontos
        cols = ("Nº", "Piloto", "Sigla", "Equipe", "Pontos")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("F1.Treeview",
            background=F1_SILVER, fieldbackground=F1_SILVER,
            foreground=F1_BLACK, rowheight=28,
            font=("Courier New", 10)
        )
        style.configure("F1.Treeview.Heading",
            background=F1_RED, foreground=F1_WHITE,
            font=("Impact", 11), relief="flat"
        )
        style.map("F1.Treeview",
            background=[("selected", F1_RED)],
            foreground=[("selected", F1_WHITE)]
        )

        tree_frame = tk.Frame(main, bg=F1_GRAY)
        tree_frame.pack(fill="both", expand=True, padx=2, pady=2)

        self.tree = ttk.Treeview(
            tree_frame, columns=cols, show="headings",
            style="F1.Treeview"
        )
        widths = {"Nº": 55, "Piloto": 160, "Sigla": 70, "Equipe": 150, "Pontos": 70}
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=widths[c], anchor="center")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self._all_rows = []

    def _refresh_table(self):
        """Busca dados do banco e atualiza _all_rows + tabela."""
        motoristas = self.repo.listar_motoristas()
       
        # repositório retorna: (numero_carro, nome, sigla, time, pontos)
        self._all_rows = [
            (str(m[0]), m[1], m[2], m[3], str(m[4]))
            for m in motoristas
        ]
        self._populate(self._all_rows)

    def _populate(self, rows):
        self.tree.delete(*self.tree.get_children())
        for i, row in enumerate(rows):
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end", values=row, tags=(tag,))
        self.tree.tag_configure("even", background=F1_SILVER)
        self.tree.tag_configure("odd",  background="#D8D8D8")

    def _filter_table(self, *_):
        q = self.search_var.get().lower()
        filtered = [r for r in self._all_rows
                    if any(q in str(v).lower() for v in r)]
        self._populate(filtered)

    # ── Painel direito
    def _build_right_panel(self, parent):
        right = tk.Frame(parent, bg=F1_BLACK, width=170, padx=8, pady=10)
        right.pack(side="left", fill="y", padx=(6, 0))
        right.pack_propagate(False)

        tk.Label(
            right, text="PILOTOS", font=("Impact", 15),
            fg=F1_ACCENT, bg=F1_BLACK
        ).pack(pady=(0, 6))

        tk.Label(
            right,
            text="🏎  Temporada\n2024",
            font=("Courier New", 10, "bold"),
            fg=F1_WHITE, bg=F1_BLACK, justify="center"
        ).pack(pady=4)

        tk.Frame(right, bg=F1_RED, height=3).pack(fill="x", pady=6)

        sair_btn = tk.Button(
            right, text="SAIR ✕", command=self.quit,
            font=("Impact", 13),
            bg=F1_ACCENT, fg=F1_BLACK,
            activebackground="#FFF0A0",
            relief="flat", bd=0, cursor="hand2",
            width=14, height=2
        )
        sair_btn.pack(side="bottom", pady=8, fill="x")
        sair_btn.bind("<Enter>", lambda e: sair_btn.config(bg="#FFE040"))
        sair_btn.bind("<Leave>", lambda e: sair_btn.config(bg=F1_ACCENT))

        tk.Label(
            right,
            text="● SISTEMA ONLINE",
            font=("Courier New", 8),
            fg="#00FF80", bg=F1_BLACK
        ).pack(side="bottom", pady=2)

 
    def _on_cadastro(self):
        self._open_dialog("CADASTRO DE PILOTO", [
            "Número:", "Nome:", "Sigla:", "Equipe:", "Pontos:"
        ], self._save_pilot)

    def _on_atualizar(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um piloto na lista.")
            return
        vals = self.tree.item(sel, "values")
        self._open_dialog("ATUALIZAR PILOTO", [
            "Número:", "Nome:", "Sigla:", "Equipe:", "Pontos:"
        ], lambda v: self._update_pilot(v), prefill=vals)

    def _on_remover(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um piloto na lista.")
            return
        vals = self.tree.item(sel, "values")
        nome, numero = vals[1], int(vals[0])
        if messagebox.askyesno("Confirmar", f"Remover {nome}?"):
            if self.repo.remover_motorista(numero):
                self._refresh_table()
            else:
                messagebox.showerror("Erro", "Piloto não encontrado no banco.")

    def _on_listar(self):
        self.search_var.set("")
        self._refresh_table()

    def _on_ordenar(self):
        self._all_rows = sorted(
            self._all_rows,
            key=lambda r: int(r[4]) if r[4].isdigit() else 0,
            reverse=True
        )
        self._populate(self._all_rows)

    def _on_importar_api(self):
        total = self.repo.importar_api()
        if total == -1:
            messagebox.showerror("Erro", "Falha ao conectar com a API OpenF1.")
        else:
            messagebox.showinfo("API", f"{total} pilotos novos importados!")
            self._refresh_table()

    def _save_pilot(self, values):
        try:
            numero = int(values[0])
            pontos = int(values[4]) if values[4] else 0
        except ValueError:
            messagebox.showerror("Erro", "Número e Pontos devem ser inteiros.")
            return
        if self.repo.cadastrar_motorista(numero, values[1], values[2], values[3], pontos):
            self._refresh_table()
        else:
            messagebox.showerror("Erro", f"Número {numero} já cadastrado.")

    def _update_pilot(self, values):
        try:
            numero = int(values[0])
            pontos = int(values[4]) if values[4] else 0
        except ValueError:
            messagebox.showerror("Erro", "Número e Pontos devem ser inteiros.")
            return
        if self.repo.atualizar_motorista(numero, values[1], values[2], values[3], pontos):
            self._refresh_table()
        else:
            messagebox.showerror("Erro", f"Piloto #{numero} não encontrado.")

    def _open_dialog(self, title, fields, callback, prefill=None):
        dlg = tk.Toplevel(self)
        dlg.title(title)
        dlg.configure(bg=F1_BLACK)
        dlg.resizable(False, False)
        dlg.grab_set()

        tk.Label(
            dlg, text=title, font=("Impact", 14),
            fg=F1_ACCENT, bg=F1_BLACK
        ).grid(row=0, column=0, columnspan=2, pady=(12, 8), padx=16)

        entries = []
        for i, field in enumerate(fields, start=1):
            tk.Label(
                dlg, text=field, font=("Courier New", 10),
                fg=F1_WHITE, bg=F1_BLACK, anchor="e"
            ).grid(row=i, column=0, sticky="e", padx=(16, 4), pady=4)
            e = tk.Entry(
                dlg, font=("Courier New", 10), width=22,
                bg=F1_SILVER, fg=F1_BLACK, relief="flat", insertbackground=F1_RED
            )
            e.grid(row=i, column=1, sticky="w", padx=(0, 16), pady=4, ipady=3)
            if prefill:
                e.insert(0, prefill[i - 1])
            entries.append(e)

        def confirm():
            vals = [e.get().strip() for e in entries]
            if not vals[0] or not vals[1]:
                messagebox.showwarning("Aviso", "Preencha ao menos Nº e Nome.", parent=dlg)
                return
            callback(vals)
            dlg.destroy()

        btn_frame = tk.Frame(dlg, bg=F1_BLACK)
        btn_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=12)

        tk.Button(
            btn_frame, text="CONFIRMAR", command=confirm,
            font=("Impact", 11), bg=F1_RED, fg=F1_WHITE,
            relief="flat", padx=16, pady=4, cursor="hand2"
        ).pack(side="left", padx=6)

        tk.Button(
            btn_frame, text="CANCELAR", command=dlg.destroy,
            font=("Impact", 11), bg="#444", fg=F1_WHITE,
            relief="flat", padx=16, pady=4, cursor="hand2"
        ).pack(side="left", padx=6)

        entries[0].focus()
        return dlg


if __name__ == "__main__":
    app = F1App()
    app.mainloop()
