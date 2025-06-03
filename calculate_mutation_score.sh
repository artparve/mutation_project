#!/bin/bash

LOG_FILE="mutmut.log"

# Проверка существования файла лога
if [ ! -f "$LOG_FILE" ]; then
    echo "Error: File $LOG_FILE not found!"
    exit 1
fi

# Извлечение последней строки
LAST_LINE=$(tail -1 "$LOG_FILE")
echo "$LAST_LINE"

arr=($LAST_LINE)

# Парсинг значений
for i in "${!arr[@]}"; do
  case "${arr[$i]}" in
    KILLED)     KILLED=${arr[$((i+1))]} ;;
    TIMEOUT)    TIMEOUT=${arr[$((i+1))]} ;;
    SUSPICIOUS) SUSPICIOUS=${arr[$((i+1))]} ;;
    SURVIVED)   SURVIVED=${arr[$((i+1))]} ;;
    SKIPPED)    SKIPPED=${arr[$((i+1))]} ;;
  esac
done

# echo "$KILLED $TIMEOUT $SUSPICIOUS $SURVIVED $SKIPPED"


# Проверка валидности данных
if [ -z "$KILLED" ] || [ -z "$SURVIVED" ]; then
    echo "Error: Failed to parse mutation data"
    exit 2
fi

# Расчет процента
TOTAL=$((KILLED + SURVIVED + SUSPICIOUS))
SCORE=$(echo "scale=2; $KILLED * 100 / $TOTAL" | bc)

echo "Mutation Score: ${SCORE}% (Killed: $KILLED, Suspicious: $SUSPICIOUS, Survived: $SURVIVED)" | tee mutation_score.txt
