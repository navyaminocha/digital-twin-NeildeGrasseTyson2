# digital-twin-NeildeGrasseTyson2
# 🔭 Neil deGrasse Tyson Digital Twin

An AI-powered Digital Twin of Neil deGrasse Tyson that combines Retrieval-Augmented Generation (RAG), Long-Term Memory, Temporal Awareness, and Voice Interaction to create an engaging and personalized conversational experience.

---

## 📖 Overview

This project simulates conversations with Neil deGrasse Tyson by combining a curated knowledge base, memory management, and Large Language Models. The system remembers user information, retrieves relevant knowledge, and responds in Neil's characteristic style of scientific storytelling and cosmic analogies.

The Digital Twin can:

- Maintain conversational context
- Remember user facts across sessions
- Reference scientific events and timelines
- Provide educational explanations grounded in retrieved knowledge
- Support voice-based interaction

---

## ✨ Features

### 🧠 Retrieval-Augmented Generation (RAG)
- Retrieves relevant knowledge before generating responses.
- Improves factual accuracy.
- Reduces hallucinations.

### 💾 Long-Term Memory
- Stores previous conversations across sessions.
- Remembers important user information.
- Enables personalized interactions.

### 👤 Personal Fact Extraction
- Extracts and stores:
  - User names
  - Interests
  - Hobbies
  - Preferences

### 💬 ChatGPT-Style Conversation Interface
- Interactive chat interface.
- Continuous conversation flow.
- Multiple conversation sessions.

### 🔄 Conversation Management
- Current conversation tracking.
- New Conversation functionality.
- Persistent memory across conversations.

### 📅 Temporal Awareness
- Uses the current date.
- References Neil deGrasse Tyson's career timeline.
- References major scientific discoveries and milestones.

### 🎙️ Voice Interaction
- Text-to-Speech output.
- Listen to Neil's responses.
- Improved accessibility and user engagement.

### 🧠 Persona Engineering
- Simulates Neil deGrasse Tyson's communication style.
- Scientific storytelling.
- Cosmos-based analogies.
- Educational explanations.

### 📊 Memory Dashboard
Displays:
- Total memories
- Recent memories
- Known facts about the user
- Memory exploration tools

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### AI & NLP
- Google Gemini API
- Sentence Transformers

### Retrieval System
- ChromaDB
- Vector Embeddings
- Semantic Search

### Memory
- JSON-Based Storage
- Session State Management

### Voice
- Text-to-Speech (TTS)

### Language
- Python

---

## 📂 Project Structure

```text
digital_twin/
│
├── app.py
├── gemini_helper.py
├── retriever.py
├── memory.py
├── voice_helper.py
│
├── data/
│   ├── knowledge_base.txt
│   └── embeddings/
│
├── memory.json
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Clone the Repository

```bash
git clone https://github.com/navyaminocha/digital-twin-NeildGegrasseTyson.git
cd digital-twin-NeildGegrasseTyson
```

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
GOOGLE_API_KEY=YOUR_API_KEY
```

---

## ▶️ Running the Application

```bash
streamlit run app.py
```

---

## 🚀 Future Improvements

- Voice cloning for Neil deGrasse Tyson's voice
- Fully integrated speech-to-text interaction
- Advanced memory ranking and retrieval
- Multi-user memory support
- Custom frontend implementation
- Streaming responses

---

## 📚 Learning Outcomes

Through this project, I gained practical experience in:

- Retrieval-Augmented Generation (RAG)
- Prompt Engineering
- Long-Term Memory Systems
- Conversational AI Design
- Vector Databases and Embeddings
- Streamlit Development
- Voice Interaction Systems
- API Integration
- Debugging and Problem Solving

I also learned how to combine multiple AI technologies to build a realistic digital twin capable of maintaining context, retrieving knowledge, and personalizing conversations.

---

## 👨‍💻 Author

**Navya Minocha**

Developed as an AI Digital Twin project inspired by Neil deGrasse Tyson's scientific communication and educational approach.
