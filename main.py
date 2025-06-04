import TimeSeries
import sys
import json


def parse_manual_equation():
    """
    Interface interactive pour saisir manuellement les paramètres de l'équation différentielle
    """
    print("\n=== SAISIE MANUELLE DE L'ÉQUATION DIFFÉRENTIELLE DU SECOND ORDRE ===")
    print("Équation générale: m*ÿ + c*ẏ + k*y = F(t)")
    print("ou sous forme normalisée: ÿ + 2*ζ*ωn*ẏ + ωn²*y = F(t)/m")
    print()
    
    choice = input("Choisissez le format de saisie:\n1. Paramètres physiques (m, c, k)\n2. Paramètres normalisés (ωn, ζ)\nChoix (1 ou 2): ").strip()
    
    manual_params = {}
    
    if choice == "1":
        print("\n--- Saisie des paramètres physiques ---")
        manual_params['m'] = float(input("Masse (m) [kg]: "))
        manual_params['c'] = float(input("Coefficient d'amortissement (c) [N⋅s/m]: "))
        manual_params['k'] = float(input("Rigidité (k) [N/m]: "))
        manual_params['A'] = float(input("Amplitude initiale (A): ") or "1.0")
        manual_params['offset'] = float(input("Décalage vertical (offset): ") or "0.0")
        manual_params['phi'] = float(input("Déphasage initial (φ) [rad]: ") or "0.0")
        
        # Calcul des paramètres normalisés
        omega_n = (manual_params['k'] / manual_params['m']) ** 0.5
        zeta = manual_params['c'] / (2 * (manual_params['m'] * manual_params['k']) ** 0.5)
        
        manual_params['omega_n'] = omega_n
        manual_params['zeta'] = zeta
        manual_params['format'] = 'physical'
        
        print(f"\nParamètres calculés:")
        print(f"Pulsation naturelle (ωn): {omega_n:.4f} rad/s")
        print(f"Facteur d'amortissement (ζ): {zeta:.4f}")
        
    elif choice == "2":
        print("\n--- Saisie des paramètres normalisés ---")
        manual_params['omega_n'] = float(input("Pulsation naturelle (ωn) [rad/s]: "))
        manual_params['zeta'] = float(input("Facteur d'amortissement (ζ): "))
        manual_params['A'] = float(input("Amplitude (A): ") or "1.0")
        manual_params['offset'] = float(input("Décalage vertical (offset): ") or "0.0")
        manual_params['phi'] = float(input("Déphasage initial (φ) [rad]: ") or "0.0")
        manual_params['format'] = 'normalized'
        
    else:
        print("Choix invalide. Retour à l'ajustement automatique.")
        return None
    
    # Classification du système
    zeta = manual_params['zeta']
    if zeta < 1:
        system_type = "sous-amorti (oscillations amorties)"
    elif zeta == 1:
        system_type = "amortissement critique"
    else:
        system_type = "sur-amorti (pas d'oscillations)"
    
    print(f"\nType de système: {system_type}")
    
    # Confirmation
    confirm = input("\nConfirmer ces paramètres? (o/n): ").strip().lower()
    if confirm in ['o', 'oui', 'y', 'yes']:
        return manual_params
    else:
        return None


def save_equation_params(params, filename):
    """Sauvegarde les paramètres dans un fichier JSON"""
    params_file = filename[:-4] + "_equation_params.json"
    with open(params_file, 'w') as f:
        json.dump(params, f, indent=2)
    print(f"Paramètres sauvegardés dans: {params_file}")


def load_equation_params(filename):
    """Charge les paramètres depuis un fichier JSON"""
    params_file = filename[:-4] + "_equation_params.json"
    try:
        with open(params_file, 'r') as f:
            params = json.load(f)
        print(f"Paramètres chargés depuis: {params_file}")
        return params
    except FileNotFoundError:
        return None


def main():
    #retreive first parameter
    if len(sys.argv)>=2:
        filename = str(sys.argv[1])
    else :
        print("Usage : $python main.py file.csv [timestamp_col_number] [nb_mesures] [--no-fit] [--manual] [--load-params]")
        print("Options:")
        print("  --no-fit      : Désactive l'ajustement automatique")
        print("  --manual      : Saisie manuelle des paramètres d'équation")
        print("  --load-params : Charge les paramètres depuis un fichier JSON")
        quit()

    #retreive second parameter
    if len(sys.argv)>=4:
        timestamp_col_number = int(sys.argv[2])
        nb_mesures = int(sys.argv[3])
    elif len(sys.argv)==3 :
        timestamp_col_number = 0
        nb_mesures = int(sys.argv[2])
    else:
        print("Usage : $python main.py file.csv [timestamp_col_number] [nb_mesures] [--no-fit] [--manual] [--load-params]")
        quit()

    # Gestion des options
    fit_differential = True
    manual_mode = False
    load_params = False
    manual_params = None
    
    if '--no-fit' in sys.argv:
        fit_differential = False
    if '--manual' in sys.argv:
        manual_mode = True
    if '--load-params' in sys.argv:
        load_params = True

    print(f"Traitement du fichier: {filename}")
    print(f"Colonne temporelle: {timestamp_col_number}")
    print(f"Nombre de mesures: {nb_mesures}")

    # Gestion des paramètres manuels
    if load_params:
        manual_params = load_equation_params(filename)
        if manual_params:
            print("Paramètres chargés avec succès!")
            manual_mode = True
        else:
            print("Aucun fichier de paramètres trouvé. Passage en mode automatique.")
    
    if manual_mode and manual_params is None:
        manual_params = parse_manual_equation()
        if manual_params:
            save_params = input("Sauvegarder ces paramètres? (o/n): ").strip().lower()
            if save_params in ['o', 'oui', 'y', 'yes']:
                save_equation_params(manual_params, filename)

    if manual_params:
        print(f"Mode: Équation manuelle")
        fit_differential = True  # On active l'affichage avec les paramètres manuels
    elif fit_differential:
        print(f"Mode: Ajustement automatique")
    else:
        print(f"Mode: Affichage simple (sans équation)")

    #build time series
    ts=TimeSeries.create_csv_file(filename,
                                  timestamp_col_number,
                                  'temps en secondes',
                                  'distance en milimètres',
                                  nb_mesures)

    #swap curves
    TimeSeries.swap_column(ts,1,2)

    #show and/or save curves with differential equation fitting
    TimeSeries.plot(ts, show=True, save=True, name=filename[:-4]+".pdf", 
                   fit_differential_equation=fit_differential,
                   manual_equation_params=manual_params)

if __name__=="__main__":
    main()