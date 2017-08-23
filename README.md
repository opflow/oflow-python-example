# opflow-python-example

## Requirement installation

```
pip install -r requirements.txt
```

## Run RPC example

Executes RPC worker with `localhost` Rabbitmq:

```
python main/fibonacci_rpc_worker.py
```

For remote Rabbitmq Server (example: 192.168.1.77):

```
python main/fibonacci_rpc_worker.py username:password@192.168.1.77
```

Default RPC master (`localhost` and sequence of number from 20 to 40):

```
python main/fibonacci_rpc_master.py
```

For other configuration, use the following command:

```
python main/fibonacci_rpc_master.py \
		--uri=username:password@192.168.1.77
		--number=36
```
