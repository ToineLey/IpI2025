import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.integrate import solve_ivp


class Timeseries: pass


def _construct(data, labels: list, id_temps: int, data_temps, x_label: str, y_label: str,
               titre: tuple) -> Timeseries:
    """
    description : La fonction (normalement pas appellé par l'utilisateur) permet de construire un tad.
    :param data: Contient la liste des éléments contenus dans le csv sous format array de Numpy (c'est pour cela que son type n'est pas spécifié)
    :param labels: Contient la liste des labels de chaque colonne
    :param id_temps: Contient l'index de la colonne temporelle
    :param data_temps: Contient la liste des moments
    :param x_label: Contient le nom de la colonne temporelle
    :param y_label: Contient le nom de la colonne de la valeur (soit la distance)
    :param titre: Contient un tuple contenant les informations du titre du graphique
    :return: Renvoie le tad construit
    """

    timeseries = Timeseries()
    timeseries.data = data
    timeseries.labels = labels
    timeseries.temps = id_temps
    timeseries.x_label = x_label
    timeseries.y_label = y_label
    timeseries.data_temps = data_temps
    timeseries.titre = "Fluide = " + titre[0] + ", Degrés d'ouverture = " + titre[1]
    return timeseries


def create_csv_file(filename: str, id_temps: int, x_label: str,
                    y_label: str, nb_mesures: int = 1) -> Timeseries:
    """
    description : La fonction, qui elle est appelé par le programme utilisateur, permet de lire un fichier CSV et de construire un tad à l'aide de la fonction _construct.
    :param filename: Contient le nom du fichier CSV
    :param id_temps: Contient l'index de la colonne temporelle'
    :param x_label: Contient le nom de la colonne temporelle
    :param y_label: Contient le nom de la colonne de la valeur (soit la distance)
    :param nb_mesures: Contient le nombre de mesures contenues dans le fichier CSV
    :return: Renvoie le tad construit
    """

    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        labels = next(reader)
        data = []
        l = []

        for row in reader:
            data.append(row)

        titre = (data[0].pop(4 + (nb_mesures - 1)), data[0].pop(4 + (nb_mesures - 1)))

        for i in range(len(data)):
            for j in range(len(data[i])):
                if data[i][j] == '' and j not in l:
                    l.append(j)

                try:
                    data[i][j] = float(data[i][j])
                finally:
                    continue

    for i in range(len(data)):
        for elem in sorted(l, reverse=True):
            if elem < len(data[i]):
                del data[i][elem]

    data = [row for row in data if row and all(isinstance(val, float) for val in row)]

    if not data:
        raise ValueError("Les données du fichier CSV sont vides ou invalides après nettoyage.")

    labels.pop(id_temps)

    data_temps = []
    premier_temps = float(data[0][id_temps])

    for line in data:
        data_temps.append(float(line.pop(id_temps)) - premier_temps)

    try:
        data_np = np.array(data, dtype=float)
        data_temps_np = np.array(data_temps, dtype=float)
        data_np -= 225
    except ValueError as e:
        raise ValueError(f"Erreur de conversion des données en tableau NumPy : {e}")

    return _construct(data_np, labels, id_temps, data_temps_np, x_label, y_label, titre)


def second_order_response(t, A, omega_n, zeta, phi=0, offset=0):
    """
    Réponse d'un système du second ordre sous-amorti
    :param t: temps
    :param A: amplitude
    :param omega_n: pulsation naturelle
    :param zeta: facteur d'amortissement
    :param phi: déphasage
    :param offset: décalage vertical
    :return: réponse du système
    """
    if zeta >= 1:
        # Système sur-amorti ou critique
        if zeta == 1:
            # Amortissement critique
            return A * (1 + omega_n * t) * np.exp(-omega_n * t) + offset
        else:
            # Sur-amorti
            r1 = -omega_n * (zeta + np.sqrt(zeta**2 - 1))
            r2 = -omega_n * (zeta - np.sqrt(zeta**2 - 1))
            return A * (np.exp(r1 * t) - np.exp(r2 * t)) + offset
    else:
        # Sous-amorti
        omega_d = omega_n * np.sqrt(1 - zeta**2)
        return A * np.exp(-zeta * omega_n * t) * np.cos(omega_d * t + phi) + offset


def fit_second_order_system(t_data, y_data):
    """
    Ajuste une réponse du second ordre aux données expérimentales
    :param t_data: données temporelles
    :param y_data: données de position/distance
    :return: paramètres optimisés et métriques d'erreur
    """
    
    # Estimation initiale des paramètres
    y_mean = np.mean(y_data)
    y_max = np.max(y_data)
    y_min = np.min(y_data)
    A_init = (y_max - y_min) / 2
    
    # Estimation de la fréquence naturelle par analyse spectrale
    from scipy.fft import fft, fftfreq
    n = len(y_data)
    dt = t_data[1] - t_data[0] if len(t_data) > 1 else 1.0
    
    # FFT pour estimer la fréquence dominante
    y_fft = fft(y_data - np.mean(y_data))
    freqs = fftfreq(n, dt)
    
    # Trouver la fréquence dominante (excluant la composante DC)
    positive_freqs = freqs[1:n//2]
    positive_fft = np.abs(y_fft[1:n//2])
    
    if len(positive_fft) > 0:
        dominant_freq = positive_freqs[np.argmax(positive_fft)]
        omega_n_init = 2 * np.pi * dominant_freq
    else:
        omega_n_init = 1.0
    
    # Estimation du facteur d'amortissement
    # Méthode du décrément logarithmique si oscillations visibles
    peaks = []
    for i in range(1, len(y_data) - 1):
        if y_data[i] > y_data[i-1] and y_data[i] > y_data[i+1]:
            peaks.append((t_data[i], y_data[i]))
    
    if len(peaks) >= 2:
        # Calcul du décrément logarithmique
        delta = np.log(peaks[0][1] / peaks[1][1]) if peaks[1][1] != 0 else 0.1
        zeta_init = delta / np.sqrt((2*np.pi)**2 + delta**2)
    else:
        zeta_init = 0.1  # Valeur par défaut pour sous-amortissement
    
    # Paramètres initiaux
    p0 = [A_init, abs(omega_n_init), zeta_init, 0, y_mean]
    
    try:
        # Ajustement avec limites raisonnables
        bounds = (
            [-np.inf, 0.1, 0, -np.pi, -np.inf],  # limites inférieures
            [np.inf, 100, 2, np.pi, np.inf]       # limites supérieures
        )
        
        popt, pcov = curve_fit(second_order_response, t_data, y_data, 
                              p0=p0, bounds=bounds, maxfev=5000)
        
        # Calcul des métriques d'erreur
        y_pred = second_order_response(t_data, *popt)
        
        # Erreur quadratique moyenne (RMSE)
        rmse = np.sqrt(np.mean((y_data - y_pred)**2))
        
        # Coefficient de détermination (R²)
        ss_res = np.sum((y_data - y_pred)**2)
        ss_tot = np.sum((y_data - np.mean(y_data))**2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        # Erreur relative moyenne
        relative_error = np.mean(np.abs((y_data - y_pred) / y_data)) * 100 if np.all(y_data != 0) else 0
        
        return popt, pcov, rmse, r_squared, relative_error, y_pred
        
    except Exception as e:
        print(f"Erreur lors de l'ajustement : {e}")
        return None, None, None, None, None, None


def plot(ts, show: bool, save: bool, name: str = "courbe-sans-titre", 
         fit_differential_equation: bool = True, manual_equation_params: dict = None) -> None:
    """
    description : La fonction permet d'afficher le graphique du tad précédemment construit avec option d'ajustement d'équation différentielle.
    :param ts: Contient le tad construit
    :param show: Contient un booléen qui permet de savoir si on affiche ou non le graphique
    :param save: Contient un booléen qui permet de savoir si on enregistre ou non le graphique
    :param name: Contient une chaîne de caractère qui permet de nommer le graphique
    :param fit_differential_equation: Active l'ajustement de l'équation différentielle du second ordre
    :param manual_equation_params: Paramètres manuels pour l'équation différentielle (dict ou None)
    :return: Ne retourne rien
    """

    # Vérifications de base
    if not hasattr(ts, 'data') or not hasattr(ts, 'data_temps'):
        raise ValueError("L'objet timeseries ne contient pas les attributs 'data' ou 'data_temps'.")
    if len(ts.data) == 0 or len(ts.data_temps) == 0:
        raise ValueError("Les données ou les temps sont vides.")
    
    try:
        data_array = np.array(ts.data, dtype=float)
        temps_array = np.array(ts.data_temps, dtype=float)
    except ValueError as e:
        raise ValueError(f"Erreur : Les données ne peuvent pas être converties en tableau NumPy : {e}")
    
    if len(temps_array) != data_array.shape[0]:
        raise ValueError("Le nombre de points temporels et de données ne correspond pas.")

    # Configuration de la figure
    if fit_differential_equation:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(30, 24))
    else:
        plt.figure(figsize=(30, 18))
        ax1 = plt.gca()

    # Tracé des données expérimentales
    if data_array.ndim == 1:
        ax1.scatter(temps_array, data_array, label="Données expérimentales", alpha=0.7, color='blue')
        experimental_data = data_array
    elif data_array.ndim >= 2:
        # Prendre la première colonne pour l'ajustement
        experimental_data = data_array[:, 0]
        for index, column in enumerate(data_array.T):
            ax1.plot(temps_array, column,
                    label=f"Exp. {ts.labels[index]}" if ts.labels else f"Exp. Colonne {index + 1}",
                    alpha=0.7)

    # Configuration du premier graphique
    ax1.set_ylim(data_array.min(), data_array.max())
    ax1.set_xlim(temps_array[0], temps_array[-1])
    ax1.legend(loc="upper right")
    ax1.set_xlabel(ts.x_label)
    ax1.set_ylabel(ts.y_label)
    ax1.set_title(f"{ts.titre} - Données expérimentales")
    ax1.grid(True, alpha=0.3)

    # Ajustement de l'équation différentielle si demandé
    if fit_differential_equation:
        if manual_equation_params is not None:
            # Mode manuel : utiliser les paramètres fournis
            print("Utilisation des paramètres manuels de l'équation différentielle...")
            
            # Extraire les paramètres
            A = manual_equation_params.get('A', 1.0)
            omega_n = manual_equation_params['omega_n']
            zeta = manual_equation_params['zeta']
            phi = manual_equation_params.get('phi', 0.0)
            offset = manual_equation_params.get('offset', 0.0)
            
            # Générer la courbe théorique
            y_pred = second_order_response(temps_array, A, omega_n, zeta, phi, offset)
            
            # Calculer les métriques d'erreur
            rmse = np.sqrt(np.mean((experimental_data - y_pred)**2))
            ss_res = np.sum((experimental_data - y_pred)**2)
            ss_tot = np.sum((experimental_data - np.mean(experimental_data))**2)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
            relative_error = np.mean(np.abs((experimental_data - y_pred) / experimental_data)) * 100 if np.all(experimental_data != 0) else 0
            
            # Affichage des résultats
            print(f"\n=== PARAMÈTRES MANUELS UTILISÉS ===")
            if manual_equation_params.get('format') == 'physical':
                print(f"Masse (m): {manual_equation_params.get('m', 'N/A')} kg")
                print(f"Amortissement (c): {manual_equation_params.get('c', 'N/A')} N⋅s/m")
                print(f"Rigidité (k): {manual_equation_params.get('k', 'N/A')} N/m")
            print(f"Amplitude (A): {A:.4f}")
            print(f"Pulsation naturelle (ωn): {omega_n:.4f} rad/s")
            print(f"Fréquence naturelle (fn): {omega_n/(2*np.pi):.4f} Hz")
            print(f"Facteur d'amortissement (ζ): {zeta:.4f}")
            print(f"Déphasage (φ): {phi:.4f} rad")
            print(f"Décalage (offset): {offset:.4f}")
            print(f"\n=== MÉTRIQUES D'ERREUR (Manuel vs Expérimental) ===")
            print(f"RMSE: {rmse:.4f}")
            print(f"R²: {r_squared:.4f}")
            print(f"Erreur relative moyenne: {relative_error:.2f}%")
            
            # Classification du système
            if zeta < 1:
                print(f"Système sous-amorti (ζ < 1)")
                print(f"Fréquence amortie: {omega_n * np.sqrt(1 - zeta**2):.4f} rad/s")
            elif zeta == 1:
                print(f"Système à amortissement critique (ζ = 1)")
            else:
                print(f"Système sur-amorti (ζ > 1)")

            # Tracé de la courbe théorique sur le premier graphique
            ax1.plot(temps_array, y_pred, 'r--', linewidth=2, 
                    label=f'Modèle manuel (ζ={zeta:.3f})')
            ax1.legend(loc="upper right")

            # Deuxième graphique : comparaison et résidus
            ax2.plot(temps_array, experimental_data, 'b-', label='Données expérimentales', linewidth=2)
            ax2.plot(temps_array, y_pred, 'r--', label=f'Modèle manuel (ζ={zeta:.3f})', linewidth=2)
            
            # Résidus
            residuals = experimental_data - y_pred
            ax2_twin = ax2.twinx()
            ax2_twin.plot(temps_array, residuals, 'g:', alpha=0.7, linewidth=1.5, label='Résidus')
            ax2_twin.set_ylabel('Résidus', color='g')
            ax2_twin.tick_params(axis='y', labelcolor='g')

            ax2.set_xlabel(ts.x_label)
            ax2.set_ylabel(ts.y_label)
            ax2.set_title(f'Modèle Manuel vs Expérimental (R²={r_squared:.3f}, RMSE={rmse:.3f})')
            ax2.legend(loc="upper left")
            ax2_twin.legend(loc="upper right")
            ax2.grid(True, alpha=0.3)

            # Ajout de texte avec les paramètres
            if manual_equation_params.get('format') == 'physical':
                textstr = f'MANUEL\nm = {manual_equation_params.get("m", "N/A"):.3f} kg\nc = {manual_equation_params.get("c", "N/A"):.3f} N⋅s/m\nk = {manual_equation_params.get("k", "N/A"):.3f} N/m\nωn = {omega_n:.3f} rad/s\nζ = {zeta:.3f}\nR² = {r_squared:.3f}'
            else:
                textstr = f'MANUEL\nωn = {omega_n:.3f} rad/s\nζ = {zeta:.3f}\nR² = {r_squared:.3f}\nRMSE = {rmse:.3f}'
            
            props = dict(boxstyle='round', facecolor='lightblue', alpha=0.8)
            ax2.text(0.02, 0.98, textstr, transform=ax2.transAxes, fontsize=12,
                    verticalalignment='top', bbox=props)
            
        else:
            # Mode automatique : ajustement par optimisation
            print("Ajustement automatique de l'équation différentielle du second ordre...")
            
            result = fit_second_order_system(temps_array, experimental_data)
            
            if result[0] is not None:
                popt, pcov, rmse, r_squared, relative_error, y_pred = result
                A, omega_n, zeta, phi, offset = popt
                
                # Affichage des résultats
                print(f"\n=== RÉSULTATS DE L'AJUSTEMENT AUTOMATIQUE ===")
                print(f"Amplitude (A): {A:.4f}")
                print(f"Pulsation naturelle (ωn): {omega_n:.4f} rad/s")
                print(f"Fréquence naturelle (fn): {omega_n/(2*np.pi):.4f} Hz")
                print(f"Facteur d'amortissement (ζ): {zeta:.4f}")
                print(f"Déphasage (φ): {phi:.4f} rad")
                print(f"Décalage (offset): {offset:.4f}")
                print(f"\n=== MÉTRIQUES D'ERREUR ===")
                print(f"RMSE: {rmse:.4f}")
                print(f"R²: {r_squared:.4f}")
                print(f"Erreur relative moyenne: {relative_error:.2f}%")
                
                # Classification du système
                if zeta < 1:
                    print(f"Système sous-amorti (ζ < 1)")
                    print(f"Fréquence amortie: {omega_n * np.sqrt(1 - zeta**2):.4f} rad/s")
                elif zeta == 1:
                    print(f"Système à amortissement critique (ζ = 1)")
                else:
                    print(f"Système sur-amorti (ζ > 1)")

                # Tracé de la courbe théorique sur le premier graphique
                ax1.plot(temps_array, y_pred, 'r--', linewidth=2, 
                        label=f'Modèle ajusté (ζ={zeta:.3f})')
                ax1.legend(loc="upper right")

                # Deuxième graphique : comparaison et résidus
                ax2.plot(temps_array, experimental_data, 'b-', label='Données expérimentales', linewidth=2)
                ax2.plot(temps_array, y_pred, 'r--', label=f'Modèle ajusté (ζ={zeta:.3f})', linewidth=2)
                
                # Résidus
                residuals = experimental_data - y_pred
                ax2_twin = ax2.twinx()
                ax2_twin.plot(temps_array, residuals, 'g:', alpha=0.7, linewidth=1.5, label='Résidus')
                ax2_twin.set_ylabel('Résidus', color='g')
                ax2_twin.tick_params(axis='y', labelcolor='g')

                ax2.set_xlabel(ts.x_label)
                ax2.set_ylabel(ts.y_label)
                ax2.set_title(f'Ajustement Automatique vs Expérimental (R²={r_squared:.3f}, RMSE={rmse:.3f})')
                ax2.legend(loc="upper left")
                ax2_twin.legend(loc="upper right")
                ax2.grid(True, alpha=0.3)

                # Ajout de texte avec les paramètres
                textstr = f'AJUSTÉ\nωn = {omega_n:.3f} rad/s\nζ = {zeta:.3f}\nR² = {r_squared:.3f}\nRMSE = {rmse:.3f}'
                props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
                ax2.text(0.02, 0.98, textstr, transform=ax2.transAxes, fontsize=12,
                        verticalalignment='top', bbox=props)
                
            else:
                print("Échec de l'ajustement automatique de l'équation différentielle.")
                if fit_differential_equation:
                    ax2.text(0.5, 0.5, 'Échec de l\'ajustement\nautomatique de l\'équation différentielle', 
                            transform=ax2.transAxes, ha='center', va='center', 
                            fontsize=16, bbox=dict(boxstyle='round', facecolor='lightcoral'))

    plt.tight_layout()

    if save:
        plt.savefig(name, dpi=300, bbox_inches='tight')
    if show:
        plt.show()
    plt.clf()


def swap_column(ts, col1: int, col2: int) -> None:
    """
    description : La fonction permet d'échanger la position de deux colonnes.
    :param ts: Contient le tad construit
    :param col1: Contient l'indice de la première colonne
    :param col2: Contient l'indice de la seconde colonne
    :return: Ne retourne rien
    """
    ts.data[col1], ts.data[col2] = ts.data[col2], ts.data[col1]
    ts.labels[col1], ts.labels[col2] = ts.labels[col2], ts.labels[col1]