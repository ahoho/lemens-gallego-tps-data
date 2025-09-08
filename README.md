# OrdinalTPS Experiments

The idea is to query a model to place a text item on a left--right scale with `basic` and `technical` prompts. `technical` prompts constitute the `with context` setting

## British Party Manifestos

We have data annotated by both experts and crowdworkers. We would like to measure the OrdinalTPS of the technical prompt when the target is the expert label and see if the technical prompt persuades the model to look more like the expert ratings.

### Data
The main file is `./british-party-manifestos/processed/manifestos_filtered.jsonl`. The structure is as follows

```json
{
    "id":"10000021",
    "source":"Crowd",
    "policy_area":"Economic",
    "party":"Conservatives",
    "year":1987,
    "sentence_text":"We have fostered a new spirit of enterprise.",
    "n_annotators":14,
    "label_mean":3.7142857143,
    "label_std":0.6112498455,
    "label_ordinal":4
}
```

The important variables are:
  * `sentence_text`: the text to be annotated
  * `policy_area`: whether the text corresponds to `"Social"` or `"Economic"` policy (which have different prompts, see below)
  * `label_ordinal`: the label on a 1 to 5 scale where 1 is liberal/left-wing and 5 is conservative/right wing
  * `source`: Whether the item was annotated by `"Crowd"` workers or `"Experts"`. In the data, sentences are annotated by both experts and crowdworkers

### Prompts

Prompts are in `./british-party-manifestos/prompts/`

Use the `social` or `economic` prompts for the data filtered to the corresponding `policy_area`.

They are templates, so you can use them as follows:

```python
with open("<prompt_file>.txt") as infile:
     template = infile.read()

for example in data:
    prompt = template.format(text=example["sentence_text"])     
```

### Experimentation

**Setup**: Filter the data to the `"Social"` `policy_area` and to `"Experts"`, compute OrdinalTPS against the `label_ordinal`, comparing the `prompt_social_basic.txt` and `prompt_social_technical.txt` prompts. 

Then repeat, filtering to the `"Social"` data and using the corresponding prompts.

We should favor the largest model for these experiments.

**Qualitative**: For each `policy_area`, provide a list of items with the highest 10 TPS scores, the lowest 10, and the 10 closest to 0.

The result can be a CSV with all the columns of the original data, plus the OrdinalTPS score (and, if possible, the model probabilities over scores from 1 to 5).

**Quantitative**: Compute the difference between the `label_mean` for the `Experts` and the `Crowd`. Show a scatter plot of this difference against the `OrdinalTPS`. separately for each `policy_area`. Compute the pearson and spearman correlations.

As an additional check, perhaps also plot the absolute difference.

It may also be worth filtering the data such that the crowd data has higher agreement (`label_std<0.5`).

**Additional check**: Compute the `OrdinalTPS` where the target comes from the *crowd*. I believe hypothesis is that these will be smaller on average than for the expert labels.