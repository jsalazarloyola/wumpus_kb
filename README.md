# Wumpus KB

Implementación del mundo de Wumpus con una base de conocimientos basada en [lógica de primer orden](https://en.wikipedia.org/wiki/First-order_logic)

Para ejecutar, se puede correr el archivo `wumpus.py`.

La base de conocimientos (*knowledge base*) es implementada en el archivo `kb.py`, que include dos funciones de actualización, `KnowledgeBase.update_safety` y `KnowledgeBase.update_kb`, que infieren qué celdas son seguras y dónde podrían estar el wumpus y los pozos, respectivamente, utilizando una implementación del algoritmo de *forward chaining*, que consiste *grosso modo* en aplicar todas las reglas de inferencia sobre los hechos conocidos y actualizar la base, hasta que ya no queden más actualizaciones que hacer. En pseudocódigo, corresponde a hacer lo siguiente:

```
changed = True
while changed:
    changed = False
    for room in rooms:
        if check_facts(room, kb) changed kb:
            changed = True
```

En el caso de `update_safety`, que busca deducir cuáles cuartos no visitados, pero vecinos a los visitados, son seguros, el "`check_facts`" correspondería a comprobar si dichos vecinos son seguros (podemos inferir que no hay wumpus o pozos en ellos, o que no tienen hedor ni brizas, o que todos los vecinos son seguros). Si esta función cambia lo que se sabe (la base de conocimientos), se vuelven a revisar todos los cuartos. Una idea similar se aplica para actualizar las inferencias de ubicación de los pozos y el wumpus.

## Interfaz

La interfaz muestra una grilla de cuadros blancos, donde la posición del agente está en negro. El estado del agente aparece en el marco inferior de la ventana. En cada casilla, si hay algún aspecto percibido o algo que se deduzca, se marca con los siguientes caracteres:
- "S": la casilla tiene hedor (*smelly*).
- "B": la casilla tiene briza (*breezy*).
- "P?": la casilla podría tener un pozo (*pit*).
- "W?": la casilla podría tener al wumpus.

El agente se puede mover exclusivamente con las teclas WASD, en su significado habitual.
