-- 1. Vider les tables (l'ordre respecte les potentielles dépendances)
DELETE FROM Resultat;
DELETE FROM ConfigJournee;
DELETE FROM Consommation;
DELETE FROM Ressource;
DELETE FROM Materiel;

-- 2. Réinitialiser l'auto-incrément à 2
-- Note : Le prochain insert sera la valeur spécifiée + l'incrément.
-- Pour que le prochain ID soit 2, on initialise la graine à 1.
DBCC CHECKIDENT ('Materiel', RESEED, 0);
DBCC CHECKIDENT ('Consommation', RESEED,0);
DBCC CHECKIDENT ('Ressource', RESEED, 0);
DBCC CHECKIDENT ('ConfigJournee', RESEED, 0);
DBCC CHECKIDENT ('Resultat', RESEED, 0);
