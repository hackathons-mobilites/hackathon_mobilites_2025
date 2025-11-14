import datetime
import holidays  # pip install holidays

def velo_transportable(date=None):
    if date is None:
        date = datetime.datetime.now()
    else :
        date = datetime.datetime.strptime(date, "%Y%m%dT%H%M%S")
    
    # Jour de la semaine (lundi=0, dimanche=6)
    jour_semaine = date.weekday()
    heure = date.time()
    
    # Vérifier si jour férié (exemple pour la France)
    jours_feries = holidays.France(years=date.year)
    est_ferie = date.date() in jours_feries
    
    # Condition 1 : samedi (5), dimanche (6) ou jour férié → toute la journée
    if jour_semaine in (5, 6) or est_ferie:
        return True
    
    # Condition 2 : autres jours
    if (heure < datetime.time(6, 30) or
        datetime.time(9, 30) <= heure <= datetime.time(16, 30) or
        heure >= datetime.time(19, 0)):
        return True
        
    return False