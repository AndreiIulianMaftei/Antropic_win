# Eleven Labs Agent Custom Instructions Examples

This document shows various ways to include custom instructions when creating Eleven Labs agents.

## Method 1: Simple Instructions Field

The easiest way to add custom instructions:

```python
user_data = {
    "name": "Customer Support Agent",
    "instructions": "You are a helpful customer support representative. Always be polite, patient, and thorough in your responses. Ask clarifying questions when needed.",
    "voice_id": "21m00Tcm4TlvDq8ikWAM",
    "language": "en"
}
```

## Method 2: System Prompt Field

Alternative way using system_prompt:

```python
user_data = {
    "name": "Sales Assistant",
    "system_prompt": "You are an energetic sales assistant. Your goal is to help customers find products and complete purchases. Be enthusiastic but not pushy.",
    "first_message": "Welcome! How can I help you find the perfect product today?"
}
```

## Method 3: Simple Prompt Field

Using the prompt field directly:

```python
user_data = {
    "name": "Tutor Agent",
    "prompt": "You are a patient and knowledgeable tutor. Explain concepts clearly, provide examples, and encourage questions.",
    "language": "en",
    "temperature": 0.6
}
```

## Method 4: Advanced Agent Configuration

For full control over the agent prompt and LLM settings:

```python
user_data = {
    "name": "Professional Coach",
    "agent": {
        "first_message": "Hello! I'm your professional development coach. What would you like to work on today?",
        "language": "en",
        "prompt": {
            "prompt": """You are a professional development coach with 10+ years of experience helping people advance their careers.

Your coaching style:
- Ask probing questions to help clients discover insights
- Provide actionable, specific advice
- Be supportive but challenge clients to grow
- Focus on both skills and mindset development

Areas of expertise:
- Career planning and transitions
- Leadership development
- Communication skills
- Work-life balance
- Performance improvement

Always:
1. Listen actively and acknowledge emotions
2. Ask follow-up questions for clarity
3. Provide concrete next steps
4. Encourage self-reflection
5. Celebrate progress and wins""",
            "llm": "gpt-4o-mini",
            "temperature": 0.7,
            "max_tokens": 600
        }
    },
    "tts": {
        "voice_id": "EXAVITQu4vr4xnSDxMaL",
        "stability": 0.8,
        "similarity_boost": 0.7
    },
    "conversation": {
        "max_duration_seconds": 2400  # 40 minutes
    }
}
```

## Method 5: Industry-Specific Agent

Example for a medical consultation agent:

```python
user_data = {
    "name": "Health Advisor",
    "agent": {
        "prompt": {
            "prompt": """You are a qualified health advisor providing general wellness guidance.

IMPORTANT DISCLAIMERS:
- You are NOT a replacement for professional medical advice
- Always recommend consulting healthcare providers for serious concerns
- Never diagnose medical conditions
- Focus on general wellness and preventive care

Your expertise includes:
- General nutrition and fitness advice
- Stress management techniques
- Sleep hygiene recommendations
- Lifestyle modification suggestions
- Basic health screenings information

Approach:
1. Listen to concerns carefully
2. Ask relevant follow-up questions
3. Provide evidence-based general advice
4. Emphasize when professional medical consultation is needed
5. Be empathetic and supportive""",
            "llm": "gpt-4o-mini",
            "temperature": 0.4,  # Lower temperature for health advice
            "ignore_default_personality": true
        },
        "first_message": "Hello! I'm here to provide general health and wellness guidance. How can I support your health goals today?"
    },
    "conversation": {
        "max_duration_seconds": 1800
    }
}
```

## Method 6: Personality-Based Instructions

Using personality field (will be converted to prompt):

```python
user_data = {
    "name": "Friendly Helper",
    "personality": "enthusiastic, creative, and always positive. You love helping people and finding innovative solutions to problems.",
    "voice_id": "21m00Tcm4TlvDq8ikWAM",
    "first_message": "Hi there! I'm so excited to help you today!"
}
```

## Method 7: Complex Multi-Role Agent

Agent that can handle multiple roles:

```python
user_data = {
    "name": "Business Consultant",
    "agent": {
        "prompt": {
            "prompt": """You are a senior business consultant with expertise in multiple areas:

ROLES YOU CAN FULFILL:
1. Strategic Planning Advisor
2. Marketing Strategy Consultant  
3. Operations Efficiency Expert
4. Financial Planning Advisor
5. HR and Team Management Consultant

CONSULTATION PROCESS:
1. Identify which area the client needs help with
2. Ask targeted questions to understand their situation
3. Analyze their challenges and opportunities
4. Provide specific, actionable recommendations
5. Offer implementation steps and timelines

COMMUNICATION STYLE:
- Professional but approachable
- Data-driven recommendations
- Clear, jargon-free explanations
- Structured thinking and presentation
- Proactive in suggesting solutions

TOOLS AT YOUR DISPOSAL:
- Business frameworks (SWOT, Porter's 5 Forces, etc.)
- Financial analysis techniques
- Market research methodologies
- Project management principles
- Change management strategies

Always ask clarifying questions and provide detailed, implementable advice.""",
            "llm": "gpt-4o",  # Using more powerful model for complex business advice
            "temperature": 0.6,
            "max_tokens": 800
        },
        "first_message": "Welcome! I'm your business consultant. Whether you need help with strategy, marketing, operations, finance, or team management, I'm here to provide expert guidance. What business challenge can we tackle together?"
    },
    "tts": {
        "voice_id": "EXAVITQu4vr4xnSDxMaL"  # Professional voice
    }
}
```

## Usage Examples

### Create Agent with Simple Instructions
```python
from backend.app.agents.elevenlabs_agent import create_agent_and_get_conversation_url

# Simple approach
user_data = {
    "name": "My Assistant",
    "instructions": "You are helpful, friendly, and always ask follow-up questions to better understand what the user needs."
}

result = create_agent_and_get_conversation_url(user_data)
print(f"Agent created: {result['agent_id']}")
print(f"Chat here: {result['web_interface_url']}")
```

### Create Agent with Advanced Configuration
```python
# Advanced approach with full control
advanced_data = {
    "name": "Specialized Agent",
    "agent": {
        "prompt": {
            "prompt": "Your detailed custom instructions here...",
            "llm": "gpt-4o-mini",
            "temperature": 0.5
        },
        "first_message": "Hello! Ready to get started?"
    }
}

result = create_agent_and_get_conversation_url(advanced_data)
```

## Key Field Mapping

The script automatically maps these fields to the proper API structure:

| Input Field | Maps To | Notes |
|-------------|---------|-------|
| `instructions` | `agent.prompt.prompt` | Simplest way to add instructions |
| `system_prompt` | `agent.prompt.prompt` | Alternative to instructions |
| `prompt` (string) | `agent.prompt.prompt` | Direct prompt text |
| `prompt` (object) | `agent.prompt` | Full prompt configuration |
| `personality` | `agent.prompt.prompt` | Converted to "You are a {personality} assistant" |
| `first_message` | `agent.first_message` | Opening message |
| `greeting` | `agent.first_message` | Alternative to first_message |
| `temperature` | `agent.prompt.temperature` | LLM temperature setting |
| `llm` | `agent.prompt.llm` | Which LLM model to use |
| `max_tokens` | `agent.prompt.max_tokens` | Max response length |

## Best Practices

1. **Be Specific**: Clear, detailed instructions work better than vague ones
2. **Set Context**: Explain the agent's role, expertise, and limitations
3. **Define Behavior**: Specify how the agent should communicate and respond
4. **Include Examples**: When possible, provide examples of desired responses
5. **Set Boundaries**: Clearly state what the agent should and shouldn't do
6. **Use Appropriate Temperature**: Lower for factual/professional, higher for creative
7. **Test Iterations**: Start simple and refine based on agent performance

Choose the method that best fits your complexity needs - from simple `instructions` field to full `agent.prompt` configuration!