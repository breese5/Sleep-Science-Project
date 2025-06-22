"""
Chat bot model for the Sleep Science Explainer Bot.
"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
import boto3
import json
from botocore.exceptions import ClientError

from backend.core.logging import LoggerMixin
from backend.core.config import settings


class ChatBot(LoggerMixin):
    """
    Main chat bot implementation using AWS Bedrock.
    
    This class handles:
    - Conversation management
    - AI response generation
    - Context management
    - Error handling
    """
    
    def __init__(self):
        """Initialize the chat bot with AWS Bedrock client."""
        self.logger.info("Initializing ChatBot")
        
        # Initialize AWS Bedrock client
        self.bedrock_client = boto3.client(
            'bedrock-runtime',
            region_name=settings.aws_bedrock_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key
        )
        
        # Conversation storage (in production, this would be in a database)
        self.conversations: Dict[str, Dict[str, Any]] = {}
        
        # System prompt for sleep science expertise
        self.system_prompt = self._get_system_prompt()
        
        self.logger.info("ChatBot initialized successfully")
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the sleep science bot."""
        return """You are a Sleep Science Explainer Bot, an AI assistant specialized in explaining sleep-related research, medical guidelines, and health information in simple, accessible terms.

Your expertise includes:
- Sleep cycles and circadian rhythms
- Sleep disorders (insomnia, sleep apnea, etc.)
- Sleep hygiene and best practices
- Sleep research and scientific studies
- Sleep medicine and treatments
- Sleep and overall health relationships

Guidelines:
1. Always provide evidence-based information from reputable sources
2. Explain complex medical concepts in simple, layperson-friendly language
3. Be accurate and avoid making medical diagnoses
4. Encourage users to consult healthcare professionals for medical advice
5. Cite sources when referencing specific research or guidelines
6. Be empathetic and supportive
7. Focus on education and understanding rather than medical advice

When discussing research papers or studies:
- Summarize key findings clearly
- Explain the significance and implications
- Note any limitations or caveats
- Provide context about the research quality

Remember: You are an educational tool, not a replacement for professional medical advice."""

    async def generate_response(
        self,
        message: str,
        conversation_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a response to a user message.
        
        Args:
            message: The user's message
            conversation_id: Optional conversation ID for context
            context: Additional context information
            
        Returns:
            Dictionary containing response data
        """
        self.logger.info(
            "Generating response",
            conversation_id=conversation_id,
            message_length=len(message)
        )
        
        try:
            # Create or get conversation
            if not conversation_id:
                conversation_id = str(uuid.uuid4())
                self.conversations[conversation_id] = {
                    "messages": [],
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            
            # Add user message to conversation
            self._add_message_to_conversation(
                conversation_id, "user", message
            )
            
            # Generate AI response
            ai_response = await self._generate_ai_response(conversation_id)
            
            # Add AI response to conversation
            self._add_message_to_conversation(
                conversation_id, "assistant", ai_response["content"]
            )
            
            return {
                "response": ai_response["content"],
                "conversation_id": conversation_id,
                "sources": ai_response.get("sources"),
                "confidence": ai_response.get("confidence", 0.8)
            }
            
        except Exception as e:
            self.logger.error(
                "Error generating response",
                error=str(e),
                conversation_id=conversation_id
            )
            raise
    
    async def _generate_ai_response(self, conversation_id: str) -> Dict[str, Any]:
        """
        Generate response using AWS Bedrock.
        
        Args:
            conversation_id: The ID of the current conversation.
            
        Returns:
            Dictionary containing AI response data
        """
        try:
            # Get the message history for the conversation
            messages = self.conversations.get(conversation_id, {}).get("messages", [])

            # Format messages for the Anthropic Claude 3 model
            formatted_messages = []
            for msg in messages:
                # Skip system messages if they are accidentally stored
                if msg["role"] != "system":
                    formatted_messages.append({"role": msg["role"], "content": [{"type": "text", "text": msg["content"]}]})

            # Prepare the request body for Bedrock
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": settings.bedrock_max_tokens,
                "temperature": settings.bedrock_temperature,
                "system": self.system_prompt,
                "messages": formatted_messages,
            }

            # Call Bedrock API
            response = self.bedrock_client.invoke_model(
                modelId=settings.bedrock_model_id,
                body=json.dumps(body),
                contentType="application/json",
                accept="application/json"
            )
            
            # Parse response
            response_body = json.loads(response.get("body").read())
            
            # Extract the response text
            response_text = ""
            for block in response_body.get("content", []):
                if block.get("type") == "text":
                    response_text += block.get("text", "")

            return {
                "content": response_text,
                "sources": [],  # Placeholder for future implementation
                "confidence": 0.9  # Placeholder
            }
            
        except ClientError as e:
            self.logger.error(f"AWS Bedrock error: {e}")
            raise Exception("Failed to generate AI response due to a client error.")
        except Exception as e:
            self.logger.error(f"Error in _generate_ai_response: {e}")
            raise
    
    def _prepare_conversation_context(
        self,
        conversation_id: str,
        additional_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Prepare conversation context for AI processing.
        
        Args:
            conversation_id: The conversation ID
            additional_context: Additional context information
            
        Returns:
            Formatted conversation context string
        """
        conversation = self.conversations.get(conversation_id, {})
        messages = conversation.get("messages", [])
        
        # Format conversation history
        context_parts = []
        
        # Add additional context if provided
        if additional_context:
            context_parts.append(f"Additional context: {additional_context}")
        
        # Add conversation history
        for msg in messages[-10:]:  # Last 10 messages for context
            role = msg["role"]
            content = msg["content"]
            context_parts.append(f"{role}: {content}")
        
        return "\n".join(context_parts)
    
    def _add_message_to_conversation(
        self,
        conversation_id: str,
        role: str,
        content: str
    ) -> None:
        """
        Add a message to the conversation history.
        
        Args:
            conversation_id: The conversation ID
            role: Message role (user/assistant)
            content: Message content
        """
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = {
                "messages": [],
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow()
        }
        
        self.conversations[conversation_id]["messages"].append(message)
        self.conversations[conversation_id]["updated_at"] = datetime.utcnow()
    
    async def get_conversation_history(self, conversation_id: str) -> Dict[str, Any]:
        """
        Get conversation history.
        
        Args:
            conversation_id: The conversation ID
            
        Returns:
            Conversation history data
        """
        if conversation_id not in self.conversations:
            raise ValueError("Conversation not found")
        
        return self.conversations[conversation_id]
    
    async def delete_conversation(self, conversation_id: str) -> None:
        """
        Delete a conversation.
        
        Args:
            conversation_id: The conversation ID
        """
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            self.logger.info(f"Deleted conversation: {conversation_id}")
        else:
            raise ValueError("Conversation not found") 