LINE WORKS & ChatGPT Sample
====

## Prepare environment settings

See and copy .env.sample to .env
```
$ cp .env.sample .env
```

After setting environment variables
```
$ source .env
$ echo $OPENAI_API_KEY
xxxxxxx
```

## Usage

Run server
```sh
$ pip install -r requirements.txt
$ uvicorn main:app --reload
```

## dev mode

Run server
```sh
$ pip install -r requirements.txt
$ uvicorn main:app --reload
```

If you use ngrok as dev mode,
```sh
$ ngrok http 8000
```

## prod mode

```
# uvicorn main:app --port 80 --host 0.0.0.0
```

## Author

[shiraco](https://github.com/shiraco)