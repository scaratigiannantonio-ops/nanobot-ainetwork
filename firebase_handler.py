import firebase_admin
from firebase_admin import credentials, firestore
import re

cred = credentials.Certificate("/app/firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

async def handle_whatsapp_message(message, user_code=None):
    match = re.search(r'-\s*(\w+)', message)
    if match:
        user_code = match.group(1)
    
    users_ref = db.collection('users')
    query = users_ref.where('inviteCode', '==', user_code).limit(1)
    results = query.get()
    
    if results:
        user = results[0].to_dict()
        system_prompt = f"""
        Sei {user.get('name', 'un consulente')}.
        Tono: {user.get('aiTone', 'professionale')}.
        Target: {user.get('aiTarget', 'chi cerca opportunità')}.
        Presentati così: {user.get('aiIntro', 'Sono un networker')}.
        Prodotti: {user.get('aiProduct', 'network marketing')}.
        Rispondi in modo coerente con questa identità.
        Non rivelare mai che sei un'AI.
        """
        return system_prompt, user
    
    return "Sei un assistente generico. Rispondi gentilmente.", None
