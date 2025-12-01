# 📚 Course‑Info Chatbot (Streamlit + Ollama + ChromaDB)

A **local RAG chatbot** that lets you upload plain‑text course information (fees, duration, syllabus, test pattern, etc.) and ask natural‑language questions.  The app:

- **Embeds** the text with a Sentence‑Transformer model.
- **Stores** the embeddings in a local **ChromaDB** vector store.
- **Retrieves** the most relevant chunks for each query.
- **Answers** using the **Mistral** model served locally by **Ollama** (no API key required).

---

## 🛠️ Prerequisites

| Requirement | Why you need it |
|------------|-----------------|
| **Windows 10/11** | OS we are targeting. |
| **Python 3.11.x** (exact version) | `chromadb==0.5.5` and `sentence‑transformers==3.0.1` only ship wheels for 3.8‑3.11. |
| **Ollama** (latest) | Provides the local Mistral LLM. |
| **Git (optional)** | To clone the repo if you prefer. |

---

## 📦 1️⃣ Install Ollama

1. Download the Windows installer from <https://ollama.com/download> **or** run:
   ```powershell
   winget install ollama
   ```
2. After installation, open a **new PowerShell window** and start the server:
   ```powershell
   ollama serve
   ```
   You should see a line like `Listening on 127.0.0.1:11434`.  Keep this window open for the whole session.
3. Pull the Mistral model (≈ 4 GB):
   ```powershell
   ollama pull mistral
   ```
   (You can replace `mistral` with any other Ollama model later.)

---

## 📂 2️⃣ Clone / create the project folder

If you already have the folder `C:\Users\trimo\OneDrive\Desktop\School Bot` you can skip this step.  Otherwise:

```powershell
mkdir "C:\Users\trimo\OneDrive\Desktop\School Bot"
cd "C:\Users\trimo\OneDrive\Desktop\School Bot"
``` 

Place the following files inside that folder (they are already part of the repo):
- `app.py` (the Streamlit app – already updated to use the new Chroma client)
- `requirements.txt`
- `data/` directory (contains the sample `courses.txt` and the newly added `students_batches.txt`).

---

## 🐍 3️⃣ Create a **Python 3.11** virtual environment

```powershell
# From the project root
python -m venv .venv
.\.venv\Scripts\activate   # PowerShell syntax
```
You should now see `(venv)` at the beginning of the prompt.

> **Important:** If you have multiple Python installations, make sure the `python` command points to **Python 3.11**.  Run `python --version` to verify.

---

## 📦 4️⃣ Install Python dependencies

```powershell
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```
The `requirements.txt` pins the exact versions that work with the new Chroma client:
```
streamlit==1.38.0
chromadb==0.5.5
sentence-transformers==3.0.1
torch==2.4.0+cpu   # CPU‑only wheel (compatible with Python 3.11)
httpx==0.27.2
python-dotenv==1.0.1   # optional, not used by the app but harmless
```
If you see any errors during the install, double‑check that you are still inside the activated venv and that you are using Python 3.11.

---

## 🚀 5️⃣ Run the Streamlit app

```powershell
streamlit run app.py
```
A browser tab should open automatically at `http://localhost:8501`.  If it does not, copy the URL printed in the console and paste it into a browser.

### What you will see
- **Title:** *Course‑Info Chatbot (Ollama + ChromaDB)*
- **Expander** to upload one or more `.txt` files.
- **Chat box** at the bottom where you can type questions.

---

## 📂 6️⃣ Provide course data

### Option A – **Static auto‑load** (recommended for quick start)
The repository already contains two sample files inside the `data/` folder:
- `courses.txt` – contains course type, duration, fees, syllabus, test pattern, etc.
- `students_batches.txt` – contains the number of students per batch (added on request).
The app automatically loads any `.txt` file found in `data/` when it starts, so you can simply **run the app** and you’ll see a green banner:
```
✅ Pre‑loaded `courses.txt` into the vector store.
✅ Pre‑loaded `students_batches.txt` into the vector store.
```
### Option B – **Manual upload**
1. Click the **“Upload additional course data (.txt)”** expander.
2. Drag‑&‑drop one or more `.txt` files (e.g., a new `my_new_course.txt`).
3. Press **Process & Index**.
4. The app will embed the chunks and store them in ChromaDB.

> **Chunking rule:** The app splits a file on **double newlines** (`\n\n`).  If you want each line to be a separate chunk, insert a blank line between lines in the file.

---

## 💬 7️⃣ Ask questions

Type anything in the chat box, for example:
- `What is the fee structure for the Data Science Bootcamp?`
- `How many students are in Batch C?`
- `Give me the total number of students across all batches.`

The workflow is:
1. Retrieve the most relevant chunks from ChromaDB.
2. Build a prompt that includes those chunks + your question.
3. Send the prompt to the **local Mistral model** via Ollama.
4. Display the answer.

---

## 🛠️ 8️⃣ Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `Import "chromadb" could not be resolved` | Wrong Python version or missing package. | Ensure you are inside the venv with Python 3.11 and run `pip install -r requirements.txt`. |
| `Import "sentence_transformers" could not be resolved` | Same as above – missing dependency. | Re‑install the requirements inside the venv. |
| `PermissionError: [WinError 32]` when starting the app | The old `chroma_db` folder is locked by a previous run. | Stop the Streamlit process (Ctrl +C) and Ollama, then delete `chroma_db` manually (`Remove-Item -Recurse -Force .\chroma_db`). Restart the app. |
| No response from the chatbot | Ollama server not running. | Open a separate terminal and run `ollama serve`. |
| Model not found (`mistral`) | Model not pulled. | Run `ollama pull mistral`. |
| UI shows “Processing…” forever | Large file without double‑newline separation → single huge chunk. | Add blank lines between logical sections or split the file manually. |

---

## 🎨 9️⃣ Design & Aesthetics (optional)

The current UI uses Streamlit’s default theme, which is already clean and responsive.  If you want a darker look, add a `~/.streamlit/config.toml` file with:
```toml
[theme]
base="dark"
primaryColor="#ff6f61"
backgroundColor="#0e1117"
secondaryBackgroundColor="#262730"
textColor="#fafafa"
```
Restart the app to see the new theme.

---

## 📚 10️⃣ Summary of files in the project
```
School Bot/
├─ app.py                 # Streamlit app (single‑file implementation)
├─ requirements.txt       # Exact pinned dependencies
├─ README.md              # **You are reading it now**
└─ data/
   ├─ courses.txt        # Sample course information (type, duration, fees…)
   └─ students_batches.txt # Batch‑wise student numbers (added on request)
```

---

## 🚀 Ready to go!
1. **Start Ollama** (`ollama serve`).
2. **Activate the venv** (`.\.venv\Scripts\activate`).
3. **Install deps** (`pip install -r requirements.txt`).
4. **Run** `streamlit run app.py`.
5. **Upload** or rely on the static `data/` files.
6. **Chat** away!

If you need any further customisation (e.g., adding more data files, changing the model, styling the UI), just let me know. Happy building! 🎉