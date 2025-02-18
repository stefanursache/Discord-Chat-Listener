import discord
import asyncio
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# Replace with your bot token
TOKEN = "chatbot token id"
CHANNEL_ID = channel_ids  # Replace with your channel ID

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Required to read message content
client = discord.Client(intents=intents)


def summarize_text(text, sentence_count=3):
    """Summarizes text using Latent Semantic Analysis (LSA)."""
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentence_count)
    return " ".join(str(sentence) for sentence in summary)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    channel = client.get_channel(CHANNEL_ID)

    if channel:
        print(f"Fetching messages from #{channel.name}...")

        messages = []
        # Fetch last 50 messages
        async for message in channel.history(limit=50):
            if not message.author.bot:  # Ignore bot messages
                messages.append(message.content)

        if messages:
            full_text = " ".join(messages)
            summary = summarize_text(full_text)
            print("\nChat Summary:\n", summary)
            await channel.send(f"**Summary of recent discussion:**\n{summary}")
        else:
            print("No messages found.")

client.run(TOKEN)
