from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

# language code mapping dict (Llama2)
language_codes = {
    'Arabic': 'ar_AR',
    'Czech': 'cs_CZ',
    'German': 'de_DE',
    'English': 'en_XX',
    'Spanish': 'es_XX',
    'Estonian': 'et_EE',
    'Finnish': 'fi_FI',
    'French': 'fr_XX',
    'Gujarati': 'gu_IN',
    'Hindi': 'hi_IN',
    'Italian': 'it_IT',
    'Japanese': 'ja_XX',
    'Kazakh': 'kk_KZ',
    'Korean': 'ko_KR',
    'Lithuanian': 'lt_LT',
    'Latvian': 'lv_LV',
    'Burmese': 'my_MM',
    'Nepali': 'ne_NP',
    'Dutch': 'nl_XX',
    'Romanian': 'ro_RO',
    'Russian': 'ru_RU',
    'Sinhala': 'si_LK',
    'Turkish': 'tr_TR',
    'Vietnamese': 'vi_VN',
    'Chinese': 'zh_CN',
    'Afrikaans': 'af_ZA',
    'Azerbaijani': 'az_AZ',
    'Bengali': 'bn_IN',
    'Persian': 'fa_IR',
    'Hebrew': 'he_IL',
    'Croatian': 'hr_HR',
    'Indonesian': 'id_ID',
    'Georgian': 'ka_GE',
    'Khmer': 'km_KH',
    'Macedonian': 'mk_MK',
    'Malayalam': 'ml_IN',
    'Mongolian': 'mn_MN',
    'Marathi': 'mr_IN',
    'Polish': 'pl_PL',
    'Pashto': 'ps_AF',
    'Portuguese': 'pt_XX',
    'Swedish': 'sv_SE',
    'Swahili': 'sw_KE',
    'Tamil': 'ta_IN',
    'Telugu': 'te_IN',
    'Thai': 'th_TH',
    'Tagalog': 'tl_XX',
    'Ukrainian': 'uk_UA',
    'Urdu': 'ur_PK',
    'Xhosa': 'xh_ZA',
    'Galician': 'gl_ES',
    'Slovene': 'sl_SI'
}

model = MBartForConditionalGeneration.from_pretrained("SnypzZz/Llama2-13b-Language-translate")
tokenizer = MBart50TokenizerFast.from_pretrained("SnypzZz/Llama2-13b-Language-translate", src_lang="en_XX")

def translate_survey_questions(text_list: list, target_lng: str):
    """
    Translates a list of survey questions from English to the specified target language.
    
    Args:
        text_list (list): A list of strings containing survey questions in English.
        target_lng (str): The language code of the target language for translation.

    Returns:
        list: A list of translated survey questions in the target language.
    """
    model_inputs = tokenizer(text_list, return_tensors="pt", padding=True, truncation=True, max_length = 40)

    # translate from English to Spanish
    generated_tokens = model.generate(
        **model_inputs,
        forced_bos_token_id=tokenizer.lang_code_to_id[target_lng]
    )

    translation = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    print(translation)
    return translation
    
if __name__ == "__main__":
    # print(generate_survey_statements("car manufacturing", "electric cars"))
    # langchain_agent("Ford Mustang Mach‑E® electric SUV")
    translate_survey_questions('Hi! Nice to meet you!', language_codes['Spanish'])
    print('ok')