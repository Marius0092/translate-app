import logging
from collections import namedtuple

import ctranslate2
import sentencepiece as spm
from flask import Flask, request, jsonify
from flask import logging as flask_logging
from flask_cors import CORS
from nltk import sent_tokenize


app = Flask(__name__)
CORS(app)


logger = flask_logging.create_logger(app)
logger.setLevel(logging.DEBUG)


models_paths = {
    "en-it": {
        "model": "models/enit/enit_ctranslate2",
        "source": "models/enit/source.spm",
        "target": "models/enit/target.spm",
    },
    "it-en": {
        "model": "models/iten/iten_ctranslate2/",
        "source": "models/iten/source.spm",
        "target": "models/iten/target.spm",
    },
}

Translator = namedtuple("Translator", ["engine", "source_spm", "target_spm"])

cuda = ctranslate2.Device.cuda
cpu = ctranslate2.Device.cpu

translators = {}
for lang in models_paths:
    ct_model_path = models_paths[lang]["model"]
    sp_source_model_path = models_paths[lang]["source"]
    sp_target_model_path = models_paths[lang]["target"]

    device = "cpu"
    translator = ctranslate2.Translator(ct_model_path, device)
    sp_source_model = spm.SentencePieceProcessor(sp_source_model_path)
    sp_target_model = spm.SentencePieceProcessor(sp_target_model_path)
    translators[lang] = Translator(translator, sp_source_model, sp_target_model)

logger.info(translators)


def translate(
    source: str,
    translator: ctranslate2.Translator,
    sp_source_model: spm.SentencePieceProcessor,
    sp_target_model: spm.SentencePieceProcessor,
):
    """Use CTranslate model to translate a sentence

    Args:
        source: Source sentences to translate
        translator: Object of Translator, with the CTranslate2 model
        sp_source_model: Object of SentencePieceProcessor, with the SentencePiece source model
        sp_target_model: Object of SentencePieceProcessor, with the SentencePiece target model
    Returns:
        Translation of the source text
    """
    logger.info(f"received text: {source}")
    source_sentences = sent_tokenize(source)
    source_tokenized = sp_source_model.encode(source_sentences, out_type=str)
    translations = translator.translate_batch(source_tokenized)
    translations = [translation[0]["tokens"] for translation in translations]
    translations_detokenized = sp_target_model.decode(translations)
    translation = " ".join(translations_detokenized)
    logger.info(f"produced translation: {translation}")

    return translation


@app.route("/translate", methods=["POST"])
def translate_service():
    logger.info("processing request")
    if request.is_json:
        # Get the JSON data from the request
        json_data = request.get_json()
        logger.info(f"received data: {json_data}")
        try:
            text = json_data["text"]
            source_lang = json_data["source-lang"]
            target_lang = json_data["target-lang"]
        except KeyError:
            logger.warning("Malformed input")
            return jsonify({"error", "Malformed input"}), 500

        lang_pair = (
            f"{source_lang.split('-')[0].lower()}-{target_lang.split('-')[0].lower()}"
        )
        translator = translators[lang_pair]
        translated = translate(text, *translator)
        json_data["translation"] = translated

        # Return the processed JSON data
        return jsonify(json_data)
    else:
        # Return an error response if the request does not contain JSON data
        logger.warning("No json data")
        return jsonify({"error": "No JSON data found"}), 400


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
