```
from redis.commands.json.path import Path
import redis.commands.search.aggregation as aggregations
import redis.commands.search.reducers as reducers
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import NumericFilter, Query
idx=IndexDefinition( prefix=['node:'], index_type=IndexType.JSON )
dschema=( TextField( '$.node', as_name='node',sortable=True),
         TagField( '$.docker', as_name = 'docker', sortable=True ),
         TextField( '$.platform', as_name='platform',sortable=True),
         TextField( '$.python3', as_name='python3',sortable=True))
r.ft('info').create_index(dschema,definition=idx)
```

`curl http://localhost/api/hello`
