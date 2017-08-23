# opflow-python-example

## Requirement installation

```shell
pip install -r requirements.txt
```

## Execute RPC example

Executes RPC worker with `localhost` Rabbitmq:

```shell
python main/rpc_worker.py
```

For remote Rabbitmq Server (example: 192.168.1.77):

```shell
python main/rpc_worker.py \
		--uri=username:password@192.168.1.77
```

Default RPC master (`localhost` and a sequence of numbers from 20 to 40):

```shell
python main/rpc_master.py
```

For other configuration, use the following command:

```shell
python main/rpc_master.py \
		--uri=username:password@192.168.1.77 \
		--number=36
```

## Execute Pub/Sub example

Invoke `Subscriber` with the following command:

```shell
python main/subscriber.py \
		--uri=username:password@192.168.1.77
```

Publish one number:

```shell
python main/publisher.py \
		--uri=username:password@192.168.1.77 \
		--number=36
```

or a sequence of numbers:

```shell
python main/publisher.py \
		--uri=username:password@192.168.1.77
```

