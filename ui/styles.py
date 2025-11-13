"""
Styles CSS pour l'interface utilisateur de Vel'Octo
"""

# CSS pour nettoyer les attributions de carte
MAP_ATTRIBUTION_CSS = """
<style>
.leaflet-control-attribution {
    font-size: 8px !important;
    background-color: rgba(255, 255, 255, 0.8) !important;
    padding: 2px 5px !important;
    max-width: 80px !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
}
.leaflet-control-attribution a {
    display: none !important;
}
</style>
<script>
function cleanAttributions() {
    var attribution = document.querySelector('.leaflet-control-attribution');
    if (attribution) {
        var text = attribution.textContent || attribution.innerText || '';

        // Simplifier le texte selon le contenu
        if (text.includes('OpenStreetMap')) {
            attribution.innerHTML = 'OSM';
        } else if (text.includes('CARTO')) {
            attribution.innerHTML = 'CARTO';
        } else if (text.includes('Esri')) {
            attribution.innerHTML = 'Esri';
        } else {
            // Nettoyer le texte générique
            text = text.replace('Leaflet', '').replace('|', '').trim();
            if (text.length > 12) {
                text = text.substring(0, 12) + '...';
            }
            attribution.innerHTML = text || 'Map';
        }
    }
}

// Nettoyer plusieurs fois pour s'assurer que ça marche
setTimeout(cleanAttributions, 100);
setTimeout(cleanAttributions, 500);
setTimeout(cleanAttributions, 1000);
setTimeout(cleanAttributions, 2000);

// Observer les changements
if (typeof MutationObserver !== 'undefined') {
    var observer = new MutationObserver(cleanAttributions);
    setTimeout(function() {
        var attribution = document.querySelector('.leaflet-control-attribution');
        if (attribution) {
            observer.observe(attribution, {
                childList: true,
                subtree: true,
                characterData: true
            });
        }
    }, 500);
}
</script>
"""

# CSS pour les boutons d'itinéraires
ROUTE_BUTTONS_CSS = """
<style>
.stButton > button {
    height: 80px !important;
    white-space: pre-line !important;
    line-height: 1.2 !important;
}
</style>
"""

# CSS pour le bouton options sans bords
EXPANDER_CSS = """
<style>
div[data-testid="stExpander"] {
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;
}
div[data-testid="stExpander"] > div {
    border: none !important;
    box-shadow: none !important;
}
div[data-testid="stExpander"] details {
    border: none !important;
}
div[data-testid="stExpander"] details summary {
    border: none !important;
    background: transparent !important;
    padding: 0.25rem 0 !important;
    border-radius: 0 !important;
    box-shadow: none !important;
}
div[data-testid="stExpander"] details summary:hover {
    background: rgba(0,0,0,0.05) !important;
}
/* Masquer le chevron/flèche */
div[data-testid="stExpander"] details summary::-webkit-details-marker {
    display: none !important;
}
div[data-testid="stExpander"] details summary::marker {
    display: none !important;
}
div[data-testid="stExpander"] details summary {
    list-style: none !important;
}
</style>
"""
