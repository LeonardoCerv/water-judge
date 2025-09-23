# Water Judge - EigenLabs Challenge

[![Views](https://badges.0xleo.dev/badge/dynamic/viewers?repo=leonardocerv/water-judge&edges=round&text=repository%20views&bgColor=white&textColor=blue&v=1234567890)](https://github.com/LeonardoCerv/ez-badges)

[![Python](https://badges.0xleo.dev/badge?text=Python&bgColor=3776AB&textColor=FFFFFF&iconColor=FFFFFF&icon=simple-icons:python)](https://www.python.org/)
[![FastAPI](https://badges.0xleo.dev/badge?text=FastAPI&bgColor=009688&textColor=FFFFFF&iconColor=FFFFFF&icon=simple-icons:fastapi)](https://fastapi.tiangolo.com/)
[![Cerebras](https://badges.0xleo.dev/badge?text=cerebras%20API&bgColor=FFFFFF&textColor=black&icon=https://cloud.cerebras.ai/images/logo/cerebras-logo-black.svg)](https://cerebras.ai/)
[![EigenLabs](https://badges.0xleo.dev/badge?text=EigenCloud&bgColor=DA70D6&textColor=FFFFFF&iconColor=FFFFFF&icon=https://www.eigencloud.xyz/images/Eigen_Cloud_Logo.png)](https://www.eigenlabs.org/)
[![Ethereum](https://badges.0xleo.dev/badge?text=Ethereum&bgColor=3C3C3D&textColor=FFFFFF&iconColor=FFFFFF&icon=simple-icons:ethereum)](https://ethereum.org/)
[![Docker](https://badges.0xleo.dev/badge?text=Docker&bgColor=2496ED&textColor=FFFFFF&iconColor=FFFFFF&icon=simple-icons:docker)](https://www.docker.com/)
[![License](https://badges.0xleo.dev/badge?text=License&bgColor=750014&textColor=FFFFFF&iconColor=FFFFFF&icon=https://cdn.uconnectlabs.com/wp-content/themes/uConnect_MIT/images/mit-capd-left.svg?v=2)](https://opensource.org/licenses/MIT)

Imagine you have a water test strip with numbers like pH or chlorine levels. You send that data to this API, and it tells you if the water is safe for drinking, bathing, or other uses. It also gives tips on how to clean the water if needed. 

The special part is EigenLabs. It uses Ethereum (a type of blockchain) to sign each decision, like putting a digital seal on the result. This seal proves the result is real and hasn't been changed. No one can fake it because it's checked on the blockchain.

## How EigenLabs Makes This Work

EigenLabs helps create systems where people can trust information without needing a big company in charge. Here's how it works in this project, step by step:

- **Signing with a Secret Key**: When the API makes a decision about the water, it uses a secret key from an Ethereum wallet to create a digital signature. This signature is like a unique fingerprint for that decision. Anyone can check this fingerprint later to make sure the decision came from this API and wasn't tampered with.

- **Checking on the Blockchain**: The signature can be verified on the Ethereum blockchain, which is a public record that everyone can see. This means you don't have to trust the API owner—you can check the proof yourself. It's like having a receipt that shows the transaction happened.

- **Working with EigenLayer**: EigenLayer is a way to make blockchain security stronger by reusing it for different things. In this project, the water data can be part of a bigger security network. For example, if water quality data is important for insurance or farming, it can help secure those systems too.

- **Turning Opinions into Facts**: Water testing used to be subjective—someone might say "this water looks okay." Now, with EigenLabs, it's objective data that can be proven. This data can connect to other systems, like financial apps (DeFi), insurance, or environmental monitoring, making everything more reliable.

This project shows how EigenLabs can make real-world problems, like water safety, work in a decentralized way, without needing big companies to control everything.

## What the API Can Do

- **Smart Water Checks**: It uses AI from Cerebras to look at your water test numbers and give a health score, like "80% safe."
- **Advice for Different Uses**: Tells you if the water is okay for drinking, washing, watering plants, etc.
- **Warning About Risks**: Points out dangers, like too much iron or bacteria.
- **Cleaning Steps**: Gives simple instructions on how to make the water safer, like boiling or filtering.
- **Trusted Results**: Every answer is signed with blockchain, so you know it's real.
- **Easy to Use API**: Built with FastAPI, which makes it fast and gives you automatic docs.

## How to Get Started

Follow these steps to run the API on your computer. Don't worry if you're new—this is straightforward.

1. **Get the Code**: First, download the project from GitHub. Open your terminal (the command line on your computer) and type:
   ```bash
   git clone https://github.com/LeonardoCerv/water-judge.git
   cd water-judge
   ```
   This copies the code to your computer and goes into the folder.

2. **Install What You Need**: The project needs some tools to work. Install them with:
   ```bash
   pip install -r requirements.txt
   ```
   Pip is a tool that downloads and installs Python packages. This might take a minute.

3. **Set Up Secrets**: The API needs a secret key for the wallet and an API key for the AI. Create a file called `.env`:
   ```bash
   cp .env.example .env
   ```
   Then open `.env` in a text editor and add your MNEMONIC (a phrase for your Ethereum wallet) and CEREBRAS_API_KEY (from Cerebras).

4. **Run the API**: Start the server with:
   ```bash
   python src/judge.py
   ```
   You'll see messages saying it's running. It will show the address of the API.

5. **Use the API**: Open your web browser and go to `http://localhost:8000` for info, or `http://localhost:8000/docs` for the full guide on how to send requests.

## Using Docker (Optional)

If you have Docker, you can run everything in a container without installing Python stuff. Here's how:

1. **Build the Container**: This creates a package with everything inside.
   ```bash
   docker build -t water-judge .
   ```

2. **Run the Container**: Start it and connect it to your computer.
   ```bash
   docker run -p 80:80 --env-file .env water-judge
   ```
   Now the API is at `http://localhost:80`.

Docker makes it easy to run on any computer without setup hassles.

## How to Use the API

The main way to use it is by sending data about your water test. Here's a simple example:

### Check Water Quality

Send a POST request to `/judge` with your data. You can use tools like Postman or curl, or even the docs page.

The data should look like this JSON:

```json
{
  "use_case": "drinking",
  "location": {"hint": "Well water in rural area"},
  "strip": {
    "values": {
      "pH": 7.2,
      "Total Chlorine": 0.5,
      "Iron": 0.1
    }
  }
}
```

- `use_case`: What you want to use the water for, like "drinking" or "bathing."
- `location`: A hint about where the water is from, to help the AI.
- `strip`: The numbers from your test strip, like pH level or chlorine amount.

The API will reply with:
- A health score (like "75%")
- If it's safe for your use
- Any risks
- Steps to clean it
- A signature to prove it's real

## Tools and Tech Used

- **Python 3.12**: The main programming language.
- **FastAPI**: A tool to build the web API quickly.
- **Uvicorn**: Runs the API server.
- **Cerebras AI**: Provides the smart AI for analyzing water.
- **Ethereum**: Used for signing results with a wallet.
- **Docker**: Packages everything for easy running.
