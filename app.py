python
from flask import Flask, send_file
import os

from recuperation_donnees import recuperer_bougies
from detection_eqh_eql import trouver_sommets_creux, detecter_eqh_eql
from detection_order_blocks import detecter_order_blocks_5_etoiles
from detection_trendlines import detecter_trendlines
from generation_page import generer_page

app = Flask(__name__)

def lancer_analyse_complete():
    df = recuperer_bougies("BTCUSDT", "15m", 300)
    
    sommets, creux = trouver_sommets_creux(df, ordre=3)
    zones_eqh, zones_eql = detecter_eqh_eql(df, tolerance_pct=1.0, min_points=3)
    order_blocks = detecter_order_blocks_5_etoiles(df, zones_eqh, zones_eql, sommets, creux)
    trendlines_hautes = detecter_trendlines(sommets, tolerance_pct=0.5, min_touches=3)
    trendlines_basses = detecter_trendlines(creux, tolerance_pct=0.5, min_touches=3)
    
    return generer_page(df, zones_eqh, zones_eql, order_blocks, trendlines_hautes, trendlines_basses)


@app.route("/")
def page_accueil():
    chemin_page = lancer_analyse_complete()
    return send_file(chemin_page)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
```

Une fois collé, cliquez sur **"Commit changes"** tout en bas pour l'enregistrer. Dites-moi quand c'est fait.
