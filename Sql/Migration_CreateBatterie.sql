-- Migration : Créer table Batterie
-- Cette table stocke les batteries avec leurs capacités

CREATE TABLE Batterie (
    id INT PRIMARY KEY IDENTITY(1,1),
    capaciteTheorique DECIMAL(10, 2) NULL,
    capaciteReelle DECIMAL(10, 2) NULL,
    rendement DECIMAL(10, 2) DEFAULT 100.0,
    dateCreation DATETIME DEFAULT GETDATE()
);

DROP TABLE Batterie;

-- Note: Cette table est séparée de Ressource
-- Les batteries spécifiques sont stockées ici
-- Les ressources (panneau solaire) restent dans Ressource

-- Exemple d'insertion:
-- INSERT INTO Batterie (capaciteTheorique, capaciteReelle, rendement)
-- VALUES (240.0, 360.0, 95.0);
