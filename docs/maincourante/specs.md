Specifications de la main courante
==================================


Definition des concepts de donnees
----------------------------------


Definition d'un message (similaire a un evenement)

+ Identifiant unique du message/evenement
+ Identifiant unique de l'operation associee
+ Type d'operation sur le message (creation/suppression/modification)
+ Identifiant du message parent (optionnel)
+ Identifiant de l'operateur pour cette operation
+ Horodatage
+ Expediteur (si creation)
+ Recipiendaire (si creation)
+ Corps du mesage (si creation/modification)
+ Raison de la suppresion (si suppression)

Definition d'une operation

+ Identifiant unique
+ Nom
+ Status (en cours/cloturee)

Definition de l'IHM
-------------------

IHM : login + mot de passe

* Si operateur => page unique 'principale'
* Si root => page 'principale' par defaut + liens en haut
  vers gestion utilisateurs, gestion operatoins, vocabulaire,
  page principale

Note : pour la page principale : bouton logout


Definition des differentes fonctions
------------------------------------

* Affichage liste des messages

I/F : page "principale"

1 liste de messages par ordre 'plus recent d'abord'

Marquage :

+ Horodatage + expediteur + recipiendaire + contenu
+ Flag message modifie avec code couleur + click possible pour expand
  historique des modifications
+ Icone pencil pour modification de message (sauf si message supprime)
+ Icone poubelle pour suppression message 

Gestion en "push" des nouveaux messages provenant des autres operateurs

* Ajouter un message

I/F : page "principale" 

2 text box  + 1 text area 

+ De : auto completion sur les indicatifs
+ Vers : auto completion sur les indicatifs
+ Corps du message : (prio 2) auto completion avec un vocabulaire commun

1 bouton submit : rajout a la liste des messages + horodatage
1 bouton clear/reset : suppresion des contenus 2 text box + text area

Navigation TAB et MAJ tab entre les 4 controles

* Modifier un message

I/F : page "principale" depuis l'icone pencil correspondant a 
un message

Apparition d'un text area avec message existant + bouton submit et cancel

+ Submit : enregistre le nouveau message (mais archivage de l'ancien avec
enregistrement de l'id du message parent) + mise a jour de la liste 
affichee avec modification du flag
+ Cancel

Si deux modifications concurrentes : on garde les deux

* Supprimer un message
 
I/F : page "principale" depuis l'icone poubelle correspondant a un message

Affichage d'une text box avec raison de suppression + boutons submit
et cancel

+ Submit : la supression est loggee (affichage grise dans la liste des 
message) 

* Definition vocabulaire indicatifs (=expediteur et recipiendaire)

I/F : page "Vocabulaire"

Text box + liste + bouton Add

+ Text box : on rentre un mot de vocabulaire
+ Liste : liste des mots deja rentres avec une croix pour effacer

Note : pas d'edition possible
Note : lors de la supression ca n'a pas d'impact les messages deja
saisis mais ca ne sera plus propose a la completion

* Identifier un utilisateur

I/F : page "Ouverture"

login + mot de passe + selecteur d'operation


* Ajouter un utilisateur operateur (reserve a root)

I/F : page "gestion utilisateurs"

* Modifier un utilisateur operateur (reserve a root)

I/F : page "gestion utilisateurs"

Desactivation/re-activation

* Generer un PDF

I/F : page "gestion operations" (reserve a root)

Submit : creation d'un PDF avec un filigrane "en cours"
si operation non cloturee


* Clore une operation

I/F : page "gestion operations" (reserve a root)

Submit : confirmation (oui/cancel) + generation d'un PDF et modification
du status de l'operation dans la base

* Creer une operation (reserve a root)

I/F : page "gestion operations"

Text box + submit

+ Text box : nom de l'operation
+ Submit : creation de l'operation et changement de l'operation par defaut
