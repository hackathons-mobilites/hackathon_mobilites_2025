from abc import ABC, abstractmethod


class JobRunner(ABC):
    """
    Classe abstraite définissant le contrat de base pour l'exécution d'un traitement de données.

    Cette classe sert de modèle pour toutes les classes de type "Job" du projet.
    Chaque implémentation concrète doit définir la méthode `process()`
    qui contient la logique métier principale du job.
    """

    @abstractmethod
    def process(self):
        """
        Méthode abstraite principale à implémenter par toutes les classes héritées.

        Cette méthode doit contenir la logique complète du job :
        chargement des données, transformation, sauvegarde, etc.

        Raises:
            NotImplementedError: Si la méthode n'est pas implémentée dans la classe fille.
        """
        raise NotImplementedError(
            "La méthode 'process()' doit être implémentée dans la classe fille.")
