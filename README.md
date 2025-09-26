# UNICORN RADAR

An AI-Powered Founder Analysis System that leverages artificial intelligence to gather and analyze information from multiple platforms including LinkedIn, GitHub, and OpenAlex. The system also supports personalized interviews using beyondpresence.ai or elevenlabs.io. It employs Model Context Protocol (MCP) servers to interact with various APIs and provides structured, intelligent analysis of professional profiles.

## Features

- **LinkedIn Profile Analysis**
  - Professional experience summarization
  - Education background extraction
  - Skills identification
  - Notable position highlighting

- **GitHub Profile Analysis**
  - Repository listing and analysis
  - Star count aggregation
  - Follower metrics
  - Contribution activity tracking
  - Programming language preferences

- **OpenAlex Academic Analysis**
  - Publication metrics
  - Citation statistics
  - Research impact assessment
  - Academic collaboration analysis

## Technology Stack

- **Backend**
  - FastAPI
  - Python 3.12+
  - Pydantic
  - Pydantic-AI
  - Model Context Protocol (MCP)

## Prerequisites

- Python 3.12 or higher
- UV package manager
- Docker (for LinkedIn MCP server)
- Environment variables:
  ```
  LINKEDIN_COOKIE=your_linkedin_cookie
  GITHUB_PERSONAL_ACCESS_TOKEN=your_github_token
  OPENALEX_MAILTO=your_email@domain.com
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YourUsername/Antropic_win.git
   cd Antropic_win
   ```

2. Install dependencies using UV:
   ```bash
   uv install
   ```

3. Install test dependencies:
   ```bash
   uv install -E test
   ```

## Project Structure

```
Antropic_win/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── linkedin_agent.py
│   │   │   ├── github_agent.py
│   │   │   └── openalex_agent.py
│   │   ├── core/
│   │   │   ├── prompts/
│   │   │   └── config.py
│   │   └── models/
│   │       └── publication.py
│   └── tests/
│       ├── test_linkedin_agent.py
│       ├── test_github_agent.py
│       └── test_openalex_agent.py
├── requirements.txt
└── pyproject.toml
```

## Usage

### Starting the System

1. Start the backend server:
   ```bash
   uv run python3 backend/fastapi_server.py
   ```

2. Start the frontend (in a new terminal):
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. Access the UI through the link provided in the frontend terminal.


### Running Tests
```bash
pytest backend/tests/
```


# Similar patterns for GitHub and OpenAlex agents
```

## API Documentation

Once the FastAPI server is running, visit:
- API documentation: `http://localhost:8000/docs`
- Alternative documentation: `http://localhost:8000/redoc`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- LinkedIn MCP Server
- GitHub API
- OpenAlex API
- Pydantic-AI Framework
