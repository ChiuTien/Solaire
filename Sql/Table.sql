-- Création de la table Materiel
CREATE TABLE Materiel (
    id INT PRIMARY KEY IDENTITY(1,1),
    nom NVARCHAR(100)
);

-- Création de la table Consommation
CREATE TABLE Consommation (
    id INT PRIMARY KEY IDENTITY(1,1),
    idMateriel INT,
    puissance INT,
    heureDebut TIME,
    heureFin TIME
);

-- Création de la table Ressource
-- Note : DOUBLE(10,2) devient FLOAT ou DECIMAL(10,2). DECIMAL est préférable pour la précision.
CREATE TABLE Ressource (
    id INT PRIMARY KEY IDENTITY(1,1),
    nom NVARCHAR(100),
    puissanceTheorique DECIMAL(10,2),
    puissanceReelle DECIMAL(10,2)
);

-- Création de la table ConfigJournee
CREATE TABLE ConfigJournee (
    id INT PRIMARY KEY IDENTITY(1,1),
    heureDebut TIME,
    heureFin TIME,
    rendement INT,
    idStatut INT
);

-- Création de la table Resultat
CREATE TABLE Resultat (
    id INT PRIMARY KEY IDENTITY(1,1),
    idConfigJournee INT,
    idRessource INT
);

-- Création de la table statut 
CREATE TABLE Statut (
    id INT PRIMARY KEY IDENTITY(1,1),
    nom VARCHAR(100)
);

CREATE TABLE ChargeBatterie(
    id INT PRIMARY KEY IDENTITY(1,1),
    heureDebut TIME,
    heureFin TIME,
    Capacite  FLOAT,
    PuisanceNecessaire FLOAT
);