-- Migration : Ajouter colonnes quantite, prix_unitaire et puissance_nominale à la table Ressource
-- puissance_nominale: puissance d'UN SEUL panneau (ce que dit le vendeur) - ne change pas
-- quantite: nombre de panneaux/batteries nécessaires
-- prix_unitaire: prix par unité

ALTER TABLE Ressource
ADD puissance_nominale DECIMAL(10, 2) DEFAULT NULL;

ALTER TABLE Ressource
ADD quantite INT DEFAULT 0;

ALTER TABLE Ressource
ADD prix_unitaire DECIMAL(10, 2) DEFAULT 0.0;

-- Note: 
-- puissanceTheorique: puissance théorique TOTALE requise (sera écrasée à chaque calcul)
-- puissance_nominale: puissance d'UN SEUL panneau (reste inchangée, saisie une fois) 
-- quantite: sera calculée automatiquement : quantite = CEILING(puissanceTheorique / puissance_nominale)
-- prix_unitaire: prix par unité, entré manuellement
-- Prix total final = quantite * prix_unitaire
