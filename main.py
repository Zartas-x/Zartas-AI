def fetch_ai_response(self, text, key):
        # ВНИМАНИЕ: Изменили v1beta на v1 и добавили приставку models/ внутри строки
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
        
        params = {'key': key}
        headers = {'Content-Type': 'application/json'}
        payload = {"contents": [{"parts": [{"text": text}]}]}
        
        try:
            self.chat_log.text += f"\n[LOG]: Стучусь в стабильную версию v1..."
            session = requests.Session()
            session.trust_env = False 
            
            # В версии v1 ключ ОБЯЗАТЕЛЬНО передаем через params
            r = session.post(url, params=params, headers=headers, json=payload, timeout=15)
            
            self.chat_log.text += f"\n[LOG]: Статус ответа: {r.status_code}"
            
            if r.status_code == 200:
                ans = r.json()['candidates'][0]['content']['parts'][0]['text']
                self.chat_log.text += f"\n[color=00FF00][b]Zartas AI:[/b][/color] {ans}\n"
            else:
                self.chat_log.text += f"\n[ОШИБКА]:\n{r.text}\n"
        except Exception as e:
            self.chat_log.text += f"\n[СБОЙ СЕТИ]: {str(e)}\n"
