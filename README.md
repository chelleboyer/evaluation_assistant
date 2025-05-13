# 🚀 AI Evaluation Assistant

> *Because analyzing research papers shouldn't feel like having your teeth pulled!*

![AI Assistant](https://img.icons8.com/fluency/96/artificial-intelligence.png)

## What is this magic? ✨

The AI Evaluation Assistant is your new best friend when it comes to making sense of AI evaluation, academic jargon, and cutting-edge ML evaluation techniques. It's like having a super-smart buddy who read all the boring stuff so you don't have to!

### Features that'll make you go "woah!" 🤯

- **Document Search**: Instantly find answers in loaded research papers
- **Web Search**: Get real-time info from the vast internet without leaving the app
- **ArXiv Integration**: Access academic papers without falling asleep at your keyboard
- **Slick UI**: A beautiful interface that doesn't look like it was designed in 1997

## Tech Stack 🛠️

This project leverages some seriously cool tech:

- **LangChain** + **LangGraph**: For building powerful AI workflows
- **Chainlit**: For that smooth chat interface you can't stop looking at
- **OpenAI Embeddings**: To understand your questions (even the weird ones)
- **Vector Database**: For lightning-fast document retrieval

## Getting Started 🏁

Want to run this bad boy locally? Here's how:

```bash
# Clone the repo (you know the drill)
git clone https://github.com/yourusername/evaluation-assistant.git

# Install dependencies like a boss
pip install -r requirements.txt

# Set your OpenAI API key (no key, no fun)
export OPENAI_API_KEY=your_key_here

# Fire it up!
chainlit run app.py
```

## Example Queries 💬

Try these and prepare to be amazed:

- "What methods are used for evaluating large language models?"
- "Explain the key metrics for measuring AI performance"
- "Search for the latest LLM benchmarks"
- "Find arxiv papers on AI alignment"

## Contributing 🤝

Found a bug? Want to add a feature? Have a suggestion that'll make this even more awesome? We're all ears! Just open an issue or PR and let's make this thing even cooler together.

## License 📄

MIT - Because sharing is caring!

---

Made with ❤️ and excessive amounts of coffee 

## Deployment to Hugging Face Spaces

This application can be deployed to Hugging Face Spaces using Docker.

### Option 1: Using the Hugging Face UI

1. Create a new Space on [Hugging Face Spaces](https://huggingface.co/spaces)
2. Choose "Docker" as the Space SDK
3. Upload this repository to the Space
4. Set the following environment variables in the Space settings:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `TAVILY_API_KEY`: Your Tavily API key (for web search)
5. The Space will automatically build and deploy the Docker image

### Option 2: Using the Hugging Face CLI

1. Install the Hugging Face CLI: `pip install huggingface_hub`
2. Login to Hugging Face: `huggingface-cli login`
3. Create a new Space:
   ```
   huggingface-cli repo create ai-evaluation-assistant --type space --private
   ```
4. Clone the empty repository:
   ```
   git clone https://huggingface.co/spaces/YOUR_USERNAME/ai-evaluation-assistant
   ```
5. Copy your code to the cloned repository
6. Add, commit, and push your code:
   ```
   git add .
   git commit -m "Initial commit"
   git push
   ```
7. Set the required environment variables in the Space settings on the Hugging Face website

## Local Development

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   chainlit run app.py
   ```

3. Open your browser at `http://localhost:8000`

## Building the Docker Image Locally

```
docker build -t ai-evaluation-assistant .
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key -e TAVILY_API_KEY=your_key ai-evaluation-assistant 