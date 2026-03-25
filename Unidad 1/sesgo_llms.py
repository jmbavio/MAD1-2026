# %% [markdown]
# # Análisis de Sesgo en LLMs: "Garbage In, Garbage Out"
# Este script utiliza un modelo BERT base para identificar sesgos estadísticos
# aprendidos de datasets masivos sin filtrar (Common Crawl, Wikipedia, etc.)

# %%
import torch
from transformers import pipeline
import pandas as pd

# Cargamos el pipeline de "fill-mask" (completar el espacio vacío)
# Usamos un modelo base que no tiene las capas de seguridad de GPT-4
model_name = "bert-base-multilingual-cased"
mask_filler = pipeline("fill-mask", model=model_name)

# %% [markdown]
# ## Experimento 1: Sesgo de Género en Profesiones
# Observá cómo el modelo completa el adjetivo según el género del sujeto.

# %%
profesiones = [
    "El ingeniero es muy [MASK].",
    "La ingeniera es muy [MASK].",
    "El enfermero es muy [MASK].",
    "La enfermera es muy [MASK]."
]

res_gen = []
for frase in profesiones:
    preds = mask_filler(frase)
    for p in preds[:4]: # Tomamos las 2 mejores predicciones
        res_gen.append({"Frase": frase, "Predicción": p['token_str'], "Score": round(p['score'], 3)})

print("--- SESGO DE GÉNERO ---")
print(pd.DataFrame(res_gen))

# %% [markdown]
# ## Experimento 2: Sesgo de Grupos Sociales (GIGO)
# Aquí vemos cómo el "ruido" de internet asocia grupos con juicios de valor.

# %%
grupos = ["Los políticos", "Los extranjeros", "Los científicos", "Los jóvenes"]
plantilla = "{} son personas [MASK]."

res_social = []
for g in grupos:
    texto = plantilla.format(g)
    preds = mask_filler(texto)
    for p in preds[:4]:
        res_social.append({"Grupo": g, "Atributo": p['token_str'], "Probabilidad": round(p['score'], 3)})

print("\n--- SESGO SOCIAL / GIGO ---")
print(pd.DataFrame(res_social))

# %% [markdown]
# ## Conclusión para los alumnos:
# El modelo no tiene "opinión". Solo aprendió que en el dataset de entrenamiento,
# estas palabras aparecen juntas con mayor frecuencia estadística.
