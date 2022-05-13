# Movie recommendation app

Projet réalisé pour le cours de Cloud Computing de l'Ensae.

Pour lancer le projet : 

```
docker build -t flask_app .
docker run -t -p 5000:5000 --name flask_app flask_app
```

La partie flask de l'application est inspirée par le tutoriel de Corey Schafer : https://www.youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH, et réutilise certaines parties de son code (notamment pour le système de login et le style graphique).
On a utilisé plusieurs méthodes pour implémenter le système de recommandation: Factorisation matricielle/ Plus proches voisins et des méthodes de Machine learning ( régression linéaire/ arbre de décision).
