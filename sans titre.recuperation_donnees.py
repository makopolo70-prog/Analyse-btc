Parfait, le premier fichier `requirements.txt` est prêt ! On passe au deuxième fichier.

**Créez un nouveau fichier** nommé exactement **`recuperation_donnees.py`** (même méthode : bouton "+" dans QuickEdit), et collez-y ce contenu :

```
import requests
import pandas as pd

def recuperer_bougies(symbole="BTCUSDT", intervalle="15m", limite=200):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbole,
        "interval": intervalle,
        "limit": limite
    }
    
    reponse = requests.get(url, params=params)
    reponse.raise_for_status()
    donnees = reponse.json()
    
    colonnes = [
        "temps_ouverture", "ouverture", "haut", "bas", "cloture", "volume",
        "temps_fermeture", "volume_quote", "nb_trades",
        "volume_achat", "volume_quote_achat", "ignorer"
    ]
    df = pd.DataFrame(donnees, columns=colonnes)
    
    df["temps_ouverture"] = pd.to_datetime(df["temps_ouverture"], unit="ms")
    for col in ["ouverture", "haut", "bas", "cloture", "volume"]:
        df[col] = df[col].astype(float)
    
    return df[["temps_ouverture", "ouverture", "haut", "bas", "cloture", "volume"]]
```

Dites-moi quand c'est collé et enregistré.