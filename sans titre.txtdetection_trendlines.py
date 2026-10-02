Parfait, on passe au **cinquième fichier**, nommé exactement **`detection_trendlines.py`** — avec la version corrigée qu'on a validée par les tests.

```
def detecter_trendlines(points, tolerance_pct=0.5, min_touches=3, max_affichees=5):
    trendlines_valides = []
    n = len(points)
    if n < min_touches:
        return trendlines_valides
    
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = points[i][0], points[i][2]
            x2, y2 = points[j][0], points[j][2]
            if x2 == x1:
                continue
            pente = (y2 - y1) / (x2 - x1)
            origine = y1 - pente * x1
            
            touches = []
            for p in points:
                x, y = p[0], p[2]
                y_droite = pente * x + origine
                ecart_pct = abs(y - y_droite) / y_droite * 100
                if ecart_pct <= tolerance_pct:
                    touches.append(p)
            
            if len(touches) >= min_touches:
                index_touches = tuple(sorted(p[0] for p in touches))
                trendlines_valides.append({
                    "pente": pente,
                    "origine": origine,
                    "touches": len(touches),
                    "points": touches,
                    "index_touches": index_touches
                })
    
    vues = set()
    filtrees = []
    for tl in sorted(trendlines_valides, key=lambda t: -t["touches"]):
        if tl["index_touches"] not in vues:
            vues.add(tl["index_touches"])
            filtrees.append(tl)
    
    return sorted(filtrees, key=lambda t: -t["touches"])[:max_affichees]
```

Dites-moi quand c'est collé et enregistré, et on passera à l'avant-dernier fichier.