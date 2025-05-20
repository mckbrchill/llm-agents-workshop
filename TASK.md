# Задание для самостоятельной работы

1. **Добавить в VT Agent Tool, которая может получать [информацию о доменах](https://docs.virustotal.com/reference/domain-info) (по аналогии с IP)**

2. **Добавить в схему агента для анализа командлайнов. Агент должен выполнять следующие функции:**
    -  Анализировать информацию в object.process.cmdline (процесс, флаги, параметры)
    - Для малоизвестных процессов искать [информацию в сети](https://docs.tavily.com/documentation/quickstart)
    - Генерировать результат в [формате JSON](https://docs.mistral.ai/capabilities/structured-output/json_mode/)

```
{
  "cmdline_analysis": {
    "main_process_name": str,
    "parent_process": str,
    "suspicions": list[str],
    "explanation": str,
    "severity": str,
    "confidence": str
    }
}
```