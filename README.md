# Movie recommendation app

Projet réalisé pour le cours de Cloud Computing de l'Ensae.

Pour lancer le projet : 

```
docker build -t flask_app .
docker run -t -p 5000:5000 --name flask_app flask_app
```

L'application devrait ensuite être trouvable à l'addresse localhost:5000 de votre navigateur.

La partie flask de l'application est inspirée par le tutoriel de Corey Schafer : https://www.youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH, et réutilise certaines parties de son code (notamment pour le système de login et le style graphique).
On a utilisé plusieurs méthodes pour implémenter le système de recommandation: Factorisation matricielle/ Plus proches voisins et des méthodes de Machine learning ( régression linéaire/ arbre de décision).

Le système utilisé pour l'application est le système de factorisation matricielle. Puisque c'est un système assez simple, pour avoir des recommendations qui ont du sens il faudrait noter un nombre important de films. 

Les trois systèmes de recommendations sont illustrés par des notebooks.

Il y a plusieurs onglets sur l'application. Un premier onglet pour rechercher des films, un second pour voir les films que l'utilisateur a noté et un troisième qui donne les recommendations. Pour pouvoir noter les films, il faut s'inscrire (register) puis se connecter. Il faut pour cela renseigner une adresse mail un username et un mot de passe, mais ceux-ci peuvent être quelconques ( pas de validation de mail, c'était uniquement plus logique d'ajouter un système de connexion à l'interface ).
