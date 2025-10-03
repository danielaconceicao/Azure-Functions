import azure.functions as func
import json
import base64
import tiktoken
from PIL import Image
import io
import azure.cognitiveservices.speech as speechsdk
import tempfile
import os
from dotenv import load_dotenv


app = func.FunctionApp()
load_dotenv()
speech_key = os.getenv("SPEECH_KEY")
speech_region = os.getenv("SPEECH_REGION")

# calcular fatorial
@app.route(route="factorial/{number}", methods=["GET"])
def factorial_route(req: func.HttpRequest) -> func.HttpResponse:

    # pega a chave do dicionario se nao existir retorne nada
    number = int(req.route_params.get("number", None))

    def factorial(number):
        if number == 0 or number == 1:
            return 1
        elif number < 0:
            return -1
        else:
            return number * factorial(number-1)

    result = factorial(number)
    if result == -1:
        return func.HttpResponse("Erro: Insira um numero inteiro valido", status_code=400)
    else:
        return func.HttpResponse(f"O fatorial de {str(number)} é {result}", status_code=200)


# contar tokens em uma string
@app.route(route="count_tokens", methods=["POST"])
def tokens_route(req: func.HttpRequest) -> func.HttpResponse:
    # recebe o texto do body JSON
    text = req.params.get('text')
    if not text:
        try:
            req_body = req.get_json()
            text = req_body.get('text')
        except ValueError:
            return func.HttpResponse('json invalido', status_code=400)

    if not text:
        return func.HttpResponse("texto é necessario", status_code=400)

    # carregar o modelo de codificação
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

    # conta os tokens
    tokens = encoding.encode(text)

    # encontar o numero de tokens verificando o comprimento
    token_count = len(tokens)

    # deu tudo certo? entao me retorne um resultado em json
    return func.HttpResponse(json.dumps({"tokens": token_count}), mimetype="application/json")


# converter imagem para preto e branco
@app.route(route="convert_image", methods=["POST"])
def convert_image_route(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # recebe do cliente um json com a string base64 da imagem que vem do frontend
        req_body = req.get_json()
        image_base64 = req_body.get('image')
        if not image_base64:
            return func.HttpResponse("parametro imagem é necessario", status_code=400)

        # decodificar base64 em bytes
        image_bytes = base64.b64decode(image_base64)

        # abrir imagem com pillow
        image = Image.open(io.BytesIO(image_bytes))

        # converte a imagem para preto e branco usando grayscale
        bw_image = image.convert("L")

        # salva a imagem convertida em memoria
        buffer = io.BytesIO()
        bw_image.save(buffer, format="PNG")
        bw_image_bytes = buffer.getvalue()

        # re-encoda a imagem em base64
        bw_image_base64 = base64.b64encode(bw_image_bytes).decode("utf-8")

        # retorna um novo base64 no json
        return func.HttpResponse(
            json.dumps({"image_bw": bw_image_base64}),
            mimetype="application/json"
        )

    # deu erro? entao me devolta o erro
    except Exception as e:
        return func.HttpResponse(f"Erro: {str(e)}", status_code=500)


# transcrever áudio
@app.route(route="transcribe", methods=["POST"])
def transcribe_audio(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        audio_base64 = req_body.get("audio")

        if not audio_base64:
            return func.HttpResponse("Campo audio é necessário", status_code=400)

        # decodifica base64 -> arquivo temporário
        audio_bytes = base64.b64decode(audio_base64)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            f.write(audio_bytes)
            audio_path = f.name

        # configura Azure Speech
        speech_config = speechsdk.SpeechConfig(
            subscription=speech_key,
            region=speech_region
        )
        audio_config = speechsdk.AudioConfig(filename=audio_path)
        recognizer = speechsdk.SpeechRecognizer(speech_config, audio_config)

        # transcreve
        result = recognizer.recognize_once()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return func.HttpResponse(
                json.dumps({"transcription": result.text}),
                mimetype="application/json"
            )
        else:
            return func.HttpResponse(f"Erro na transcrição: {result.reason}", status_code=500)

    except Exception as e:
        return func.HttpResponse(f"Erro: {str(e)}", status_code=500)
