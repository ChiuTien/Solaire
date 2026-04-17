USE Solaris;


INSERT INTO Solaris.dbo.Statut (nom) VALUES
	 (N'matin'),
	 (N'midi'),
	 (N'soir');


INSERT INTO Solaris.dbo.Materiel (nom) VALUES
	 (N'Refrigerateur'),
	 (N'TV'),
	 (N'Ventillateur'),
	 (N'Lampe'),
	 (N'Routeur wifi');


-- RESSOURCES = PANNEAUX SOLAIRES SEULEMENT
INSERT INTO Solaris.dbo.Ressource (nom, puissanceTheorique, puissanceReelle) VALUES
	 (N'Panneau solaire scolaire', 931.25, 372.50),
	 (N'Panneau solaire secondaire', 500.00, 200.00);


-- BATTERIES = TABLE SEPAREE
INSERT INTO Solaris.dbo.Batterie (capaciteTheorique, capaciteReelle, rendement) VALUES
	 (2205.00, 1470.00, 95.0),
	 (3440.00, 2580.00, 90.0);


INSERT INTO Solaris.dbo.Consommation (idMateriel, puissance, heureDebut, heureFin) VALUES
	 (1, 120, '06:00:00', '17:00:00'),
	 (2, 55, '08:00:00', '12:00:00'),
	 (3, 75, '10:00:00', '14:00:00'),
	 (4, 10, '17:00:00', '19:00:00'),
	 (2, 55, '17:00:00', '19:00:00'),
	 (5, 10, '19:00:00', '06:00:00'),
	 (1, 120, '19:00:00', '06:00:00'),
	 (4, 10, '19:00:00', '23:00:00');

INSERT INTO Solaris.dbo.ConfigJournee (heureDebut, heureFin, rendement, idStatut) VALUES
	 ('06:00:00', '17:00:00', 40, 1),
	 ('17:00:00', '19:00:00', 30, 2),
	 ('19:00:00', '06:00:00', 0, 3);


-- RESULTATS = Association Config + Ressources (panneaux)
INSERT INTO Solaris.dbo.Resultat (idConfigJournee, idRessource) VALUES
	 (1, 1),
	 (1, 1),
	 (2, 1),
	 (2, 2),
	 (1, 1),
	 (2, 2),
	 (1, 1),
	 (2, 2);    


-- CHARGE BATTERIE = Heures de charge de la batterie
INSERT INTO Solaris.dbo.ChargeBatterie (heureDebut, heureFin, Capacite, PuisanceNecessaire) VALUES
	 ('10:00:00', '14:00:00', 2205.0, 551.25),
	 ('10:00:00', '16:00:00', 3440.0, 860.00),
	 ('10:00:00', '15:00:00', 3440.0, 688.00),
	 ('11:00:00', '15:00:00', 2205.0, 551.25),
	 ('10:00:00', '17:00:00', 1470.0, 210.00);