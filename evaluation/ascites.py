import random
import openai  

# Lista de patologías que pueden causar ascitis
pathologies_with_ascites = [
    "Abdominal trauma", "Acute cholecystitis", "Cirrhosis",
    "Congestive heart failure", "Ectopic pregnancy",
    "Malignancy", "Portal hypertension", 
    "Ruptured abdominal aortic aneurysm"
]

def generate_false_options(correct_pathology, num_options=2):
    """Genera opciones incorrectas que parecen plausibles."""
    # Prompt en inglés conforme a lo solicitado
    prompt = (
        f"Create medically plausible false options, one or two words, and very occasionally up to 3. "
        f"They can be real but incorrect: \n"
        f"examples: \n"
        f"1. Irritable bowel syndrome\n"
        f"2. Familial polyposis\n"
        f"3. Megacolon\n"
        f"4. etc..\n"
        f"or they can be made up but sound real: \n"
        f"example: \n"
        f"1. Rott's syndrome\n"
        f"2. Duodenal edema\n"
        f"3. Hepatic lipomatosis\n"
        f"4. Gastric thrombosis\n"
        f"5. etc..\n"
        f"for a condition different than {correct_pathology}."
    )
    
    # Aquí se entregará el prompt al código donde haces la llamada a OpenAI
    return prompt 

def generate_questions(num_questions=6):
    """Genera preguntas sobre patologías asociadas a ascitis."""
    questions = []
    for _ in range(num_questions):
        question_type = random.choice(["cause", "exclude"])  # Elige tipo de pregunta
        correct_indices = random.sample(range(len(pathologies_with_ascites)), 2)
        correct_pathology1 = pathologies_with_ascites[correct_indices[0]]
        correct_pathology2 = pathologies_with_ascites[correct_indices[1]]
        
        if question_type == "cause":
            prompt = generate_false_options(correct_pathology1)  # Llamar a la generación del prompt de opciones falsas
            # Aquí llamarías a OpenAI y obtendrías las opciones falsas, por ahora asumimos que haces algo como:
            # false_options = llamar_a_openai(prompt)
            # Para simplicity asumamos que false_options = ["Opción falsa 1", "Opción falsa 2"]
            false_options = ["Opción falsa 1", "Opción falsa 2"]
            questions.append((
                f"¿Cuál de estas patologías puede ser causa de ascitis?",
                correct_pathology1,
                [correct_pathology1, false_options[0], false_options[1]]
            ))
        else:
            prompt1 = generate_false_options(correct_pathology1)  # Llamar a la generación del prompt de opciones falsas
            prompt2 = generate_false_options(correct_pathology2)  # Llamar a la generación del prompt de opciones falsas
            # Aquí llamarías a OpenAI y obtendrías las opciones falsas, por ahora asumimos que haces algo como:
            # false_option1 = llamar_a_openai(prompt1)
            # false_option2 = llamar_a_openai(prompt2)
            # Para simplicity asumamos que false_option1 = "Opción falsa 1" y false_option2 = "Opción falsa 2"
            false_option1 = "Opción falsa 1"
            false_option2 = "Opción falsa 2"
            questions.append((
                f"Estas patologías son causa de ascitis, excepto:",
                false_option1,
                [false_option1, correct_pathology1, correct_pathology2]
            ))
    return questions

def check_answer(correct_pathology, user_answer):
    """Verifica si la respuesta es correcta."""
    return user_answer.lower() == correct_pathology.lower()

def get_explanation(correct_pathology):
    """Genera una explicación para la respuesta correcta."""
    # Aquí es donde defines tu prompt.
    prompt = (
        f"Explain in detail why {correct_pathology} can cause ascites. "
        f"Include the physiological and pathological mechanisms that lead to the development of ascites in this condition."
    )
    
    # Aquí se entregará el prompt al código donde haces la llamada a OpenAI
    return prompt

# Funcción para realizar la llamada a OpenAI
def llamar_a_openai(prompt):
    openai.api_key = 'YOUR_API_KEY'  # Reemplaza con tu clave de API
    
    response = openai.Completion.create(
        engine="text-davinci-003",  # Asegúrate de usar el modelo correcto
        prompt=prompt,
        max_tokens=100,  # Ajusta según la necesidad
        n=1,
        stop=None
    )
    
    return response['choices'][0]['text'].strip()

# Ejemplo de uso
if __name__ == "__main__":
    # Generar opciones incorrectas para una patología específica
    prompt_false_options = generate_false_options("Cirrhosis")
    false_options = llamar_a_openai(prompt_false_options)
    print(f"False options generated: {false_options}")

    # Generar una explicación detallada
    prompt_explanation = get_explanation("Cirrhosis")
    explanation = llamar_a_openai(prompt_explanation)
    print(f"Explanation: {explanation}")

    # Generar preguntas de ejemplo
    questions = generate_questions(1)  # Generamos solo una pregunta para el ejemplo
    print(f"Generated questions: {questions}")

    # Ejemplo de revisión de respuesta
    correct_pathology = "Cirrhosis"
    user_answer = "Cirrhosis"
    is_correct = check_answer(correct_pathology, user_answer)
    print(f"Is the user's answer correct? {is_correct}")
