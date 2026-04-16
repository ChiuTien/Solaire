USE Solaris;

DELETE FROM Resultat;
DELETE FROM ConfigJournee;
DELETE FROM Consommation;
DELETE FROM Ressource;
DELETE FROM Materiel;
DELETE FROM Statut;

INSERT INTO Materiel (nom) VALUES
('Panneau solaire'),
('Batterie');

INSERT INTO Consommation (idMateriel, puissance, heureDebut, heureFin) VALUES
(1, 6, '06:00:00', '19:00:00'),
(1, 9, '19:00:00', '06:00:00'),
(2, 2, '20:00:00', '08:00:00');

INSERT INTO Ressource (nom, puissanceTheorique, puissanceReelle) VALUES
('Panneau solaire', 100.00, 40.00),
('Batterie', 100.00, 150.00);

INSERT INTO Statut (nom) VALUES
('matin'),
('midi'),
('soir');

INSERT INTO ConfigJournee (heureDebut, heureFin, rendement, idStatut) VALUES
('06:00:00', '19:00:00', 0.40, 1),
('19:00:00', '06:00:00', 0.50, 2),
('20:00:00', '08:00:00', 1.50, 3);

INSERT INTO Resultat (idConfigJournee, idRessource) VALUES
(1, 1),
(2, 1),
(3, 2);
