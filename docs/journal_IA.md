# Journal d'usage de l'IA

> Le format de ce journal reprend celui du livrable d'exemple ; les situations présentées ont été adaptées à notre projet. L'IA a servi de soutien ponctuel, et chaque ligne renvoie à un fichier de ce dépôt. Les prompts et les réponses sont résumés à partir du travail réalisé.

**Outils utilisés :** un assistant de code dans l'éditeur, et un chat pour les questions de méthode.

| Fichier ou étape | Aide demandée | Ce que l'IA a apporté | Gardé, modifié ou refusé |
|---|---|---|---|
| `backend/data.py` et `backend/sql/table_analyse.sql` | Comprendre le chargement des données et la construction de la table d'analyse. | Des pistes pour suivre le passage du CSV à SQLite puis à la requête SQL. | Les explications ont permis de mieux comprendre le flux ; les propositions de code ont été vérifiées avant d'être reprises. |
| `backend/model.py` | Comprendre certaines parties complexes du code et les méthodes, comme le `Pipeline`, le prétraitement des variables et K-means. | Des explications et des pistes de code pour avancer sur ces étapes. | Les idées utiles au backend ont été conservées ou adaptées ; les propositions trop complexes ou inadaptées ont été refusées. |
| `backend/train.py` et `backend/model.py` | Comprendre la séparation entraînement/test, la validation croisée et les métriques. | Des pistes pour interpréter la MAE et le R², et comparer le modèle à la baseline. | Les résultats ont été vérifiés avec le code et les données. L'accuracy a été écartée, car la cible est continue. L'interprétation définitive des performances et le choix des critères n'ont pas été confiés à l'IA. |
| `backend/train.py` et `docs/Model_Card.md` | Vérifier les interprétations concernant la stratification, la baseline et l'équité du modèle. | Des explications et des formulations possibles. | Les propositions ont été confrontées au code et aux données ; les affirmations non vérifiées ont été écartées afin d'éviter une interprétation erronée. La validation finale reste à la charge de l'équipe. |
| `docs/Model_Card.md` et `docs/note_synthese.md` | Gagner du temps dans la compréhension des méthodes, l'interprétation des résultats et la rédaction des documents du projet. | Des explications et une aide à la formulation. | Les documents ont été relus et corrigés pour rester cohérents avec les méthodes et les résultats effectivement obtenus. |
| `backend/service.py` | Chercher une manière de ne pas recharger le modèle à chaque prédiction. | Une piste de mise en cache du modèle. | Une solution simple a été retenue dans le backend ; les propositions ajoutant une complexité ou une dépendance inutile ont été refusées. |

## Bilan en 3 lignes

- Ce que l'IA nous a fait gagner : du temps dans la compréhension des méthodes, l'interprétation des résultats et la rédaction des documents du projet.

- L'erreur qui aurait pu nous coûter le plus cher : reprendre une interprétation ou une formulation sans la vérifier, notamment concernant la stratification des données, la baseline ou l'équité du modèle.

- Ce que nous ne lui confierions pas sans relecture : l'interprétation définitive des performances, le choix des critères de décision et la validation des résultats. Les propositions de l'IA doivent toujours être confrontées au code et aux données réels.
