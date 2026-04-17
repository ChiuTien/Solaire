-- Migration : Ajouter colonne rendement à la table Ressource
-- Cette colonne représente le rendement spécifique à chaque ressource
-- Pour les panneaux : rendement du panneau (ex: 40%)
-- Pour les batteries : rendement de conversion (ex: 95%)

ALTER TABLE Ressource
ADD rendement DECIMAL(10, 2) DEFAULT 100.0;

-- Note: Le rendement est en pourcentage (0-100)
-- Après cette migration, exécuter:
-- UPDATE Ressource SET rendement = 100.0 WHERE rendement IS NULL;
