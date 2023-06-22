# CryptoSentry

CryptoSentry is a powerful cryptocurrency bot designed to send signals for coins that are approaching a Dollar Cost Averaging (DCA) level or a profit level. It is built using Python and leverages the Disnake library for Discord interactions.

## Key Features

- **Automated Signal Generation**: CryptoSentry sends signals for coins that are nearing a DCA level or a profit level.
- **Real-time Price Fetching**: Utilizes the CoinMarketCap API to fetch the latest prices for multiple coins.
- **Interactive Commands**: Users can retrieve coins that are near a level using the `/dca` command.

## Installation & Setup

Follow these steps to install and run CryptoSentry:

1. **Clone the repository**:

\`\`\`bash
git clone https://github.com/AccursedGalaxy/CryptoSentry.git
\`\`\`

2. **Navigate to the project directory**:

\`\`\`bash
cd CryptoSentry
\`\`\`

3. **Install the necessary dependencies**:

\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. **Set up your environment variables**:

You will need to set the following variables:

- `CMC_API_KEY`: Your CoinMarketCap API key
- `TEST_GUILD_IDS`: The Discord guild ID for the server
- `SIGNAL_CHANNEL_ID`: Channel ID for the signals
- `X_RAPIDAPI_KEY`: API key from RapidAPI for API access

5. **Run the bot**:

\`\`\`bash
python bot.py
\`\`\`

## Usage

Once the bot is running, it will automatically send signals for coins that are near a DCA level or a profit level every 15 minutes. You can also use the `/dca` command to get coins that are near a level.

## License

CryptoSentry is licensed under the MIT License. See [LICENSE](LICENSE) for more information.

## Contact & Support

If you have any questions or need further clarification, feel free to open an issue or send me a message on Discord at `accursedgalaxy`.
