import tkinter as tk
from tkinter import messagebox
from config.datasets_config import cohort_paths
from nhr_template_creation.nhr_main import run_nhr_main
from excepties.excepties_main2 import run_exceptions


# ---------- functies ----------
def run_nhr(dataset_key):
    """Draait alleen de NHR-template pipeline."""
    msg = run_nhr_main(dataset_key)
    messagebox.showinfo("Klaar", f"NHR-template voltooid voor {dataset_key}\n\n{msg}")

def run_excepties(dataset_key):
    """Draait alleen de excepties pipeline."""
    run_exceptions(dataset_key)
    messagebox.showinfo("Klaar", f"Excepties verwerkt voor {dataset_key}")

def run_full(dataset_key):
    """Draait NHR-template + daarna excepties."""
    run_nhr_main(dataset_key)
    run_exceptions(dataset_key)
    messagebox.showinfo("Klaar", f"Volledige flow voltooid voor {dataset_key}")


# ---------- GUI ----------
root = tk.Tk()
root.title("NHR Automatisering Launcher")
root.geometry("460x340")
root.resizable(False, False)

tk.Label(root, text="Selecteer cohort:", font=("Segoe UI", 11, "bold")).pack(pady=(15, 5))

# lijst met cohorten
cohort_var = tk.StringVar(value=list(cohort_paths.keys())[0])
cohort_box = tk.Listbox(root, listvariable=tk.StringVar(value=list(cohort_paths.keys())),
                        height=6, exportselection=False)
cohort_box.selection_set(0)
cohort_box.pack(pady=5)

# lijst met acties
tk.Label(root, text="Wat wil je uitvoeren?", font=("Segoe UI", 11, "bold")).pack(pady=(10, 5))
action_var = tk.StringVar(value="NHR Template")

actions = ["NHR Template", "Excepties", "Volledige flow"]
action_box = tk.Listbox(root, listvariable=tk.StringVar(value=actions),
                        height=3, exportselection=False)
action_box.selection_set(0)
action_box.pack(pady=5)


def execute():
    selected_cohort = cohort_box.get(tk.ACTIVE)
    selected_action = action_box.get(tk.ACTIVE)

    if not selected_cohort:
        messagebox.showwarning("Selectie", "⚠️ Kies eerst een cohort.")
        return

    try:
        if selected_action == "NHR Template":
            run_nhr(selected_cohort)
        elif selected_action == "Excepties":
            run_excepties(selected_cohort)
        elif selected_action == "Volledige flow":
            run_full(selected_cohort)
    except Exception as e:
        messagebox.showerror("Fout", f"Er ging iets mis bij {selected_cohort}:\n\n{e}")


tk.Button(root, text="▶ Run selectie", command=execute,
          width=20, bg="#2196F3", fg="white").pack(pady=15)

tk.Label(root, text="NHR & Excepties automatisering – CHVC MUMC+",
         font=("Segoe UI", 9, "italic")).pack(side="bottom", pady=6)

root.mainloop()
