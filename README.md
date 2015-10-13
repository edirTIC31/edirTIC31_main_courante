# edirTIC31_main_courante
Dépôt de l'EDIR-TIC de la DDUS31 lié au dévelopemment de la main courante

# Utilisation de django

Il vous faut Python >= 3.4, pip, et éventuellement virtualenv, voire virtualenvwrapper ou virtualfish.

```bash
cd edirtic
pip install -U -r requirements.dev.txt  # installation des dépendances
./manage.py migrate  # création du schéma de la base de données
./manage.py createsuperuser  # création d’un superuser
./manage.py runserver
```

Ensuite, vous pouvez aller sur http://localhost:8000/admin/, vous logger, créer un évènement.

Le reste de l’application est disponible sur http://localhost:8000/

## API REST

Par exemple: http://localhost:8000/api/v1/message/?format=json
