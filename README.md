# Projet_trading

Lien vers l'adresse AppEngine :

    L'application est accessible en ligne à l'adresse suivante : https://projet-trading.ew.r.appspot.com

Exécution en local :

    Pour exécuter l'application Flask localement, suivez ces étapes :

        1. Assurez-vous d'avoir gunicorn installé. Sinon, installez-le à l'aide de la commande pip install gunicorn.

        2. Ouvrez un terminal dans le dossier du projet.

        3. Exécutez la commande suivante pour lancer l'application : gunicorn app:app -b 0.0.0.0:5000

        L'application sera maintenant accessible via le lien suivant : http://localhost:5000

Problème d'accès à l'adresse AppEngine :

    Actuellement, l'adresse AppEngine https://projet-trading.ew.r.appspot.com ne semble pas afficher l'application web Flask correctement. L'erreur pourrait être liée à une exécution incorrecte du fichier app.py.

    J'ai choisi d'utiliser Gunicorn pour le déploiement sur App Engine, car la documentation d'App Engine le recommande explicitement. Vous pouvez trouver cette recommandation dans la documentation d'App Engine pour Python 3 à l'adresse suivante : https://cloud.google.com/appengine/docs/standard/python3/runtime?hl=fr

Dossier "fonction" :

    Le dossier "fonction" n'est pas nécessaire pour le bon fonctionnement de l'application Flask. Il regroupe les fichiers utilisés pour l'analyse de la DataFrame, mais ils ne sont plus utiles pour l'application en production.

