# opflow-python-example

## Requirement installation

```shell
pip install -r requirements.txt
```

## Execute RPC example

Executes RPC worker with `localhost` Rabbitmq:

```shell
python main/fibonacci_rpc_worker.py
```

For remote Rabbitmq Server (example: 192.168.1.77):

```shell
python main/fibonacci_rpc_worker.py \
		--uri=username:password@192.168.1.77
```

Default RPC master (`localhost` and sequence of number from 20 to 40):

```shell
python main/fibonacci_rpc_master.py
```

For other configuration, use the following command:

```shell
python main/fibonacci_rpc_master.py \
		--uri=username:password@192.168.1.77 \
		--number=36
```

