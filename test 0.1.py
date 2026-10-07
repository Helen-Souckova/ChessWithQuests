from __future__ import annotations

import tkinter as tk
from tkinter import messagebox
from dataclasses import dataclass, field
from typing import Optional
from abc import ABC, abstractmethod
from datetime import datetime


# ============================================================
# DOMÉNOVÉ TŘÍDY PODLE DIAGRAMU
# ============================================================












# ============================================================
# FIGURKY
# ============================================================






















# ============================================================
# HERNÍ PLOCHA
# ============================================================


# ============================================================
# REVIZOR TAHU
# ============================================================




# ============================================================
# TIMER
# ============================================================



# ============================================================
# GAME LOGGER
# ============================================================



# ============================================================
# GAME MANAGER
# ============================================================



# ============================================================
# CONTROLLER
# ============================================================




# ============================================================
# GAME VIEW
# ============================================================

class GameView(tk.Frame):

    POLICKO = 75

    BARVA_SVETLA = "#F0D9B5"
    BARVA_TMAVA = "#B58863"
    BARVA_VYBER = "#F7EC5E"

    def __init__(self, parent, controller):

        super().__init__(parent)

        self.controller = controller

        self.canvas = tk.Canvas(
            self,
            width=self.POLICKO * 8,
            height=self.POLICKO * 8,
            highlightthickness=0
        )

        self.canvas.pack()

        self.canvas.bind(
            "<Button-1>",
            self.klik
        )

        self.vybrane_pole = None

        self.nakresli()

    def nakresli(self):

        self.canvas.delete("all")

        plocha = self.controller.game_manager.plocha

        for r in range(8):
            for c in range(8):

                x1 = c * self.POLICKO
                y1 = r * self.POLICKO

                x2 = x1 + self.POLICKO
                y2 = y1 + self.POLICKO

                barva = (
                    self.BARVA_SVETLA
                    if (r + c) % 2 == 0
                    else self.BARVA_TMAVA
                )

                if self.vybrane_pole == (r, c):
                    barva = self.BARVA_VYBER

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=barva,
                    outline=""
                )

                figurka = plocha.vrat_obsah((r, c))

                if figurka:

                    self.canvas.create_text(
                        x1 + self.POLICKO / 2,
                        y1 + self.POLICKO / 2,
                        text=figurka.symbol,
                        font=("Arial", 48)
                    )

        # Souřadnice šachovnice.
        for c in range(8):
            pismeno = chr(ord("a") + c)

            self.canvas.create_text(
                c * self.POLICKO + 5,
                8 * self.POLICKO - 5,
                text=pismeno,
                anchor="sw",
                font=("Arial", 9)
            )

        for r in range(8):
            cislo = str(8 - r)

            self.canvas.create_text(
                5,
                r * self.POLICKO + 5,
                text=cislo,
                anchor="nw",
                font=("Arial", 9)
            )

    def klik(self, event):

        col = event.x // self.POLICKO
        row = event.y // self.POLICKO

        if not (0 <= row < 8 and 0 <= col < 8):
            return

        pole = (row, col)

        # První kliknutí – výběr figurky.
        if self.vybrane_pole is None:

            if self.controller.je_vlastni_figurka(pole):

                self.vybrane_pole = pole
                self.nakresli()

            return

        # Druhé kliknutí – provedení tahu.
        start = self.vybrane_pole
        cil = pole

        uspech, zprava = self.controller.proved_tah(
            start,
            cil
        )

        if not uspech:

            # Pokud klikne na jinou vlastní figurku,
            # přepneme výběr.
            if self.controller.je_vlastni_figurka(cil):
                self.vybrane_pole = cil
                self.nakresli()
                return

            messagebox.showwarning(
                "Neplatný tah",
                zprava
            )

        self.vybrane_pole = None

        self.nakresli()

        if uspech:
            self.controller.game_manager.uloz_log()


# ============================================================
# HRAC GAME VIEW
# ============================================================

class HracGameView(tk.Frame):

    def __init__(self, parent, controller):

        super().__init__(parent)

        self.controller = controller

        self.label = tk.Label(
            self,
            text="",
            font=("Arial", 14)
        )

        self.label.pack(pady=10)

        self.aktualizuj_hrace(
            controller.game_manager.hraci
        )

    def aktualizuj_hrace(self, hraci):

        aktivni = self.controller.game_manager.aktivni_hrac

        barva = (
            "Bílý"
            if aktivni == 1
            else "Černý"
        )

        self.label.config(
            text=f"Na tahu je: {barva}"
        )

        self.after(
            250,
            lambda: self.aktualizuj_hrace(hraci)
        )


# ============================================================
# HLAVNÍ APLIKACE
# ============================================================

class ChessApp:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title("Šachy")

        self.root.resizable(False, False)

        # Uživatelé.
        bily_uzivatel = Uzivatel(
            uzivatelske_jmeno="white",
            jmeno="Bílý hráč",
            email="white@example.com",
            elo=1200
        )

        cerny_uzivatel = Uzivatel(
            uzivatelske_jmeno="black",
            jmeno="Černý hráč",
            email="black@example.com",
            elo=1200
        )

        # Hráči.
        hraci = [
            Hrac(
                barva=1,
                uzivatel=bily_uzivatel
            ),
            Hrac(
                barva=-1,
                uzivatel=cerny_uzivatel
            )
        ]

        self.game_manager = GameManager(hraci)

        self.controller = GameManagerController(
            self.game_manager
        )

        # -----------------------------
        # Horní panel
        # -----------------------------

        top = tk.Frame(self.root)

        top.pack(fill="x")

        self.status = tk.Label(
            top,
            text="Na tahu je: Bílý",
            font=("Arial", 15, "bold")
        )

        self.status.pack(side="left", padx=10, pady=10)

        tk.Button(
            top,
            text="Nová hra",
            command=self.nova_hra
        ).pack(side="right", padx=5)

        tk.Button(
            top,
            text="Zpět tah",
            command=self.zpet_tah
        ).pack(side="right", padx=5)

        tk.Button(
            top,
            text="Uložit log",
            command=self.uloz_log
        ).pack(side="right", padx=5)

        # -----------------------------
        # Herní plocha
        # -----------------------------

        self.game_view = GameView(
            self.root,
            self.controller
        )

        self.game_view.pack()

        # -----------------------------
        # Informace o hráčích
        # -----------------------------

        self.players_frame = HracGameView(
            self.root,
            self.controller
        )

        self.players_frame.pack()

        self.aktualizuj_status()

    def aktualizuj_status(self):

        barva = self.game_manager.aktivni_hrac

        text = (
            "Na tahu je: Bílý"
            if barva == 1
            else "Na tahu je: Černý"
        )

        self.status.config(text=text)

        self.root.after(
            200,
            self.aktualizuj_status
        )

    def nova_hra(self):

        odpoved = messagebox.askyesno(
            "Nová hra",
            "Opravdu chcete začít novou hru?"
        )

        if not odpoved:
            return

        self.game_manager = GameManager(
            self.game_manager.hraci
        )

        self.controller = GameManagerController(
            self.game_manager
        )

        self.game_view.controller = self.controller
        self.game_view.vybrane_pole = None

        self.game_view.nakresli()

    def zpet_tah(self):

        if self.game_manager.zrus_tah():
            self.game_view.vybrane_pole = None
            self.game_view.nakresli()
        else:
            messagebox.showinfo(
                "Zpět",
                "Není co vrátit."
            )

    def uloz_log(self):

        self.game_manager.uloz_log()

        messagebox.showinfo(
            "Log",
            "Log hry byl uložen do game_log.txt."
        )

    def run(self):
        self.root.mainloop()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    app = ChessApp()
    app.run()