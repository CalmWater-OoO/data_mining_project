Equipe : Kyllian BERNARD, Marie DE AMORIM PEREIRA DA SILVA, Miki PAAGALUA-HENRY, Sofiane TOUZANI
Dataset : Médical Cost Personnal Dataset - Kaggle 
Client imaginé : Une compagnie d'assurance santé, et plus particulièrement son service de tarification et d'analyse des risques.

1. La question business
Une compagnie d'assurance souhaite mieux anticiper les dépenses médicales associés à ses assurés.
Comment estimer les frais médicaux d'un individu à partir de ses caractéristiques pour mieux comprendre les profils associés aux dépenses les plus élevées ?

2. Les 5 questions du cours 1

| Question | Réponse | 
| ----- | ----- | 
| Qu'appelle-t-on exactement la cible ? | Le montant des frais médicaux (charges) associé à chaque assuré, exprimé en dollars. | 
| Que fera le client du résultat ? | Le service de tarification pourra utiliser les estimations pour analyser les dépenses médicales et mieux comprendre les profils d'assurés et aider à l'analyse des risques. | 
| Combien de cas peut-il traiter ? | Le modèle peut produire une estimation pour chaque profil renseigné, sans limite de capacité particulière identifiée dans le projet. | 
| Combien coûte une erreur, combien rapporte une bonne décision ? | Une sous-estimation peut conduire à sous-évaluer les dépenses médicales, tandis qu'une surestimation peut conduire à les surévaluer mais ces coûts ne sont pas renseigner dans le projet. | 
| Quelles données, depuis quand, et qui les connaît ? | 1 338 observations issues du dataset Medical Cost Personal Dataset (Kaggle), portant sur des assurés aux États-Unis. Les données contiennent notamment l'âge, le sexe, l'IMC, le nombre d'enfants, le statut de fumeur, la région et les frais médicaux. La période exacte de collecte n'est pas précisée. | 

3. Les familles de méthodes prévues

| Famille (carte du data mining) | Pour répondre à quelle question du client ? | 
| ----- | ----- | 
| Supervisé : régression (Random Forest) | Quel montant de frais médicaux peut-on estimer pour un assuré à partir de ses caractéristiques ? | 
| Non supervisé : clustering (K-means) | Quels grands profils d'assurés peut-on identifier selon leur âge, leur IMC et leurs frais médicaux ? | 
| Bonus : aucun prévu | ----- | 

4. Comment saura-t-on que ca marche ?

- Baseline (ce qu'on fait sans modèle) : Prédire le montant moyen des frais médicaux pour tous les assurés. MAE de référence : environ 9 644$.
- Métrique qui compte pour le client : L'erreur absolue moyenne (MAE), qui mesure l'écart moyen entre les frais réels et les frais estimés.
- Succès : Obtenir une MAE nettement inférieur à celle de la baseline sur le jeu de test. Le modèle Random Forest atteint une MAE d'environ 2 504$.

5. Les risques déjà vus 

Le dataset est assez limité (1 338 observations) et porte uniquement sur des assurés aux Etats-Unis. Les résultats ne sont donc pas généralisables directement à d'autres populations. Certaines variables comme le sexe, l'âge ou encore le statut de fumeur peuvent soulever des questions d'équité. Pour finir, les frais médicaux peuvent dépendre d'autres facteurs qui ne sont pas présent dans le dataset.

6. Qui a fait quoi 

| Membre | Rôle principal | 
| ----- | ----- | 
| Kyllian | Organisation du projet + documentation des fichiers md | 
| Marie | Frontend | 
| Miki | Tests unitaires + Soutenance| 
| Soufiane | Backend | 
