import plotly.graph_objects as go

def generer_page(df, zones_eqh, zones_eql, order_blocks, trendlines_hautes, trendlines_basses, nom_fichier="analyse_btc.html"):
    fig = go.Figure()
    
    fig.add_trace(go.Candlestick(
        x=df["temps_ouverture"],
        open=df["ouverture"],
        high=df["haut"],
        low=df["bas"],
        close=df["cloture"],
        name="BTC/USDT",
        increasing_line_color="#26a69a",
        decreasing_line_color="#ef5350"
    ))
    
    for zone in zones_eqh:
        fig.add_hline(
            y=zone["prix"],
            line_color="violet",
            line_dash="dot",
            annotation_text=f"EQH ({zone['touches']} touches) - Zone de VENTE",
            annotation_position="top right"
        )
    
    for zone in zones_eql:
        fig.add_hline(
            y=zone["prix"],
            line_color="blue",
            line_dash="dot",
            annotation_text=f"EQL ({zone['touches']} touches) - Zone d'ACHAT",
            annotation_position="bottom right"
        )
    
    for ob in order_blocks:
        couleur = "rgba(38,166,154,0.3)" if ob["direction"] == "haussier" else "rgba(239,83,80,0.3)"
        label = "OB 5 etoiles ACHAT" if ob["direction"] == "haussier" else "OB 5 etoiles VENTE"
        fig.add_hrect(
            y0=ob["bas"], y1=ob["haut"],
            fillcolor=couleur,
            line_width=1,
            annotation_text=label,
            annotation_position="left"
        )
    
    for tl in trendlines_hautes:
        points = sorted(tl["points"], key=lambda p: p[0])
        x_vals = [df["temps_ouverture"].iloc[p[0]] for p in points]
        y_vals = [p[2] for p in points]
        fig.add_trace(go.Scatter(
            x=x_vals, y=y_vals, mode="lines",
            line=dict(color="orange", width=2),
            name=f"Trendline resistance ({tl['touches']} touches)"
        ))
    
    for tl in trendlines_basses:
        points = sorted(tl["points"], key=lambda p: p[0])
        x_vals = [df["temps_ouverture"].iloc[p[0]] for p in points]
        y_vals = [p[2] for p in points]
        fig.add_trace(go.Scatter(
            x=x_vals, y=y_vals, mode="lines",
            line=dict(color="cyan", width=2),
            name=f"Trendline support ({tl['touches']} touches)"
        ))
    
    fig.update_layout(
        title="Analyse BTC/USDT - Zones detectees automatiquement",
        xaxis_title="Temps",
        yaxis_title="Prix (USDT)",
        template="plotly_dark",
        xaxis_rangeslider_visible=False,
        height=800
    )
    
    fig.write_html(nom_fichier)
    return nom_fichier