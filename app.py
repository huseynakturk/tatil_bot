from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Gemini
GOOGLE_API_KEY = "AIzaSyCDlFxyyilnZgl51fadCynNiNq9aPAUAMQ"
genai.configure(api_key=GOOGLE_API_KEY)

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Load Excel data
def load_reservations():
    try:
        df = pd.read_excel('data/reservations.xlsx')
        return df
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return pd.DataFrame()

# FAQ responses
FAQ_RESPONSES = {
    "rezervasyon": "Rezervasyon yapmak için lütfen web sitemizdeki rezervasyon formunu doldurun veya bizi arayın.",
    "iptal": "Rezervasyon iptali için en az 48 saat önceden bildirim yapmanız gerekmektedir.",
    "ödeme": "Ödemeler kredi kartı veya banka havalesi ile yapılabilir.",
    "check-in": "Check-in saati 14:00'dır. Erken gelişler için ek ücret talep edilebilir.",
    "check-out": "Check-out saati 12:00'dır. Geç çıkışlar için ek ücret talep edilebilir."
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/faq', methods=['POST'])
def get_faq():
    data = request.json
    question = data.get('question', '').lower()
    
    # Check if question matches any FAQ
    for key, response in FAQ_RESPONSES.items():
        if key in question:
            return jsonify({'response': response})
    
    return jsonify({'response': "Üzgünüm, bu soru için önceden tanımlanmış bir cevap bulamadım."})

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    try:
        # Check if it's a reservation query
        if "rezervasyonum" in user_message.lower():
            df = load_reservations()
            if not df.empty:
                # Here you would implement the actual search logic
                return jsonify({'response': "Rezervasyon bilgileriniz kontrol ediliyor..."})
        
        # Use Gemini for general questions
        prompt = f"""Sen bir tatil kiralama platformu chatbot'usun. 
        Kullanıcılara tatil kiralama ile ilgili soruları yanıtlıyorsun.
        Kullanıcı sorusu: {user_message}
        """
        
        response = model.generate_content(prompt)
        return jsonify({'response': response.text})
    
    except Exception as e:
        return jsonify({'response': f"Üzgünüm, bir hata oluştu: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True) 