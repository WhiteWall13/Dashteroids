# Utiliser une image Python de base
FROM python:3.10

# Copier les fichiers source dans le conteneur
COPY . /app

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires pour GDAL
RUN apt-get update && apt-get install -y libgdal-dev

# Définir les variables d'environnement pour GDAL
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Installer les dépendances Python
RUN pip install -r requirements.txt

# Exposer le port sur lequel l'application Dash écoute
EXPOSE 8050

# Commande pour exécuter l'application Dash
CMD ["python", "main.py"]