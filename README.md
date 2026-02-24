# Graph API

Приложение умеет:
- генерировать граф
- строить MST (алгоритм Краскала)
- искать кратчайший путь по MST
- удалять node или edge из переданного графа

## Запуск сервера

Из корня проекта:

```bash
python main.py server --host 127.0.0.1 --port 8000
```

После запуска сервер доступен по адресу:

`http://127.0.0.1:8000`

## Формат графа

Во всех endpoint'ах, где передаётся граф, используется формат:

```json
{
  "graph": {
    "nodes": [
      {"id": 0, "x": 0.1, "y": 0.2},
      {"id": 1, "x": 0.4, "y": 0.8}
    ],
    "edges": [
      {"u": 0, "v": 1, "w": 5}
    ],
    "obstacles": []
  }
}
```

## Endpoint'ы

### 1) Получить сгенерированный граф

`GET /graph?n=15&obstacle_prob=0.2`

Пример:

```bash
curl "http://127.0.0.1:8000/graph?n=10&obstacle_prob=0.25"
```

Ответ:

```json
{
  "graph": {
    "nodes": [...],
    "edges": [...],
    "obstacles": [...]
  }
}
```

### 2) Построить MST для переданного графа

`POST /mst`

Пример:

```bash
curl -X POST "http://127.0.0.1:8000/mst" \
  -H "Content-Type: application/json" \
  -d '{
    "graph": {
      "nodes": [{"id":0,"x":0.1,"y":0.2},{"id":1,"x":0.4,"y":0.8}],
      "edges": [{"u":0,"v":1,"w":5}],
      "obstacles": []
    }
  }'
```

Ответ:

```json
{
  "mst": [[0, 1, 5]]
}
```

### 3) Получить shortest path по переданным node'ам

`POST /shortest-path`

Важно: текущая реализация принимает готовый `mst`, а не `graph`.

Тело запроса:
- `start` (int)
- `goal` (int)
- `mst` (массив рёбер формата `[u, v, w]`)

Пример:

```bash
curl -X POST "http://127.0.0.1:8000/shortest-path" \
  -H "Content-Type: application/json" \
  -d '{
    "start": 0,
    "goal": 3,
    "mst": [[0,1,7],[1,2,2],[2,3,4]]
  }'
```

Ответ:

```json
{
  "start": 0,
  "goal": 3,
  "reachable": true,
  "distance": 13,
  "path": [0, 1, 2, 3]
}
```

### 4) Удалить node из графа

`POST /graph/remove-node`

Тело запроса:
- `graph` (объект графа)
- `node_id` (int)

Пример:

```bash
curl -X POST "http://127.0.0.1:8000/graph/remove-node" \
  -H "Content-Type: application/json" \
  -d '{
    "graph": {
      "nodes": [{"id":0,"x":0.1,"y":0.2},{"id":1,"x":0.4,"y":0.8}],
      "edges": [{"u":0,"v":1,"w":5}],
      "obstacles": []
    },
    "node_id": 1
  }'
```

Ответ:

```json
{
  "graph": {
    "nodes": [...],
    "edges": [...],
    "obstacles": [...]
  }
}
```

### 5) Удалить edge из графа

`POST /graph/remove-edge`

Тело запроса:
- `graph` (объект графа)
- `u` (int)
- `v` (int)

Пример:

```bash
curl -X POST "http://127.0.0.1:8000/graph/remove-edge" \
  -H "Content-Type: application/json" \
  -d '{
    "graph": {
      "nodes": [{"id":0,"x":0.1,"y":0.2},{"id":1,"x":0.4,"y":0.8}],
      "edges": [{"u":0,"v":1,"w":5}],
      "obstacles": []
    },
    "u": 0,
    "v": 1
  }'
```

Ответ:

```json
{
  "graph": {
    "nodes": [...],
    "edges": [...],
    "obstacles": [...]
  }
}
```

## Типичные ошибки

- `400 Invalid JSON` - некорректный JSON
- `400 Field ... is required` - не хватает обязательного поля
- `400 Node ... does not exist` - попытка удалить несуществующую вершину
- `400 Edge (u, v) does not exist` - попытка удалить несуществующее ребро
