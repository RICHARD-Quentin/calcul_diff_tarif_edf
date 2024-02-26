Ajouter son Bearer token et votre Personal ext id dans le fichier .env ( infos trouvables dans les requetes dans le dashboard d'edf dans les requetes XHR type consumptions)
```
BEARER_TOKEN=<votre token>
PERSONAL_EXT_ID=<votre id>
```

Ajouter votre tarif dans le fichier .env
```
TARIF_PERSO=<votre tarif>
```
Liste des tarifs disponibles:
- BASE
- HP/HC
- TEMPO

## Utilisation
```bash
make main
```