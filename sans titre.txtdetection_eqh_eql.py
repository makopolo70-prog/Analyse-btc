Oui, exactement ! Le fichier `recuperation_donnees.py` étant fait et enregistré, on crée maintenant le **troisième fichier**, nommé exactement **`detection_eqh_eql.py`** (même méthode : bouton "+" dans QuickEdit).

Une fois le fichier créé et ouvert, collez-y ce contenu :

```
import pandas as pd

def trouver_sommets_creux(df, ordre=3):
    sommets = []
    creux = []
    
    for i in range(ordre, len(df) - ordre):
        fenetre_haut = df["haut"].iloc[i-ordre:i+ordre+1]
        fenetre_bas = df["bas"].iloc[i-ordre:i+ordre+1]
        
        if df["haut"].iloc[i] == fenetre_haut.max():
            sommets.append((i, df["temps_ouverture"].iloc[i], df["haut"].iloc[i]))
        
        if df["bas"].iloc[i] == fenetre_bas.min():
            creux.append((i, df["temps_ouverture"].iloc[i], df["bas"].iloc[i]))
    
    return sommets, creux


def detecter_eqh_eql(df, tolerance_pct=1.0, min_points=3, ordre=3):
    sommets, creux = trouver_sommets_creux(df, ordre)
    
    def regrouper_par_tolerance(points, tolerance_pct):
        if not points:
            return []
        
        points_tries = sorted(points, key=lambda p: p[2])
        groupes = []
        groupe_actuel = [points_tries[0]]
        
        for point in points_tries[1:]:
            prix_reference = groupe_actuel[0][2]
            ecart_pct = abs(point[2] - prix_reference) / prix_reference * 100
            
            if ecart_pct <= tolerance_pct:
                groupe_actuel.append(point)
            else:
                if len(groupe_actuel) >= min_points:
                    groupes.append(groupe_actuel)
                groupe_actuel = [point]
        
        if len(groupe_actuel) >= min_points:
            groupes.append(groupe_actuel)
        
        return groupes
    
    zones_eqh = regrouper_par_tolerance(sommets, tolerance_pct)
    zones_eql = regrouper_par_tolerance(creux, tolerance_pct)
    
    resultat_eqh = [
        {"prix": sum(p[2] for p in g) / len(g), "touches": len(g), "points": g}
        for g in zones_eqh
    ]
    resultat_eql = [
        {"prix": sum(p[2] for p in g) / len(g), "touches": len(g), "points": g}
        for g in zones_eql
    ]
    
    return resultat_eqh, resultat_eql
```

Dites-moi quand c'est collé et enregistré, et on passera au quatrième fichier.