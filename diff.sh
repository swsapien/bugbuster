#!/bin/bash

# Comprobar que se pasaron al menos dos parámetros
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <branch1> <branch2> [extensions]"
    exit 1
fi

# Ramas a comparar
BRANCH1="origin/$1"
BRANCH2="$2"

# Extensiones opcionales
EXTENSIONS="$3"

# Asegurarse de que las ramas existen
if ! git rev-parse --verify "$BRANCH1" >/dev/null 2>&1; then
    echo "Error: Branch $BRANCH1 does not exist."
    exit 1
fi

if ! git rev-parse --verify "$BRANCH2" >/dev/null 2>&1; then
    echo "Error: Branch $BRANCH2 does not exist."
    exit 1
fi

# Obtener la lista de archivos modificados de un ancestro en común
FILES=$(git diff --name-only "$BRANCH1"..."$BRANCH2" --)

# Comprobar si hay archivos modificados
if [ -z "$FILES" ]; then
    exit 0
fi

# Si se especificaron extensiones, filtrar los archivos
if [ -n "$EXTENSIONS" ]; then
    # Crear una expresión regular para las extensiones
    EXT_REGEX=$(echo "$EXTENSIONS" | tr ',' '|')
    FILES=$(echo "$FILES" | grep -E "\.($EXT_REGEX)$")
fi

# Comprobar si hay archivos modificados después del filtro
if [ -z "$FILES" ]; then
    echo "No files with specified extensions were found."
    exit 0
fi

# Declarar el array para almacenar las diferencias
declare -a DIFF_ARRAY

# Procesar cada archivo
for FILE in $FILES; do
    # Extraer las líneas añadidas (que comienzan con '+', pero no '++') y quitar el '+' inicial
    ADDED_LINES=$(git diff "$BRANCH1"..."$BRANCH2" -U0 -- "$FILE" -- | grep '^\+[^+]' | sed 's/^+//')

    # Verificar si el archivo tiene líneas añadidas
    if [ -n "$ADDED_LINES" ]; then
        # Crear un elemento del array con el nombre del archivo y las líneas de diferencia
        DIFF_ITEM="File: $FILE\n$ADDED_LINES"
        DIFF_ARRAY+=("$DIFF_ITEM")
    fi
done

# Mostrar el contenido del array con las diferencias
for ITEM in "${DIFF_ARRAY[@]}"; do
    echo -e "$ITEM"
    echo -e "\n---\n"
done
