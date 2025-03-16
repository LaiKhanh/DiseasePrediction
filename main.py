from flask import Flask, request, render_template, jsonify  # Import jsonify
import numpy as np
import pandas as pd
import pickle
import spacy
import re
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from transformers import GPT2Tokenizer, GPT2LMHeadModel


# flask app
app = Flask(__name__)

keywords_new = {
    "itching": ["itching", "itch"],
    "skin_rash": ["skin rash", "rash"],
    "nodal_skin_eruptions": ["nodal skin eruptions"],
    "continuous_sneezing": ["continuous sneezing"],
    "shivering": ["shivering", "chills"],
    "chills": ["chills", "fever"],
    "joint_pain": ["joint pain", "arthritis"],
    "stomach_pain": ["stomach pain", "abdominal pain"],
    "acidity": ["acidity", "heartburn"],
    "ulcers_on_tongue": ["ulcers on tongue", "mouth sores"],
    "muscle_wasting": ["muscle wasting", "muscle weakness"],
    "vomiting": ["vomiting", "nausea"],
    "burning_micturition": ["burning micturition", "painful urination"],
    "spotting_urination": ["spotting urination", "frequent urination"],
    "fatigue": ["fatigue", "tiredness"],
    "weight_gain": ["weight gain", "obesity"],
    "anxiety": ["anxiety", "stress"],
    "cold_hands_and_feets": ["cold hands and feet", "poor circulation"],
    "mood_swings": ["mood swings", "irritability"],
    "weight_loss": ["weight loss", "slimming"],
    "restlessness": ["restlessness", "insomnia"],
    "lethargy": ["lethargy", "apathy"],
    "patches_in_throat": ["patches in throat", "sore throat"],
    "irregular_sugar_level": ["irregular sugar level", "diabetes"],
    "cough": ["cough", "respiratory issues"],
    "high_fever": ["high fever", "temperature elevation"],
    "sunken_eyes": ["sunken eyes", "fatigue"],
    "breathlessness": ["breathlessness", "shortness of breath"],
    "sweating": ["sweating", "perspiration"],
    "dehydration": ["dehydration", "water loss"],
    "indigestion": ["indigestion", "heartburn"],
    "headache": ["headache", "migraine"],
    "yellowish_skin": ["yellowish skin", "jaundice"],
    "dark_urine": ["dark urine", "kidney issues"],
    "nausea": ["nausea", "vomiting"],
    "loss_of_appetite": ["loss of appetite", "decreased hunger"],
    "pain_behind_the_eyes": ["pain behind the eyes", "eye strain"],
    "back_pain": ["back pain", "muscle strain"],
    "constipation": ["constipation", "bowel issues"],
    "abdominal_pain": ["abdominal pain", "stomach cramps"],
    "diarrhoea": ["diarrhoea", "frequent bowel movements"],
    "mild_fever": ["mild fever", "low-grade temperature"],
    "yellow_urine": ["yellow urine", "urine color change"],
    "yellowing_of_eyes": ["yellowing of eyes", "jaundice"],
    "acute_liver_failure": ["acute liver failure", "liver dysfunction"],
    "fluid_overload": ["fluid overload", "edema"],
    "swelling_of_stomach": ["swelling of stomach", "abdominal distension"],
    "swelled_lymph_nodes": ["swelled lymph nodes", "enlarged lymph nodes"],
    "malaise": ["malaise", "general discomfort"],
    "blurred_and_distorted_vision": ["blurred and distorted vision", "eye problems"],
    "phlegm": ["phlegm", "mucus"],
    "throat_irritation": ["throat irritation", "sore throat"],
    "redness_of_eyes": ["redness of eyes", "eye irritation"],
    "sinus_pressure": ["sinus pressure", "congestion"],
    "runny_nose": ["runny nose", "rhinorrhea"],
    "congestion": ["congestion", "stuffy nose"],
    "chest_pain": ["chest pain", "cardiac issues"],
    "weakness_in_limbs": ["weakness in limbs", "muscle weakness"],
    "fast_heart_rate": ["fast heart rate", "tachycardia"],
    "pain_during_bowel_movements": ["pain during bowel movements", "rectal pain"],
    "pain_in_anal_region": ["pain in anal region", "anal pain"],
    "bloody_stool": ["bloody stool", "hematochezia"],
    "irritation_in_anus": ["irritation in anus", "anal itching"],
    "neck_pain": ["neck pain", "cervical pain"],
    "dizziness": ["dizziness", "lightheadedness"],
    "cramps": ["cramps", "muscle spasms"],
    "bruising": ["bruising", "ecchymosis"],
    "obesity": ["obesity", "overweight"],
    "swollen_legs": ["swollen legs", "edema"],
    "swollen_blood_vessels": ["swollen blood vessels", "vasculitis"],
    "puffy_face_and_eyes": ["puffy face and eyes", "edema"],
    "enlarged_thyroid": ["enlarged thyroid", "goiter"],
    "brittle_nails": ["brittle nails", "nail fragility"],
    "swollen_extremeties": ["swollen extremeties", "edema"],
    "excessive_hunger": ["excessive hunger", "polyphagia"],
    "extra_marital_contacts": ["extra marital contacts", "infidelity"],
    "drying_and_tingling_lips": ["drying and tingling lips", "cheilitis"],
    "slurred_speech": ["slurred speech", "dysarthria"],
    "knee_pain": ["knee pain", "knee joint pain"],
    "hip_joint_pain": ["hip joint pain", "hip arthritis"],
    "muscle_weakness": ["muscle weakness", "muscle atrophy"],
    "stiff_neck": ["stiff neck", "cervical stiffness"],
    "swelling_joints": ["swelling joints", "joint swelling"],
    "movement_stiffness": ["movement stiffness", "muscle rigidity"],
    "spinning_movements": ["spinning movements", "vertigo"],
    "loss_of_balance": ["loss of balance", "ataxia"],
    "unsteadiness": ["unsteadiness", "lightheadedness"],
    "weakness_of_one_body_side": ["weakness of one body side", "hemiparesis"],
    "loss_of_smell": ["loss of smell", "anosmia"],
    "bladder_discomfort": ["bladder discomfort", "urinary issues"],
    "foul_smell_of_urine": ["foul smell of urine", "urinary tract infection"],
    "continuous_feel_of_urine": ["continuous feel of urine", "urinary frequency"],
    "passage_of_gases": ["passage of gases", "flatulence"],
    "internal_itching": ["internal itching", "pruritus"],
    "toxic_look_typhos": ["toxic look typhos", "typhoid fever"],
    "depression": ["depression", "mental health disorders"],
    "irritability": ["irritability", "mood swings"],
    "muscle_pain": ["muscle pain", "myalgia"],
    "altered_sensorium": ["altered sensorium", "confusion"],
    "red_spots_over_body": ["red spots over body", "petechiae"],
    "belly_pain": ["belly pain", "abdominal pain"],
    "abnormal_menstruation": ["abnormal menstruation", "menstrual irregularities"],
    "dischromic_patches": ["dischromic patches", "skin discoloration"],
    "watering_from_eyes": ["watering from eyes", "lacrimation"],
    "increased_appetite": ["increased appetite", "polyphagia"],
    "polyuria": ["polyuria", "frequent urination"],
    "family_history": ["family history", "genetic disorders"],
    "mucoid_sputum": ["mucoid sputum", "respiratory issues"],
    "rusty_sputum": ["rusty sputum", "hemoptysis"],
    "lack_of_concentration": ["lack of concentration", "attention deficit"],
    "visual_disturbances": ["visual disturbances", "blurred vision"],
    "receiving_blood_transfusion": ["receiving blood transfusion", "blood transfusion"],
    "receiving_unsterile_injections": ["receiving unsterile injections", "unsterile injections"],
    "coma": ["coma", "unconsciousness"],
    "stomach_bleeding": ["stomach bleeding", "gastrointestinal bleeding"],
    "distention_of_abdomen": ["distention of abdomen", "abdominal swelling"],
    "history_of_alcohol_consumption": ["history of alcohol consumption", "alcoholism"],
    "fluid_overload.1": ["fluid overload", "edema"],
    "blood_in_sputum": ["blood in sputum", "hemoptysis"],
    "prominent_veins_on_calf": ["prominent veins on calf", "varicose veins"],
    "palpitations": ["palpitations", "heart palpitations"],
    "painful_walking": ["painful walking", "foot pain"],
    "pus_filled_pimples": ["pus filled pimples", "acne"],
    "blackheads": ["blackheads", "comedones"],
    "scurring": ["scurring", "scarring"],
    "skin_peeling": ["skin peeling", "exfoliation"],
    "silver_like_dusting": ["silver like dusting", "skin discoloration"],
    "small_dents_in_nails": ["small dents in nails", "nail abnormalities"],
    "inflammatory_nails": ["inflammatory nails", "nail inflammation"],
    "blister": ["blister", "fluid-filled bumps"],
    "red_sore_around_nose": ["red sore around nose", "nasal irritation"],
    "yellow_crust_ooze": ["yellow crust ooze", "pus-filled crust"]
}


# load databasedataset===================================
sym_des = pd.read_csv("./datasets/symtoms_df.csv")
precautions = pd.read_csv("./datasets/precautions_df.csv")
workout = pd.read_csv("./datasets/workout_df.csv")
description = pd.read_csv("./datasets/description.csv")
medications = pd.read_csv("./datasets/medications.csv")
diets = pd.read_csv("./datasets/diets.csv")


# load model===========================================
with open('./models/logistic_regression_model.pkl', 'rb') as file:
    loaded_clf = pickle.load(file)
# Load the saved GPT-2 model and tokenizer
model = GPT2LMHeadModel.from_pretrained("./gpt2_model")
tokenizer = GPT2Tokenizer.from_pretrained("./gpt2_tokenizer")

# Function to match the generated text to symptoms (dummy example)
def match_generated_text_to_symptoms(generated_text):
    # Find matching symptoms in the generated text
    symptoms = {symptom: 0 for symptom in keywords_new.keys()}
    for symptom, keywords in keywords_new.items():
        if any(keyword in generated_text for keyword in keywords):
            symptoms[symptom] = 1
    return symptoms

# Function to use GPT-2 to preprocess the input text for symptom extraction
def map_symptoms_with_llm(text):
    inputs = tokenizer.encode(text, return_tensors="pt")
    outputs = model.generate(inputs, max_length=150, num_return_sequences=1)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Here, you'd implement logic to map the generated text to actual symptoms.
    # This is where you can match it against your symptom_keywords, similar to what you were doing earlier.
    symptoms = match_generated_text_to_symptoms(generated_text)
    return symptoms

#============================================================
# custome and helping functions
#==========================helper funtions================
def helper(diseases):
    all_desc = []
    all_pre = []
    all_med = []
    all_die = []
    all_wrkout = []

    for dis in diseases:
        desc = description[description['Disease'] == dis]['Description']
        desc = " ".join([w for w in desc])
        all_desc.append(desc)

        pre = precautions[precautions['Disease'] == dis][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
        pre = [col for col in pre.values]
        all_pre.append(pre)

        med = medications[medications['Disease'] == dis]['Medication']
        med = [med for med in med.values]
        all_med.append(med)

        die = diets[diets['Disease'] == dis]['Diet']
        die = [die for die in die.values]
        all_die.append(die)

        wrkout = workout[workout['disease'] == dis]['workout']
        wrkout = [wrk for wrk in wrkout.values]
        all_wrkout.append(wrkout)

    return all_desc, all_pre, all_med, all_die, all_wrkout

# Define the pipeline
pipeline = Pipeline([
    # ('symptom_mapping', map_symptoms),  # Ensure map_symptoms is defined correctly
    ('symptom_mapping', map_symptoms_with_llm),
    ('create_dataframe', lambda x: pd.DataFrame([x], columns=x.keys())),
    ('disease_classification', loaded_clf)  # Ensure loaded_clf is a trained LogisticRegression model
])

le = LabelEncoder()
le.fit(sym_des['Disease'])


def predict_disease(text):
    symptoms = pipeline['symptom_mapping'](text)
    df = pipeline['create_dataframe'](symptoms)
    probabilities = pipeline['disease_classification'].predict_proba(df)
    top_5_indices = probabilities.argsort()[0][-5:][::-1]
    top_5_diseases = le.inverse_transform(top_5_indices)
    top_5_probabilities = (probabilities[0][top_5_indices] * 100).round(2)
    return list(zip(top_5_diseases, top_5_probabilities))

def get_symptoms(text):
    symptoms = pipeline['symptom_mapping'](text)
    filtered_symptoms = [symptom for symptom, value in symptoms.items() if value == 1]
    return filtered_symptoms


# creating routes========================================
@app.route("/")
def index():
    return render_template("index.html")

# Define a route for the home page
@app.route('/predict', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text = request.form.get('symptoms')
        print(text)
        if not text or text.isspace() or text.isnumeric():
            warning_message = "Please enter some symptoms."
            return render_template('index.html', warning_message=warning_message, input_text=text)
        else:
            predicted_disease = predict_disease(text)

            my_symptoms = []
            detected_symptoms = get_symptoms(text)
            for symptpom in detected_symptoms:
                my_symptoms.append(symptpom.replace("_", " "))

            dis_des, precautions, medications, rec_diet, workout = helper([disease for disease, _ in predicted_disease])

            success_message = "Predicted successfully. View details below"
            my_precautions = []
            for i in precautions[0]:
                my_precautions.append(i)

            return render_template('index.html', predicted_disease=predicted_disease, my_symptoms=my_symptoms,
                                   dis_des=dis_des, my_precautions=my_precautions, medications=medications, 
                                   my_diet=rec_diet, workout=workout, success_message=success_message, input_text=text)

    return render_template('index.html')


# about view funtion and path
@app.route('/about')
def about():
    return render_template("about.html")
# contact view funtion and path
@app.route('/contact')
def contact():
    return render_template("contact.html")

# developer view funtion and path
@app.route('/developer')
def developer():
    return render_template("developer.html")

# about view funtion and path
@app.route('/blog')
def blog():
    return render_template("blog.html")


if __name__ == '__main__':

    app.run(debug=True)