from route_optimizer import RouteOptimizer
from config import SPATIAL_CONFIG, setup_logger


def main():
    logger = setup_logger("Main")
    parquet_path = "data/emplacement-des-gares-idf.parquet"
    
    # Points de test (coordonnées du fichier original)  
    origin_coords = (2.301582862195426, 48.79715061389867)  # Bagneux
    destination_coords = (1.7437261161738455, 48.98632597135369)  # Limay
    
    logger.info("Démarrage de l'optimisation de trajet")
    logger.info(f"Origine: {origin_coords} | Destination: {destination_coords}")
    logger.info(f"Rayon de recherche: {SPATIAL_CONFIG['default_buffer_radius']}m")
    
    # Créer l'optimiseur
    optimizer = RouteOptimizer(parquet_path=parquet_path)
    
    # Trouver les itinéraires optimaux
    best_routes = optimizer.find_optimal_routes(
        origin_coords=origin_coords,
        destination_coords=destination_coords,
        buffer_radius=SPATIAL_CONFIG["default_buffer_radius"]
    )
        
    if len(best_routes) > 0:
        # Statistiques utiles
        if 'rabattement_distance' in best_routes.columns:
            avg_rab_dist = best_routes['rabattement_distance'].mean()
            logger.info(f"Distance moyenne de rabattement: {avg_rab_dist:.0f}m")
        
        if 'diffusion_distance' in best_routes.columns:
            avg_diff_dist = best_routes['diffusion_distance'].mean() 
            logger.info(f"Distance moyenne de diffusion: {avg_diff_dist:.0f}m")
        
        logger.debug("\nPremiers résultats:")
        logger.debug(f"\n{best_routes["geometry_ori"][:5]}")
        
        # Sauvegarder les résultats
        output_file = "data/itineraires_optimises.csv"
        best_routes.to_csv(output_file, index=False, quotechar="'")
        logger.info(f"💾 Résultats sauvegardés dans {output_file}")
    else:
        logger.warning("❌ Aucun itinéraire trouvé")


if __name__ == "__main__":
    main()