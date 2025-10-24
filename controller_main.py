import tkinter as tk
from tkinter import messagebox
from config.datasets_config import cohort_paths
from nhr_template_creation.nhr_main import run_nhr_main
from excepties.excepties_main import run_exceptions
import traceback

# functies
def run_nhr(dataset_key):
    """Output: alleen het NHR incl.rules bestand """
    msg = run_nhr_main(dataset_key)
    messagebox.showinfo("Klaar", f"NHR incl. rules voltooid voor {dataset_key}\n\n{msg}")

def run_excepties(dataset_key):
    """Output: alleen excepties """
    run_exceptions(dataset_key)
    messagebox.showinfo("Klaar", f"Excepties verwerkt voor {dataset_key}")

def run_full(dataset_key):
    """Draait NHR-template + daarna excepties."""
    run_nhr_main(dataset_key)
    run_exceptions(dataset_key)
    messagebox.showinfo("Klaar", f"Volledige flow voltooid voor {dataset_key}")


# interface code
root = tk.Tk()
root.title("NHR Automatisering")
root.geometry("550x400")
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

actions = ["NHR incl. Rules", "Excepties", "Volledige flow"]
action_box = tk.Listbox(root, listvariable=tk.StringVar(value=actions),
                        height=3, exportselection=False)
action_box.selection_set(0)
action_box.pack(pady=5)

tk.Label(root, text="Type variabelen:", font=("Segoe UI", 11, "bold")).pack(pady=(10, 5))
var_type_var = tk.StringVar(value="Interventievariabelen")

var_types = ["Interventievariabelen", "Follow-up variabelen"]
var_type_box = tk.Listbox(root, listvariable=tk.StringVar(value=var_types),
                          height=2, exportselection=False)
var_type_box.selection_set(0)
var_type_box.pack(pady=5)

def execute():
    selected_cohort = cohort_box.get(tk.ACTIVE)
    selected_action = action_box.get(tk.ACTIVE)
    selected_var_type = var_type_box.get(tk.ACTIVE)

    if not selected_cohort:
        messagebox.showwarning("Selectie", "Kies eerst een cohort.")
        return

    try:
        if selected_action == "NHR Template":
            run_nhr(selected_cohort)
        elif selected_action == "Excepties":
            run_exceptions(selected_cohort, selected_var_type)
        elif selected_action == "Volledige flow":
            run_full(selected_cohort)
    except Exception as e:
        tb = traceback.format_exc()
        print(f"Fout bij {selected_cohort}:\n{tb}")
        messagebox.showerror("Fout", f"Er ging iets mis bij {selected_cohort}:\n\n{tb}")



tk.Button(root, text="▶ Run selectie", command=execute,
          width=20, bg="#2196F3", fg="white").pack(pady=15)

tk.Label(root, text="NHR & Excepties HVC",
         font=("Segoe UI", 9, "italic")).pack(side="bottom", pady=4)

root.mainloop()
