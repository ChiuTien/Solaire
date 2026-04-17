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


INSERT INTO Solaris.dbo.Ressource (nom,puissanceTheorique,puissanceReelle) VALUES
	 (N'panneaux scolaire',NULL,NULL),
	 (N'batterie',NULL,NULL),
	 (N'Panneau solaire scolaire',931.25,372.50),
	 (N'Batterie scolaire',2205.00,1470.00);



INSERT INTO Solaris.dbo.Consommation (idMateriel,puissance,heureDebut,heureFin) VALUES
	 (1,120,'06:00:00.0000000','17:00:00.0000000'),
	 (2,55,'08:00:00.0000000','12:00:00.0000000'),
	 (3,75,'10:00:00.0000000','14:00:00.0000000'),
	 (4,10,'17:00:00.0000000','19:00:00.0000000'),
	 (2,55,'17:00:00.0000000','19:00:00.0000000'),
	 (5,10,'19:00:00.0000000','06:00:00.0000000'),
	 (1,120,'19:00:00.0000000','06:00:00.0000000'),
	 (4,10,'19:00:00.0000000','23:00:00.0000000');

INSERT INTO Solaris.dbo.ConfigJournee (heureDebut,heureFin,rendement,idStatut) VALUES
	 ('06:00:00.0000000','17:00:00.0000000',40,1),
	 ('17:00:00.0000000','19:00:00.0000000',50,2),
	 ('19:00:00.0000000','06:00:00.0000000',150,3);


INSERT INTO Solaris.dbo.Resultat (idConfigJournee,idRessource) VALUES
	 (1,3),
	 (1,4),
	 (1,3),
	 (2,4),
	 (1,3),
	 (2,4),
	 (1,3),
	 (2,4);    


INSERT INTO Solaris.dbo.ChargeBatterie (heureDebut,heureFin,Capacite,PuisanceNecessaire) VALUES
	 ('06:00:00.0000000','17:00:00.0000000',3440.0,312.72727272727275),
	 ('06:00:00.0000000','17:00:00.0000000',3440.0,312.72727272727275),
	 ('06:00:00.0000000','19:00:00.0000000',3440.0,264.61538461538464),
	 ('06:00:00.0000000','19:00:00.0000000',3440.0,264.61538461538464),
	 ('06:00:00.0000000','19:00:00.0000000',1470.0,122.5);